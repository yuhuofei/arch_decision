# AI Coding SDD 项目技术架构与框架选择知识库

> Version: 1.0
> Purpose: 为 Claude Code、Codex、Cursor、Kiro、GitHub Copilot 等 AI Coding Agent 提供项目架构设计、技术栈选择和 Spec 生成的先验知识。
>
> 使用方式：在执行 SDD 的 `specify / plan / design` 阶段，将本文档作为 Architecture Knowledge Base / Project Bootstrap Knowledge 输入。

---

# 1. 文档目标

本知识库用于解决以下问题：

当用户只提出：

> “帮我开发一个订单管理系统。”

Agent 不应该立即开始写代码，也不应该随机选择：

* Python / Go / Java / TypeScript
* FastAPI / Flask / Django
* Gin / Echo / net/http
* Vue / React / Next.js
* PostgreSQL / MySQL
* Redis
* RabbitMQ / Kafka
* REST / GraphQL
* Monolith / Microservices
* 前后端分离 / 全栈
* ORM / SQL
* Docker / Kubernetes

而应该首先：

1. 分析业务规模；
2. 分析用户数量；
3. 分析并发与性能要求；
4. 分析数据模型；
5. 分析部署环境；
6. 分析团队技术能力；
7. 分析未来扩展性；
8. 分析是否需要异步处理；
9. 分析是否需要缓存；
10. 分析是否需要搜索；
11. 分析是否需要实时通信；
12. 分析安全与合规要求；
13. 根据决策规则选择合理的技术架构；
14. 对重要架构选择记录理由；
15. 将架构选择写入 `plan.md` / `architecture.md` / ADR；
16. 不因为“流行”而引入不必要的技术。

---

# 2. 总体原则

## 2.1 默认原则

遵循：

> Simple First, Explicit Decisions, Minimal Dependencies, Evolvable Architecture.

优先：

```text
简单
>
可维护
>
可测试
>
可观察
>
可扩展
>
极致性能
```

除非需求明确要求，否则不要为了未来可能存在的需求提前引入复杂架构。

---

# 3. 架构选择总决策树

Agent 在设计项目时按照以下顺序判断。

```text
                    用户需求
                       │
                       ▼
                项目类型是什么？
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Web/API       CLI/Job      Data/AI
          │
          ▼
       规模？
          │
     ┌────┴────┐
     ▼         ▼
    小/中      大/高并发
     │         │
     ▼         ▼
  Monolith   Modular
             Monolith
                │
         是否必须拆服务？
                │
         ┌──────┴──────┐
         ▼             ▼
        否             是
         │             │
 Modular Monolith   Microservices
```

默认：

> **新项目优先 Modular Monolith，而不是 Microservices。**

只有出现以下条件之一时，才考虑微服务：

* 明确的团队边界；
* 服务需要独立扩展；
* 服务需要独立部署；
* 不同服务具有明显不同的技术/资源需求；
* 独立故障隔离有实际价值；
* 已经存在稳定的服务边界；
* 系统规模足以证明微服务带来的运维成本是值得的。

---

# 4. 项目类型分类

Agent 首先将项目归类。

## 4.1 Web Application

典型：

* SaaS
* ERP
* CRM
* OA
* Admin
* CMS
* 电商
* 内部管理系统

默认：

```text
Frontend
+
Backend API
+
Relational Database
```

---

## 4.2 API / Backend Service

典型：

* REST API
* BFF
* Mobile Backend
* Third-party API
* Internal Service

默认：

```text
Backend
+
PostgreSQL/MySQL
```

需要时增加：

```text
Redis
Message Queue
Object Storage
Search
```

---

## 4.3 Data / AI Application

典型：

* RAG
* AI Agent
* LLM Application
* Data Pipeline
* Recommendation
* Analytics

典型架构：

```text
Frontend
    │
    ▼
API / Agent Service
    │
 ┌──┼──────────────┐
 ▼  ▼              ▼
DB Redis       Vector Store
    │
    ▼
Object Storage
```

---

## 4.4 CLI / Automation

默认：

```text
Python / Go
```

如果主要处理：

* 数据
* 自动化
* AI
* ETL

优先 Python。

如果主要处理：

* 系统工具
* 网络工具
* DevOps
* 高性能 CLI

优先 Go。

---

## 4.5 Worker / Background Job

适合：

* 异步任务
* 文件处理
* 邮件发送
* 数据同步
* ETL
* AI 批处理

推荐：

```text
Python
+
Celery / RQ / Arq
+
Redis / RabbitMQ
```

或：

```text
Go
+
Asynq / 自建 Worker
+
Redis
```

---

# 5. 编程语言选择

## 5.1 Python

默认适用于：

* Web API
* AI
* LLM
* 数据分析
* 自动化
* ETL
* 快速业务开发
* 内部系统
* CRUD 系统

优势：

* 开发速度快；
* AI/ML 生态强；
* AI Agent 对 Python 代码理解通常较好；
* Web、数据、AI 生态成熟。

不足：

* CPU 密集型任务性能通常不如 Go/Rust；
* 大型项目需要严格控制类型、模块边界和依赖。

默认：

```text
Python 3.x
+
uv
+
FastAPI
+
Pydantic
+
SQLAlchemy
+
Alembic
+
pytest
```

---

# 6. Python Web Framework

## 6.1 FastAPI —— 默认 API 首选

适用于：

* REST API
* 微服务
* BFF
* AI Backend
* CRUD API
* 异步 IO 服务

