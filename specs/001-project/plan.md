# Implementation Plan — 001-project（示例实例）

> 按 `.sdd/templates/plan.md` 填写（16 节）。plan.md 描述 **HOW**、架构与技术选择（`res.md §99,§100`）。
> 上游：`spec.md`（WHAT/WHY）、`technology-selection.md`（选型结论 + 复杂度预算）。
> 本实例以"订单管理系统（Small SaaS）"为例，与 `technology-selection.md` 的结论保持一致。

---

## 1. Architecture

### Architecture Style
**Modular Monolith**（单应用 + 单数据库 + 多模块）。
依据：复杂度 medium、服务独立性低、团队 6 人（`knowledge/architecture.md` §2.2；`Matrix §5.2`）。未满足 Microservices 强条件（`Matrix §5.3`）。

### Component Diagram
```
                 ┌──────────────────────────────────────┐
                 │   Vue 3 + TS + Vite（frontend/）      │
                 └──────────────────┬───────────────────┘
                                    │ REST + OpenAPI → 生成的 TS Client
                 ┌──────────────────▼───────────────────┐
                 │   FastAPI 应用（backend/app/）        │
                 │  ┌────────┬────────┬────────┬──────┐ │
                 │  │ users  │ orders │payments│notify│ │
                 │  └────────┴────────┴────────┴──────┘ │
                 │   api / services / repositories 分层  │
                 └───────┬───────────────────────┬──────┘
                         │                       │
              ┌──────────▼─────────┐   ┌─────────▼─────────┐
              │ PostgreSQL         │   │ S3-compatible     │
              │ orders/order_items │   │ 附件（object_key）│
              └────────────────────┘   └───────────────────┘
```

### Data Flow
创建订单（同步主链路）：
```
POST /api/v1/orders
  → orders module（领域校验 / 事务边界）
  → repositories → PostgreSQL
  → 事务提交后：向 notifications module 发内部事件（进程内，非 MQ）
  → 返回 201 + 订单号
```

---

## 2. Technology Stack
> 取自 `technology-selection.md`（含 Decision Status 与复杂度预算）。

| 层 | 选择 | Decision Status |
| --- | --- | --- |
| Language | Python 3.x | `AUTO` |
| Backend | FastAPI + Pydantic + SQLAlchemy + Alembic | `AUTO` |
| Frontend | Vue 3 + TypeScript + Vite + Pinia | `AUTO` |
| CSS / UI | Tailwind CSS + Element Plus（单库） | `AUTO` |
| Database | PostgreSQL | `AUTO` |
| Cache | 暂不引入（Redis 非默认，`knowledge/caching.md` §1） | — |
| Message Queue | 暂不引入（无异步/事件驱动需求） | — |
| Search | PostgreSQL Full Text Search | `AUTO` |
| Object Storage | S3-compatible | `AUTO` |
| Authentication | Session（Cookie + Server-side） | `AUTO` |
| Authorization | RBAC | `AUTO` |
| Observability | 结构化日志 + Metrics（OpenTelemetry） | `AUTO` |
| Deployment | Docker + Docker Compose（MVP 档） | `AUTO` |
| Testing | pytest + Vitest + Playwright | `AUTO` |

---

## 3. Project Structure

```
backend/
├── app/
│   ├── api/            # 路由层（薄，只做参数校验与编排）
│   ├── core/           # 配置、安全、依赖注入
│   ├── models/         # SQLAlchemy 模型
│   ├── schemas/        # Pydantic schema
│   ├── services/       # 业务逻辑（可单测）
│   ├── repositories/   # 数据访问
│   └── main.py
├── migrations/         # Alembic
├── tests/
├── pyproject.toml
└── Dockerfile

frontend/
├── src/
│   ├── components/
│   ├── views/
│   ├── layouts/
│   ├── router/
│   ├── stores/         # Pinia（仅 Global Client State）
│   ├── services/       # API Service 层
│   ├── api/            # OpenAPI 生成的 TS Client
│   ├── types/
│   └── utils/
├── tests/
└── vite.config.ts

docker-compose.yml
```

