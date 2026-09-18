# Workflow: New Project（新项目）

> 来源：res.md §0,§91-§118,§116；Matrix §43（Agent 决策循环）；知识库 §59,§81,§88；
> mod_gpt.md §1（Spec 前置）,§2（确认收窄）,§7（默认值语义）。
> 入口：`CLAUDE.md` §2。治理：`.sdd/decision-trees/decision-protocol.md`。

## 流程骨架（canonical order）

```
User Requirement
   ↓
1. Project Discovery         → templates/project-discovery.md
   ↓
2. Draft Specification       → templates/spec.md（Status: Draft）
   ↓                          写明 WHAT / WHY / NFR / Hard Constraints /
                              Acceptance Criteria / Open Questions
                              **不写技术实现**（不写语言/框架/数据库/部署）
        ┌── 门槛①：Draft Spec 足以支撑架构判断 ──┐
   ↓
3. 读决策材料                → knowledge/architecture.md
                              + decision-trees/{architecture,backend,frontend,database,infrastructure}.md
                              + 按项目类型追加领域知识
                              + knowledge/versioning.md（版本）
   ↓
4. Technology Selection      → templates/technology-selection.md + decision.json
   ↓                          Hard Constraint elimination
                              → Candidates
                              → （必要时）Scoring（decision-protocol §4.1）
                              → Simplest Sufficient
                              → Decision Status
        ┌── 门槛②：仅 REQUIRE_CONFIRMATION 项需人确认 ──┐
   ↓
5. Finalize                  → Final spec.md（Status: Accepted）
                              → plan.md
                              → design.md（**按需**，判据见 LAYOUT.md §1）
                              → adr/（**按需**，存在 Architecture Decision 才建）
                              → tasks.md
   ↓
6. Implementation            → 实现前读 Rules/TS/Spec/Plan/Tasks（res.md §100）
   ↓
7. Test                      → Testing Pyramid（knowledge/testing.md）
   ↓
8. Verify                    → 对照 Acceptance Criteria + Traceability
   ↓
Convergence
```

> **顺序不可交换**：先把 Spec 写出来（哪怕只是 Draft），再谈技术。
> 反过来做就是 `Prompt → Tech Stack → Spec`，等于放弃 SDD（`mod_gpt.md §1`）。

## Agent 决策循环（Matrix §43，15 步）
> 本循环对应上面骨架的 **第 3–4 步**，是"决策"这个子过程的展开；它发生在 **Draft Spec 之后**。
```
1. Read requirements             → 读 Draft spec.md（不是从零重读用户原话）
2. Classify project              → knowledge/architecture.md §1（项目类型矩阵）
3. Extract hard constraints      → decision-protocol.md §3.1（P0A / P0B）
4. Extract soft constraints      → decision-protocol.md §3.2（P1-P3）
5. Detect existing stack         → Brownfield 则 preserve（Matrix §34 / 知识库 §75）
6. Generate candidates           → decision-trees/*.md（默认值只是候选先验，decision-protocol §3.4）
7. Eliminate hard-constraint violations
8. Score remaining candidates    → decision-protocol.md §4.1（仅当消除后仍 ≥2 且规则无法区分）
9. Select simplest sufficient architecture
10. Generate ADR                 → templates/adr.md（含 Status/Confidence）※按需
11. Mark confidence / Decision Status
12. Identify human-confirmation decisions  → decision-protocol.md §6
13. Generate plan.md             → templates/plan.md
14. Generate tasks.md            → templates/tasks.md
15. Run consistency analysis     → spec.md ↔ plan.md ↔ tasks.md
```

## 人工确认门槛（已收窄）

**只有标记为 `REQUIRE_CONFIRMATION` 的决策必须人工确认。**
默认清单：Microservices / K8s / Multi-region / DB migration / Auth architecture / Authz model /
Payment / Data residency / Compliance / 云商 / Event-driven / CQRS / Event Sourcing /
Distributed Tx / Public API contract / Breaking API / 重大技术迁移（含破坏性版本升级）。

```
Architecture Proposal
   ↓
Human Confirmation（仅对 REQUIRE_CONFIRMATION 项）
   ↓
固化进 plan.md + decision.json + ADR
```

**清单之外的不阻塞**（`mod_gpt.md §2`）：
普通语言、框架、ORM、测试工具、包管理器、缓存是否引入、目录结构、命名 —— 只要满足 Hard Constraint
且属 `AUTO`/`RECOMMEND`，**Agent 自行选择并记录，不逐个征询用户**。

```
AUTO      → 直接执行并记录
RECOMMEND → 采用推荐方案继续执行；记录 alternatives / assumptions / reversibility；不阻塞
REQUIRE_CONFIRMATION → 用户确认后继续
BLOCKED   → 缺失信息会导致重大、不可逆或高风险决策，且无安全可逆默认值时才停止
```
> 如果把"AUTO 也去问用户"，整套决策协议只剩仪式感 —— 这是本条被反复强调的原因。

## 默认技术矩阵（res.md §110 / 知识库 §82）

**默认值是候选先验（candidate prior），不是决策结果。**

```
DEFAULT does not mean SELECTED.

A default:
1. enters the candidate set;                                    # 进入候选集
2. may become AUTO only when no P0/P1 constraint differentiates candidates;
3. must yield to existing stack and demonstrated team expertise;
4. must not bypass candidate elimination.
```

无特殊约束时按 `knowledge/` 的 DEFAULT 选型作为**起点**；中小 SaaS→Vue+FastAPI+PG（`知识库 §59`）；
AI→Next.js+FastAPI+pgvector（`知识库 §60`）；高并发→Go（`知识库 §61`）；企业→Spring Boot（`知识库 §62`）。
—— 这些场景描述的是"先验偏置哪个候选更可能赢"，**不是"答案"**。具体见 `decision-protocol §3.4`。

## 关键检查（res.md §116 Architecture Review Checklist）
Project type / Scale / Architecture / Backend / Frontend / Database / Cache / Queue / Search / Storage /
Authentication / API / Testing / Observability / Deployment / CI-CD / Security / Backup / Risks / Open questions
—— 全部文档化。

## 原则
未解决架构决策前**不得**写实现代码（`CLAUDE.md` §2）。
`design.md` 与 `adr/` 是**按需产物**：没有对应内容就不要为了"目录规范"制造文件（`LAYOUT.md` §1）。
