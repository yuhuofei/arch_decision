# Template: Spec（规格说明）

> 用途：Spec 是 Source of Truth，描述 WHAT 与 WHY（res.md §91,§117；知识库 §76,§79）。
> 落点：`specs/<id>-<name>/spec.md`（目录约定见 `.sdd/LAYOUT.md`；引用约定见 `.sdd/CONVENTIONS.md`）。
> 不要把大量 implementation detail 放进需求 Spec（知识库 §76）。
> **节数以本模板的 14 节为准**；与 res.md §117 的 23 项差异见文末「节数取舍」。

# Specification: <Feature Name>

## 1. Overview
### Problem
### Goal
### Non-Goals
### Users

## 2. Context
### Existing System
### Business Context
### Constraints

## 3. User Stories
### US-001
As a ... / I want ... / So that ...

## 4. Functional Requirements
### FR-001
The system SHALL ...
#### Scenario
- GIVEN ... / WHEN ... / THEN ...

## 5. Non-Functional Requirements
### Performance / Security / Availability / Scalability / Observability

## 6. Data Requirements
### Entities / Relationships / Constraints

## 7. API Requirements
### Endpoint / Request / Response / Error

## 8. Integration Requirements
### External Services / Authentication / Retry / Timeout

## 9. Architecture Constraints
- Must use ... / Must not use ... / Must remain compatible with ... / Must support ...

## 10. Acceptance Criteria
- [ ] AC-001 ...

## 11. Assumptions

## 12. Open Questions

## 13. Out of Scope

## 14. Traceability
| Requirement | Design | Task | Test |
| --- | --- | --- | --- |
| FR-001 | D-001 | T-001 | TEST-001 |

---

## 与 Plan/Tasks 的关系（知识库 §77,§88）
- spec.md → WHAT/WHY/Acceptance
- plan.md → HOW/技术栈/设计
- tasks.md → 可执行实现工作
- 每个 Requirement 至少对应一个验证方式；每个 Task 追溯到需求/设计（decision-protocol §8 规则 24）。

---

## 节数取舍（res.md §117 的 23 项 → 本模板 14 节）

`res.md` §117 列出 spec.md「至少包含」23 项，其中若干项属于 **HOW**（架构与技术决策）。本规则库维持
**「spec = WHAT/WHY，plan = HOW」**（`CLAUDE.md` §7 Golden Rule），故将 HOW 类内容下沉到 `plan.md`。
两处结论不同，此处为**显式取舍记录**，非遗漏。

| res.md §117 | 落点 |
| --- | --- |
| 1 Overview / 2 Goals / 3 Non-Goals / 4 Users | `spec.md` §1 Overview |
| 5 Functional Requirements | `spec.md` §4 |
| 6 Non-Functional Requirements | `spec.md` §5 |
| 7 Scale | `spec.md` §5 + `plan.md` §1 |
| 8 Architecture | **`plan.md` §1**（HOW） |
| 9 Technology Decisions | **`technology-selection.md`** + `plan.md` §2（HOW） |
| 10 Repository Structure | **`plan.md` §3**（HOW） |
| 11 Data Model | `spec.md` §6（需求）+ **`plan.md` §6**（设计） |
| 12 API Design | `spec.md` §7（需求）+ **`plan.md` §7**（设计） |
| 13 Authentication / 14 Authorization | `spec.md` §9 Architecture Constraints + **`plan.md` §10** |
| 15 Error Handling | **`plan.md` §7** |
| 16 Logging | **`plan.md` §12** |
| 17 Testing | **`plan.md` §11**（策略取自 `knowledge/testing.md`） |
| 18 CI/CD / 19 Deployment | **`plan.md` §13** |
| 20 Security | `spec.md` §5 + **`plan.md` §10** |
| 21 Risks | **`plan.md` §15** |
| 22 Open Questions | `spec.md` §12 |
| 23 Acceptance Criteria | `spec.md` §10 |

> 结论：**23 项全部有落点，其中 HOW 类下沉到 `plan.md` / `technology-selection.md`。** 任何引用 spec.md 的章节号时，一律以本模板的 14 节编号为准。
