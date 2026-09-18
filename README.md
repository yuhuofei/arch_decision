# arch_decision — Agent SDD 项目框架选择规则库

> 给"用 SDD（Spec-Driven Development）模式编程的 Agent"提供一套**可解释的决策系统**，
> 而不是把 `Python + FastAPI + PostgreSQL` 当最佳实践硬塞给它。

---

## 这是什么

当用户说"帮我开发 XXX"时，Agent **不允许**直接从技术栈名称开始决策。它必须走：

```
分类项目 → 提取硬约束 → 生成候选 → 消除违规候选 → 评分
        → 选最简且充分的架构 → 标注决策状态 → 人工确认（必要时）
        → 固化 ADR + plan.md → 才允许写代码
```

本仓就是这套流程的规则载体。衡量标准不是"用了多先进的技术"，而是
Correctness + Maintainability + Simplicity + Testability + Observability + Security + Evolvability（`res.md §120`）。

---

## 快速导航（按角色）

| 你是 | 先读 |
| --- | --- |
| Agent（Claude Code / Cursor / Codex） | `CLAUDE.md`（何时读什么）、`AGENTS.md`（通用规则 + 读取顺序） |
| 人（想理解体系） | 本文件 → `.sdd/README.md` |
| 想知道"东西应该放哪" | `.sdd/LAYOUT.md` |
| 想知道"引用怎么写" | `.sdd/CONVENTIONS.md` |
| 想追溯"某条源规则落在哪" | `.sdd/TRACEABILITY.md` |

---

## 目录结构

```
README.md                       本文件
CLAUDE.md                       Agent 入口：什么时候读什么
AGENTS.md                       通用工程规则 + 读取顺序
CHANGELOG.md                    规则库版本变更

sources/                        【只读】源文档归档（Agent 决策时【不读取】）
└── v1.0/

.sdd/                           规则库
├── LAYOUT.md                   目录约定（唯一权威）
├── CONVENTIONS.md              引用编号与命名约定
├── TRACEABILITY.md             源规则 → 落点反向索引
├── schema/                     机器可校验 Schema
├── knowledge/                  13 个领域知识文件
├── decision-trees/             7 个决策树（含元治理 decision-protocol）
├── templates/                  7 个文档模板
├── workflows/                  5 个流程
└── examples/                   5 个已决策示例

specs/                          项目实例
└── 001-project/                示例实例（含 plan.md 与 adr/）

scripts/                        校验与迁移脚本
```

---

## 三条主线

1. **决策治理** — `.sdd/decision-trees/decision-protocol.md`
   约束优先级 P0–P3 / Hard·Soft Constraint / 技术选型评分 / 架构复杂度预算（含计分表）/
   决策状态 `AUTO·RECOMMEND·REQUIRE_CONFIRMATION·BLOCKED` / 人工确认门槛 / 15 步决策循环 / 30 条规则。

2. **领域知识** — `.sdd/knowledge/`
   architecture、backend、frontend、database、caching、messaging、api、security、
   testing、deployment、observability、**ai-llm**、**data**。

3. **执行流程** — `.sdd/workflows/`
   new-project、new-feature、**small-change**、bugfix、refactor。

---

## 使用方式

见 `.sdd/README.md` §使用方式。核心一句话：

> **技术栈更新只改 `.sdd/knowledge/` 与 `.sdd/decision-trees/`；`CLAUDE.md` / `AGENTS.md` 基本不动。**

---

## 校验

```bash
python3 scripts/validate_rules.py     # 引用完整性 + Decision Schema + 复杂度预算
```

---

## 版本

见 `CHANGELOG.md`。当前规则库版本：**v1.1**。
