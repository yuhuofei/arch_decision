# Technology Selection — 001-project（示例实例）

> 按 `.sdd/templates/technology-selection.md` 填写。生成前读 `.sdd/decision-trees/*.md`、`.sdd/knowledge/*.md`、`.sdd/knowledge/versioning.md`。
> **机器可读契约：同目录 `decision.json`**（真 Schema 校验由 `scripts/validate_rules.py` 执行）。

## Project Type
SaaS / Business Application（示例：订单管理系统）

## Scale
Small/Medium（user_count < 100k，team_size 6）

## Architecture
### Candidates
- Monolith
- Modular Monolith
- Microservices
### Selected
Modular Monolith
### Reason
复杂度 medium、服务独立性低、团队 ≤20；无独立部署/扩缩需求。
### Alternatives
Microservices
### Rejected Because
不满足强条件（Matrix §5.3）；为架构而架构违背 FINAL PRINCIPLE（res.md §120）。`REQUIRE_CONFIRMATION` 未触发。

## Backend
### Selected
Python + FastAPI（默认 API 首选）
### Reason
CRUD/API + 非极端性能 → Python（Matrix §6.1）。新 API 项目默认 FastAPI > Flask。
### Rejected Because
Go 仅高并发/网络服务更优；本例非此场景。

## Frontend
Vue 3 + TypeScript + Vite（默认，Enterprise/Admin/CRUD）

## Database
PostgreSQL（新关系型项目默认，res.md §23/Matrix §10）

## Cache
None initially（Redis 非默认；待 cache/session/rate-limit 需求出现再引入）

## Message Queue
None initially

## Search
PostgreSQL Full Text Search

## Storage
S3-compatible Object Storage

## Authentication
Session（传统 Web / 同域）；多 client 时改 JWT/OIDC

## Authorization
RBAC

## Observability
Structured Logging + Metrics + OpenTelemetry（tracing 待多服务时开启）

## Deployment
Docker + Docker Compose（本地/MVP）

## Testing
pytest + Vitest + Playwright（CRUD API：Unit High / Integration High / E2E Medium）

---

## 决策输出 Schema（Matrix §40，示例填充）

```yaml
architecture_decision:
  project: { type: SaaS, scale: Small/Medium, team_size: 6, deployment: Docker }
  architecture: { style: Modular Monolith, reason: "no independent scaling/deployment need" }
  backend: { language: Python, framework: FastAPI, reason: "CRUD/API, non-extreme-perf" }
  frontend: { language: TypeScript, framework: Vue 3 + Vite, reason: "business admin app" }
  database: { primary: PostgreSQL, reason: "relational default" }
  cache: { enabled: false, purpose: "introduce only if cache/session/rate-limit required" }
  messaging: { enabled: false, purpose: "introduce only if async/event-driven" }
  search: { enabled: false, technology: PostgreSQL FTS }
  vector: { enabled: false }
  object_storage: { enabled: true, technology: S3-compatible }
  authentication: { strategy: Session }
  authorization: { strategy: RBAC }
  observability: { logging: true, metrics: true, tracing: false }
  testing: { unit: High, integration: High, e2e: Medium }
  deployment: { strategy: Docker }
  rejected:
    - { option: Microservices, reason: "no strong-condition satisfied" }
    - { option: MySQL, reason: "greenfield, no MySQL constraint → PostgreSQL preferred" }
  risks: [ "Redis may be needed later for session; revisit" ]
  assumptions: [ "single-region; no compliance requirement yet" ]
  confidence: { overall: 4 }
```

## 决策状态
- Architecture=Modular Monolith → `AUTO`
- Backend=Python+FastAPI → `AUTO`
- Frontend=Vue 3 + Vite → `AUTO`
- Database=PostgreSQL → `AUTO`
- Auth=Session → `AUTO`（若改 JWT/OIDC 或涉及 Auth architecture 变更 → `REQUIRE_CONFIRMATION`）
- 本实例**无 `REQUIRE_CONFIRMATION` 项** → 无需人工确认门槛（decision-protocol §6）

## Versions（见 knowledge/versioning.md）
| Technology | Selected | Support Status | Reason |
| --- | --- | --- | --- |
| Python | UNKNOWN | UNKNOWN | 本示例未联网核对上游，按 versioning.md §4 不编造版本号；实现前补齐 |
| PostgreSQL | UNKNOWN | UNKNOWN | 同上：取目标平台可用的 supported stable major |
> 与 `decision.json` 的 `versions` 数组保持一致。

## 复杂度预算（口径见 decision-protocol §5.1）
```
PostgreSQL(1) + 对象存储(1) = 2  ≤ Small SaaS 预算 8   ✅
Docker / Docker Compose 属打包方式，不计分。
```

## 决策记录（ADR 索引；按需，见 LAYOUT.md §1.2）
- [x] PostgreSQL → `specs/001-project/adr/ADR-001-postgres.md`
- [x] FastAPI → `specs/001-project/adr/ADR-002-fastapi.md`
- [x] Session Auth → `specs/001-project/adr/ADR-003-session-auth.md`
> 只记录进入 `decision.json` 的重要决策，不为凑目录制造 ADR。