依据：`knowledge/backend.md` §7、`knowledge/frontend.md` §7、`res.md §78`。

---

## 4. Backend Design

### Modules
`users` / `orders` / `payments` / `notifications`。模块间只通过 service 接口调用，**不跨模块直接访问对方的 repository**。

### Services
- `OrderService.create()`：校验 SKU 与数量 → 计算金额 → 事务内写 `orders` + `order_items`。
- `PaymentService.confirm()`：状态机流转，覆盖 Money 关键状态（`res.md §67`）。

### Repositories
每个模块一个 repository；SQL 显式书写，不使用懒加载。

### Middleware
请求 ID 注入 → 结构化日志 → 异常统一转换（`res.md §70`）→ 认证 → 授权（RBAC）。

---

## 5. Frontend Design

### Pages
登录 / 订单列表 / 订单详情 / 订单创建 / 用户管理。

### Components
列表页统一使用同一张表格封装；表单校验规则与后端 Pydantic schema 对齐。

### State Management
`res.md §75`：Server State → TanStack Query；UI State → 组件本地；Global Client State（当前用户、主题）→ Pinia。
**不把服务端数据复制成全局 state。**

### API Client
`OpenAPI → 生成 TypeScript Client`（`知识库 §52-§53`）。组件内**禁止**直接 `fetch()`。

---

## 6. Database

### Tables
- `users(id uuid pk, email unique, password_hash, status, created_at)`
- `orders(id uuid pk, order_no unique, user_id fk, status, total_amount, created_at, updated_at)`
- `order_items(id uuid pk, order_id fk, sku, qty, unit_price)`

### Indexes
`orders(user_id, created_at desc)`、`orders(status)`、`order_items(order_id)`。

### Constraints
金额用 `numeric`（禁止 float）；`status` 用枚举或 check 约束；外键均设约束。

### Migration Strategy
Alembic 版本化迁移；**禁止手工改生产 schema**（`res.md §64`）。

设计规则：第三范式优先（`res.md §66`）；事务覆盖 Money/Inventory/Permission/关键状态（`res.md §67`）；ID 用 UUIDv7（`res.md §68`）；时间 UTC 存储、API ISO 8601（`res.md §69`）。

---

## 7. API

### REST
资源化路径 + HTTP 方法 + 状态码；分页 cursor-based（`res.md §71`）；公开端点限流（`res.md §72`）。

### Authentication / Authorization
Session Cookie（同域 Web）；RBAC。

### Error Model
```json
{ "error": { "code": "ORDER_INVALID_SKU", "message": "...", "details": {} }, "request_id": "..." }
```
统一格式（`res.md §70`）；**业务错误不得暴露 DB exception**。

### OpenAPI
所有 REST 端点产出 OpenAPI 3.x（`res.md §33`），并以此生成前端 TS Client。

---

## 8. Async Processing
**当前不引入异步链路**（无明确需求，`res.md §74`）。
若后续出现"订单创建后发通知"的可靠性要求，则演进为：
```
HTTP → Create Job → Queue(Redis/RabbitMQ) → Worker → DB
```
届时需按 `knowledge/caching.md` §2 与 `decision-protocol §5.1` 重新计算复杂度预算。

---

## 9. Cache
当前 `cache = false`（不满足 `knowledge/caching.md` §1 的读密集 + 低变更 + 命中收益条件）。
引入时必须定义 TTL / Invalidation / Stale 容忍 / Failure 行为 / Key 设计（`res.md §73`）。

---

## 10. Security
- Auth：Session（**禁止自研密码加密 / 会话加密**，`知识库 §33`）
- Authz：RBAC + resource-level 校验（禁止在业务代码散落 `if user.is_admin`，`知识库 §34`）
- API baseline：输入校验 / 限流 / CORS / CSRF / SQL 注入 / XSS / SSRF / 文件上传（`res.md §45`）
- Secrets：环境变量注入，**不提交 Git**（`res.md §87`）

---

## 11. Testing
按 `Matrix §28` 的 CRUD API 档：**Unit High / Integration High / E2E Medium**。

