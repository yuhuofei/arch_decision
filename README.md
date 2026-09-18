# arch_decision — Agent SDD 项目框架选择规则库

> 给"用 SDD（Spec-Driven Development）模式编程的 Agent"提供一套**可解释的决策系统**，
> 而不是把 `Python + FastAPI + PostgreSQL` 当最佳实践硬塞给它。

---

## 这是什么

当用户说"帮我开发 XXX"时，Agent **不允许**直接从技术栈名称开始决策。它必须走：

```
Discovery → Draft Spec（WHAT/WHY）→ 分类项目 → 提取硬约束（P0A/P0B）
        → 生成候选 → 消除违规候选 →（必要时）评分 → 选最简且充分的架构
        → 标注决策状态 → 人工确认（**仅** REQUIRE_CONFIRMATION）
        → 固化 technology-selection.md + decision.json + plan.md（ADR **按需**：
          仅存在重要 Architecture Decision 时才建，见 `.sdd/LAYOUT.md` §1.2）
        → Final Spec（Accepted）→ 才允许写代码
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
| 想追溯"某条源规则落在哪、落到哪一层" | `.sdd/TRACEABILITY.md` |
| 想知道"同一件事哪份文件说了算" | `.sdd/CANONICAL.md`（规则归属矩阵） |

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
├── VERSION                     规则库版本号的**唯一来源**（README/CHANGELOG 都引用它）
├── LAYOUT.md                   目录约定（唯一权威）
├── CONVENTIONS.md              引用编号与命名约定
├── CANONICAL.md                规则归属矩阵（同一语义只有一个权威定义）
├── TRACEABILITY.md             源规则 → 落点反向索引（四态，脚本生成）
├── traceability.json           同上，机器可读版
├── schema/                     机器可读契约（JSON Schema，**真校验**）
├── knowledge/                  20 个领域知识文件（含 versioning）
├── decision-trees/             8 个决策树（含元治理 decision-protocol 与 impact-analysis）
├── templates/                  8 个文档模板
├── workflows/                  5 个流程
└── examples/                   5 个已决策示例

specs/                          项目实例
├── 001-project/                示例实例（plan.md、decision.json；因存在重要架构决策故有 adr/）
└── 002-demo-todo-cli/          演示实例（design/ADR 均按需，故不存在）

scripts/                        校验与迁移脚本
```

---

## 三条主线

1. **决策治理** — `.sdd/decision-trees/decision-protocol.md`
   约束优先级 **P0A / P0B** / P1–P3（安全合规不可被用户偏好覆盖）/ Hard·Soft Constraint /
   技术选型评分**标尺**与适用门槛 / 架构复杂度预算（含计分表）/ 默认值语义（Default = Candidate Prior）/
   决策状态 `AUTO·RECOMMEND·REQUIRE_CONFIRMATION·BLOCKED`（仅 CONFIRMATION 阻塞）/ **21 步全链路决策循环** / 30 条规则。

2. **领域知识** — `.sdd/knowledge/`
   architecture、backend、frontend、database、caching、messaging、api、security、
   testing、deployment、observability、ai-llm、data、versioning（版本策略唯一实现）、
   **multi-tenancy**、**reliability**、**data-lifecycle**、**integration**、**configuration**、**dependency-management**。

3. **执行流程** — `.sdd/workflows/`
   new-project、new-feature（含 **Impact Analysis** 前置）、small-change（含 **Behavioral Risk Check**）、bugfix、refactor。

---

## 使用方式

见 `.sdd/README.md` §使用方式。核心一句话：

> **技术栈更新只改 `.sdd/knowledge/` 与 `.sdd/decision-trees/`；`CLAUDE.md` / `AGENTS.md` 基本不动。**

---

## 校验

```bash
python3 scripts/gen_traceability.py   # 重建 5 份来源 → 落点的反向索引（改引用后必跑）
python3 scripts/validate_rules.py     # 引用完整性 / 真 Schema 校验 / Cost 语义 / 版本一致性 / Canonical 不变量
```

---

## 版本

见 `CHANGELOG.md`。当前规则库版本：**v1.5**（版本号唯一来源：`.sdd/VERSION`，由自检脚本核对三处一致）。