推荐组合：

```text
FastAPI
Pydantic
SQLAlchemy
Alembic
pytest
```

FastAPI 的核心优势包括类型提示、自动 API 文档和现代 Python async 支持。

默认 API 项目优先使用 FastAPI。

---

## 6.2 Flask

适用于：

* 小型 API
* 极简 Web 服务
* 已有 Flask 项目
* 需要高度自由组合组件

Flask 官方定位就是 lightweight WSGI framework，并强调从小型应用扩展到复杂应用的能力。

不要因为“Python Web”就自动选择 Flask。

新项目如果主要是 API，默认：

```text
FastAPI > Flask
```

如果团队已经大量使用 Flask，则保持一致性优先。

---

## 6.3 Django

适用于：

* 后台管理系统
* CMS
* 大量 CRUD
* 用户、权限、Admin、ORM 都很重要的项目
* 传统企业 Web

如果需求是：

```text
用户
+
权限
+
后台
+
CRUD
+
数据库
```

可以优先考虑 Django。

不要为了一个简单 REST API 引入 Django 全家桶。

---

# 7. Go

Go 优先用于：

* 高并发 API
* 微服务
* 网络服务
* Gateway
* Infrastructure
* DevOps
* CLI
* 长时间运行服务
* CPU/IO 混合型服务

Go 自带 `net/http` 已经能够构建完整 HTTP 服务，现代 Go 的标准库路由能力也已经增强，因此小型服务不应机械地引入大型 Web Framework。

---

# 8. Go Web Framework

## 8.1 Gin

适用于：

* REST API
* 微服务
* 高并发 Web 服务
* 团队熟悉 Gin 的项目

Gin 官方定位就是高性能 HTTP Web framework，适用于 REST API、Web Application 和 Microservice。

默认：

```text
Go + Gin
```

适合大多数 Go Web 项目。

---

## 8.2 Echo

适用于：

* REST API
* 微服务
* 需要简洁框架的 Go 项目

如果团队已有 Gin 经验，不要为了 Echo 更换。

---

## 8.3 net/http

适用于：

* 小型 API
* 内部服务
* 极简服务
* 希望最少依赖的系统

默认规则：

```text
小服务 → net/http
普通 API → Gin
特殊需求 → 评估 Echo / Chi
```

---

# 9. TypeScript / Node.js

优先用于：

* Web Full Stack
* BFF
* Frontend-heavy Application
* Real-time Application
* API Gateway
* SaaS

推荐：

```text
TypeScript
+
Node.js
```

不要新项目使用纯 JavaScript，除非项目非常简单或已有 JavaScript 生态约束。

---

# 10. Java / Kotlin

适用于：

* 企业级后端
* 大型业务系统
* 金融
* ERP
* 大型团队
* 已有 Java 技术体系

默认：

```text
Java/Kotlin
+
Spring Boot
+
PostgreSQL/MySQL
+
Redis
```

如果组织已经以 Java 为核心技术栈，不要为了 AI Coding 而强行迁移 Python/Go。

---

# 11. Rust

适用于：

* 极致性能
* 系统工具
* 高性能服务
* 安全要求极高的底层组件
* WebAssembly
* 网络基础设施

默认不用于普通 CRUD Web 项目。

---

# 12. 前后端架构

## 12.1 前后端分离

默认适用于：

* SaaS
* Admin
* 多终端系统
* Mobile + Web
* API 对外开放
* 多个前端共享 API

典型：

```text
Vue/React
    │
    │ HTTPS/JSON
    ▼
Backend API
    │
    ▼
Database
```

这是企业 Web 项目的默认方案。

---

# 13. 前后端合并

适用于：

* 小型工具
* 内容网站
* 简单后台
* SEO 网站
* MVP
* 内部工具

例如：

```text
Next.js
```

本身就是 React 全栈 Web framework，可以同时处理 UI、Server Components、Server Functions 和后端逻辑。

因此：

```text
简单 Web App
→ Next.js Full Stack
```

是合理方案。

---

# 14. Vue

默认适用于：

* 企业后台
* 管理系统
* ERP
* CRM
* SaaS
* 中后台

推荐：

```text
Vue 3
+
TypeScript
+
Vite
+
Pinia
+
Vue Router
```

Vue 官方对 TypeScript 有一等支持，官方 `create-vue` 也提供 Vite + TypeScript 项目初始化方式。

---

# 15. React

适用于：

* 大型 Web App
* 高度交互系统
* 复杂前端
* React 生态
* Next.js 项目

推荐：

```text
React
+
TypeScript
+
Vite
```

如果需要全栈：

```text
Next.js
+
React
+
TypeScript
```

React 官方已经不推荐 Create React App，新项目应选择推荐 framework 或自行配置现代工具链。

---

# 16. Next.js

适用于：

* SEO
* SSR
* Full Stack Web
* 内容网站
* SaaS
* React 全栈

推荐：

```text
Next.js App Router
+
TypeScript
```

除非存在历史兼容需求，否则新项目优先 App Router。

---

# 17. Angular

适用于：

* 大型企业前端
* 强约束团队
* 大型后台
* 已经存在 Angular 技术体系

如果团队没有 Angular 经验，不应仅因为“企业级”而选择 Angular。

---

# 18. CSS/UI 技术

默认：

```text
Tailwind CSS
```

适用于：

* AI Coding
* SaaS
* Admin
* 快速 UI 开发

