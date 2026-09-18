#!/usr/bin/env python3
"""JSON Schema **子集** 校验器（纯标准库，无第三方依赖）。

存在理由：`.sdd/schema/decision.schema.json` 是真正的 JSON Schema，但早先的
`validate_rules.py` 只用正则检查「键名在不在」，因此下面这种数据也能通过：

```yaml
architecture_decision:
  project: hello
  backend: 123        # 应为 object
  database: []        # 应为 object
  rejected: wrong     # 应为 array
  confidence: foo     # 应为 object
```

即「名义上 Schema 化，实际上 regex 化」。本模块补上**真校验**：
把 `decision.json`（JSON，标准库可直接解析）交给它逐关键字校验。

**为什么是子集而不是引入 `jsonschema` 依赖**：本仓的公开属性是「纯标准库、无依赖」，
新增开发依赖会让校验脚本在干净环境里跑不起来。代价是子集校验器可能不认识
Schema 里新加的校验关键字 —— 这种情况**必须报错而非静默忽略**，否则又会退化成
"名义校验"。故本模块维护 `SUPPORTED_KEYWORDS` 白名单，遇到未知关键字直接报错，
迫使 Schema 的演进与校验器同步。

支持的校验关键字：type / enum / const / required / properties / additionalProperties /
items / minItems / maxItems / uniqueItems / minimum / maximum / exclusiveMinimum /
exclusiveMaximum / minLength / maxLength / pattern / oneOf / anyOf / allOf

用法：
    import json, mini_schema
    schema = json.loads(Path("...json").read_text())
    errs = mini_schema.validate(json.loads(Path("decision.json").read_text()), schema)
"""

from __future__ import annotations

import re

ANNOTATION_KEYWORDS = {
    "$schema",
    "$id",
    "title",
    "description",
    "examples",
    "default",
    "deprecated",
    "$comment",
}

SUPPORTED_KEYWORDS = {
    "type",
    "enum",
    "const",
    "required",
    "properties",
    "additionalProperties",
    "items",
    "minItems",
    "maxItems",
    "uniqueItems",
    "minimum",
    "maximum",
    "exclusiveMinimum",
    "exclusiveMaximum",
    "minLength",
    "maxLength",
    "pattern",
    "oneOf",
    "anyOf",
    "allOf",
}

_JSON_TYPES: dict[str, type | tuple[type, ...]] = {
    "object": dict,
    "array": list,
    "string": str,
    # bool 是 int 的子类，需在 _type_ok 里单独排除
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def _type_ok(value, type_name: str) -> bool:
    if type_name not in _JSON_TYPES:
        return False
    if type_name in ("integer", "number") and isinstance(value, bool):
        return False  # JSON 语义：true/false 不是数字
    return isinstance(value, _JSON_TYPES[type_name])


def _json_eq(a, b) -> bool:
    """JSON 语义的相等（True != 1，与 Python 的 `==` 不同）。"""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a is b
    return a == b


def validate(data, schema, path: str = "$") -> list[str]:
    """按 `schema` 校验 `data`，返回错误列表（空 = 通过）。"""
    errors: list[str] = []

    if not isinstance(schema, dict):
        return [f"{path}: Schema 节点不是对象"]

    for kw in schema:
        if kw not in SUPPORTED_KEYWORDS and kw not in ANNOTATION_KEYWORDS:
            errors.append(
                f"{path}: Schema 使用了未支持的校验关键字 `{kw}` —— "
                f"请扩展 scripts/mini_schema.py 的 SUPPORTED_KEYWORDS，不要静默跳过"
            )
    if errors:
        return errors

    if "type" in schema:
        types = schema["type"]
        types = [types] if isinstance(types, str) else list(types)
        if not any(_type_ok(data, t) for t in types):
            return [
                f"{path}: 期望 type={schema['type']}，实际 {type(data).__name__}"
            ]

    if "const" in schema and not _json_eq(data, schema["const"]):
        errors.append(f"{path}: 期望常量 {schema['const']!r}，实际 {data!r}")

    if "enum" in schema and not any(_json_eq(data, v) for v in schema["enum"]):
        errors.append(f"{path}: 取值 {data!r} 不在枚举 {schema['enum']} 中")

    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: 长度 {len(data)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(f"{path}: 长度 {len(data)} > maxLength {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], data):
            errors.append(f"{path}: 不匹配 pattern {schema['pattern']!r}")

    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: {data} < minimum {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path}: {data} > maximum {schema['maximum']}")
        if "exclusiveMinimum" in schema and data <= schema["exclusiveMinimum"]:
            errors.append(f"{path}: {data} <= exclusiveMinimum {schema['exclusiveMinimum']}")
        if "exclusiveMaximum" in schema and data >= schema["exclusiveMaximum"]:
            errors.append(f"{path}: {data} >= exclusiveMaximum {schema['exclusiveMaximum']}")

    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(f"{path}: 元素数 {len(data)} < minItems {schema['minItems']}")
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append(f"{path}: 元素数 {len(data)} > maxItems {schema['maxItems']}")
        if schema.get("uniqueItems"):
            seen: list[object] = []
            for item in data:
                if any(_json_eq(item, s) for s in seen):
                    errors.append(f"{path}: uniqueItems 违反，重复元素 {item!r}")
                    break
                seen.append(item)
        if "items" in schema:
            for i, item in enumerate(data):
                errors += validate(item, schema["items"], f"{path}[{i}]")

    if isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}: 缺少必填项 `{key}`")
        props = schema.get("properties", {})
        for key, sub in props.items():
            if key in data:
                errors += validate(data[key], sub, f"{path}.{key}")
        extra = [k for k in data if k not in props]
        ap = schema.get("additionalProperties", True)
        if ap is False and extra:
            errors.append(f"{path}: 出现未声明字段 {extra}（additionalProperties=false）")
        elif isinstance(ap, dict):
            for key in extra:
                errors += validate(data[key], ap, f"{path}.{key}")

    for branch, label in (("allOf", "allOf"), ("anyOf", "anyOf"), ("oneOf", "oneOf")):
        if branch not in schema:
            continue
        subs = schema[branch]
        results = [validate(data, s, path) for s in subs]
        if label == "allOf":
            for r in results:
                errors += r
        elif label == "anyOf":
            if not any(not r for r in results):
                errors.append(f"{path}: 不满足 anyOf 任一分支")
        else:  # oneOf
            ok = sum(1 for r in results if not r)
            if ok != 1:
                errors.append(f"{path}: oneOf 需恰好满足一个分支，实际满足 {ok} 个")

    return errors
