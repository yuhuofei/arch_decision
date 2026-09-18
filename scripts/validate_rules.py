#!/usr/bin/env python3
"""规则库自检（纯标准库，无需第三方依赖）。

检查项：
  1. 引用编号   —— 全仓禁止裸写 `§N`（约定见 .sdd/CONVENTIONS.md §1）
  2. 来源条号   —— `res.md §N` / `Matrix §N` / `知识库 §N` / `mod_gpt.md §N` 的 N 必须真实存在
                    （识别 `§A,§B` 压缩与 `§A-§B` 区间写法，见 scripts/sdd_refs.py）
  3. 文件引用   —— 反引号内的 `.md` 路径必须真实存在（占位符与按需产物除外）
  4. Decision Schema —— 两级校验，语义不同，不要混为一谈：
        (a) `specs/*/decision.json`  → **真 JSON Schema 校验**（scripts/mini_schema.py）
        (b) `specs/**/*.md` 的 YAML 代码块 → **structural validation**（只查必填键是否存在）
             YAML 无标准库解析器，故 (b) 不做类型校验；(a) 才是权威
  5. 复杂度预算 —— complexity.score 不得大于 complexity.budget（取 (a) 的 JSON，回退到 (b) 的 YAML）

用法：
    python3 scripts/validate_rules.py
退出码：0 = 全部通过；1 = 存在错误。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# 扫描范围与引用解析统一由 sdd_refs 提供，避免两个脚本各自维护正则而漂移
import mini_schema  # noqa: E402
from sdd_refs import (  # noqa: E402
    LABELS,
    ROOT,
    SOURCES,
    iter_refs,
    parse_source_items,
    targets,
)

# 按需产物 / 外部约定文件 / 已废弃约定中的旧文件名：允许被引用但不必存在
ALLOWED_MISSING = {
    "research.md", "data-model.md", "api-contract.md", "architecture.md",
    "engineering-rules.md", "context.md", "requirements.md", "decisions.md",
    "specification.md", "constitution.md",
    # Matrix §45 提出但本仓已 superseded 的文件名（见 .sdd/LAYOUT.md §2）
    "principles.md", "decision-matrix.md", "decision-tree.md", "scoring.md",
}

SEP = re.compile(r"[；;。\n]")
BARE = re.compile(r"§\d+(?!\.\d)")
BACKTICK_MD = re.compile(r"`([A-Za-z0-9._\-/]*[A-Za-z0-9_\-]\.md)`")
BACKTICK_JSON = re.compile(r"`([A-Za-z0-9._\-/]*[A-Za-z0-9_\-]\.json)`")
YAML_BLOCK = re.compile(r"```ya?ml\n(.*?)```", re.S)

SCHEMA_PATH = ROOT / ".sdd" / "schema" / "decision.schema.json"

errors: list[str] = []
warnings: list[str] = []
counters: dict[str, int] = {}


def check_bare_refs(files: list[Path]) -> None:
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            for m in BARE.finditer(line):
                seg_start = 0
                for sm in SEP.finditer(line[: m.start()]):
                    seg_start = sm.end()
                segment = line[seg_start : m.start()]
                if any(lb in segment for lb in LABELS):
                    continue
                errors.append(f"[裸引用] {p.relative_to(ROOT)}:{i}  {line.strip()[:90]}")


def check_source_refs(files: list[Path], items: dict[str, set[tuple[int, int]]]) -> None:
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            # iter_refs 已展开 `§A,§B` 与 `§A-§B`，故压缩写法中的越界条号同样会被抓到
            for name, n in iter_refs(line):
                if n not in items[name]:
                    errors.append(
                        f"[来源条号不存在] {p.relative_to(ROOT)}:{i}  {name} §{n}"
                    )


def check_file_refs(files: list[Path]) -> None:
    # 文件引用既可能是 .md，也可能是 .json（如 specs/<id>/decision.json、
    # .sdd/schema/decision.schema.json）——存在性集合必须同时覆盖两种扩展名。
    all_files = list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.json"))
    all_rel = {str(p.relative_to(ROOT)) for p in all_files}
    all_names = {p.name for p in all_files}
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            refs = [m.group(1) for m in BACKTICK_MD.finditer(line)]
            # 只检查带路径的 `.json` 引用：裸 `decision.json` 是"按需产物"的泛指写法
            refs += [m.group(1) for m in BACKTICK_JSON.finditer(line) if "/" in m.group(1)]
            for ref in refs:
                if "<" in ref or ">" in ref or "{" in ref:
                    continue
                base = ref.split("/")[-1]
                if ref in all_rel or base in all_names or base in ALLOWED_MISSING:
                    continue
                if base.startswith("ADR-") or re.match(r"^adr-?\d", base):
                    continue
                warnings.append(
                    f"[文件引用可能失效] {p.relative_to(ROOT)}:{i}  `{ref}`"
                )


def _python_ok(v) -> str:
    return type(v).__name__


def check_decision_json() -> None:
    """(a) specs/*/decision.json —— 真 JSON Schema 校验。"""
    if not SCHEMA_PATH.exists():
        errors.append("[Schema] 缺少 .sdd/schema/decision.schema.json")
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    found = sorted(ROOT.glob("specs/*/decision.json"))
    counters["decision.json"] = len(found)
    for p in found:
        rel = p.relative_to(ROOT)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"[decision.json 非法 JSON] {rel}  {e}")
            continue
        for msg in mini_schema.validate(data, schema):
            errors.append(f"[Decision Schema 违规（真校验）] {rel}  {msg}")
        check_complexity_json(data, rel)


