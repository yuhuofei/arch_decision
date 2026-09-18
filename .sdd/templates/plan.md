# Template: Plan（实施计划 / 技术架构）

> 用途：plan.md 描述 HOW、架构与技术选择（res.md §99,§100；知识库 §77,§80）。
> 实现前必须读：Project Rules / Technology Selection / Relevant Spec / Design / Tasks（res.md §100）。
> 只有 `REQUIRE_CONFIRMATION` 的技术决策需先 `Human Confirmation` 再固化（decision-protocol §6）。
> **`design.md` 只写本文件装不下的细节**，两边不得重述同一件事（缓存 TTL、模块划分等只写一处），判据见 `.sdd/LAYOUT.md` §1.2。

# Implementation Plan: <Feature Name>

## 1. Architecture
### Architecture Style
### Component Diagram
### Data Flow

## 2. Technology Stack
### Language / Backend Framework / Frontend Framework
### Database / Cache / Message Queue / Search / Object Storage
> 取自 technology-selection.md（含 Decision Status 与复杂度预算）

## 3. Project Structure
```
...（见 knowledge/{backend,frontend}.md 的 Repository Structure）
```

## 4. Backend Design
### Modules / Services / Repositories / Middleware

## 5. Frontend Design
### Pages / Components / State Management / API Client

## 6. Database
### Tables / Indexes / Constraints / Migration Strategy

## 7. API
### REST / GraphQL / gRPC / Authentication / Authorization / Error Model

## 8. Async Processing
### Jobs / Queue / Retry / Idempotency

## 9. Cache
### Cache Keys / TTL / Invalidation

## 10. Security
### Auth / Authz / API Security / Secrets

## 11. Testing
### Unit / Integration / E2E（参考 testing.md 的 Test Strategy Matrix）

## 12. Observability
### Logs / Metrics / Tracing

## 13. Deployment
### Strategy / Container / CI-CD

## 14. Architecture Decisions
### ADR-001
Decision: / Reason: / Alternatives: / Rejected: / Status: / Confidence:

## 15. Risks

## 16. Migration

---

## Change Management（res.md §101）
发现 Spec 错误 → 更新 Spec → Design → Tasks → 继续实现，不直接绕过。
