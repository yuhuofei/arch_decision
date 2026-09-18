#!/usr/bin/env python3
"""规则库自检（纯标准库，无需第三方依赖）。

检查项：
  1. 引用编号   —— 全仓禁止裸写 `§N`（约定见 .sdd/CONVENTIONS.md §1）
  2. 来源条号   —— `res.md §N` / `Matrix §N` / `知识库 §N` / `mod_gpt.md §N` /
                    `modv2.md §N` 的 N 必须真实存在
                    （识别 `§A,§B` 压缩、`§A-§B` 区间、`§N.M` 子条目，见 scripts/sdd_refs.py）
  3. 文件引用   —— 反引号内的 `.md` / `.json` 路径必须真实存在（占位符与按需产物除外）
  4. Decision Schema —— 两级校验，语义不同，不要混为一谈：
        (a) `specs/*/decision.json`  → **真 JSON Schema 校验**（scripts/mini_schema.py）
        (b) `specs/**/*.md` 的 YAML 代码块 → **structural validation**（只查必填键是否存在）
             YAML 无标准库解析器，故 (b) 不做类型校验；(a) 才是权威
  5. 复杂度预算 —— complexity.score 不得大于 complexity.budget
  6. Verification —— 三级：(a) `verification.json` 真 Schema 校验；(b) `verification.md`
                    必填且含 8 节结构；(c) 两者 Status / Verdict / AC 集合一致
  7. Cost 语义  —— `cap` 未知时不得判定 `within_budget = true`（modv2.md §7）
  8. 版本一致性 —— `.sdd/VERSION` ≡ README 声明 ≡ CHANGELOG 最新版本（modv2.md §12）
  9. Canonical 不变量（modv2.md §22，见 .sdd/CANONICAL.md）：
        - 权威归属矩阵与代码登记表一致
        - Workflow 顺序一致（Draft Spec 必须早于技术决策）
        - 决策状态旧语义不得回流（禁止短语表）
        - LAYOUT 标「必填」的产物必须有对应模板

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
    is_audit,
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

SCHEMA_DIR = ROOT / ".sdd" / "schema"
SCHEMA_PATH = SCHEMA_DIR / "decision.schema.json"
VERIF_SCHEMA_PATH = SCHEMA_DIR / "verification.schema.json"
VERSION_PATH = ROOT / ".sdd" / "VERSION"
CANONICAL_PATH = ROOT / ".sdd" / "CANONICAL.md"
LAYOUT_PATH = ROOT / ".sdd" / "LAYOUT.md"

# --- Canonical 归属登记表 -------------------------------------------------
# 必须与 .sdd/CANONICAL.md 的表格一致（check_canonical_registry 会核对）。
# 格式：(主题, 权威路径)
CANONICAL_TOPICS: list[tuple[str, str]] = [
    ("Workflow order", ".sdd/workflows/new-project.md"),
    ("Decision semantics", ".sdd/decision-trees/decision-protocol.md"),
    ("Complexity budget", ".sdd/decision-trees/decision-protocol.md"),
    ("Default matrix", ".sdd/decision-trees/"),
    ("Artifact required/optional", ".sdd/LAYOUT.md"),
    ("Directory", ".sdd/LAYOUT.md"),
    ("Reference syntax", ".sdd/CONVENTIONS.md"),
    ("Release version", ".sdd/VERSION"),
    ("Machine contract", ".sdd/schema/decision.schema.json"),
    ("Machine instance", "specs/<id>/decision.json"),
    ("Human-readable decision", ".sdd/templates/technology-selection.md"),
    ("Spec structure", ".sdd/templates/spec.md"),
    ("Verification", ".sdd/templates/verification.md"),
    ("Traceability", ".sdd/TRACEABILITY.md"),
    ("Agent entry — read routing", "CLAUDE.md"),
    ("Agent entry — engineering rules + DoD", "AGENTS.md"),
    ("Semantic routing", "AGENTS.md"),
]

# 决策状态旧语义的**禁止短语**（modv2.md §1：这些是 v1.3 已修掉、但会回流的写法）。
# 命中即说明"上层已改、底层残留"，必须修。
FORBIDDEN_SEMANTICS = [
    "提出方案，建议人确认",
    "信息不足，停止，请求澄清",
    "用户明确要求是 Hard Constraint",
    "技术栈类决定建议先",
    "技术栈类决定有长期锁定成本",
    "先输出给人确认",
]

# 流程顺序检查：`Draft Spec` 必须早于"技术决策"。参与检查的文件与标记。
WORKFLOW_FILES = [
    "CLAUDE.md",
    "AGENTS.md",
    ".sdd/README.md",
    ".sdd/workflows/new-project.md",
    ".sdd/decision-trees/decision-protocol.md",
]
TECH_MARKERS = ("Technology Selection", "Technology Decision", "Architecture Decision",
                "Architecture Proposal", "Technology + Decision")

VERIF_HEADINGS = [
    "1. Verification Status",
    "2. Acceptance Criteria",
    "3. Requirement Traceability",
    "4. Test Results",
    "5. Non-Functional Verification",
    "6. Consistency Check",
    "7. Known Issues",
    "8. Final Verdict",
]
VERDICT_LINE = re.compile(r"^\s*(PASS WITH KNOWN ISSUES|PASS|FAIL)\s*(#.*)?$", re.M)
AC_ID = re.compile(r"\bAC-\d{3}\b")

errors: list[str] = []
warnings: list[str] = []
counters: dict[str, int] = {}


def _rel(p: Path) -> Path:
    return p.relative_to(ROOT)


def strict_files(files: list[Path]) -> list[Path]:
    """审计报告（`REVIEW-*.md`）豁免「引用写法」类检查 —— 判定见 `sdd_refs.is_audit`。"""
    return [p for p in files if not is_audit(str(p.relative_to(ROOT)))]


# --- 1~3：引用完整性 -------------------------------------------------------


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
                errors.append(f"[裸引用] {_rel(p)}:{i}  {line.strip()[:90]}")


def check_source_refs(files: list[Path], items: dict[str, set[tuple[int, int]]]) -> None:
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            # iter_refs 已展开 `§A,§B` 与 `§A-§B`，故压缩写法中的越界条号同样会被抓到
            for name, n in iter_refs(line):
                if n not in items[name]:
                    errors.append(f"[来源条号不存在] {_rel(p)}:{i}  {name} §{n}")


def check_file_refs(files: list[Path]) -> None:
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
                warnings.append(f"[文件引用可能失效] {_rel(p)}:{i}  `{ref}`")


# --- 4~5：Decision 契约 ----------------------------------------------------


def check_decision_json() -> None:
    """(a) specs/*/decision.json —— 真 JSON Schema 校验 + 复杂度预算。"""
    if not SCHEMA_PATH.exists():
        errors.append("[Schema] 缺少 .sdd/schema/decision.schema.json")
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    found = sorted(ROOT.glob("specs/*/decision.json"))
    counters["decision.json"] = len(found)
    for p in found:
        rel = _rel(p)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"[decision.json 非法 JSON] {rel}  {e}")
            continue
        for msg in mini_schema.validate(data, schema):
            errors.append(f"[Decision Schema 违规（真校验）] {rel}  {msg}")
        check_complexity_json(data, rel)
        check_cost_consistency(data, rel)


