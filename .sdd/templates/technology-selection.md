# Template: Technology Selection（技术选型）

> 用途：固化技术决策（res.md §94,§109；Matrix §40；知识库 §84）。
> 生成前读：`.sdd/decision-trees/*.md`（含 `decision-protocol.md`）、`.sdd/knowledge/*.md`、`.sdd/knowledge/versioning.md`。
> **本文件是「人读」版本；机器可读契约写同目录 `decision.json`**（真 Schema 校验，见 `.sdd/LAYOUT.md` §1.1）。
> ADR **按需**创建（`.sdd/templates/adr.md`）——没有重要 Architecture Decision 就不建。

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

## Versions（版本，见 knowledge/versioning.md）
<!-- 不写死版本号；未核对上游官方文档的写 UNKNOWN，禁止编造（CONVENTIONS.md §4） -->
| Technology | Selected | Support Status | Verified | Reason |
| --- | --- | --- | --- | --- |
| <Python> | UNKNOWN | UNKNOWN | — | 实现前按 versioning.md §4 核对上游 |

---

## 决策输出 Schema（Matrix §40；本文件只做 structural validation，真校验见 `decision.json`）

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
  versions: [ { technology:, selected:, support_status:, verified_at:, reason: } ]
  decision_status: { architecture:, backend:, frontend:, database:, authentication: }
  complexity: { score:, budget:, items: [ { component:, points: } ] }
  cost: { recurring:, cap:, within_budget: }
  rejected: [ { option:, reason: } ]
  risks: [ ... ]
  assumptions: [ ... ]
  confidence: { overall: }
```

## 决策状态（decision-protocol §6，每项标一个）
- `AUTO` → 直接执行并记录，**不征询用户**
- `RECOMMEND` → **采用推荐方案继续**，记录 alternatives / assumptions / reversibility，**不阻塞**
- `REQUIRE_CONFIRMATION` → 必须人确认，不得静默决定
- `BLOCKED` → 仅当缺失信息会导致重大、不可逆或高风险决策，且无安全可逆默认值时
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

## 技术选型评分（Matrix §36 / 知识库 §72；标尺见 decision-protocol §4.1）
```
Score = Requirement Fit×40 + Maintainability×20 + Team Fit×15 + Operational Simplicity×15 + Ecosystem×10
```
每项 0–5，**必须按 decision-protocol §4.1 的 rubric 打分**（0=明确不满足 … 5=高度匹配且有直接证据）；
Hard Constraint 失败 = 直接淘汰，不是降分。

**只在同时满足下列两条时才评分**：
- Hard Constraint elimination 后仍有 ≥2 个合理候选；
- 候选 trade-off 无法由 decision-trees / knowledge 的规则直接判定。
> Scoring is a tie-break / comparison tool, not the decision itself. 不为用公式而制造候选。

## Architecture Summary（知识库 §84，先输出给人确认）
```
Project Type / Architecture / Language / Backend / Frontend / Database
Cache / Message Queue / Storage / Authentication / Testing / Deployment
Key Decisions / Alternatives Considered
```
> **只有 `REQUIRE_CONFIRMATION` 项**需要 `Architecture Proposal → Human Confirmation`，确认后固化进 plan.md + `decision.json` + ADR（decision-protocol §6/§9）。其余项按 AUTO/RECOMMEND 直接执行并记录，不阻塞。

## 决策记录（ADR 索引；**按需**创建，判据见 LAYOUT.md §1.2）
- [ ] PostgreSQL → `specs/<id>/adr/ADR-001-postgres.md`
- [ ] FastAPI → `specs/<id>/adr/ADR-002-fastapi.md`
