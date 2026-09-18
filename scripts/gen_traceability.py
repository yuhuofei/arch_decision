#!/usr/bin/env python3
"""由源文档与规则库自动生成 `.sdd/TRACEABILITY.md`（源规则 → 落点反向索引）。

引用解析规则统一在 `scripts/sdd_refs.py`（逗号压缩、区间展开、子条目 `§N.M`、
按最近前置来源名归属）。修改扫描范围或解析规则时**只改那个模块**。

用法：
    python3 scripts/gen_traceability.py
退出码：0 = 无越界引用；1 = 存在引用了不存在条号的位置。
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdd_refs import (  # noqa: E402
    ROOT,
    SOURCES,
    Key,
    fmt_ref,
    iter_refs,
    parse_titles,
    targets,
)

OUT = ROOT / ".sdd" / "TRACEABILITY.md"

# 已知的真实落点缺失：内容在本仓确无对应物。人工分诊后登记于此，
# 使「未引用」清单不至于把真实缺口淹在噪声里。格式：(来源, 条号, 说明)
#
# 2026-09-19 一审登记 res.md §13/§81（NestJS 默认选型在本仓无落点），
# 二审已修复（AGENTS.md 默认矩阵 + decision-trees/backend.md §4 + knowledge/backend.md），故清空。
KNOWN_GAPS: list[tuple[str, Key, str]] = []


def collect_refs() -> dict[str, dict[Key, set[str]]]:
    """返回 {来源: {条号: {直接引用该条号的文件}}}。"""
    refs: dict[str, dict[Key, set[str]]] = {k: defaultdict(set) for k in SOURCES}
    for p in targets():
        rel = str(p.relative_to(ROOT))
        for name, key in iter_refs(p.read_text(encoding="utf-8")):
            refs[name][key].add(rel)
    return {k: dict(v) for k, v in refs.items()}


def rollup(refs: dict[Key, set[str]]) -> dict[Key, bool]:
    """顶层条目是否「已覆盖」——它自身或其任一子条目被引用即算覆盖。"""
    covered: dict[Key, bool] = {}
    for key in refs:
        covered[key] = True
        if key[1] > 0:
            covered[(key[0], 0)] = True
    return covered


def main() -> int:
    titles = {name: parse_titles(name, path) for name, path in SOURCES.items()}
    refs = collect_refs()

    lines: list[str] = []
    lines.append("# TRACEABILITY.md — 源规则 → 落点反向索引\n")
    lines.append("> 本文件由 `scripts/gen_traceability.py` **自动生成，请勿手工编辑**。\n")
    lines.append("> 用途：源文档升级时快速评估影响面——某条规则被本仓哪些文件引用。\n")
    lines.append(
        "> 引用解析（`§A,§B` 压缩、`§A-§B` 区间、`§N.M` 子条目）见 `scripts/sdd_refs.py`；"
        "书写约定见 `.sdd/CONVENTIONS.md` §1。\n"
    )
    lines.append(
        "> 读表约定：**（未引用）** = 无文件写明该条号为出处；"
        "**（未直接引用；见子条目）** = 只有它的 `§N.M` 被引用，父条目本身未出现。\n"
    )
    lines.append("\n---\n")

    stats: list[tuple[str, int, int]] = []
    for name in SOURCES:
        t = titles[name]
        r = refs[name]
        covered = rollup(r)

        lines.append(f"\n## {name}（条目 {len(t)} 条，含子条目）\n")
        lines.append("| 源规则 | 标题 | 落点文件 |")
        lines.append("| --- | --- | --- |")
        for key in sorted(t):
            files = sorted(r.get(key, ()))
            if files:
                cell = "<br>".join(f"`{f}`" for f in files)
            elif key[1] == 0 and covered.get(key):
                cell = "**（未直接引用；见子条目）**"
            else:
                cell = "**（未引用）**"
            label = fmt_ref(name, key)
            indent = "　" if key[1] > 0 else ""
            lines.append(f"| `{label}` | {indent}{t[key]} | {cell} |")

        missing = [
            k for k in sorted(t) if not (k in r or (k[1] == 0 and covered.get(k)))
        ]
        lines.append(f"\n**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：{len(missing)} 条**\n")
        if missing:
            lines.append("　")
            lines.append("　".join(f"`{fmt_ref(name, k)}`" for k in missing))
        else:
            lines.append("（无）")
        lines.append("")
        stats.append((name, len(t) - len(missing), len(t)))

    lines.append("\n---\n")
    lines.append("## 关于「未被引用」\n")
    lines.append("机器只能判断「有无写明出处」，不能判断「内容是否已被覆盖」。清单需人工分诊：\n")
    lines.append("- **已覆盖未标注**：内容已在知识/决策文件中表达，只是没写来源条号 —— 补标注即可。")
    lines.append("- **真实落点缺失**：该规则在本仓确无对应内容 —— 需新增落点，或在此显式登记为不适用。")
    lines.append("")
    lines.append(
        "> **引用率 ≠ 内容覆盖率。** 下表全空只说明「每条源规则都至少被一处声明为来源」，"
        "不说明该条已被完整、正确地落地。内容质量仍需人工评审。"
    )
    lines.append("")
    if KNOWN_GAPS:
        lines.append("**已确认的真实缺口**（人工分诊结果，登记于 `scripts/gen_traceability.py`）：\n")
        for name, key, why in KNOWN_GAPS:
            lines.append(f"- `{fmt_ref(name, key)}` —— {why}")
    else:
        lines.append("**已确认的真实缺口**：（无）")

    lines.append("\n---\n")
    lines.append("## 校验：引用了不存在的条号（应为空）\n")
    problems: list[str] = []
    for name in SOURCES:
        for key in sorted(set(refs[name]) - set(titles[name])):
            problems.append(
                f"- `{fmt_ref(name, key)}` → " + "、".join(sorted(refs[name][key]))
            )
    lines.append("\n".join(problems) if problems else "（无）")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"已生成 {OUT.relative_to(ROOT)}")
    for name, cov, total in stats:
        print(f"  {name}: {cov}/{total} 条被引用（覆盖率 {cov * 100 // max(total, 1)}%）")
    print(f"  引用不存在的条号：{len(problems)} 处")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