如果企业已经有：

```text
Ant Design
Element Plus
MUI
Naive UI
```

则优先保持已有技术栈。

---

# 19. UI Component Library

Vue：

```text
Element Plus
Naive UI
Ant Design Vue
```

React：

```text
Ant Design
MUI
shadcn/ui
```

选择原则：

```text
企业后台 → Element Plus / Ant Design
高度定制 → shadcn/ui / Tailwind
已有体系 → 保持一致
```

---

# 20. Database 选择

数据库首先按照：

```text
关系型
文档型
KV
搜索
向量
时序
```

分类。

---

# 21. PostgreSQL

新项目默认关系数据库优先考虑 PostgreSQL。

适用于：

* SaaS
* ERP
* CRM
* 订单
* 财务
* 工作流
* 多租户
* 复杂查询
* JSON 数据
* 地理信息
* AI 应用

优势：

* SQL 能力强；
* 事务完整；
* JSON/JSONB；
* 丰富的数据类型；
* 扩展能力强；
* 复杂查询能力强。

如果没有明确的 MySQL 生态约束：

```text
PostgreSQL = Default
```

---

# 22. MySQL

适用于：

* 已有 MySQL 技术体系；
* 电商；
* CMS；
* 传统企业系统；
* 团队已有大量 MySQL 运维经验；
* 云环境已有成熟 MySQL 服务。

不要因为 PostgreSQL“功能更多”就迁移已有 MySQL 系统。

原则：

```text
Greenfield:
PostgreSQL 优先

Existing:
保持原数据库优先
```

MySQL 仍然是成熟的关系数据库，官方文档当前仍维护 8.0、8.4 等版本线。

---

# 23. SQLite

适用于：

* CLI
* Desktop
* MVP
* 本地工具
* 测试
* 单机应用
* 小型内部系统

不要把 SQLite 作为高并发、多实例 Web 系统的默认生产数据库。

---

# 24. Redis

Redis 不应该默认作为“第二数据库”。

它优先用于：

```text
Cache
Session
Rate Limit
Distributed Lock
Queue
Pub/Sub
Temporary State
```

Redis 官方数据类型覆盖 Strings、Lists、Sets、Sorted Sets、Streams、JSON 等，并可用于缓存、队列和事件处理。

默认原则：

```text
PostgreSQL/MySQL = Source of Truth

Redis = Performance / Temporary State
```

不要把重要业务数据只放 Redis。

---

# 25. ORM

Python：

```text
SQLAlchemy
```

Django：

```text
Django ORM
```

Go：

```text
GORM
sqlc
ent
```

选择：

```text
CRUD 项目
→ ORM

复杂 SQL / 性能敏感
→ SQL / sqlc

大型系统
→ ORM + 明确 SQL 边界
```

AI Coding 项目尤其需要避免：

```text
一个 Query 到处复制
```

数据库访问必须集中管理。

---

# 26. API 风格

默认：

```text
REST + JSON
```

适用于绝大多数业务系统。

推荐：

```text
/api/v1/users
/api/v1/orders
/api/v1/products
```

必须定义：

* HTTP method
* request schema
* response schema
* error schema
* pagination
* filtering
* sorting
* authentication
* authorization

---

# 27. GraphQL

适用于：

* 前端需要高度自由查询；
* 多数据源聚合；
* 移动端；
* API Gateway；
* 已经存在 GraphQL 生态。

不应该因为“GraphQL 更先进”就默认使用。

---

# 28. gRPC

适用于：

* 内部微服务；
* 高性能 RPC；
* 强类型服务间通信；
* 多语言服务。

不建议用于：

```text
普通 Web Browser → Backend
```

的默认通信方式。

通常：

```text
Browser → REST/JSON

Service → Service
    → gRPC
```

---

# 29. Message Queue

## RabbitMQ

适用于：

* 业务消息；
* 工作队列；
* 延迟任务；
* Routing；
* Event-driven Application。

---

## Kafka

适用于：

* 高吞吐事件流；
* 日志；
* 数据管道；
* Event Streaming；
* 大规模异步系统。

不要为了“异步”就自动使用 Kafka。

---

## Redis Queue

适用于：

* 中小型异步任务；
* 简单 Job；
* 已经使用 Redis 的系统。

---

# 30. 搜索

普通数据库查询：

```text
PostgreSQL/MySQL
```

复杂全文搜索：

```text
Elasticsearch / OpenSearch
```

如果只是：

```text
用户
订单
商品
```

不要引入 Elasticsearch。

---

# 31. Vector Database

AI/RAG 项目才考虑。

选择：

```text
PostgreSQL + pgvector
```

作为第一选择。

只有规模或功能要求明显超过 PostgreSQL 时，再考虑：

```text
Qdrant
Milvus
Weaviate
```

不要默认同时部署：

```text
PostgreSQL
+
Redis
+
Elasticsearch
+
Milvus
```

除非确实有对应需求。

---

# 32. Object Storage

文件、图片、视频、附件不要直接存数据库。

默认：

```text
S3 Compatible Object Storage
```

例如：

```text
AWS S3
MinIO
Cloudflare R2
阿里云 OSS
腾讯云 COS
```

数据库只保存：

```text
object_key
url
metadata
mime_type
size
```

---

# 33. Authentication

默认：

```text
Session / Cookie
```

适用于：

```text
传统 Web
后台
同域系统
```

API / Mobile / 多客户端：