| 层 | 覆盖对象 | 工具 |
| --- | --- | --- |
| Unit | 领域逻辑、校验、状态机 | pytest |
| Integration | DB / API / 认证（用真实 PostgreSQL，Testcontainers） | pytest + httpx |
| E2E | 登录 → 创建订单 → 支付 → 确认 | Playwright |
| 前端 | 组件与交互 | Vitest + Testing Library |

每个 Requirement 至少对应一个验证方式（`知识库 §39`）。

---

## 12. Observability
- **Logs**：JSON 结构化，含 timestamp / level / service / request_id / trace_id / user_id / message（`res.md §48`）；**禁止记录** password / token / secret / 完整卡号 / 敏感 PII。
- **Metrics**：请求数 / 延迟 / 错误率 / DB 连接数 / 队列深度（`Matrix §26`）。
- **Tracing**：当前单服务，暂不开启分布式追踪；多服务时接 OpenTelemetry（`res.md §49`）。

---

## 13. Deployment
- **本地 / MVP**：Docker Compose（api + postgres）（`Matrix §24`）
- **小规模生产**：Docker + 托管数据库
- **CI/CD**：GitHub Actions — Lint → Type Check → Unit → Integration → Build → Security Scan → Deploy（`res.md §63`）
- 容器：multi-stage build、non-root、pinned deps、healthcheck、graceful shutdown（`res.md §60`）

**不引入 K8s**（未满足 `Matrix §25` 的条件，且 K8s = `REQUIRE_CONFIRMATION`）。

---

## 14. Architecture Decisions

### ADR-001
Decision: 使用 PostgreSQL 作为主数据库
Reason: 关系型事务数据，新关系型项目默认
Alternatives: MySQL / MongoDB
Rejected: MySQL（无既有约束）/ MongoDB（领域强关系型）
Status: Accepted ｜ Decision Status: `AUTO` ｜ Confidence: 5
→ `adr/ADR-001-postgres.md`

### ADR-002
Decision: 后端采用 Python + FastAPI
Reason: CRUD/API 场景且非极端性能要求（`Matrix §6.1`）；新 API 项目 FastAPI 优于 Flask
Alternatives: Django / Go
Rejected: Django（非 admin-heavy）/ Go（非高并发/网络服务场景）
Status: Accepted ｜ Decision Status: `AUTO` ｜ Confidence: 4
→ `adr/ADR-002-fastapi.md`

### ADR-003
Decision: 认证采用 Session（Cookie + Server-side）
Reason: 传统同域 Web 应用、仅浏览器客户端（`Matrix §20` 的 Session 分支）
Alternatives: JWT
Rejected: JWT（当前无多客户端/无状态 API 需求；`知识库 §33` 反对因流行而默认 JWT）
Status: Accepted ｜ Decision Status: `AUTO`（若改为 JWT/OIDC 则升为 `REQUIRE_CONFIRMATION`）｜ Confidence: 4
→ `adr/ADR-003-session-auth.md`

---

## 15. Risks

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 后续出现 Session 跨端需求 | 需改认证架构 | 一旦需要多客户端即走 `REQUIRE_CONFIRMATION` 评审 JWT/OIDC |
| 单库成为写瓶颈 | 性能 | 先加索引与读写分离；确有成瓶颈证据后再评估（不提前引入 Redis/分库） |
| 通知可靠性不足（进程内事件） | 丢通知 | 达到可靠性要求时引入真正的 task queue，并重算复杂度预算 |
| 复杂度预算被悄悄突破 | 架构失控 | 每次引入组件都按 `decision-protocol §5.1` 计分并记录 ADR |

---

## 16. Migration
本实例为 Greenfield，无迁移。
若为存量项目，须先按 `.sdd/workflows/refactor.md` 与 `res.md §102` 生成 `project-discovery.md`，
且**技术栈迁移一律 `REQUIRE_CONFIRMATION`**（`Matrix §34-§35`）。

---

## Change Management（`res.md §101`）
发现 Spec 错误 → 更新 Spec → Design → Tasks → 继续实现，**不直接绕过**。
