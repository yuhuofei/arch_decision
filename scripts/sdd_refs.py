#!/usr/bin/env python3
"""源文档引用解析的唯一实现（`gen_traceability.py` 与 `validate_rules.py` 共用）。

存在的理由：这两个脚本原先各自维护一份 `(res\\.md|Matrix|知识库) §(\\d+)` 正则，
它只认「来源名 + 紧随其后的单个 §N」，漏掉两类合法写法：

* 逗号压缩：`Matrix §24,§25,§45`  —— 只识别到 §24
* 区间：    `res.md §50-§58`       —— 只识别到 §50
* 子条目：  `知识库 §6.1`          —— 被截断记成 §6，张冠李戴

实测库内共 69 处压缩/区间写法、30+ 处子条目引用。漏识别造成两个后果：
  1. TRACEABILITY.md 误报大量「（未引用）」，误导「该规则可安全删除」的判断；
  2. 校验脚本放过了压缩写法中的越界条号（如 `Matrix §3,§999`）。

两份实现必然漂移，故合并为本模块。修改解析规则时**只改这里**。

条号模型：`(major, minor)` 二元组。
  * `§12`   → `(12, 0)`   「顶层条目」
  * `§12.3` → `(12, 3)`   「子条目」
用同一命名空间可让排序自然，也便于区分「引用了 §6」与「引用了 §6.1」。

用法：
    from sdd_refs import iter_refs, parse_source_items, parse_titles, fmt_ref, SOURCES
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "v1.0"

SOURCES: dict[str, Path] = {
    "res.md": SRC / "res.md",
    "Matrix": SRC / "AI Architecture Decision Matrix.md",
    "知识库": SRC / "AI Coding SDD 项目技术架构与框架选择知识库.md",
}
SOURCE_NAMES = tuple(SOURCES)

# 扫描范围：全仓 Markdown，排除源文档归档、本地状态、脚本目录
SKIP_DIRS = {"sources", ".workbuddy", ".git", "scripts", "node_modules"}
# 生成物自身（自引用无意义）与临时审计报告（非规范性文档）不入索引
SKIP_FILES = {"TRACEABILITY.md", "REVIEW-2026-09-19.md"}

Key = tuple[int, int]  # (major, minor)，minor == 0 表示顶层条目

_SOURCE_RE = re.compile(r"res\.md|Matrix|知识库")
_NUM_RE = re.compile(r"§\s*(\d+)(?:\.(\d+))?")
# 区间必须两侧都带 §（如 `§50-§58`、`§1.2-§1.4`）。裸 `§1-2` 全库不存在，若支持会与
# 「§1 的 2 项」这类叙述冲突，故不识别。
_RANGE_RE = re.compile(
    r"§\s*(\d+(?:\.\d+)?)\s*[-–—~～]\s*§\s*(\d+(?:\.\d+)?)"
)

# 单次区间展开上限：防止把笔误（如 §1-§9999）展开成海量条号
_MAX_RANGE_SPAN = 300

_TOP_RE = re.compile(r"^#*\s*(\d+)\.\s+(.+?)\s*$")
_SUB_RE = re.compile(r"^#+\s*(\d+)\.(\d+)\s+(.+?)\s*$")
_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
_MAX_TITLE_LEN = 70


def fmt_ref(name: str, key: Key) -> str:
    """`(name, key)` → `"res.md §1"` / `"知识库 §6.1"`。"""
    major, minor = key
    return f"{name} §{major}" if minor == 0 else f"{name} §{major}.{minor}"


def _split_num(s: str) -> Key:
    major, _, minor = s.partition(".")
    return int(major), int(minor) if minor else 0


def expand_ranges(line: str) -> str:
    """把 `§50-§58` / `§1.2-§1.4` 就地展开为逐个条号，使后续只需处理单个 §N。

    展开规则：
    * 两端均为顶层（`§50-§58`）    → 顶层区间
    * 同主号且带小数（`§1.2-§1.4`）→ 子条目区间
    * 跨主号且带小数（`§1.2-§3.4`）→ **不展开**（语义不唯一，宁可保留原样）
    """

    def repl(m: re.Match[str]) -> str:
        a, b = _split_num(m.group(1)), _split_num(m.group(2))
        if a > b:
            a, b = b, a
        if a[1] == 0 and b[1] == 0:
            keys = [(n, 0) for n in range(a[0], b[0] + 1)]
        elif a[0] == b[0]:
            keys = [(a[0], n) for n in range(a[1], b[1] + 1)]
        else:
            return m.group(0)
        if len(keys) > _MAX_RANGE_SPAN:
            return m.group(0)
        return ",".join(fmt_ref("", k).lstrip() for k in keys)

    return _RANGE_RE.sub(repl, line)


def iter_refs(text: str):
    """逐行产出 `(来源名, (major, minor))`。

    归属规则：每个 `§N` 归属于**其前方最近的一个来源名**。这样一行内的
    `res.md §60-§65,§86；Matrix §24,§25；知识库 §44-§46` 三组引用各自归位，
    无需按标点切分（`；`、`。` 分隔符在源文档里并不统一）。
    """
    for line in text.split("\n"):
        line = expand_ranges(line)
        tokens: list[tuple[int, int, object]] = []
        for m in _SOURCE_RE.finditer(line):
            tokens.append((m.start(), 0, m.group(0)))
        for m in _NUM_RE.finditer(line):
            minor = int(m.group(2)) if m.group(2) else 0
            tokens.append((m.start(), 1, (int(m.group(1)), minor)))
        tokens.sort()

        current: str | None = None
        for _, kind, val in tokens:
            if kind == 0:
                current = str(val)
            elif current is not None:
                yield current, val  # type: ignore[misc]


def _title_lines(name: str, path: Path):
    """产出源文档中形如 `N. TITLE` / `N.M TITLE` 的条目。

    源文档格式不统一，需分别处理：
    * `res.md`：部分条目写作 `# N. TITLE`，部分写作裸 `N. TITLE`（全大写英文）；
      `§0` / `§117` / `§118` 内部含中文编号列表，借「无 CJK」排除。
    * `Matrix` / `知识库`：条目均为 Markdown 标题（`#` 开头），标题可为中文。
    子条目（`N.M`）恒为 `#` 标题，不受上述排除规则影响。
    """
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = _SUB_RE.match(line)
        if m:
            yield (
                (int(m.group(1)), int(m.group(2))),
                m.group(3).strip(),
            )
            continue

        m = _TOP_RE.match(line)
        if not m:
            continue
        if line.lstrip().startswith("#"):
            ok = True
        elif name == "res.md":
            ok = not _CJK_RE.search(m.group(2))
        else:
            ok = False
        if ok:
            yield (int(m.group(1)), 0), m.group(2).strip()


def parse_source_items(name: str, path: Path) -> set[Key]:
    """源文档中真实存在的条号集合（用于「引用条号是否存在」校验）。"""
    return {k for k, _ in _title_lines(name, path)}


def parse_titles(name: str, path: Path) -> dict[Key, str]:
    """条号 → 标题（只取每个条号的首次出现；超长标题视为正文列表，跳过）。"""
    titles: dict[Key, str] = {}
    for k, title in _title_lines(name, path):
        if k not in titles and len(title) < _MAX_TITLE_LEN:
            titles[k] = title
    return titles


def targets() -> list[Path]:
    """参与引用统计的 Markdown 文件（两个脚本共用，避免范围漂移）。"""
    out: list[Path] = []
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if p.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        out.append(p)
    return out


if __name__ == "__main__":  # 自检：解析规则的可视化验证
    for src_path in targets():
        rel = src_path.relative_to(ROOT)
        refs = list(iter_refs(src_path.read_text(encoding="utf-8")))
        if refs:
            print(f"{rel}: {len(refs)} 处引用")
