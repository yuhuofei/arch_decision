# AI Architecture Decision Matrix

> Purpose: 将项目需求转换为可执行的技术架构决策。
>
> Target: AI Coding Agent / Claude Code / Codex / Cursor / Spec Kit / OpenSpec
>
> Core principle:
>
> **Requirements → Constraints → Decision Matrix → Candidate Architecture → ADR → Plan → Tasks**

---

# 1. Agent 总决策协议

Agent 不允许直接从技术栈名称开始决策。

必须按照以下顺序：

```text
INPUT
  ↓
Project Classification
  ↓
Hard Constraints
  ↓
Architecture Decision
  ↓
Backend Decision
  ↓
Frontend Decision
  ↓
Data Decision
  ↓
Infrastructure Decision
  ↓
Testing / Observability / Security
  ↓
Architecture Validation
  ↓
ADR
  ↓
plan.md
```

每一个重大技术决策必须输出：

```yaml
decision:
reason:
evidence:
alternatives:
rejected:
constraints:
risks:
confidence:
```

---

# 2. 决策优先级

当多个规则冲突时，按照以下优先级执行：

| Priority | Rule                           | 类型                |
| -------- | ------------------------------ | ----------------- |
| P0       | Existing system constraints    | Hard Constraint   |
| P0       | Security / Compliance          | Hard Constraint   |
| P0       | Explicit user requirement      | Hard Constraint   |
| P0       | Deployment/platform constraint | Hard Constraint   |
| P1       | Functional requirements        | Strong Constraint |
| P1       | Performance requirements       | Strong Constraint |
| P1       | Data characteristics           | Strong Constraint |
| P1       | Team expertise                 | Strong Constraint |
| P2       | Maintainability                | Preference        |
| P2       | Testability                    | Preference        |
| P2       | Operational simplicity         | Preference        |
| P3       | Ecosystem maturity             | Preference        |
| P3       | Developer popularity           | Weak Preference   |

**禁止：**

```text
Popularity > Requirement
Framework preference > Existing system
Personal preference > Explicit requirement
Architecture fashion > Simplicity
```

---

# 3. Hard Constraint / Soft Constraint

## 3.1 Hard Constraint

满足以下任意条件时，视为 Hard Constraint：

```text
用户明确指定
现有系统强依赖
法规/合规要求
部署平台限制
数据库兼容性要求
必须支持的第三方系统
性能 SLA
安全要求
组织标准
```

Hard Constraint 不允许 Agent 自行覆盖。

例如：

```text
Requirement:
必须部署到 AWS Lambda

Decision:
不能默认选择长期运行的传统 server architecture。
```

---

## 3.2 Soft Constraint

以下属于 Soft Constraint：

```text
团队熟悉度
开发效率
生态成熟度
维护成本
学习成本
社区活跃度
性能余量
未来扩展性
```

Soft Constraint 可以比较，但不能覆盖 Hard Constraint。

---

# 4. 项目类型矩阵

| 条件                  | Project Type                |
| ------------------- | --------------------------- |
| API + CRUD + Web UI | SaaS / Business Application |
| AI / LLM / RAG      | AI Application              |
| 数据处理 / ETL          | Data Application            |
| CLI                 | CLI                         |
| SDK / Library       | Library                     |
| 高吞吐网络服务             | High-Concurrency Backend    |
| 内部管理系统              | Internal Tool               |
| Mobile App          | Mobile                      |
| 实时通信                | Realtime Application        |
| IoT / Device        | IoT                         |
| 基础设施工具              | Infrastructure              |
| 定时任务 / Automation   | Automation                  |
| 多服务业务平台             | Distributed System          |

如果同时命中多个类型：

```text
Primary Type = 主要业务价值
Secondary Type = 技术特征
```

例如：

```text
AI SaaS

Primary:
SaaS

Secondary:
AI / RAG
```

---

# 5. Architecture Decision Matrix

## 5.1 Monolith

### 默认

```text
IF
  user_count < 100000
  AND
  team_size <= 10
  AND
  independent_scaling = false
  AND
  deployment_complexity must_be_low
THEN
  architecture = Monolith
```