```text
OAuth2 / OIDC
JWT
```

企业统一认证：

```text
OIDC
OAuth2
SSO
Keycloak / Auth0 / 云 IAM
```

不要自行实现密码加密、OAuth Server 等核心安全组件。

---

# 34. Authorization

不要把：

```text
if user.is_admin
```

散落在业务代码。

推荐：

```text
RBAC
+
Policy
```

例如：

```text
Role
 ├── Admin
 ├── Manager
 └── User

Permission
 ├── order.read
 ├── order.create
 ├── order.update
 └── order.delete
```

复杂系统可增加：

```text
ABAC
```

---

# 35. API Security

所有 API 默认考虑：

```text
Authentication
Authorization
Input Validation
Rate Limit
CORS
CSRF
SQL Injection
XSS
SSRF
File Upload Security
Secrets
Audit Log
```

Agent 不允许自行降低安全级别。

---

# 36. Configuration

统一：

```text
Environment Variables
+
Config Object
```

例如：

```text
DATABASE_URL
REDIS_URL
JWT_SECRET
S3_ENDPOINT
```

禁止：

```text
密码写入代码
API Key 写入 Git
生产配置提交仓库
```

---

# 37. Logging

默认：

```text
Structured JSON Logging
```

日志必须包含：

```text
timestamp
level
service
request_id
trace_id
user_id (if allowed)
message
error
```

禁止日志记录：

```text
password
token
secret
完整银行卡号
敏感个人信息
```

---

# 38. Observability

生产系统默认：

```text
Logs
+
Metrics
+
Tracing
```

推荐：

```text
OpenTelemetry
```

监控：

```text
Request Count
Latency
Error Rate
CPU
Memory
DB Connections
Queue Depth
Cache Hit Rate
```

---

# 39. Testing

默认测试金字塔：

```text
             E2E
            /   \
         Integration
        /           \
      Unit          Unit
```

推荐：

```text
Unit Test
Integration Test
API Test
E2E Test
```

AI Coding 项目尤其要求：

> 每一个 Requirement 至少对应一个验证方式。

---

# 40. Python Testing

默认：

```text
pytest
```

配合：

```text
pytest-asyncio
httpx
factory-boy
```

必要时：

```text
Hypothesis
```

---

# 41. Frontend Testing

默认：

```text
Vitest
+
Testing Library
+
Playwright
```

E2E：

```text
Playwright
```

---

# 42. Go Testing

优先：

```text
testing
```

必要时：

```text
testify
gomock
```

E2E / API：

```text
httptest
```

---

# 43. Java Testing

默认：

```text
JUnit 5
+
Mockito
+
Testcontainers
```

---

# 44. Container

默认：

```text
Docker
```

至少提供：

```text
Dockerfile
docker-compose.yml
```

本地开发建议：

```text
docker compose up
```

用于：

```text
PostgreSQL
Redis
RabbitMQ
MinIO
```

---

# 45. Kubernetes

不要默认 Kubernetes。

适用：

* 多服务；
* 大规模部署；
* 自动扩缩容；
* 多环境；
* 企业已有 Kubernetes 平台。

小项目：

```text
Docker
+
VM / Cloud Run / ECS / App Service
```

通常更简单。

---

# 46. CI/CD

默认：

```text
GitHub Actions
```

或企业已有：

```text
GitLab CI
Jenkins
Azure DevOps
```

Pipeline：

```text
Lint
 ↓
Type Check
 ↓
Unit Test
 ↓
Integration Test
 ↓
Build
 ↓
Security Scan
 ↓
Deploy
```

---

# 47. Python 项目工具链

推荐默认：

```text
Python
uv
FastAPI
Pydantic
SQLAlchemy
Alembic
pytest
Ruff
mypy / pyright
```

---

# 48. Go 项目工具链

推荐：

```text
Go
Go Modules
Gin / net/http
sqlc / GORM
golangci-lint
testing
Docker
```

---

# 49. Frontend Vue 工具链

推荐：

```text
Vue 3
TypeScript
Vite
Vue Router
Pinia
Vitest
Playwright
ESLint
Prettier
```

---

# 50. Frontend React 工具链

普通 SPA：

```text
React
TypeScript
Vite
React Router
TanStack Query
Vitest
Playwright
```

Full Stack：

```text
Next.js
TypeScript
App Router
```

Next.js 当前官方文档将 App Router 定义为基于文件系统的 Router，并使用 Server Components、Suspense 和 Server Functions 等 React 能力。

---

# 51. 前端状态管理

不要默认所有数据放全局 Store。

分类：

```text
Server State
    ↓
TanStack Query

UI State
    ↓
Local State

Global Client State
    ↓
Pinia / Zustand / Redux
```

原则：

> Server State 不应该复制成大量 Global State。

---

# 52. API Client

不要在每个组件中直接：

```text
fetch(...)
```

应该：

```text
API Client
    ↓
Service
    ↓
Component
```

推荐：

```text
OpenAPI
 ↓
Generated TypeScript Client
```

这样前后端可以共享 API Contract。

---

# 53. API Contract

推荐：

```text
OpenAPI 3.x
```

流程：

```text
Backend
 ↓
OpenAPI
 ↓
TypeScript Client
 ↓
Frontend
```

这样可以减少：

```text
Backend response
≠
Frontend expectation
```

---

# 54. Monorepo

适用于：

```text
frontend
backend
shared
packages
```

例如：