def _arch(data) -> dict:
    if isinstance(data, dict) and isinstance(data.get("architecture_decision"), dict):
        return data["architecture_decision"]
    return {}


def check_complexity_json(data, rel: Path) -> None:
    cplx = _arch(data).get("complexity")
    if not isinstance(cplx, dict):
        warnings.append(f"[复杂度预算] {rel} 未记录 complexity（score/budget）")
        return
    score, budget = cplx.get("score"), cplx.get("budget")
    if isinstance(score, int) and isinstance(budget, int) and score > budget:
        errors.append(f"[复杂度超预算] {rel}  score={score} > budget={budget}")


def check_cost_consistency(data, rel: Path) -> None:
    """(modv2.md §7) 预算上限未知却判定"在预算内"是逻辑矛盾。"""
    cost = _arch(data).get("cost")
    if not isinstance(cost, dict):
        return
    cap = cost.get("cap")
    within = cost.get("within_budget")
    cap_unknown = cap is None or (isinstance(cap, str) and cap.strip().upper() == "UNKNOWN")
    if cap_unknown and within is True:
        errors.append(
            f"[Cost 逻辑矛盾] {rel}  cap 未知却 within_budget=true"
            f"（应为 null 并说明 budget_basis；见 modv2.md §7）"
        )
    if within is True and not cost.get("budget_basis"):
        warnings.append(f"[Cost 依据缺失] {rel}  within_budget=true 但未写 budget_basis")