适用于：

```text
MVP
内部系统
普通 CRUD
早期 SaaS
管理后台
简单 API
```

---

# 5.2 Modular Monolith

### 默认优先级

```text
IF
  application_complexity >= medium
  AND
  service_independence = low
  AND
  team_size <= 20
THEN
  architecture = Modular Monolith
```

推荐作为新企业应用的默认架构。

典型：

```text
Auth
Users
Billing
Orders
Notifications
Reporting
```

部署：

```text
1 application
1 database
multiple modules
```

---

# 5.3 Microservices

不得因为“未来可能扩展”直接选择 Microservices。

必须满足以下条件中的至少 2 个：

```text
IF
  independent_scaling = true
OR
  independent_deployment = true
OR
  team_ownership_boundary = strong
OR
  technology_boundary = strong
OR
  failure_isolation = required
OR
  workload_profile differs significantly
```

并且：

```text
microservices_benefit > operational_complexity
```

否则：

```text
Microservices = REJECT
Modular Monolith = DEFAULT
```

---

# 6. Backend Language Matrix

## 6.1 Python

命中条件：

```text
IF
  AI = true
OR
  ML = true
OR
  Data Processing = true
OR
  Automation = true
OR
  CRUD/API = true
AND
  extreme_performance = false
THEN
  language = Python
```

优先：

```text
AI
RAG
LLM
ETL
Automation
Admin API
Business API
Data Science
```

---

# 6.2 Go

命中条件：

```text
IF
  concurrency = high
OR
  network_service = true
OR
  infrastructure = true
OR
  latency_requirement = strict
OR
  CPU_efficiency = important
THEN
  language = Go
```

尤其适合：

```text
Gateway
Proxy
Infrastructure
Network Service
High-Concurrency API
Distributed System
```

如果只是普通 CRUD：

```text
Go = optional
Python / TypeScript = evaluate first
```

---

# 6.3 TypeScript

命中：

```text
IF
  fullstack_web = true
OR
  frontend = true
OR
  node_backend = true
THEN
  language = TypeScript
```

特别适合：

```text
Web Application
BFF
Fullstack
Frontend-heavy application
```

---

# 6.4 Java / Kotlin

命中：

```text
IF
  enterprise_java_ecosystem = required
OR
  organization_standard = Java
OR
  existing_system = Spring
OR
  enterprise_integration = high
THEN
  language = Java/Kotlin
```

---

# 6.5 Rust

只有在以下场景明显成立时进入候选：

```text
IF
  memory_safety = critical
AND
  performance = critical
AND
  team_has_rust_expertise = true
THEN
  Rust = candidate
```

否则不要为了性能猜测而引入 Rust。

---

# 7. Backend Framework Matrix

## Python

| Requirement               | Decision        |
| ------------------------- | --------------- |
| General API               | FastAPI         |
| Async API                 | FastAPI         |
| AI API                    | FastAPI         |
| CRUD-heavy admin          | Django          |
| Existing Flask            | Preserve Flask  |
| Very small service        | Flask / FastAPI |
| Django ecosystem required | Django          |

---

## Go

| Requirement                 | Decision       |
| --------------------------- | -------------- |
| Simple HTTP API             | net/http       |
| Standard-library-first      | net/http       |
| REST API                    | net/http / Gin |
| Advanced middleware/routing | Gin            |
| Existing Gin project        | Preserve Gin   |

Go 标准库已经提供 HTTP server/router 能力，因此 Agent 不应该默认引入第三方 framework；只有在 routing、middleware、生态等需求存在时才引入。

---

## TypeScript

| Requirement         | Decision     |
| ------------------- | ------------ |
| Fullstack Web       | Next.js      |
| React frontend only | React + Vite |
| Vue application     | Vue + Vite   |
| Existing Next.js    | Preserve     |
| Existing Vue        | Preserve     |

Next.js 本身定位为 React 的 full-stack web framework；因此如果需求是 React + frontend/backend integration，Next.js 可以进入默认候选。

