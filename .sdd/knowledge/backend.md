# Knowledge: Backend（后端语言与框架）

> 来源：res.md §5-§15,§28,§54,§56,§57,§58,§59,§64,§78-§82,§88,§89；Matrix §6-§7,§14；知识库 §5-§11（含 §5.1,§6.1-§6.3,§8.1-§8.3）,§25,§47,§48
> 决策树：`.sdd/decision-trees/backend.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## 1. Backend Language Matrix（Matrix §6，正式条件）

### Python（Matrix §6.1；句式按 decision-protocol §3.4 修正为候选先验）
```
IF AI OR ML OR Data Processing OR Automation OR CRUD/API
   AND extreme_performance = false
THEN Python SHOULD be included as a candidate
```
优先：AI / RAG / LLM / ETL / Automation / Admin API / Business API / Data Science。默认栈：Python 3.x + uv + FastAPI + Pydantic + SQLAlchemy + Alembic + pytest。

### Go（Matrix §6.2）
```
IF concurrency = high OR network_service OR infrastructure OR latency_requirement = strict OR CPU_efficiency = important
THEN Go SHOULD receive strong preference as a candidate
```
适合 Gateway/Proxy/Infra/Network/High-Concurrency API/Distributed。普通 CRUD：Go 可选，先评估 Python/TS。

### TypeScript（Matrix §6.3）
```
IF fullstack_web OR frontend OR node_backend
THEN TypeScript SHOULD be included as a candidate
```
适合 Web/BFF/Fullstack/Frontend-heavy。
**框架默认**（res.md §110 / §81）：纯 TS 后端服务 → **NestJS**，备选 Fastify / Hono；含前端的 fullstack → Next.js。判定逻辑见 `decision-trees/backend.md` §4。

### Java / Kotlin（Matrix §6.4）
```
IF enterprise_java_ecosystem OR organization_standard = Java OR existing = Spring OR enterprise_integration = high
THEN Java/Kotlin SHOULD be included as a candidate
```

### Rust（Matrix §6.5，仅候选）
```
IF memory_safety = critical AND performance = critical AND team_has_rust_expertise = true
THEN Rust = candidate
```
否则不要为性能猜测引入 Rust。适合极致性能/系统工具/安全底层/WASM/网络基础设施；默认不用于普通 CRUD Web。

## 2. Backend Framework Matrix（Matrix §7）

### Python（默认 FastAPI）
| Requirement | Decision |
| --- | --- |
| General / Async / AI API | FastAPI |
| CRUD-heavy admin | Django |
| Existing Flask | Preserve Flask |
| Very small service | Flask / FastAPI |
| Django ecosystem required | Django |

Django 选：Admin-heavy/CMS/Enterprise CRUD/ORM-heavy/server-rendered。新项目 FastAPI > Flask（非绝对）。

### Go（Matrix §7 关键修正）
**Go 标准库 `net/http` 已能构建完整 HTTP 服务**，Agent 不应默认引入第三方 framework。
| Requirement | Decision |
| --- | --- |
| Simple HTTP API / Standard-library-first / 极简 | `net/http` |
| REST API | `net/http` / Gin |
| Advanced middleware/routing | Gin |
| Existing Gin | Preserve Gin |

默认规则：小服务→`net/http`，普通 API→Gin，特殊需求→评估 Echo/Chi。

### TypeScript
| Requirement | Decision |
| --- | --- |
| Fullstack Web | Next.js |
| React frontend only | React + Vite |
| Vue application | Vue + Vite |
| Existing Next.js / Vue | Preserve |

### Java / Kotlin
默认 Spring Boot + Spring Web/Security/Data JPA + PostgreSQL + Redis/Kafka(按需) + JUnit + Testcontainers。

## 3. ORM（res.md §28 / 知识库 §25）
- Python：SQLAlchemy（FastAPI/显式 SQL）；Django 项目用 Django ORM。
- Go：simple SQL → `database/sql`；type-safe → `sqlc`；ORM required → GORM/Ent。Agent 不得因"ORM 方便"自动加 ORM。
- TS：Prisma / Drizzle。Java：Spring Data JPA；复杂 SQL → jOOQ。

## 4. 后台任务 / Worker（res.md §37 / 知识库 §4.5）
- Python：Celery / RQ / Arq + Redis/RabbitMQ（AI 批处理亦可用）。
- Go：Asynq / 自建 Worker + Redis。
- **BackgroundTasks ≠ 分布式可靠队列**；需 Retry/Persistence/分布式/Scheduling 用真正 task queue。

## 5. Package Management / Migration / Version（res.md §59,§64,§88,§89）
**版本选择策略只有一处实现**：`.sdd/knowledge/versioning.md`（本文件不写死版本号）。
见 deployment.md 与 backend 工具链。默认工具链（知识库 §47-§48）：
- Python：uv + FastAPI + Pydantic + SQLAlchemy + Alembic + pytest + Ruff + mypy/pyright
- Go：Go Modules + Gin/net/http + sqlc/GORM + golangci-lint + testing + Docker

## 6. 用户显式指定（res.md §1.5）
用户**明确表达「必须 / 不得 / 组织标准 / 不可改变」**时 = Hard Constraint（P0B），不得擅自改（decision-protocol §3.1）。
用户只说「偏好 / 熟悉 / 倾向 / 最好用」时只是候选先验，不构成约束（decision-protocol §3.4）。
若用户指定撞 P0A（EOL 运行时 / 明文存 token / 不可行架构），必须标 `BLOCKED` 提出异议，不得照做。

## 7. Repository Structure（res.md §78-§82 / 知识库 §55-§56）
- Python：`backend/app/{api,core,models,schemas,services,repositories}/main.py` + tests + migrations + pyproject.toml + Dockerfile
- Go：`backend/cmd/server/` + `internal/{handler,service,repository,model,middleware}/` + migrations + go.mod + Dockerfile