```text
apps/
├── web
├── api
└── worker

packages/
├── types
├── api-client
└── config
```

工具：

```text
pnpm workspace
Turborepo
Nx
```

不要为了两个目录就引入复杂 Monorepo 工具。

---

# 55. Repository Structure

## Python Backend

推荐：

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── main.py
├── tests/
├── migrations/
├── pyproject.toml
└── Dockerfile
```

---

# 56. Go Backend

推荐：

```text
backend/
├── cmd/
│   └── server/
├── internal/
│   ├── handler/
│   ├── service/
│   ├── repository/
│   ├── model/
│   └── middleware/
├── migrations/
├── tests/
├── go.mod
└── Dockerfile
```

---

# 57. Vue Frontend

推荐：

```text
frontend/
├── src/
│   ├── components/
│   ├── views/
│   ├── layouts/
│   ├── router/
│   ├── stores/
│   ├── services/
│   ├── api/
│   ├── types/
│   └── utils/
├── tests/
├── package.json
└── vite.config.ts
```

---

# 58. React Frontend

推荐：

```text
frontend/
├── src/
│   ├── components/
│   ├── features/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── api/
│   ├── types/
│   └── utils/
├── tests/
└── package.json
```

Feature-based architecture 优先于无限扩张的：

```text
components/
utils/
services/
```

---

# 59. 推荐的默认技术栈

当用户没有特别约束时，Agent 可以优先考虑以下组合。

## 企业 CRUD SaaS

```text
Frontend:
Vue 3 + TypeScript + Vite

Backend:
Python + FastAPI

Database:
PostgreSQL

Cache:
Redis

API:
REST + OpenAPI

ORM:
SQLAlchemy

Migration:
Alembic

Testing:
pytest + Vitest + Playwright

Deployment:
Docker

CI:
GitHub Actions

Architecture:
Modular Monolith
```

---

# 60. AI / RAG SaaS

```text
Frontend:
Next.js + TypeScript

Backend:
Python + FastAPI

Database:
PostgreSQL

Vector:
pgvector

Cache:
Redis

Object Storage:
S3

LLM:
Provider abstraction

Observability:
OpenTelemetry

Testing:
pytest + Playwright

Deployment:
Docker
```

---

# 61. 高并发 API

```text
Language:
Go

Framework:
Gin / net/http

Database:
PostgreSQL

Cache:
Redis

Communication:
REST / gRPC

Async:
Kafka / RabbitMQ

Testing:
Go testing

Deployment:
Docker

Architecture:
Modular Monolith → Microservices when justified
```

---

# 62. 企业 Java 系统

```text
Java / Kotlin
Spring Boot
Spring Security
PostgreSQL / MySQL
Redis
Kafka
JUnit 5
Testcontainers
Docker
Kubernetes (if required)
```

---

# 63. 小型内部工具

优先：

```text
Option A:

Next.js
+
PostgreSQL
```

或者：

```text
Option B:

FastAPI
+
Vue
+
PostgreSQL
```

不要默认：

```text
Microservices
Kafka
Kubernetes
Elasticsearch
Redis
```

---

# 64. MVP

默认：

```text
Monolith
+
PostgreSQL
+
简单 Cache（必要时）
+
Docker
```

避免：

```text
Microservices
Kafka
Kubernetes
Service Mesh
Event Sourcing
CQRS
```

除非需求明确要求。

---

# 65. 微服务决策

只有满足多个条件时才选择：

```text
Microservices
```

检查：

```text
[ ] 服务边界明确
[ ] 团队边界明确
[ ] 服务需要独立部署
[ ] 服务需要独立扩缩容
[ ] 服务需要独立故障隔离
[ ] 服务有不同技术栈需求
[ ] 单体已经成为实际瓶颈
```

如果多数为 No：

```text
Modular Monolith
```

---

# 66. Event-Driven Architecture

适用于：

```text
订单创建
    ↓
库存
    ↓
支付
    ↓
物流
    ↓
通知
```

如果业务天然存在：

```text
Event
```

可以采用：

```text
Domain Event
+
Message Broker
```

否则不要为了“架构先进”引入 Event Bus。

---

# 67. CQRS

默认关闭。

只有：

```text
读写模型差异非常大
复杂查询
高读写不对称
事件驱动
审计需求
```

时考虑。

---

# 68. Event Sourcing

默认关闭。

只有：

```text
完整历史状态
+
事件不可变
+
审计要求
+
状态可重建
```

时考虑。

---

# 69. DDD

DDD 不是默认技术架构，而是一种建模方法。

适用于：

```text
复杂业务
+
复杂领域模型
+
大量业务规则
```

简单 CRUD 不需要强行：

```text
Aggregate
Domain Event
Value Object
Repository
Domain Service
```

---

# 70. AI Coding 特殊要求

AI Coding 项目必须优先：

```text
Small Modules
Explicit Interfaces
Strong Types
Automated Tests
Deterministic Commands
Clear Directory Structure
Low Dependency Count
```

因为 Agent 最容易出问题的地方是：

```text
Implicit behavior
Huge files
Circular dependencies
Hidden global state
Magic configuration
Duplicated logic
```

---

# 71. Agent 不得自行做的决定

如果用户没有授权，Agent 不应该自行改变：

```text
Database
Architecture
Authentication
Deployment Platform
Cloud Provider
Message Broker
Public API
Programming Language
```

如果这些选择会产生长期成本，应先提出 Decision。

---

# 72. 技术选型评分模型

对于重要技术选型，Agent 可以使用：

```text
Score =
Business Fit
+
Team Fit
+
Operational Fit
+
AI Coding Fit
+
Ecosystem
+
Performance
+
Maintainability
-
Complexity
-
Operational Cost
-
Migration Cost
```

不要简单按照：

```text
GitHub Stars
+
流行程度
```

进行选择。

---

# 73. 技术选择必须记录理由

例如：

```text
Decision: PostgreSQL