---

# 8. Frontend Matrix

## 8.1 Vue

命中：

```text
IF
  business_app = true
AND
  frontend_complexity = medium
THEN
  Vue 3 + TypeScript
```

适合：

```text
Admin
Dashboard
Enterprise CRUD
Internal Tool
SaaS
```

Vue 官方提供 Vue 3 + TypeScript 的一等支持。

---

# 8.2 React

命中：

```text
IF
  react_ecosystem_required = true
OR
  existing_react = true
OR
  component_ecosystem = important
THEN
  React
```

---

# 8.3 Next.js

命中：

```text
IF
  React = true
AND
(
  SSR = true
  OR
  SEO = important
  OR
  fullstack_web = true
  OR
  server_components = useful
)
THEN
  Next.js
```

否则：

```text
React + Vite
```

---

# 8.4 Angular

命中：

```text
IF
  enterprise_frontend_standard = Angular
OR
  existing_angular = true
OR
  large_enterprise_team = true
AND
  Angular_expertise = strong
THEN
  Angular
```

否则不作为默认选择。

---

# 9. Frontend / Backend Separation Matrix

| Condition             | Decision                               |
| --------------------- | -------------------------------------- |
| Simple CRUD           | Can be integrated                      |
| SEO / public website  | Prefer Next.js                         |
| Large frontend        | Separate frontend/backend              |
| Multiple clients      | Separate API                           |
| Mobile + Web + API    | Separate API                           |
| AI API + Web          | Separate frontend/API often preferable |
| Internal tool         | Integrated acceptable                  |
| Existing architecture | Preserve                               |

---

# 10. Database Matrix

## PostgreSQL

默认候选：

```text
IF
  relational_data = true
AND
  no_specific_constraint
THEN
  PostgreSQL
```

适合：

```text
SaaS
ERP
CRM
Orders
Users
Billing
AI SaaS
RAG
Business Applications
```

---

# 11. MySQL

选择条件：

```text
IF
  existing_mysql = true
OR
  organization_standard = MySQL
OR
  ecosystem_dependency = MySQL
THEN
  MySQL
```

不要因为“数据库都差不多”而在已有 PostgreSQL 项目中切换。

---

# 12. SQLite

选择条件：

```text
IF
  single_instance = true
AND
  low_concurrency = true
AND
  database_scale = small
THEN
  SQLite
```

典型：

```text
CLI
Prototype
Local Tool
Desktop App
Small Internal Tool
Tests
```

---

# 13. Redis Matrix

Redis **不是默认数据库**。

只有命中以下需求才加入：

```text
cache
session
rate_limit
distributed_lock
temporary_state
queue
stream
hot_data
```

决策：

```text
IF none_of_above
THEN
  Redis = false
```

---

# 14. ORM Matrix

## Python

```text
FastAPI + relational DB
→ SQLAlchemy
```

如果：

```text
Django
→ Django ORM
```

---

## Go

根据需求：

```text
Simple SQL
→ database/sql

Type-safe SQL
→ sqlc

ORM required
→ GORM / equivalent
```

Agent 不得因为“ORM 更方便”自动增加 ORM。

---

# 15. API Protocol Matrix

## REST

默认：

```text
IF
  public_api = true
OR
  business_api = true
OR
  CRUD = true
THEN
  REST
```

---

## GraphQL

只有：

```text
IF
  frontend_data_shape_complexity = high
AND
  clients_need_different_views = true
THEN
  GraphQL = candidate
```

---

## gRPC

选择：

```text
IF
  service_to_service = true
AND
  low_latency = important
OR
  strongly_typed_contract = important
THEN
  gRPC
```

---

# 16. Message Queue Matrix

## 不需要 MQ

```text
IF
  request_response = sufficient
AND
  background_work = low
THEN
  MQ = false
```

---

## RabbitMQ

```text
IF
  task_queue = true
OR
  business_event = true
OR
  routing = important
THEN
  RabbitMQ
```

---

## Kafka

