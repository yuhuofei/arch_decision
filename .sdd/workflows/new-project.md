# Workflow: New Project（新项目）

> 来源：res.md §0,§91-§118,§116；Matrix §43（Agent 决策循环）；知识库 §81,§88。
> 入口：CLAUDE.md §2。治理：`.sdd/decision-trees/decision-protocol.md`。

## Agent 决策循环（Matrix §43，15 步）
```
1. Read requirements
2. Classify project              → knowledge/architecture.md §1（项目类型矩阵）
3. Extract hard constraints      → decision-protocol.md §3（P0）
4. Extract soft constraints      → decision-protocol.md §3（P1-P3）
5. Detect existing stack         → Brownfield 则 preserve（Matrix §34 / 知识库 §75）
6. Generate candidates           → decision-trees/*.md
7. Eliminate hard-constraint violations
8. Score remaining candidates    → decision-protocol.md §4
9. Select simplest sufficient architecture
10. Generate ADR                 → templates/adr.md（含 Status/Confidence）
11. Mark confidence / Decision Status
12. Identify human-confirmation decisions  → decision-protocol.md §6
13. Generate plan.md             → templates/plan.md
14. Generate tasks.md            → templates/tasks.md
15. Run consistency analysis     → spec.md ↔ plan.md ↔ tasks.md
```

## 人工确认门槛（关键）
技术栈类决定有长期锁定成本，**不得静默决定**：
```
Architecture Proposal
   ↓
Human Confirmation（对 REQUIRE_CONFIRMATION 项）
   ↓
固化进 plan.md + ADR（后续 Agent 默认不得擅自改）
```
默认 `REQUIRE_CONFIRMATION`：Microservices / K8s / Multi-region / DB migration / Auth architecture / Authz model / Payment / Data residency / Compliance / 云商 / Event-driven / CQRS / Event Sourcing / Distributed Tx / Public API contract / Breaking API / 重大技术迁移。

## 流程骨架
```
User Requirement
   ↓
1. Project Discovery        → templates/project-discovery.md
   ↓
2. Architecture Decision     → knowledge/architecture.md + decision-trees/architecture.md
   ↓                          （含复杂度预算检查）
3. Technology Selection      → decision-trees/* + templates/technology-selection.md
   ↓                          （Decision Output Schema + Decision Status）
4. Architecture Proposal → Human Confirmation   ← 门槛
   ↓
5. Specification             → templates/spec.md（14 节）
   ↓
6. Design / Plan             → templates/design.md + plan.md
   ↓
7. Tasks                     → templates/tasks.md
   ↓
8. Implementation            → 实现前读 Rules/TS/Spec/Design/Tasks（res.md §100）
   ↓
9. Test                      → Testing Pyramid（testing.md Matrix）
   ↓
10. Verify                  → 对照 Acceptance Criteria + Traceability
   ↓
Convergence
```

## 关键检查（res.md §116 Architecture Review Checklist）
Project type / Scale / Architecture / Backend / Frontend / Database / Cache / Queue / Search / Storage / Authentication / API / Testing / Observability / Deployment / CI-CD / Security / Backup / Risks / Open questions —— 全部文档化。

## 默认技术矩阵（res.md §110 / 知识库 §82）
无特殊约束时按 knowledge 的 DEFAULT 选型；中小 SaaS→Vue+FastAPI+PG（知识库 §59）；AI→Next.js+FastAPI+pgvector（知识库 §60）；高并发→Go（知识库 §61）；企业→Spring Boot（知识库 §62）。

## 原则
未解决架构决策前**不得**写实现代码（CLAUDE.md §2）。