Why:
1. Relational business model
2. Transaction requirements
3. Complex querying
4. JSONB requirement
5. Strong ecosystem

Alternatives:
MySQL

Rejected because:
No specific requirement favors MySQL
and PostgreSQL provides better fit for the expected data model.
```

---

# 74. Agent 技术选型规则

Agent 应遵循：

```text
Existing Project?
    │
    ├── Yes → Preserve existing stack unless migration is explicitly requested
    │
    └── No
         │
         ▼
      Requirements
         │
         ▼
      Architecture
         │
         ▼
      Technology Decision
```

**存量项目：兼容性优先。**

**新项目：需求适配优先。**

---

# 75. Existing Project 特殊规则

如果是存量项目：

禁止：

```text
为了更现代而升级整个项目
```

必须先分析：

```text
Language
Framework
Database
Dependencies
Architecture
Tests
Deployment
CI/CD
```

然后：

```text
Preserve
or
Migrate
```

所有 Migration 必须成为独立 Decision。

---

# 76. Agent 生成 spec.md 时必须包含的架构上下文

`spec.md` 主要描述：

```text
1. Problem
2. Goal
3. Users
4. User Stories
5. Functional Requirements
6. Non-functional Requirements
7. Constraints
8. Acceptance Scenarios
9. Out of Scope
10. Assumptions
```

不要把大量 implementation detail 放到需求 Spec 中。

---

# 77. plan.md 必须包含

```text
1. Architecture
2. Technology Stack
3. Project Structure
4. Database
5. API
6. Authentication
7. Authorization
8. Cache
9. Async Processing
10. External Integrations
11. Testing
12. Observability
13. Deployment
14. Security
15. Migration
16. Risks
17. Alternatives
```

---

# 78. 推荐的 SDD Artifact

```text
specs/
└── 001-order-management/
    ├── spec.md
    ├── plan.md
    ├── tasks.md
    ├── research.md
    ├── data-model.md
    ├── api-contract.md
    ├── architecture.md
    └── adr/
        ├── ADR-001-database.md
        ├── ADR-002-cache.md
        └── ADR-003-architecture.md
```

对于大型 Feature，可以拆成多个 Spec。Spec Kit 当前也提供 “spec of specs” 模式，用 roadmap 将大型功能拆成相互独立、可追踪的子 Spec。

---

# 79. 推荐的 spec.md 模板

```markdown
# Specification: [Feature Name]

## 1. Overview

### Problem

### Goal

### Non-Goals

### Users

---

## 2. Context

### Existing System

### Business Context

### Constraints

---

## 3. User Stories

### US-001

As a ...

I want ...

So that ...

---

## 4. Functional Requirements

### FR-001

The system SHALL ...

#### Scenario: ...

- GIVEN ...
- WHEN ...
- THEN ...

---

## 5. Non-Functional Requirements

### Performance

### Security

### Availability

### Scalability

### Observability

---

## 6. Data Requirements

### Entities

### Relationships

### Constraints

---

## 7. API Requirements

### Endpoint

### Request

### Response

### Error

---

## 8. Integration Requirements

### External Services

### Authentication

### Retry

### Timeout

---

## 9. Architecture Constraints

- Must use ...
- Must not use ...
- Must remain compatible with ...
- Must support ...

---

## 10. Acceptance Criteria

- [ ] AC-001
- [ ] AC-002

---

## 11. Assumptions

---

## 12. Open Questions

---

## 13. Out of Scope

---

## 14. Traceability

| Requirement | Design | Task | Test |
|---|---|---|---|
| FR-001 | D-001 | T-001 | TEST-001 |
```

---

# 80. 推荐的 plan.md 技术架构模板

````markdown
# Implementation Plan

## 1. Architecture

### Architecture Style

### Component Diagram

### Data Flow

---

## 2. Technology Stack

### Language

### Backend Framework

### Frontend Framework

### Database

### Cache

### Message Queue

### Search

### Object Storage

---

## 3. Project Structure

```text
...
````

---

## 4. Backend Design

### Modules

### Services

### Repositories

### Middleware

---

## 5. Frontend Design

### Pages

### Components

### State Management

### API Client

---

## 6. Database

### Tables

### Indexes

### Constraints

### Migration Strategy

---

## 7. API

### REST / GraphQL / gRPC

### Authentication

### Authorization

### Error Model

---

## 8. Async Processing

### Jobs

### Queue

### Retry

### Idempotency

---

## 9. Cache

### Cache Keys

### TTL

### Invalidation

---

## 10. Security

---

## 11. Testing

---

## 12. Observability

---

## 13. Deployment

---

## 14. Architecture Decisions

### ADR-001

Decision:

Reason:

Alternatives:

---

## 15. Risks

---

## 16. Migration

---

# 81. Agent 生成项目 Spec 的最终规则

当用户只给出一句：

> “开发一个 xxx 系统”

Agent 不得直接开始编码。

必须执行：