```text
IF
  event_streaming = true
AND
(
  high_event_volume = true
OR
  event_replay = true
OR
  multiple_consumers = true
OR
  stream_processing = true
)
THEN
  Kafka
```

---

## Redis Queue

```text
IF
  queue_complexity = low
AND
  Redis_already_required = true
THEN
  Redis-based queue
```

---

# 17. Search Engine Matrix

默认：

```text
PostgreSQL search
```

只有当：

```text
full_text_search = complex
OR
fuzzy_search = important
OR
search_scale = large
OR
faceting = complex
OR
search_relevance = critical
```

才考虑：

```text
OpenSearch / Elasticsearch
```

不要因为“以后可能搜索很多”提前加入搜索集群。

---

# 18. Vector Database Matrix

## pgvector

默认候选：

```text
IF
  vector_search = true
AND
  relational_data = true
AND
  vector_scale = moderate
THEN
  PostgreSQL + pgvector
```

---

## Dedicated Vector DB

只有：

```text
IF
  vector_scale = large
OR
  vector_workload = dominant
OR
  specialized_vector_features = required
THEN
  Qdrant / Milvus / Weaviate / equivalent
```

---

# 19. Object Storage Matrix

如果：

```text
file_storage = true
AND
file_size / volume > local_disk_reasonable_limit
```

选择：

```text
S3-compatible storage
```

候选：

```text
AWS S3
Cloudflare R2
MinIO
OSS
COS
```

如果只是：

```text
small local files
```

可以：

```text
local filesystem
```

---

# 20. Authentication Matrix

## No Auth

仅当：

```text
public_readonly = true
AND
user_identity_not_required = true
```

---

## Session

选择：

```text
IF
  traditional_web_application = true
AND
  browser_only = true
THEN
  Session-based auth
```

---

## JWT

选择：

```text
IF
  multiple_clients = true
OR
  stateless_api = true
OR
  mobile_client = true
THEN
  JWT / token-based auth
```

---

## OAuth / OIDC

选择：

```text
IF
  enterprise_sso = true
OR
  social_login = true
OR
  external_identity_provider = true
THEN
  OAuth/OIDC
```

---

# 21. Authorization Matrix

如果只有：

```text
admin / user
```

使用：

```text
RBAC
```

如果权限与：

```text
resource
organization
tenant
ownership
attribute
```

相关：

```text
RBAC + resource-level authorization
```

只有复杂策略场景才引入：

```text
ABAC / Policy Engine
```

---

# 22. Multi-Tenant Matrix

如果：

```text
users belong to organizations
AND
data isolation required
```

则：

```text
multi_tenant = true
```

进一步选择：

| Requirement          | Strategy                |
| -------------------- | ----------------------- |
| Small/medium SaaS    | Shared DB + tenant_id   |
| Strong isolation     | Separate schema         |
| Regulatory isolation | Separate database       |
| Extreme isolation    | Separate infrastructure |

默认：

```text
Shared DB + tenant_id
```

除非存在明确隔离要求。

---

# 23. Caching Matrix

加入 Cache 的条件：

```text
IF
  read_heavy = true
AND
  data_changes_less_frequently = true
AND
  cache_hit_benefit = significant
THEN
  cache = true
```

否则：

```text
cache = false
```

不要因为“Redis 很快”默认加入 Redis。

---

# 24. Deployment Matrix

## Local / MVP

```text
Docker Compose
```

---

## Small Production

```text
Docker
+
Managed Database
+
Managed Redis if needed
```

---

## Large Production

只有出现：

```text
multiple_services
OR
autoscaling
OR
high_availability
OR
multi_region
OR
organization_kubernetes_standard
```

才考虑：

```text
Kubernetes
```

---

# 25. Kubernetes Decision Rule

```text
IF
  deployment_complexity_requirement <= medium
THEN
  Kubernetes = false
```

```text
IF
  autoscaling = required
AND
  service_count >= multiple
AND
  operational_team = available
THEN
  Kubernetes = candidate
```

否则：

```text
Docker / Managed Container Platform
```

优先。

---

# 26. Observability Matrix

## Logging

默认：

```text
structured logging = true
```

