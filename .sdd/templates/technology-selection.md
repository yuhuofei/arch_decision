# Template: Technology Selection（技术选型）

> 用途：固化技术决策（res.md §94,§109；Matrix §40；知识库 §84）；
> 结构按 modv2.md §6,§8,§15,§16,§17 补全（evidence / constraints / alternatives / review_triggers / deferred）。
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

> 核对过上游的必须填 `Verified` 日期与 `source_url`（decision.json 的 `versions[].source_url`）——
> 「核对过」要成为**可审计的数据**，而不是一句自然语言（modv2.md §6）。

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
  versions: [ { technology:, selected:, support_status:, verified_at:, source_url:, reason: } ]
  decision_status: { architecture:, backend:, frontend:, database:, authentication: }
  complexity: { score:, budget:, items: [ { component:, points: } ] }
  cost: { recurring:, cap:, budget_basis:, within_budget: }
  evidence: [ { type:, claim:, source:, verified_at: } ]
  constraints: [ ... ]
  alternatives: [ { option:, reason: } ]
  scores: [ { option:, score:, breakdown: } ]
  rejected: [ { option:, reason: } ]
  deferred: [ { decision:, reason:, trigger: [ ... ] } ]
  review_triggers: [ ... ]
  decision_history: [ { decision:, from:, to:, changed_at:, reason:, trigger:, supersedes: } ]
  risks: [ ... ]
  assumptions: [ ... ]
  confidence: { overall: }
```

> **`decision.json` 才是权威**；本 YAML 块只做 structural validation（缺键即报错），不做类型校验。
> `cost.within_budget` 语义：`true` = 已知预算范围内 / `false` = 明确超预算 / `null` = 无预算数据，无法判断。
> **`cap` 未知时不得写 `within_budget: true`** —— 那是逻辑矛盾（modv2.md §7）。

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

## Architecture Summary（知识库 §84）
```
Project Type / Architecture / Language / Backend / Frontend / Database
Cache / Message Queue / Storage / Authentication / Testing / Deployment
Key Decisions / Alternatives Considered
```
> **仅当其中存在 `REQUIRE_CONFIRMATION` 决策时，才暂停并请求人工确认**（decision-protocol §6.1）。
> 若全部为 `AUTO` / `RECOMMEND`，Agent **直接继续生成 Final Spec / Plan / Tasks**，不阻塞（decision-protocol §6）。
> 确认后固化进 plan.md + `decision.json`；ADR **按需**（只有重要架构决策才建，见 decision-protocol §6.3）。

## 决策记录（ADR 索引；**按需**创建，判据见 LAYOUT.md §1.2）
- [ ] PostgreSQL → `specs/<id>/adr/ADR-001-postgres.md`
- [ ] FastAPI → `specs/<id>/adr/ADR-002-fastapi.md`

---

## Evidence（决策依据；`modv2.md §15`）

> **禁止**只写 `reason: PostgreSQL is preferred` 这类无法复核的理由（`reason` 字段保留，但不再是唯一依据）。
> 每条依据必须可指向具体来源：

```yaml
evidence:
  - type: requirement     # requirement / constraint / team / documentation
    claim: relational transactional workload
    source: spec.md#FR-003
  - type: documentation
    claim: selected version is supported
    source: <官方文档 URL>
    verified_at: <YYYY-MM-DD>
```

## Deferred（现在不做，但已登记；`modv2.md §17`）

> 区分 `REJECTED`（不适用）与 `DEFERRED`（当前不需要、满足条件后重评）。
> 不要把「暂不引入 Redis」一律写成 Rejected —— 那会丢失重评线索。

```yaml
deferred:
  - decision: Redis
    reason: current workload does not justify operational complexity
    trigger: [p95 latency > 300ms, cache requirement appears]
```

## Review Triggers（何时重评；`modv2.md §16`）

> `AUTO` **不是永久结论**，而是「在当前证据与约束下如此」。必须写明重评条件。

```yaml
review_triggers:
  - p95 latency > 300ms
  - cache hit opportunity > 60%
  - independent scaling requirement appears
```

## Decision History（决策变更史；`modv2.md §18`）

> 项目演进时记录「为什么改、依据什么、取代了哪条旧决策」。规模扩大后再拆成 ADR。

```yaml
decision_history:
  - decision: architecture
    from: Modular Monolith
    to: Microservices
    changed_at: <YYYY-MM-DD>
    reason: <...>
    trigger: <...>
    supersedes: ADR-001
```