```text
Step 1
Understand Requirements

Step 2
Classify Project

Step 3
Determine Scale

Step 4
Determine Architecture

Step 5
Select Language

Step 6
Select Backend

Step 7
Select Frontend

Step 8
Select Database

Step 9
Determine Cache

Step 10
Determine Async

Step 11
Determine Storage

Step 12
Determine Authentication

Step 13
Determine Observability

Step 14
Determine Testing

Step 15
Determine Deployment

Step 16
Record Architecture Decisions

Step 17
Generate spec.md

Step 18
Generate plan.md

Step 19
Generate tasks.md
```

---

# 82. 技术栈选择的默认优先级

## 普通企业 Web SaaS

```text
Vue 3
+
TypeScript
+
Vite
+
FastAPI
+
PostgreSQL
+
Redis
+
Docker
```

---

## React SaaS

```text
Next.js
+
TypeScript
+
PostgreSQL
+
Redis (if needed)
```

---

## AI Application

```text
Next.js
+
FastAPI
+
PostgreSQL
+
pgvector
+
Redis
+
S3
```

---

## 高并发 Backend

```text
Go
+
Gin/net/http
+
PostgreSQL
+
Redis
```

---

## 企业 Java

```text
Spring Boot
+
PostgreSQL/MySQL
+
Redis
+
Kafka (if required)
```

---

# 83. 默认不要使用的复杂技术

除非需求证明必要，否则不要默认引入：

```text
Kubernetes
Kafka
Elasticsearch
Service Mesh
CQRS
Event Sourcing
Microservices
GraphQL
gRPC
Vector Database
Multiple Databases
Multiple Cache Systems
```

原则：

> **Every infrastructure component must have a documented reason to exist.**

---

# 84. AI Agent 的最终输出格式

当 Agent 完成架构设计后，应首先输出：

```text
Architecture Summary

Project Type:
...

Architecture:
...

Language:
...

Backend:
...

Frontend:
...

Database:
...

Cache:
...

Message Queue:
...

Storage:
...

Authentication:
...

Testing:
...

Deployment:
...

Key Decisions:
...

Alternatives Considered:
...
```

然后再生成：

```text
spec.md
plan.md
tasks.md
```

---

# 85. 最重要的规则

### Rule 1

> 不要因为技术流行而选择技术。

### Rule 2

> 不要为了未来可能存在的需求增加架构复杂度。

### Rule 3

> 存量项目优先保持已有技术栈。

### Rule 4

> 新项目优先 Modular Monolith。

### Rule 5

> PostgreSQL 是新关系型项目的默认候选。

### Rule 6

> Redis 不是默认数据库，只在 Cache / Session / Queue / Lock 等场景使用。

### Rule 7

> REST 是默认 API 风格。

### Rule 8

> TypeScript 是新 Web Frontend 的默认语言。

### Rule 9

> Python 优先 AI / Data / CRUD / API；Go 优先高并发 / Infrastructure / Network。

### Rule 10

> 技术选型必须记录理由。

### Rule 11

> Architecture Decision 必须能够追溯到 Requirements。

### Rule 12

> Requirement 必须能够追溯到 Test。

### Rule 13

> Code 必须能够追溯到 Spec。

### Rule 14

> 不允许 AI 在没有证据的情况下自行改变核心架构。

### Rule 15

> 当存在多个合理方案时，不要假装只有一个正确答案，应列出 Alternatives 和 Trade-offs。

---

# 86. 最终 SDD Traceability

整个项目应该形成：

```text
                    Business Goal
                         │
                         ▼
                   Requirement
                         │
                         ▼
                     Scenario
                         │
                         ▼
                 Architecture Decision
                         │
                         ▼
                       Design
                         │
                         ▼
                       Task
                         │
                         ▼
                        Code
                         │
                         ▼
                       Test
                         │
                         ▼
                     Verification
```

最终形成：

```text
Requirement
     │
     ├──── Design
     │
     ├──── Task
     │
     ├──── Code
     │
     └──── Test
```

任何一个节点都应该能够向前和向后追踪。

---

# 87. 给 AI Agent 的总指令

在执行 SDD 时，遵循以下原则：

```text
You are an architecture-aware software engineering agent.

Do not start implementation immediately.

First understand the business requirements.

Then classify the project and determine:
- application type
- expected scale
- users
- concurrency
- data characteristics
- security requirements
- deployment environment
- team constraints
- integration requirements

Use the architecture knowledge base to select an appropriate:
- programming language
- backend framework
- frontend framework
- database
- cache
- message broker
- object storage
- search engine
- authentication mechanism
- authorization model
- testing framework
- observability stack
- deployment strategy

Prefer the simplest architecture that satisfies the requirements.

Prefer modular monolith over microservices unless microservices are justified.

Prefer PostgreSQL for new relational applications unless a specific requirement favors another database.

Prefer Redis only when caching, sessions, rate limiting, distributed locking, queues, or temporary state are actually required.

Prefer REST/JSON unless GraphQL or gRPC provides a clear benefit.

Prefer TypeScript for new web frontends.

Prefer Python for AI, data processing, automation, and general-purpose API applications.

Prefer Go for high-concurrency services, infrastructure, networking, and performance-sensitive backends.

For existing projects, preserve the existing technology stack unless migration is explicitly requested or the existing stack creates a demonstrated problem.

Do not introduce infrastructure components without documenting why they are required.

For every significant architecture decision:
1. state the decision;
2. state the reason;
3. list alternatives;
4. state why alternatives were not selected;
5. record constraints and risks.

Keep requirements separate from implementation details.

The specification should describe WHAT and WHY.

The implementation plan should describe HOW.

Tasks should be concrete, dependency-aware, and traceable to requirements.

Every requirement must have an acceptance scenario.

Every important requirement should have at least one automated verification strategy.

Before implementation, verify consistency between:
spec.md
plan.md
tasks.md

After implementation, verify:
requirements → design → tasks → code → tests

If requirements are ambiguous, ask questions or explicitly record assumptions.

Never silently invent important business rules.

Never silently change architecture.

Never optimize for popularity.

Optimize for:
correctness,
simplicity,
maintainability,
testability,
operability,
security,
and appropriate scalability.
```