---

## Metrics

如果：

```text
production_service = true
```

则：

```text
metrics = true
```

---

## Tracing

如果：

```text
multiple_services = true
OR
  distributed_requests = true
OR
  latency_debugging = important
```

则：

```text
distributed tracing = true
```

OpenTelemetry 作为统一 instrumentation 候选。

---

# 27. Testing Matrix

## Unit Test

默认：

```text
business_logic = true
→ unit tests
```

---

## Integration Test

如果：

```text
database = true
OR
external_api = true
OR
queue = true
```

则：

```text
integration tests = true
```

---

## E2E

如果：

```text
web_ui = true
AND
critical_user_flow = true
```

则：

```text
E2E = true
```

至少覆盖：

```text
login
critical CRUD
payment
core workflow
```

具体项目按风险决定。

---

# 28. Test Strategy Matrix

| Project        |   Unit | Integration |    E2E |
| -------------- | -----: | ----------: | -----: |
| Library        |   High |      Medium |    Low |
| CRUD API       |   High |        High | Medium |
| SaaS           |   High |        High |   High |
| AI SaaS        |   High |        High |   High |
| CLI            |   High |      Medium |    Low |
| Data Pipeline  |   High |        High |    Low |
| Infrastructure |   High |        High | Medium |
| Frontend-heavy | Medium |      Medium |   High |

---

# 29. AI Application Matrix

如果：

```text
LLM = true
```

自动检查：

```text
model_provider
prompt_management
token_cost
retry
timeout
streaming
structured_output
evaluation
fallback
observability
```

---

# 30. LLM Provider Architecture

如果只有一个模型供应商：

```text
direct SDK = acceptable
```

如果：

```text
multiple providers
OR
provider switching = expected
OR
model evaluation = required
```

则：

```text
LLM Provider Abstraction
```

但不要为了“未来支持多个模型”提前建立过度复杂的 abstraction。

---

# 31. RAG Matrix

如果：

```text
document_knowledge = true
AND
semantic_search = true
```

则：

```text
RAG = true
```

进一步：

```text
relational_data + moderate vector workload
→ PostgreSQL + pgvector

large vector workload
→ Dedicated Vector DB
```

---

# 32. Architecture Complexity Budget

Agent 必须计算：

```text
complexity_score
```

每引入一个基础设施组件：

```text
+1
```

例如：

```text
PostgreSQL        +1
Redis             +1
RabbitMQ           +1
Kafka              +2
Elasticsearch      +2
Vector DB          +2
Kubernetes         +3
Microservices      +3
```

如果：

```text
complexity_score > project_complexity_budget
```

必须重新评估。

默认预算：

| Project            | Budget |
| ------------------ | -----: |
| MVP                |      5 |
| Internal Tool      |      6 |
| Small SaaS         |      8 |
| Enterprise SaaS    |     12 |
| Distributed System |    20+ |

这不是性能评分，而是**架构复杂度控制机制**。

---

# 33. Infrastructure Introduction Rule

任何新增 infrastructure 都必须回答：

```text
1. What requirement requires it?
2. Why existing components cannot satisfy it?
3. What operational cost does it introduce?
4. What happens if it fails?
5. How will it be tested?
6. How will it be monitored?
7. Can it be removed later?
```

如果无法回答：

```text
REJECT
```

---

# 34. Existing Project Decision Matrix

这是 Brownfield 项目的最高优先级规则。

```text
IF existing_project = true
THEN
  inspect_existing_stack()
```

默认：

```text
preserve_existing_stack = true
```

只有满足：

```text
existing_stack_problem = demonstrated
```

或者：

```text
migration_requested = true
```

才允许迁移。

---

# 35. Existing Stack Conflict

如果发现：

```text
Existing:
Django + PostgreSQL + React

Knowledge Base:
FastAPI + PostgreSQL + Vue
```

结果：

```text
DO NOT migrate automatically
```

应输出：

```yaml
existing_stack:
  backend: Django
  frontend: React
  database: PostgreSQL

recommended_action:
  preserve_existing_stack: true

migration:
  required: false
```