def check_decision_contract(files: list[Path]) -> None:
    """(b) Markdown 中的 Decision Contract（YAML 块）—— structural validation only。"""
    if not SCHEMA_PATH.exists():
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    required = schema["properties"]["architecture_decision"]["required"]

    for p in files:
        if "specs" not in _rel(p).parts:
            continue
        for block in YAML_BLOCK.findall(p.read_text(encoding="utf-8")):
            if "architecture_decision:" not in block:
                continue
            for key in required:
                if not re.search(rf"^\s{{2,4}}{key}:", block, re.M):
                    errors.append(f"[Decision Contract 结构缺项] {_rel(p)}  缺少 `{key}`")
            m_score = re.search(r"score:\s*(\d+)", block)
            m_budget = re.search(r"budget:\s*(\d+)", block)
            if m_score and m_budget:
                s, b = int(m_score.group(1)), int(m_budget.group(1))
                if s > b:
                    errors.append(f"[复杂度超预算] {_rel(p)}  score={s} > budget={b}")


# --- 6：Verification -------------------------------------------------------


def check_verification_json() -> None:
    """(a) specs/*/verification.json —— 真 JSON Schema 校验。"""
    if not VERIF_SCHEMA_PATH.exists():
        errors.append("[Schema] 缺少 .sdd/schema/verification.schema.json")
        return
    schema = json.loads(VERIF_SCHEMA_PATH.read_text(encoding="utf-8"))
    found = sorted(ROOT.glob("specs/*/verification.json"))
    counters["verification.json"] = len(found)
    for p in found:
        rel = _rel(p)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"[verification.json 非法 JSON] {rel}  {e}")
            continue
        for msg in mini_schema.validate(data, schema):
            errors.append(f"[Verification Schema 违规（真校验）] {rel}  {msg}")


def check_verification_artifact() -> None:
    """(b) specs/<id>/verification.md 必填且含 8 节骨架（LAYOUT.md §1.1）。"""
    for d in sorted(p for p in (ROOT / "specs").glob("*") if p.is_dir()):
        md = d / "verification.md"
        if not md.exists():
            errors.append(
                f"[Verification 缺失] {_rel(d)}/ 无 verification.md"
                f"（LAYOUT.md §1.1 标为必填；模板见 .sdd/templates/verification.md）"
            )
            continue
        text = md.read_text(encoding="utf-8")
        counters["verification.md"] = counters.get("verification.md", 0) + 1
        missing = [h for h in VERIF_HEADINGS if h not in text]
        if missing:
            errors.append(
                f"[Verification 结构缺节] {_rel(md)}  缺少 {missing}"
                f"（对照 .sdd/templates/verification.md）"
            )
        if not re.search(r"Status:\s*(Draft|Passed|Passed with Known Issues|Failed)", text):
            errors.append(f"[Verification Status 非法] {_rel(md)}  未找到合法 `Status:` 取值")
        if not VERDICT_LINE.search(text):
            errors.append(f"[Verification 缺 Verdict] {_rel(md)}  未找到 PASS / PASS WITH KNOWN ISSUES / FAIL")
        # Passed 不得与 NOT RUN / FAIL 并存
        status = re.search(r"Status:\s*(Draft|Passed|Passed with Known Issues|Failed)", text)
        if status and status.group(1) == "Passed" and re.search(r"\bNOT RUN\b", text):
            errors.append(f"[Verification 自相矛盾] {_rel(md)}  Status=Passed 但存在 NOT RUN 项")


