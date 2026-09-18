#!/usr/bin/env python3
"""由源文档与规则库自动生成 `.sdd/TRACEABILITY.md`（源规则 → 落点反向索引）。

用法：
    python3 scripts/gen_traceability.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "v1.0"
OUT = ROOT / ".sdd" / "TRACEABILITY.md"

SOURCES = {
    "res.md": SRC / "res.md",
    "Matrix": SRC / "AI Architecture Decision Matrix.md",
    "知识库": SRC / "AI Coding SDD 项目技术架构与框架选择知识库.md",
}

SCAN_DIRS = [".sdd", "specs"]
SKIP_FILES = {"TRACEABILITY.md", "REVIEW-2026-09-19.md"}


def parse_titles(name: str, path: Path) -> dict[int, str]:
    """抽取 `N. TITLE` 形式的条目标题（只取每个 N 的首次出现）。

    源文档格式不统一，需分别处理：
    * `res.md`：部分条目写作 `# N. TITLE`，部分写作裸 `N. TITLE`（全大写英文）；
      同时 §0 / §117 / §118 内部含有编号列表，必须排除。
    * `Matrix` / `知识库`：条目均为 Markdown 标题（`#` 开头），标题可为中文。
    """
    titles: dict[int, str] = {}
    cjk = re.compile(r"[\u4e00-\u9fff]")
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^#*\s*(\d+)\.\s+(.+?)\s*$", line)
        if not m:
            continue
        if line.lstrip().startswith("#"):
            ok = True
        elif name == "res.md":
            # res.md 的裸条目为英文全大写标题；借"无 CJK"排除 §0 的中文编号列表。
            # §117/§118 的英文编号列表由"每个 N 只取首次出现"规则自动排除。
            ok = not cjk.search(m.group(2))
        else:
            ok = False
        if not ok:
            continue
        n = int(m.group(1))
        title = m.group(2).strip()
        if n not in titles and len(title) < 70:
            titles[n] = title
    return titles


def collect_refs() -> tuple[dict[str, dict[int, set[str]]], dict[str, set[int]]]:
    """返回 {来源: {条号: {引用文件}}} 与 {来源: {显式引用过的条号}}。"""
    refs: dict[str, dict[int, set[str]]] = {k: defaultdict(set) for k in SOURCES}
    pattern = re.compile(r"(res\.md|Matrix|知识库) §(\d+)")
    for d in SCAN_DIRS:
        for p in sorted((ROOT / d).rglob("*.md")):
            if p.name in SKIP_FILES:
                continue
            rel = str(p.relative_to(ROOT))
            for m in pattern.finditer(p.read_text(encoding="utf-8")):
                refs[m.group(1)][int(m.group(2))].add(rel)
    return refs, {k: set(v) for k, v in refs.items()}  # type: ignore[return-value]


def main() -> int:
    titles = {name: parse_titles(name, path) for name, path in SOURCES.items()}
    refs, _ = collect_refs()

    lines: list[str] = []
    lines.append("# TRACEABILITY.md — 源规则 → 落点反向索引\n")
    lines.append("> 本文件由 `scripts/gen_traceability.py` **自动生成，请勿手工编辑**。\n")
    lines.append("> 用途：源文档升级时快速评估影响面——某条规则被本仓哪些文件引用。\n")
    lines.append("> 引用约定见 `.sdd/CONVENTIONS.md` §1。\n")
    lines.append("\n---\n")

    for name in ("res.md", "Matrix", "知识库"):
        t = titles[name]
        r = refs[name]
        lines.append(f"\n## {name}（共 {max(t) if t else 0} 条）\n")
        lines.append("| 源规则 | 标题 | 落点文件 |")
        lines.append("| --- | --- | --- |")
        for n in sorted(t):
            files = sorted(r.get(n, ()))
            cell = "<br>".join(f"`{f}`" for f in files) if files else "**（未引用）**"
            lines.append(f"| `{name} §{n}` | {t[n]} | {cell} |")
        missing = sorted(set(t) - set(r))
        lines.append(
            f"\n**未被显式引用的条号（{len(missing)} 条，非缺陷，仅供覆盖率参考）**："
        )
        lines.append(
            "、".join(f"{name} §{n}" for n in missing) if missing else "（无）"
        )
        lines.append("")

    # 反向：本仓有无引用不存在的条号
    lines.append("\n---\n")
    lines.append("## 校验：引用了不存在的条号（应为空）\n")
    problems = []
    for name in SOURCES:
        for n in sorted(set(refs[name]) - set(titles[name])):
            problems.append(f"- `{name} §{n}` → " + "、".join(sorted(refs[name][n])))
    lines.append("\n".join(problems) if problems else "（无）")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")

    total_cited = sum(len(refs[n]) for n in SOURCES)
    print(f"已生成 {OUT.relative_to(ROOT)}")
    for name in SOURCES:
        t, r = titles[name], refs[name]
        print(f"  {name}: {len(t)} 条，被引用 {len(r)} 条，未引用 {len(set(t) - set(r))} 条")
    print(f"  引用不存在的条号：{len(problems)} 处")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