---

# 36. Technology Selection Scoring

当多个候选方案都满足 Hard Constraints 时，使用：

```text
Score =
  Requirement Fit × 40
+ Maintainability × 20
+ Team Fit × 15
+ Operational Simplicity × 15
+ Ecosystem × 10
```

每项：

```text
0 - 5
```

但：

```text
Hard Constraint failure = candidate eliminated
```

不是降低分数。

---

# 37. Example

需求：

```yaml
project:
  type: SaaS

users:
  expected: 5000

frontend:
  web: true

backend:
  api: true

data:
  relational: true

ai:
  false

concurrency:
  medium

team:
  size: 6

deployment:
  docker: true
```

候选架构：

```text
Microservices
Modular Monolith
Monolith
```

规则：

```text
team_size <= 10
independent_scaling = false
service_independence = low
```

因此：

```text
Microservices → eliminated
```

候选：

```text
Monolith
Modular Monolith
```

复杂度为 medium：

```text
Modular Monolith → selected
```

---

# 38. Example: AI SaaS

Input：

```yaml
project_type: SaaS
ai: true
rag: true
relational_data: true
vector_scale: moderate
frontend: web
team_size: 5
```

决策：

```text
Architecture
→ Modular Monolith

Frontend
→ Next.js + TypeScript

Backend
→ FastAPI

Database
→ PostgreSQL

Vector
→ pgvector

Cache
→ Redis only if cache/session/rate-limit required

Object Storage
→ S3-compatible

API
→ REST

Testing
→ pytest + frontend tests + E2E

Observability
→ structured logging + metrics
```

---

# 39. Example: High-Concurrency Service

Input：

```yaml
project_type: network_service
concurrency: very_high
latency_requirement: strict
service_to_service: true
```

Decision：

```text
Language
→ Go

HTTP
→ net/http / Gin

Protocol
→ REST externally
→ gRPC internally if justified

Database
→ PostgreSQL if relational

Cache
→ Redis if required

Architecture
→ Modular Monolith initially

Microservices
→ only if independent scaling/deployment required
```

---

# 40. Decision Output Schema

Agent 最终必须生成：

```yaml
architecture_decision:

  project:
    type:
    scale:
    team_size:
    deployment:

  architecture:
    style:
    reason:

  backend:
    language:
    framework:
    reason:

  frontend:
    language:
    framework:
    reason:

  database:
    primary:
    reason:

  cache:
    enabled:
    technology:
    purpose:

  messaging:
    enabled:
    technology:
    purpose:

  search:
    enabled:
    technology:

  vector:
    enabled:
    technology:

  object_storage:
    enabled:
    technology:

  authentication:
    strategy:

  authorization:
    strategy:

  observability:
    logging:
    metrics:
    tracing:

  testing:
    unit:
    integration:
    e2e:

  deployment:
    strategy:

  rejected:
    - option:
      reason:

  risks:
    - ...

  assumptions:
    - ...

  confidence:
    overall:
```

---

# 41. Decision Status

每个决策必须标记：

```text
AUTO
```

Agent 可以自动决定。

```text
RECOMMEND
```

Agent 可以提出方案，但需要人确认。

```text
REQUIRE_CONFIRMATION
```

存在重大架构影响，必须确认。

```text
BLOCKED
```

信息不足，不能继续。

---

# 42. 哪些决策必须人工确认

以下默认：

```text
REQUIRE_CONFIRMATION
```

包括：

```text
Microservices
Kubernetes
Multi-region
Database migration
Authentication architecture
Authorization model
Payment architecture
Data residency
Compliance architecture
Major cloud provider decision
Event-driven architecture
CQRS
Event sourcing
Distributed transaction
Public API contract
Breaking API changes
Major technology migration
```

---

# 43. Agent Decision Loop

Agent 必须执行：

```text
1. Read requirements
2. Classify project
3. Extract hard constraints
4. Extract soft constraints
5. Detect existing stack
6. Generate candidates
7. Eliminate hard-constraint violations
8. Score remaining candidates
9. Select simplest sufficient architecture
10. Generate ADR
11. Mark confidence
12. Identify human-confirmation decisions
13. Generate plan.md
14. Generate tasks.md
15. Run consistency analysis
```

