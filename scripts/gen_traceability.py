#!/usr/bin/env python3
"""由源文档与规则库自动生成 `.sdd/TRACEABILITY.md`（源规则 → 落点反向索引）。

引用解析规则统一在 `scripts/sdd_refs.py`（逗号压缩、区间展开、子条目 `§N.M`、
按最近前置标签归属）。修改扫描范围或解析规则时**只改那个模块**。

**四态模型**（`modv2.md §14`）：旧版只有"被引用 / 未被引用"两态，而"被引用"
既不能证明"被实现"，也不能证明"被验证"。现按证据强度分四级：

    SOURCE → MAPPED → IMPLEMENTED → VERIFIED

    UNMAPPED      无任何文件写明该条号为出处
    MAPPED        只有描述层文件（README / CHANGELOG / REVIEW）提到
    IMPLEMENTED   至少有一处「实现层」落点（knowledge / decision-trees /
                  templates / workflows / schema / examples / specs / 入口文件）
    VERIFIED      已实现，且另有机器校验项覆盖（见 VERIFIED_BY 登记表）

`MAPPED` 与 `IMPLEMENTED` 由落点路径自动判定；`VERIFIED` **必须人工登记**
（`VERIFIED_BY`）——机器无法推断"这条规则该由哪个检查项验证"。

用法：
    python3 scripts/gen_traceability.py
产出：`.sdd/TRACEABILITY.md`（人读）+ `.sdd/traceability.json`（机器可读）
退出码：0 = 无越界引用；1 = 存在引用了不存在条号的位置。
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdd_refs import (  # noqa: E402
    ROOT,
    SOURCES,
    Key,
    fmt_ref,
    is_audit,
    is_implementing,
    iter_refs,
    parse_titles,
    targets,
)

OUT = ROOT / ".sdd" / "TRACEABILITY.md"
OUT_JSON = ROOT / ".sdd" / "traceability.json"

# 已知的真实落点缺失：内容在本仓确无对应物。人工分诊后登记于此，
# 使「未引用」清单不至于把真实缺口淹在噪声里。格式：(来源, 条号, 说明)
#
# 2026-09-19 一审登记 res.md §13/§81（NestJS 默认选型在本仓无落点），
# 二审已修复（AGENTS.md 默认矩阵 + decision-trees/backend.md §4 + knowledge/backend.md），故清空。
KNOWN_GAPS: list[tuple[str, Key, str]] = []

# 状态排序（数值越大证据越强）
STATE_ORDER = {"UNMAPPED": 0, "MAPPED": 1, "IMPLEMENTED": 2, "VERIFIED": 3}
STATE_LABEL = {
    "UNMAPPED": "**（未引用）**",
    "MAPPED": "MAPPED",
    "IMPLEMENTED": "IMPLEMENTED",
    "VERIFIED": "**VERIFIED**",
}

# 机器校验登记表：{(来源, 条号): 校验项名称}。
# **只登记真实存在的检查项**（都在 scripts/validate_rules.py 里）——
# 登记一个不存在的检查项等于伪造"已机器验证"，比不登记更有害。
VERIFIED_BY: dict[tuple[str, Key], str] = {
    ("Matrix", (32, 0)): "check_complexity_json",
    ("Matrix", (40, 0)): "check_decision_json",
    ("res.md", (88, 0)): "check_version_consistency",
    ("modv2.md", (4, 0)): "check_verification_artifact",
    ("modv2.md", (6, 0)): "check_decision_json",
    ("modv2.md", (7, 0)): "check_cost_consistency",
    ("modv2.md", (12, 0)): "check_version_consistency",
}


def collect_refs() -> dict[str, dict[Key, set[str]]]:
    """返回 {来源: {条号: {直接引用该条号的文件}}}。"""
    refs: dict[str, dict[Key, set[str]]] = {k: defaultdict(set) for k in SOURCES}
    for p in targets():
        rel = str(p.relative_to(ROOT))
        for name, key in iter_refs(p.read_text(encoding="utf-8")):
            refs[name][key].add(rel)
    return {k: dict(v) for k, v in refs.items()}


def state_of(name: str, key: Key, files: set[str]) -> str:
    """按落点类别与登记表判定证据层级。"""
    if (name, key) in VERIFIED_BY:
        return "VERIFIED"
    if any(is_implementing(f) for f in files):
        return "IMPLEMENTED"
    return "MAPPED"


def states_for(name: str, refs: dict[Key, set[str]]) -> dict[Key, str]:
    """逐条号求状态；父条目未被直接引用但子条目被引用时，继承子条目的最强状态。"""
    states: dict[Key, str] = {k: state_of(name, k, files) for k, files in refs.items()}
    for key, state in list(states.items()):
        if key[1] == 0:
            continue
        parent = (key[0], 0)
        if STATE_ORDER[state] > STATE_ORDER.get(states.get(parent, "UNMAPPED"), 0):
            states[parent] = state
    return states


def main() -> int:
    titles = {name: parse_titles(name, path) for name, path in SOURCES.items()}
    refs = collect_refs()

    lines: list[str] = []
    lines.append("# TRACEABILITY.md — 源规则 → 落点反向索引\n")
    lines.append("> 本文件由 `scripts/gen_traceability.py` **自动生成，请勿手工编辑**。")
    lines.append("> 机器可读版本：`.sdd/traceability.json`。\n")
    lines.append("> 用途：源文档升级时快速评估影响面——某条规则被本仓哪些文件引用、落到哪一层。\n")
    lines.append(
        "> 引用解析（`§A,§B` 压缩、`§A-§B` 区间、`§N.M` 子条目）见 `scripts/sdd_refs.py`；"
        "书写约定见 `.sdd/CONVENTIONS.md` §1。\n"
    )
    lines.append("> **四态模型**（`modv2.md §14`）：证据强度由弱到强为")
    lines.append("> `MAPPED` → `IMPLEMENTED` → `VERIFIED`；`**（未引用）**` 表示无文件写明该条号为出处。")
    lines.append("> `MAPPED` 只说明被描述层文件（README / CHANGELOG / REVIEW）提到；")
    lines.append("> `IMPLEMENTED` 说明有实现层落点；`VERIFIED` 说明另有机器校验项覆盖。\n")
    lines.append("> **（未直接引用；见子条目）** = 只有它的 `§N.M` 被引用，父条目本身未出现。\n")
    lines.append("> 状态只衡量**证据层级**，**不衡量内容是否被正确、完整地实现**——见文末说明。\n")
    lines.append("\n---\n")

    machine: dict[str, dict[str, dict[str, object]]] = {}
    summary: list[tuple[str, dict[str, int], int]] = []

    for name in SOURCES:
        t = titles[name]
        r = refs[name]
        states = states_for(name, r)

        lines.append(f"\n## {name}（条目 {len(t)} 条，含子条目）\n")
        lines.append("| 源规则 | 标题 | 状态 | 落点文件 |")
        lines.append("| --- | --- | --- | --- |")
        counts: dict[str, int] = defaultdict(int)
        for key in sorted(t):
            files = sorted(r.get(key, ()))
            state = states.get(key, "UNMAPPED")
            counts[state] += 1
            if state == "UNMAPPED":
                stxt, cell = "**（未引用）**", "**（未引用）**"
            else:
                stxt = STATE_LABEL[state]
                verified = VERIFIED_BY.get((name, key))
                if verified:
                    stxt = f"**VERIFIED**<br>`{verified}`"
                cell = (
                    "<br>".join(f"`{f}`" for f in files)
                    if files
                    else "**（未直接引用；见子条目）**"
                )
            indent = "　" if key[1] > 0 else ""
            lines.append(f"| `{fmt_ref(name, key)}` | {indent}{t[key]} | {stxt} | {cell} |")

        missing = [k for k in sorted(t) if states.get(k, "UNMAPPED") == "UNMAPPED"]
        lines.append(f"\n**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：{len(missing)} 条**\n")
        lines.append("（无）" if not missing else "　" + "　".join(f"`{fmt_ref(name, k)}`" for k in missing))
        lines.append("")
        lines.append(
            f"状态分布：IMPLEMENTED {counts['IMPLEMENTED']} ／ VERIFIED {counts['VERIFIED']} ／ "
            f"MAPPED {counts['MAPPED']} ／ 未引用 {counts['UNMAPPED']}"
        )
        lines.append("")
        summary.append((name, dict(counts), len(t)))
        machine[name] = {
            fmt_ref(name, k): {
                "state": states.get(k, "UNMAPPED"),
                "title": t[k],
                "refs": sorted(r.get(k, ())),
                "verified_by": VERIFIED_BY.get((name, k)),
            }
            for k in sorted(t)
        }

    lines.append("\n---\n")
    lines.append("## 关于「未被引用」与四态\n")
    lines.append("机器只能判断「有无写明出处」与「落点在不在实现层」，**不能判断内容是否正确**。")
    lines.append("清单需人工分诊：\n")
    lines.append("- **已覆盖未标注**：内容已在知识/决策文件中表达，只是没写来源条号 —— 补标注即可。")
    lines.append("- **真实落点缺失**：该规则在本仓确无对应内容 —— 需新增落点，或在此显式登记为不适用。")
    lines.append("")
    lines.append(
        "> **引用率 ≠ 内容覆盖率，`VERIFIED` ≠ 内容正确。** 本表只回答三个问题："
        "有没有落点 / 落点在不在实现层 / 有没有检查项。规则是否被正确完整地实现，仍需人工评审。"
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
    lines.append(
        "> 只统计**非审计文件**的越界引用。审计报告（`REVIEW-*.md`）为说明「这里原本写错了什么」"
        "会把缺陷原文照抄下来，故其越界写法单独列出、不计为违规。\n"
    )
    problems: list[str] = []
    audit_exempt: list[str] = []
    for name in SOURCES:
        for key in sorted(set(refs[name]) - set(titles[name])):
            files = sorted(refs[name][key])
            live = [f for f in files if not is_audit(f)]
            cell = "、".join(f"`{f}`" for f in files)
            if live:
                problems.append(
                    f"- `{fmt_ref(name, key)}` → " + "、".join(f"`{f}`" for f in live)
                )
            else:
                audit_exempt.append(f"- `{fmt_ref(name, key)}` → {cell}")
    lines.append("\n".join(problems) if problems else "（无）")
    lines.append("")
    if audit_exempt:
        lines.append("**审计报告中引用的历史越界写法（豁免）：**\n")
        lines.append("\n".join(audit_exempt))
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "_note": "由 scripts/gen_traceability.py 生成，勿手改。四态定义见 .sdd/CANONICAL.md 与 modv2.md §14。",
                "sources": machine,
                "out_of_range_refs": problems,
                "out_of_range_in_audit_exempted": audit_exempt,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"已生成 {OUT.relative_to(ROOT)} 与 {OUT_JSON.relative_to(ROOT)}")
    for name, counts, total in summary:
        imp = counts.get("IMPLEMENTED", 0) + counts.get("VERIFIED", 0)
        print(
            f"  {name}: 实现层 {imp}/{total}（{imp * 100 // max(total, 1)}%）"
            f"  VERIFIED {counts.get('VERIFIED', 0)}  未引用 {counts.get('UNMAPPED', 0)}"
        )
    print(f"  引用不存在的条号：{len(problems)} 处")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