---

# 88. 与 Spec Kit / OpenSpec 的结合方式

这份知识库最好不要直接替代 SDD 工具，而应该作为：

```text
Architecture Knowledge Base
```

放在 SDD 的 **Plan / Architecture Decision** 阶段。

Spec Kit 当前的核心流程就是：

```text
Constitution
→ Specify
→ Clarify
→ Plan
→ Tasks
→ Analyze
→ Implement
→ Converge
```

并且官方明确把技术栈、架构和技术约束放在 Plan 阶段，而不是让 Specify 阶段过早决定实现方式。

因此最理想的 Agent workflow 是：

```text
                User
                  │
                  ▼
        /speckit-specify
                  │
                  ▼
              spec.md
        WHAT / WHY / ACCEPTANCE
                  │
                  ▼
        Architecture KB
              ▲
              │
              ▼
          /speckit-plan
                  │
                  ▼
              plan.md
        HOW / TECH STACK / DESIGN
                  │
                  ▼
          /speckit-tasks
                  │
                  ▼
              tasks.md
                  │
                  ▼
        /speckit-implement
                  │
                  ▼
                 Code
                  │
                  ▼
        /speckit-converge
```

这比把“Python + FastAPI + PostgreSQL + Vue”硬编码进 `spec.md` 更合理。

---

# 89. 推荐最终目录

如果你准备真正把这套东西用于 Claude / Cursor / Codex，我建议不要只保存成一个超大的 Markdown，而是最终整理成：

```text
ai-architecture-kb/
│
├── README.md
│
├── principles.md
│
├── decision-tree.md
│
├── languages/
│   ├── python.md
│   ├── go.md
│   ├── typescript.md
│   ├── java.md
│   └── rust.md
│
├── backend/
│   ├── fastapi.md
│   ├── flask.md
│   ├── django.md
│   ├── gin.md
│   ├── spring-boot.md
│   └── nextjs.md
│
├── frontend/
│   ├── vue.md
│   ├── react.md
│   ├── nextjs.md
│   └── angular.md
│
├── database/
│   ├── postgresql.md
│   ├── mysql.md
│   ├── sqlite.md
│   └── redis.md
│
├── infrastructure/
│   ├── docker.md
│   ├── kubernetes.md
│   ├── kafka.md
│   ├── rabbitmq.md
│   └── s3.md
│
├── architecture/
│   ├── monolith.md
│   ├── modular-monolith.md
│   ├── microservices.md
│   ├── event-driven.md
│   ├── cqrs.md
│   └── ddd.md
│
├── testing/
│   ├── python.md
│   ├── go.md
│   ├── frontend.md
│   └── e2e.md
│
├── security/
│   ├── authentication.md
│   ├── authorization.md
│   └── api-security.md
│
└── templates/
    ├── spec.md
    ├── plan.md
    ├── tasks.md
    └── adr.md
```

然后让 Agent 的项目初始化流程变成：

```text
User Requirement
       │
       ▼
Architecture KB
       │
       ▼
Decision Tree
       │
       ▼
Architecture Proposal
       │
       ▼
Human Confirmation
       │
       ▼
spec.md
       │
       ▼
plan.md
       │
       ▼
tasks.md
       │
       ▼
AI Coding
```

**这一步非常重要：不要让 Agent 直接从这份知识库“自动选技术并开干”。最好增加一个 `Architecture Proposal → Human Confirmation` 门槛。** 对技术栈这种会产生长期锁定成本的决定，人应该确认；一旦确认，就把选择固化进 `plan.md` 和 ADR，后续 Agent 默认不得擅自改变。

目前 Spec Kit 也采用类似的“先形成 artifact、再进入后续阶段”的思路，并提供 `analyze` 做 `spec.md / plan.md / tasks.md` 的一致性检查，以及 `converge` 检查实现是否满足 Spec。

另外，这份知识库最好**版本化**。例如：

```text
architecture-kb/
  v1.0/
  v1.1/
  v2.0/
```

因为框架会快速变化；例如 React 官方已经明确 Create React App 已 deprecated，Next.js 当前推荐 App Router，而 Vue 官方仍以 Vue 3 + TypeScript + Vite 为主流项目路径。

如果你下一步要把它真正用于 **Claude / Cursor / Codex**，我建议再进一步做成 **“Architecture Decision Matrix v1.0”**：把上面几十项技术整理成约 **100～150 个具体决策项**，每项包含 **选择条件、默认值、反例、优先级、依赖关系、Agent 提问项、推荐组合**，然后直接生成一份可以放到 `CLAUDE.md / AGENTS.md / .cursor/rules / Codex instructions` 中使用的版本。这样会比单纯的技术栈百科更适合实际 SDD。