这与当前 Spec Kit 的 Specify → Plan → Tasks → Analyze → Implement → Converge 工作流可以直接衔接。Spec Kit 当前也明确把技术栈、架构和技术约束放在 Plan 阶段，而 Tasks 再基于设计产出依赖有序任务。

---

# 44. 最终 Agent Rule

将下面内容作为最高层 system instruction：

```text
Architecture Decision Rules

1. Never select technology before understanding requirements.

2. Existing project constraints have priority over generic defaults.

3. Explicit user requirements are hard constraints.

4. Security, compliance, deployment and compatibility constraints
   are hard constraints.

5. Eliminate candidates that violate hard constraints.

6. Among valid candidates, prefer the simplest architecture
   that satisfies all requirements.

7. Prefer Modular Monolith over Microservices unless
   independent scaling, deployment, ownership, technology,
   or failure isolation provides a demonstrated benefit.

8. Prefer PostgreSQL for new relational applications unless
   a concrete requirement favors another database.

9. Never introduce Redis unless cache, session, rate limiting,
   locking, queueing, streams, or temporary state requires it.

10. Never introduce Kafka/RabbitMQ unless asynchronous or
    event-driven requirements justify it.

11. Never introduce Elasticsearch/OpenSearch unless database
    search capabilities are insufficient.

12. Never introduce a dedicated vector database when
    PostgreSQL + pgvector satisfies the expected workload.

13. Never introduce Kubernetes unless operational requirements
    justify its complexity.

14. Preserve existing technology in Brownfield projects unless
    migration is explicitly requested or a demonstrated
    technical problem requires change.

15. Do not optimize for popularity.

16. Do not optimize for hypothetical future requirements.

17. Every architecture component must have a documented reason.

18. Every major decision must record:
    decision
    reason
    alternatives
    rejected alternatives
    risks
    assumptions
    confidence

19. Architecture decisions must be classified as:
    AUTO
    RECOMMEND
    REQUIRE_CONFIRMATION
    BLOCKED

20. Never silently make a REQUIRE_CONFIRMATION decision.

21. spec.md describes WHAT and WHY.

22. plan.md describes HOW, architecture and technology choices.

23. tasks.md describes executable implementation work.

24. Every task must trace back to a requirement or design decision.

25. Before implementation, validate:
    spec → plan → tasks

26. After implementation, validate:
    requirements → design → tasks → code → tests

27. If ambiguity can materially change architecture,
    stop and ask for clarification.

28. If ambiguity does not materially change architecture,
    make an explicit assumption and continue.

29. Prefer reversible decisions over irreversible decisions.

30. Minimize infrastructure and operational complexity.

31. The goal is not the most advanced architecture.
    The goal is the smallest architecture that reliably
    satisfies the requirements.
```

---

# 45. 推荐最终目录

将这套 Matrix 放入：

```text
ai-architecture-kb/
├── README.md
├── principles.md
├── decision-matrix.md
├── decision-tree.md
├── scoring.md
│
├── languages/
├── backend/
├── frontend/
├── database/
├── infrastructure/
├── architecture/
├── security/
├── testing/
├── observability/
│
├── templates/
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   └── adr.md
│
└── examples/
    ├── saas.md
    ├── ai-saas.md
    ├── internal-tool.md
    ├── high-concurrency.md
    └── brownfield.md
```

其中：

```text
decision-matrix.md
        ↓
decision-tree.md
        ↓
Agent
        ↓
ADR
        ↓
spec.md
        ↓
plan.md
        ↓
tasks.md
```

这样这份知识库就不再只是“技术选型百科”，而变成了一个 **Architecture Decision Engine 的规则集**。

另外，对于超大型 feature，可以让 Agent 先把项目拆成 roadmap / sub-spec，再分别执行 spec → plan → tasks；这也是当前 Spec Kit 官方推荐的 “spec of specs” 模式。