def check_verification_mirror() -> None:
    """(c) verification.md ↔ verification.json 的 Status / Verdict / AC 集合一致。"""
    for jp in sorted(ROOT.glob("specs/*/verification.json")):
        mp = jp.with_suffix(".md")
        if not mp.exists():
            continue
        try:
            v = json.loads(jp.read_text(encoding="utf-8")).get("verification", {})
        except json.JSONDecodeError:
            continue
        text = mp.read_text(encoding="utf-8")
        m = re.search(r"Status:\s*(Draft|Passed|Passed with Known Issues|Failed)", text)
        if m and m.group(1) != v.get("status"):
            errors.append(
                f"[Verification 镜像不一致] {_rel(mp)}  Status={m.group(1)}"
                f" 与 {_rel(jp)} 的 {v.get('status')} 不符"
            )
        vm = VERDICT_LINE.search(text)
        if vm and vm.group(1) != v.get("verdict"):
            errors.append(
                f"[Verification 镜像不一致] {_rel(mp)}  Verdict={vm.group(1)}"
                f" 与 {_rel(jp)} 的 {v.get('verdict')} 不符"
            )
        md_acs = set(AC_ID.findall(text))
        json_acs = {ac.get("id") for ac in v.get("acceptance_criteria", []) if isinstance(ac, dict)}
        if md_acs != json_acs:
            errors.append(
                f"[Verification 镜像不一致] {_rel(mp)}  AC 集合 {sorted(md_acs)}"
                f" ≠ {_rel(jp)} 的 {sorted(json_acs)}"
            )


# --- 8~9：版本与 Canonical 不变量 -------------------------------------------


def check_version_consistency() -> None:
    """(modv2.md §12) 版本号只有一个来源：.sdd/VERSION。"""
    if not VERSION_PATH.exists():
        errors.append("[版本] 缺少 .sdd/VERSION（版本号的唯一来源）")
        return
    version = VERSION_PATH.read_text(encoding="utf-8").strip()
    counters["version"] = 1
    if not re.fullmatch(r"\d+\.\d+(\.\d+)?", version):
        errors.append(f"[版本] .sdd/VERSION 内容非法：{version!r}")
        return
    for rel_doc, pattern in (
        ("README.md", r"当前规则库版本[:：]\s*\*\*v?([0-9.]+)\*\*"),
        (".sdd/README.md", r"当前规则库版本[:：]\s*\*\*v?([0-9.]+)\*\*"),
    ):
        p = ROOT / rel_doc
        if not p.exists():
            warnings.append(f"[版本] {rel_doc} 不存在，跳过一致性检查")
            continue
        m = re.search(pattern, p.read_text(encoding="utf-8"))
        if not m:
            errors.append(f"[版本] {rel_doc} 未声明「当前规则库版本：**vX.Y**」")
        elif m.group(1) != version:
            errors.append(f"[版本漂移] {rel_doc} 声明 v{m.group(1)} ≠ .sdd/VERSION 的 {version}")
    cl = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    latest = re.search(r"^##\s*\[v([0-9.]+)\]", cl, re.M)
    if not latest:
        errors.append("[版本] CHANGELOG.md 未找到 `## [vX.Y]` 版本标题")
    elif latest.group(1) != version:
        errors.append(f"[版本漂移] CHANGELOG 最新版本 v{latest.group(1)} ≠ .sdd/VERSION 的 {version}")


def check_canonical_registry() -> None:
    """归属矩阵（文档）与登记表（代码）必须一致。"""
    if not CANONICAL_PATH.exists():
        errors.append("[Canonical] 缺少 .sdd/CANONICAL.md（规则归属矩阵）")
        return
    text = CANONICAL_PATH.read_text(encoding="utf-8")
    for topic, authority in CANONICAL_TOPICS:
        if authority not in text:
            errors.append(
                f"[Canonical 登记不同步] {topic} 的权威 `{authority}` 未在 .sdd/CANONICAL.md 出现"
            )


