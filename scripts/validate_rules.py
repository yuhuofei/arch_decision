#!/usr/bin/env python3
"""规则库自检（纯标准库，无需第三方依赖）。

检查项：
  1. 引用编号   —— 全仓禁止裸写 `§N`（约定见 .sdd/CONVENTIONS.md §1）
  2. 来源条号   —— `res.md §N` / `Matrix §N` / `知识库 §N` 的 N 必须真实存在
  3. 文件引用   —— 反引号内的 `.md` 路径必须真实存在（占位符与按需产物除外）
  4. 决策 Schema —— specs/ 下 Decision Output Schema 代码块的必填项
  5. 复杂度预算 —— complexity.score 不得大于 complexity.budget

用法：
    python3 scripts/validate_rules.py
退出码：0 = 全部通过；1 = 存在错误。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "v1.0"

SKIP_DIRS = {"sources", ".workbuddy", ".git", "scripts", "node_modules"}
SKIP_FILES = {"REVIEW-2026-09-19.md"}

SOURCES = {
    "res.md": SRC / "res.md",
    "Matrix": SRC / "AI Architecture Decision Matrix.md",
    "知识库": SRC / "AI Coding SDD 项目技术架构与框架选择知识库.md",
}

LABELS = [
    "res.md", "res:", "Matrix", "知识库", "decision-protocol",
    "architecture.md", "backend.md", "frontend.md", "database.md", "caching.md",
    "messaging.md", "api.md", "security.md", "testing.md", "deployment.md",
    "observability.md", "ai-llm.md", "data.md",
    "project-discovery.md", "technology-selection.md", "spec.md", "plan.md",
    "design.md", "tasks.md", "verification.md", "adr.md",
    "new-project.md", "new-feature.md", "small-change.md", "bugfix.md", "refactor.md",
    "CLAUDE.md", "AGENTS.md", "README.md", "LAYOUT.md", "CONVENTIONS.md",
    "TRACEABILITY.md", "CHANGELOG.md",
    "本文件", "本模板", "本节", "该文件", "本文档",
]

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
REF = re.compile(r"(res\.md|Matrix|知识库) §(\d+)")
BACKTICK_MD = re.compile(r"`([A-Za-z0-9._\-/]*[A-Za-z0-9_\-]\.md)`")
YAML_BLOCK = re.compile(r"```ya?ml\n(.*?)```", re.S)

errors: list[str] = []
warnings: list[str] = []


def targets() -> list[Path]:
    out: list[Path] = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if p.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        out.append(p)
    return out


def parse_source_items(name: str, path: Path) -> set[int]:
    items: set[int] = set()
    cjk = re.compile(r"[\u4e00-\u9fff]")
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^#*\s*(\d+)\.\s+(.+?)\s*$", line)
        if not m:
            continue
        if line.lstrip().startswith("#"):
            pass
        elif name == "res.md":
            if cjk.search(m.group(2)):
                continue
        else:
            continue
        items.add(int(m.group(1)))
    return items


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


def check_source_refs(files: list[Path], items: dict[str, set[int]]) -> None:
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            for m in REF.finditer(line):
                name, n = m.group(1), int(m.group(2))
                if n not in items[name]:
                    errors.append(
                        f"[来源条号不存在] {p.relative_to(ROOT)}:{i}  {name} §{n}"
                    )


def check_file_refs(files: list[Path]) -> None:
    all_md = {p.name for p in ROOT.rglob("*.md")}
    all_rel = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*.md")}
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            for m in BACKTICK_MD.finditer(line):
                ref = m.group(1)
                if "<" in ref or ">" in ref or "{" in ref:
                    continue
                base = ref.split("/")[-1]
                if ref in all_rel or base in all_md or base in ALLOWED_MISSING:
                    continue
                if base.startswith("ADR-") or re.match(r"^adr-?\d", base):
                    continue
                warnings.append(
                    f"[文件引用可能失效] {p.relative_to(ROOT)}:{i}  `{ref}`"
                )


def check_decision_schema(files: list[Path]) -> None:
    schema_path = ROOT / ".sdd" / "schema" / "decision.schema.json"
    if not schema_path.exists():
        warnings.append("[Schema] 缺少 .sdd/schema/decision.schema.json")
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = schema["properties"]["architecture_decision"]["required"]

    for p in files:
        if "specs" not in p.relative_to(ROOT).parts:
            continue
        text = p.read_text(encoding="utf-8")
        for block in YAML_BLOCK.findall(text):
            if "architecture_decision:" not in block:
                continue
            for key in required:
                if not re.search(rf"^\s{{2,4}}{key}:", block, re.M) and f"{key}:" not in block:
                    errors.append(
                        f"[Decision Schema 缺必填项] {p.relative_to(ROOT)}  缺少 `{key}`"
                    )
            # 复杂度预算校验
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
    check_decision_schema(files)
    check_traceability_fresh()

    print(f"扫描 {len(files)} 个 Markdown 文件\n")
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