def check_complexity_json(data, rel: Path) -> None:
    arch = data.get("architecture_decision") if isinstance(data, dict) else None
    cplx = (arch or {}).get("complexity") if isinstance(arch, dict) else None
    if not isinstance(cplx, dict):
        warnings.append(f"[复杂度预算] {rel} 未记录 complexity（score/budget）")
        return
    score, budget = cplx.get("score"), cplx.get("budget")
    if isinstance(score, int) and isinstance(budget, int) and score > budget:
        errors.append(f"[复杂度超预算] {rel}  score={score} > budget={budget}")


def check_decision_contract(files: list[Path]) -> None:
    """(b) Markdown 中的 Decision Contract（YAML 块）—— structural validation only。"""
    if not SCHEMA_PATH.exists():
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    required = schema["properties"]["architecture_decision"]["required"]

    for p in files:
        if "specs" not in p.relative_to(ROOT).parts:
            continue
        for block in YAML_BLOCK.findall(p.read_text(encoding="utf-8")):
            if "architecture_decision:" not in block:
                continue
            for key in required:
                if not re.search(rf"^\s{{2,4}}{key}:", block, re.M):
                    errors.append(
                        f"[Decision Contract 结构缺项] {p.relative_to(ROOT)}  缺少 `{key}`"
                    )
            m_score = re.search(r"score:\s*(\d+)", block)
            m_budget = re.search(r"budget:\s*(\d+)", block)
            if m_score and m_budget:
                s, b = int(m_score.group(1)), int(m_budget.group(1))
                if s > b:
                    errors.append(
                        f"[复杂度超预算] {p.relative_to(ROOT)}  score={s} > budget={b}"
                    )


def check_traceability_fresh() -> None:
    tb = ROOT / ".sdd" / "TRACEABILITY.md"
    if not tb.exists():
        warnings.append("[TRACEABILITY] 文件不存在，可运行 scripts/gen_traceability.py 生成")
        return
    if "（无）" not in tb.read_text(encoding="utf-8").split("## 校验")[-1]:
        errors.append("[TRACEABILITY] 存在引用了不存在条号的记录（见文件末节）")


def main() -> int:
    files = targets()
    items = {name: parse_source_items(name, path) for name, path in SOURCES.items()}

    check_bare_refs(files)
    check_source_refs(files, items)
    check_file_refs(files)
    check_decision_json()
    check_decision_contract(files)
    check_traceability_fresh()

    print(f"扫描 {len(files)} 个 Markdown 文件")
    print(f"真 Schema 校验 decision.json：{counters.get('decision.json', 0)} 个\n")
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print(
        f"\n结果：{len(errors)} 个错误，{len(warnings)} 个警告。"
        + ("  ✅ 全部通过" if not errors else "  ❌ 需修复")
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
