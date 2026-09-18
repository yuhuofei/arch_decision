# Decision Tree: Backend（后端语言与框架选型）

> 配套知识：`.sdd/knowledge/backend.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## 1. 语言（Matrix §6，正式条件）

```
IF AI OR ML OR Data Processing OR Automation OR CRUD/API
   AND extreme_performance = false
→ Python                         # AUTO

IF concurrency = high OR network_service OR infrastructure
   OR latency_requirement = strict OR CPU_efficiency = important
→ Go                             # AUTO（普通 CRUD 先评估 Python/TS）

IF fullstack_web OR frontend OR node_backend
→ TypeScript                    # AUTO

IF enterprise_java_ecosystem OR organization_standard = Java
   OR existing = Spring OR enterprise_integration = high
→ Java/Kotlin                   # AUTO（组织标准=Hard Constraint）

IF memory_safety = critical AND performance = critical
   AND team_has_rust_expertise = true
→ Rust = candidate              # RECOMMEND
```

## 2. Python 框架（Matrix §7）
```
General/Async/AI API        → FastAPI        # 默认 AUTO
CRUD-heavy admin            → Django
Existing Flask              → Preserve Flask  # Hard Constraint
Very small service          → Flask / FastAPI
```

## 3. Go 框架（Matrix §7 关键修正）
```
Simple HTTP / std-lib-first / 极简 → net/http     # 默认优先
REST API                    → net/http / Gin
Advanced middleware/routing → Gin
Existing Gin                → Preserve Gin
```
> Go 标准库 `net/http` 已能构建完整 HTTP 服务，Agent 不应默认引入第三方 framework。

## 4. TypeScript 框架（Matrix §7 / res.md §13,§81）
**纯 TS 后端服务**（API-only / BFF，无前端）：
```
default                     → NestJS      # 默认 AUTO（模块化 + DI + Guard/Interceptor）
轻量 / 低开销 / schema-first → Fastify     # 备选
Edge / Serverless / 极小体积 → Hono        # 备选
存量 Express                → Preserve    # 仅当已用且无迁移诉求
```
**含前端的 Fullstack Web**（Matrix §7）：
```
Fullstack Web               → Next.js
React frontend only         → React + Vite
Vue application             → Vue + Vite
Existing Next.js / Vue      → Preserve
```
> **不要把 Next.js 当纯后端框架**：它是 fullstack web framework，API-only 服务用 Next.js 属于过度设计。语言判定给出 `TypeScript`（本文件 §1）后，必须落到上面两组之一，否则选型未决。

## 5. Java/Kotlin 框架
```
Enterprise/复杂业务/大团队 → Spring Boot       # AUTO
```

## 6. Worker / 后台任务（知识库 §4.5）
```
Python + 异步任务 → Celery / RQ / Arq + Redis/RabbitMQ
Go + 异步任务    → Asynq + Redis
需 Retry/Persistence/分布式/Scheduling → 真正 task queue（非 BackgroundTasks）
```

## 用户显式指定
用户指定 `Python+FastAPI+PostgreSQL` 等 = Hard Constraint（P0），不得擅自改（decision-protocol §3）。

## 输出
写入 `technology-selection.md` 的 Backend 段：Candidates / Selected / Reason / Alternatives / Rejected Because / Decision Status。
