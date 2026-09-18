#!/usr/bin/env python3
"""一次性迁移：把裸 `§N` 引用统一加来源前缀（默认 `res.md `）。

约定见 `.sdd/CONVENTIONS.md` §1。设计要点：

* 只处理**不带小数点**的 `§N`（含 `§3-§5` / `§67,§68,§69` 这类组）。
  带小数点的 `§N.M` 因为 `res.md` 与 `Matrix` 都有小数编号，必须人工判定来源，脚本不动。
* 按**段**判定前缀：段分隔符为 `； ; 。 换行`。段内出现任一已登记前缀（如 `res.md` / `Matrix` /
  `知识库` / `decision-protocol` / 本文件）则视为已消歧，跳过；否则补 `res.md `。
* 跳过 `sources/`、`.workbuddy/`、`scripts/` 与评审报告（其正文刻意引用旧的裸写法）。

用法：
    python3 scripts/migrate_refs.py            # 预览（不写盘）
    python3 scripts/migrate_refs.py --apply    # 写盘
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABELS = [
    "res.md",
    "res:",
    "Matrix",
    "知识库",
    "decision-protocol",
    "architecture.md",
    "backend.md",
    "frontend.md",
    "database.md",
    "caching.md",
    "messaging.md",
    "api.md",
    "security.md",
    "testing.md",
    "deployment.md",
    "observability.md",
    "ai-llm.md",
    "data.md",
    "project-discovery.md",
    "technology-selection.md",
    "spec.md",
    "plan.md",
    "design.md",
    "tasks.md",
    "verification.md",
    "adr.md",
    "new-project.md",
    "new-feature.md",
    "small-change.md",
    "bugfix.md",
    "refactor.md",
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "LAYOUT.md",
    "CONVENTIONS.md",
    "TRACEABILITY.md",
    "CHANGELOG.md",
    "本文件",
    "本模板",
    "本节",
    "该文件",
    "本文档",
]

SEP = re.compile(r"[；;。\n]")
REF = re.compile(r"§\d+(?!\.\d)(?:\s*[-–—,、]\s*§?\d+(?!\.\d))*")
BARE = re.compile(r"§\d+(?!\.\d)")

SKIP_DIRS = {"sources", ".workbuddy", "scripts", ".git"}
SKIP_FILES = {"REVIEW-2026-09-19.md"}


def iter_targets() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if rel.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        files.append(path)
    return files


def process_line(line: str) -> tuple[str, int]:
    """返回 (新行, 本次前缀次数)。"""
    out: list[str] = []
    last = 0
    added = 0
    for m in REF.finditer(line):
        start = m.start()
        seg_start = 0
        for sm in SEP.finditer(line[:start]):
            seg_start = sm.end()
        segment = line[seg_start:start]
        labelled = any(lb in segment for lb in LABELS)
        out.append(line[last:start])
        if labelled:
            out.append(m.group(0))
        else:
            out.append("res.md " + m.group(0))
            added += 1
        last = m.end()
    out.append(line[last:])
    return "".join(out), added


def main() -> int:
    apply = "--apply" in sys.argv
    total = 0
    changed_files = 0
    print(f"{'APPLY' if apply else 'DRY-RUN'}  root={ROOT}\n")
    for path in iter_targets():
        original = path.read_text(encoding="utf-8")
        lines = original.split("\n")
        added = 0
        new_lines = []
        for line in lines:
            new_line, n = process_line(line)
            added += n
            new_lines.append(new_line)
        if added == 0:
            continue
        changed_files += 1
        total += added
        rel = path.relative_to(ROOT)
        print(f"  {added:>3}  {rel}")
        if apply:
            path.write_text("\n".join(new_lines), encoding="utf-8")

    print(f"\n共 {changed_files} 个文件，补前缀 {total} 处。")

    # 校验：仍有裸 §N 的位置（含脚本不处理的 §N.M）
    print("\n--- 仍为裸 § 的位置（需人工确认）---")
    remaining = 0
    for path in iter_targets():
        for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for m in BARE.finditer(line):
                start = m.start()
                seg_start = 0
                for sm in SEP.finditer(line[:start]):
                    seg_start = sm.end()
                segment = line[seg_start:start]
                if any(lb in segment for lb in LABELS):
                    continue
                remaining += 1
                rel = path.relative_to(ROOT)
                print(f"  {rel}:{i}  {line.strip()[:100]}")
    print(f"\n残留 {remaining} 处。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