def check_workflow_order() -> None:
    """`Draft Spec` 必须早于技术决策（modv2.md §1/§2/§13 的共同要求）。"""
    for rel_doc in WORKFLOW_FILES:
        p = ROOT / rel_doc
        if not p.exists():
            warnings.append(f"[Workflow] {rel_doc} 不存在，跳过顺序检查")
            continue
        text = p.read_text(encoding="utf-8")
        drafts = [m.start() for m in re.finditer(r"Draft\s*Spec|Status:\s*Draft|Draft Specification", text)]
        techs = [m.start() for m in re.finditer("|".join(TECH_MARKERS), text)]
        if not drafts or not techs:
            continue
        if min(drafts) > min(techs):
            errors.append(
                f"[Workflow 顺序倒置] {rel_doc}  首次出现技术决策早于 Draft Spec"
                f"（顺序见 .sdd/workflows/new-project.md）"
            )


def check_forbidden_semantics(files: list[Path]) -> None:
    """旧决策语义不得回流（modv2.md §1/§8 的回归防护）。

    豁免：`CHANGELOG.md`（历史记录必须能写明当次改掉了什么）与审计报告；
    以及**显式标注 `【已废弃】` 的行** —— 需要解释"旧规则是什么"时，加上该标记即可。
    """
    for p in files:
        rel = str(_rel(p))
        if is_audit(p.name) or p.name == "CHANGELOG.md":
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            if "【已废弃】" in line:
                continue
            for phrase in FORBIDDEN_SEMANTICS:
                if phrase in line:
                    errors.append(
                        f"[旧决策语义回流] {rel}:{i}  出现「{phrase}」"
                        f"（若为解释历史，请在该行标注 【已废弃】）"
                    )


def check_artifact_requiredness() -> None:
    """LAYOUT 标「必填」的产物必须真有模板或契约（modv2.md §3/§4）。"""
    if not LAYOUT_PATH.exists():
        return
    text = LAYOUT_PATH.read_text(encoding="utf-8")
    for name in re.findall(r"[├└]──\s+([a-z0-9\-]+\.md)\s+#\s*必填", text):
        if not (ROOT / ".sdd" / "templates" / name).exists():
            errors.append(
                f"[产物无模板] LAYOUT.md 标 `{name}` 必填，但 .sdd/templates/{name} 不存在"
            )


def check_traceability_fresh() -> None:
    tb = ROOT / ".sdd" / "TRACEABILITY.md"
    if not tb.exists():
        warnings.append("[TRACEABILITY] 文件不存在，可运行 scripts/gen_traceability.py 生成")
        return
    if "（无）" not in tb.read_text(encoding="utf-8").split("## 校验")[-1]:
        errors.append("[TRACEABILITY] 存在引用了不存在条号的记录（见文件末节）")
    if not (ROOT / ".sdd" / "traceability.json").exists():
        warnings.append("[TRACEABILITY] 缺少机器可读版 .sdd/traceability.json，请重跑生成脚本")


def main() -> int:
    files = targets()
    strict = strict_files(files)
    items = {name: parse_source_items(name, path) for name, path in SOURCES.items()}

    check_bare_refs(strict)
    check_source_refs(strict, items)
    check_file_refs(files)
    check_decision_json()
    check_decision_contract(files)
    check_verification_json()
    check_verification_artifact()
    check_verification_mirror()
    check_version_consistency()
    check_canonical_registry()
    check_workflow_order()
    check_forbidden_semantics(files)
    check_artifact_requiredness()
    check_traceability_fresh()

    print(f"扫描 {len(files)} 个 Markdown 文件；来源 {len(SOURCES)} 份")
    print(
        f"真 Schema 校验：decision.json {counters.get('decision.json', 0)} 个 / "
        f"verification.json {counters.get('verification.json', 0)} 个；"
        f"verification.md {counters.get('verification.md', 0)} 份；"
        f"版本 {VERSION_PATH.read_text(encoding='utf-8').strip() if VERSION_PATH.exists() else 'N/A'}\n"
    )
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
