# Template: Technology Selection（技术选型）

> 用途：固化技术决策（res.md §94,§109；Matrix §40；知识库 §84）。
> 生成前读：`.sdd/decision-trees/*.md`（含 `decision-protocol.md`）与 `.sdd/knowledge/*.md`。
> 每个重要决策配 ADR（`.sdd/templates/adr.md`）。

# Technology Selection

## Project Type
<!-- SaaS / AI Application / Data / CLI / Internal Tool / Distributed ... -->

## Scale
<!-- Small / Medium / Large；user_count / team_size -->

## Architecture
### Candidates
### Selected
### Reason
### Alternatives
### Rejected Because

## Backend
### Candidates / Selected / Reason / Alternatives / Rejected Because

## Frontend
## Database
## Cache
## Message Queue
## Search
## Vector
## Storage
## Authentication
## Authorization
## Observability
## Deployment
## Testing

---

## 决策输出 Schema（Matrix §40，必填）

```yaml
architecture_decision:
  project: { type:, scale:, team_size:, deployment: }
  architecture: { style:, reason: }
  backend: { language:, framework:, reason: }
  frontend: { language:, framework:, reason: }
  database: { primary:, reason: }
  cache: { enabled:, technology:, purpose: }
  messaging: { enabled:, technology:, purpose: }
  search: { enabled:, technology: }
  vector: { enabled:, technology: }
  object_storage: { enabled:, technology: }
  authentication: { strategy: }
  authorization: { strategy: }
  observability: { logging:, metrics:, tracing: }
  testing: { unit:, integration:, e2e: }
  deployment: { strategy: }
  rejected: [ { option:, reason: } ]
  risks: [ ... ]
  assumptions: [ ... ]
  confidence: { overall: }
```

## 决策状态（decision-protocol §6，每项标一个）
- `AUTO` / `RECOMMEND` / `REQUIRE_CONFIRMATION` / `BLOCKED`
- 以下默认 `REQUIRE_CONFIRMATION`：Microservices / K8s / Multi-region / DB migration / Auth architecture / Authz model / Payment / Data residency / Compliance / 云商 / Event-driven / CQRS / Event Sourcing / Distributed Tx / Public API contract / Breaking API / 重大技术迁移。

## 复杂度预算（Matrix §32；计分口径见 decision-protocol §5.1）
**计分公式（唯一口径）**：只有"新增需独立部署/运维/故障域的基础设施组件"才计分。
```
计入：主数据库 +1 / 缓存 +1 / MQ +1 / 对象存储 +1 / 独立调度器 +1
      Kafka +2 / ES·OpenSearch +2 / 专用向量库 +2 / K8s +3 / Microservices +3
不计：语言 / 框架 / ORM / Docker / CI-CD / gRPC / 部署平台
pgvector 作为 PG 扩展 → 不额外计分（独立向量库才 +2）

complexity_score = ______   ； 预算：MVP 5 / Internal 6 / Small SaaS 8 / Enterprise SaaS 12 / Distributed 20+
```
超限必须重评，并在 `risks` 中记录原因。

## 技术选型评分（Matrix §36 / 知识库 §72）
```
Score = Requirement Fit×40 + Maintainability×20 + Team Fit×15 + Operational Simplicity×15 + Ecosystem×10
```
每项 0–5；Hard Constraint 失败 = 直接淘汰。

## Architecture Summary（知识库 §84，先输出给人确认）
```
Project Type / Architecture / Language / Backend / Frontend / Database
Cache / Message Queue / Storage / Authentication / Testing / Deployment
Key Decisions / Alternatives Considered
```
> 技术栈类决定有长期锁定成本，建议 `Architecture Proposal → Human Confirmation` 后再固化进 plan.md 与 ADR（decision-protocol §9）。

## 决策记录（ADR 索引）
- [ ] PostgreSQL → adr-001-postgres.md
- [ ] FastAPI → adr-002-fastapi.md
