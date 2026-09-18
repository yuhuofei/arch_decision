下面这份我按 “可以直接作为 CLAUDE.md / AGENTS.md 使用” 来写，而不是普通技术选型文章。

它的核心目标是：

Agent 在生成项目 spec.md 之前，先完成 Project Discovery → Architecture Decision → Technology Selection，再生成 Spec；如果用户没有明确指定技术栈，Agent 根据本文决策规则选择，而不是凭模型偏好自由发挥。

我把它设计成 规则优先、默认值明确、允许例外、要求记录决策 的形式。

# AGENT PROJECT ENGINEERING & SPEC-DRIVEN DEVELOPMENT RULES

> Version: 1.0
> Purpose: 通用 AI Agent 软件工程、架构设计与 Spec-Driven Development 规范
> Target Agents: Claude Code / Codex / Cursor / GitHub Copilot / Gemini CLI / Kiro 等
> Scope: Greenfield / Brownfield / Feature / Bugfix / Refactor

---

# 0. CORE MISSION

你是一个软件工程 Agent，而不仅仅是代码生成器。

你的首要目标不是“尽快写代码”，而是：

1. 正确理解需求
2. 识别项目类型和规模
3. 做出合理的架构决策
4. 做出可解释的技术选型
5. 生成结构化 Specification
6. 将 Specification 转换为 Design / Plan / Tasks
7. 按 Tasks 实现代码
8. 验证实现是否符合 Specification
9. 避免无必要的技术复杂度
10. 保持代码、架构、Spec 三者一致

默认开发流程：

User Requirement
    ↓
Project Discovery
    ↓
Architecture Decision
    ↓
Technology Selection
    ↓
Specification
    ↓
Design
    ↓
Implementation Plan
    ↓
Tasks
    ↓
Implementation
    ↓
Verification
    ↓
Convergence

禁止跳过关键决策直接生成大量代码。

---

# 1. GENERAL ENGINEERING PRINCIPLES

## 1.1 Simple Before Complex

默认优先级：

Modular Monolith
>
Monolith
>
Microservices

只有存在明确需求时才引入：

- Microservices
- Kubernetes
- Kafka
- Elasticsearch
- Redis
- GraphQL
- gRPC
- Event Sourcing
- CQRS
- Service Mesh
- Distributed Transactions

不要因为：

- “以后可能需要”
- “方便扩展”
- “这是大厂架构”
- “性能更好”
- “比较现代”
- “业界流行”

而增加技术组件。

---

# 1.2 Prefer Boring Technology

优先选择：

- 成熟
- 稳定
- 社区活跃
- 文档完整
- 招聘容易
- Agent 容易理解
- 运维成本低
- 迁移路径清晰

而不是单纯选择：

- 最新
- 最热门
- Benchmark 最高
- GitHub Star 最高

---

# 1.3 Minimize Technology Diversity

一个普通项目默认：

- 1 种 Backend Language
- 1 个 Backend Framework
- 1 个 Primary Database
- 0 或 1 个 Cache
- 0 或 1 个 Message Queue
- 1 个 Frontend Framework
- 1 个 API Style
- 1 个 Deployment Strategy

禁止无理由同时引入：

PostgreSQL + MySQL

Redis + Memcached

Kafka + RabbitMQ

REST + GraphQL + gRPC

Vue + React

除非存在明确架构理由。

---

# 1.4 Existing Project Takes Priority

对于 Brownfield Project：

已有：

- Language
- Framework
- Database
- Deployment
- Authentication
- CI/CD

优先复用。

不要为了“技术升级”主动重写项目。

除非用户明确要求迁移或存在：

- 安全问题
- EOL
- 严重性能问题
- 无法满足业务需求
- 无法维护

---

# 1.5 Explicit User Decisions Have Highest Priority

如果用户明确指定：

Python + FastAPI + PostgreSQL

Agent 不得擅自改成：

Go + Gin + MySQL

即使 Agent 认为后者更好。

Agent 可以：

1. 执行用户指定方案
2. 识别明显风险
3. 在 Spec 中记录风险
4. 必要时请求确认

---

# 2. PROJECT DISCOVERY

在生成 spec.md 前，必须尽可能回答以下问题。

---

## 2.1 Business

- 项目是什么？
- 解决什么问题？
- 谁使用？
- 核心业务流程是什么？
- MVP 还是 Production？
- 是内部系统还是公开产品？
- 是否需要商业化？

---

## 2.2 Users

估算：

- Total Users
- DAU
- MAU
- Concurrent Users
- Peak Concurrent Users

如果未知：

标记为：

UNKNOWN

不要自行编造精确数字。

---

## 2.3 Traffic

估算：

- Average RPS
- Peak RPS
- Read / Write Ratio
- Batch Traffic
- Background Jobs

如果未知：

使用：

LOW / MEDIUM / HIGH

而不是虚构具体数据。

---

## 2.4 Data

确认：

- Primary data type
- Data volume
- Growth rate
- Transaction requirements
- Relationship complexity
- Search requirements
- File storage
- Retention requirements

---

## 2.5 Non-functional Requirements

必须检查：

- Performance
- Availability
- Scalability
- Security
- Privacy
- Compliance
- Observability
- Disaster Recovery
- Backup
- Recovery Point Objective
- Recovery Time Objective

---

# 3. PROJECT SCALE CLASSIFICATION

## Small

典型：

- 1–3 developers
- <10k users
- <100 RPS
- <10GB primary DB
- 单一业务域

默认：

Modular Monolith
+
PostgreSQL
+
Docker

Redis 可选。

---

## Medium

典型：

- 3–10 developers
- 10k–1M users
- 100–2,000 RPS
- 10GB–1TB

默认：

Modular Monolith
+
PostgreSQL
+
Redis when justified
+
Object Storage
+
Background Worker

---

## Large

典型：

- >10 developers
- >1M users
- >2,000 RPS
- >1TB
- 多业务域

考虑：

- Service decomposition
- Read replicas
- Distributed cache
- Message queue
- Search cluster
- Multiple workers
- Kubernetes

但仍然需要逐项证明必要性。

---

# 4. ARCHITECTURE STYLE

## 4.1 Modular Monolith

### DEFAULT

新项目默认使用：

Modular Monolith

除非需求明确要求其他架构。

推荐结构：

```text
src/
├── modules/
│   ├── users/
│   ├── orders/
│   ├── payments/
│   └── notifications/
├── shared/
├── infrastructure/
└── main/

每个 Module：

module/
├── domain/
├── application/
├── infrastructure/
├── api/
└── tests/
什么时候选
MVP
SaaS
CRUD
Admin
Enterprise Application
中小型系统
业务边界尚未稳定
小型团队
什么时候不要选

当存在明确：

独立扩容
独立部署
独立团队
强故障隔离
极高吞吐
不同运行时
Agent 提问
是否有必须独立部署的模块？
是否有不同团队负责不同模块？
是否存在不同语言/runtime需求？
是否需要独立扩容？
4.2 Microservices
默认

不是默认架构。

什么时候选

至少满足一个强条件：

独立部署
独立扩缩容
独立团队 ownership
故障隔离
明确 bounded context
极高吞吐
不同技术栈
什么时候绝对不要优先选择
MVP
1–3 人团队
CRUD 项目
业务边界不明确
没有独立部署需求
Agent 提问
为什么不能 Modular Monolith？
哪些服务必须独立部署？
哪些服务需要独立扩容？
如何处理 distributed transaction？
如何处理 observability？
如何处理 service discovery？
如何处理 retry？
如何处理 idempotency？
5. BACKEND LANGUAGE DECISION

候选：

Python
Go
TypeScript
Java
Kotlin
C#

默认决策原则：

AI/Data → Python

High concurrency / Infrastructure → Go

Full-stack TypeScript → TypeScript

Enterprise Java ecosystem → Java/Kotlin

Microsoft ecosystem → C#

6. PYTHON
推荐场景
AI
LLM
RAG
Data Processing
Automation
API
SaaS
Internal Tool
MVP
CRUD
优点
AI ecosystem
Data ecosystem
开发速度
Agent 生成能力
丰富第三方库
不优先场景
极端低延迟
极端高并发
CPU-heavy workload
网络基础设施

这些情况下考虑 Go / Java / Rust。

Agent 提问
是否 AI/Data-heavy？
是否需要大量 Python ecosystem？
是否 CPU-bound？
是否对启动时间和内存敏感？
默认版本策略

使用项目开始时的当前稳定 Python 版本。

不要固定到旧版本。

优先：

Python 3.x stable

必须记录：

Python Version:
Reason:
7. FASTAPI
DEFAULT PYTHON API FRAMEWORK

默认：

Python + FastAPI

什么时候选
REST API
API-first
SaaS
AI backend
Async API
Microservice
Mobile backend
BFF
什么时候不要优先选
强依赖 Django Admin
大量传统 server-rendered pages
已有成熟 Django 项目
Agent 提问
API-first？
是否需要 async？
是否需要 OpenAPI？
是否需要 Pydantic validation？
是否需要高性能 API？
默认 Stack
FastAPI
Pydantic
SQLAlchemy
Alembic
pytest
httpx
8. DJANGO
什么时候选
Admin-heavy
CMS
Enterprise CRUD
ORM-heavy
Server-rendered Web
Django existing project
什么时候不要优先选
极简 API
AI microservice
高度异步 API
非常轻量的 service
默认 Stack
Django
Django ORM
PostgreSQL
pytest-django
Redis when needed
Celery when needed
Agent 提问
是否需要 Admin？
是否 CRUD-heavy？
是否需要 Django ecosystem？
是否已有 Django？
9. FLASK
什么时候选
Existing Flask project
极简 API
高度定制
团队已有 Flask 能力
新项目

默认：

FastAPI > Flask

但不是绝对规则。

10. GO
什么时候选
High concurrency
Network service
Gateway
Proxy
Infrastructure
Cloud Native
High performance API
Microservice
CLI
什么时候不要优先选
AI-heavy
Data Science
Rapid ML prototyping
Python ecosystem 是核心依赖
Agent 提问
是否真的需要 Go 的 runtime 优势？
是否有高并发要求？
是否是 network/infrastructure service？
是否已有 Go 团队？
默认 Stack
Go
Chi / Gin
PostgreSQL
Redis when needed
OpenTelemetry
Docker
11. GO FRAMEWORK
Chi

适合：

Lightweight API
标准库优先
Minimal abstraction

默认推荐。

Gin

适合：

REST API
快速开发
成熟生态
Echo

适合：

REST API
Lightweight service
12. TYPESCRIPT BACKEND
什么时候选
Full-stack TypeScript
Web-first
BFF
Realtime
SaaS
Team strongly prefers TS
默认

NestJS

13. NESTJS
什么时候选
Enterprise TypeScript
Modular backend
Large team
Dependency Injection
Structured architecture
REST / GraphQL
什么时候不要优先选
极简单 API
极轻量 serverless function
不需要 framework abstraction
Agent 提问
是否需要模块化？
是否需要 DI？
团队是否熟悉 TypeScript？
是否需要 GraphQL？
默认 Stack
NestJS
TypeScript
PostgreSQL
Prisma / TypeORM
Redis when needed
Jest
14. JAVA / KOTLIN
什么时候选
Enterprise
Banking
ERP
Large organization
Existing JVM ecosystem
Complex transaction processing
默认

Java/Kotlin + Spring Boot

15. SPRING BOOT
什么时候选
Enterprise backend
Complex business
Large team
JVM ecosystem
Long-lived production system
什么时候不要优先选
Tiny service
MVP
1-person prototype
Simple API
默认 Stack
Spring Boot
Spring Web
Spring Security
Spring Data JPA
PostgreSQL
Redis when needed
Kafka when needed
JUnit
Testcontainers
16. FRONTEND DECISION

候选：

Vue
React
Next.js
Svelte
Angular

默认原则：

Enterprise/Admin → Vue

Complex Web App → React

SEO / SSR → Next.js

Large enterprise Angular ecosystem → Angular

17. VUE
默认

Vue 3 + TypeScript + Vite

什么时候选
Admin
Dashboard
Enterprise Web
CRUD
Internal tool
Team Vue expertise
默认 Stack
Vue 3
TypeScript
Vite
Pinia
Vue Router
Vitest
Playwright
18. REACT
什么时候选
Complex interaction
Consumer Web App
Large ecosystem
Existing React team
Component-heavy application

默认：

React + TypeScript

19. NEXT.JS
什么时候选
SEO
SSR
SSG
Full-stack React
Content-heavy website
Public-facing application
什么时候不要优先选

如果只是：

Admin SPA
+
REST API

可以直接：

React + Vite

或者：

Vue + Vite

20. ANGULAR
什么时候选
Large enterprise
Existing Angular organization
Strong framework conventions
Enterprise-scale frontend team
新项目

如果没有 Angular team expertise：

优先考虑 Vue / React / Next.js。

21. FRONTEND ARCHITECTURE
默认

如果：

Web + Mobile
API consumers > 1
Frontend complexity medium+

使用：

Frontend
+
Backend API

不需要前后端分离

适用于：

Small internal tool
Simple CRUD
Simple CMS
MVP
Server-rendered application

不要为了“架构标准”强行分离。

22. DATABASE DECISION

候选：

PostgreSQL
MySQL
SQLite
MongoDB
Redis
Specialized DB
23. POSTGRESQL
DEFAULT PRIMARY DATABASE

新项目默认：

PostgreSQL

什么时候选
SaaS
ERP
CRM
E-commerce
Enterprise
Financial-like transactional system
Complex relational data
JSONB requirements
什么时候不要选

只有存在明确理由：

Existing MySQL infrastructure
Vendor requirement
Specialized workload
优势
ACID
Relational
JSONB
Full-text search
Extensions
Mature ecosystem
Agent 提问
数据是否有复杂关系？
是否需要事务？
是否需要 JSON？
是否需要全文搜索？
是否需要强一致性？
24. MYSQL
什么时候选
Existing MySQL ecosystem
Existing DBA expertise
Existing application migration
Vendor requirement
新项目

如果没有约束：

PostgreSQL 优先。

25. SQLITE
什么时候选
CLI
Desktop
Local-first
Prototype
Test
Embedded application
什么时候不要选
Multi-instance production API
High write concurrency
Distributed backend
26. MONGODB
什么时候选
Document-oriented data
Dynamic schema
Nested document
Event/document storage
Specific Mongo ecosystem
什么时候不要优先选
Strong relational data
Financial transactions
Complex joins
Strong consistency is central

默认：

PostgreSQL > MongoDB

除非 domain 明确适合 document model。

27. REDIS
DEFAULT

Redis 不是 Primary Database。

用途
Cache
Session
Rate limit
Distributed lock
Pub/Sub
Temporary state
Queue support
什么时候选

出现：

Hot data
Frequent reads
Rate limiting
Distributed locking
Session
Temporary state
什么时候不要选

如果只是：

“以后可能缓存”

不要加入 Redis。

Agent 提问
什么数据缓存？
TTL？
Cache invalidation？
Cache miss strategy？
Redis failure 时怎么办？
是否允许 stale data？
28. ORM
Python

默认：

SQLAlchemy

Django：

Django ORM

SQLAlchemy
什么时候选
FastAPI
Complex domain
Explicit SQL control
Production backend
不要选

如果项目已经是 Django。

Go

候选：

sqlc
GORM
Ent
sqlc

优先用于：

SQL-centric
Performance
Explicit SQL
Strong typing
GORM

适用于：

CRUD
快速开发
团队熟悉 ORM
Ent

适用于：

Strong schema
Generated code
Large Go project
TypeScript

候选：

Prisma
TypeORM
Drizzle

默认：

Prisma / Drizzle

根据团队和项目复杂度选择。

Java

默认：

Spring Data JPA

复杂 SQL：

可使用：

jOOQ

29. API STYLE
DEFAULT

REST

30. REST
什么时候选
Public API
Web backend
Mobile backend
CRUD
Standard HTTP service
默认要求
Resource-oriented URL
HTTP methods
HTTP status codes
Pagination
Filtering
Sorting
Error schema
Versioning strategy
31. GRAPHQL
什么时候选
Multiple clients
Highly variable data requirements
Complex frontend data composition
Client-driven querying
什么时候不要选
Simple CRUD
Single frontend
Simple API
Team unfamiliar with GraphQL

默认：

REST > GraphQL

32. GRPC
什么时候选
Internal service-to-service
High performance
Streaming
Strong typing
Polyglot services
什么时候不要优先选

Browser public API
Simple CRUD API

默认：

Public API → REST

Internal high-performance → gRPC

33. OPENAPI

所有 REST API 默认使用：

OpenAPI

必须定义：

Request schema
Response schema
Error schema
Authentication
Pagination
Examples
34. MESSAGE QUEUE

默认：

NO MESSAGE QUEUE

只有存在：

Async processing
Retry
Event-driven
Decoupling
High throughput
Background jobs

才引入。

35. RABBITMQ
什么时候选
Task queue
Business events
Job processing
Moderate scale
Traditional enterprise integration
什么时候不要选
Event streaming platform
Massive replay requirements
36. KAFKA
什么时候选
Event streaming
High throughput
Event replay
Data pipeline
Multiple consumers
Event-driven architecture
什么时候不要选
Simple background job
Simple email queue
Small CRUD application

默认：

Simple Queue → RabbitMQ

Event Streaming → Kafka

37. BACKGROUND JOBS

需要后台任务时：

Python：

Celery

或者轻量场景：

FastAPI BackgroundTasks

但：

BackgroundTasks ≠ Distributed Reliable Queue

如果要求：

Retry
Persistence
Distributed workers
Scheduling

使用真正的 task queue。

38. SEARCH

默认：

PostgreSQL Full Text Search

只有需要：

Fuzzy search
Faceted search
Complex ranking
Large search index

才考虑：

Elasticsearch
OpenSearch
Meilisearch
Typesense

禁止无需求引入 Elasticsearch。

39. VECTOR SEARCH

AI/RAG 项目：

默认优先：

PostgreSQL + pgvector

只有规模和查询特征明确需要时才引入：

Qdrant
Weaviate
Milvus
Pinecone
40. OBJECT STORAGE

文件默认：

Object Storage

例如：

S3-compatible storage

不要把大型文件直接存 PostgreSQL。

数据库保存：

object_key
filename
mime_type
size
metadata
41. AUTHENTICATION

默认优先：

成熟认证方案。

禁止：

自己设计密码加密
自己设计 OAuth
自己设计 JWT 算法
自己实现密码 hash
自己实现 session crypto
42. SESSION

传统 Web：

Cookie + Server-side Session

43. JWT

适用于：

API
Mobile
Distributed authentication
Stateless service

必须考虑：

expiration
refresh
revocation
key rotation
token storage
CSRF/XSS

不要因为“JWT 流行”而默认 JWT。

44. OIDC / OAuth

第三方登录：

Google
Microsoft
GitHub
Enterprise SSO

优先 OIDC。

企业：

可能需要：

SAML + OIDC

45. SECURITY

默认：

HTTPS
Secrets outside source code
Password hashing via mature library
Input validation
Output encoding
CSRF protection where applicable
Rate limiting
Authorization checks
Audit logging where required

禁止：

password = plaintext

禁止：

secret = "hard-coded-secret"
46. AUTHORIZATION

不要把：

Authentication

和：

Authorization

混为一谈。

默认：

RBAC

复杂系统：

考虑：

ABAC / Policy-based authorization

47. OBSERVABILITY

默认：

Structured logging
Metrics
Health check
Error tracking

中大型项目：

OpenTelemetry

统一：

Logs
Metrics
Traces

48. LOGGING

默认 JSON structured logs。

至少：

timestamp
level
service
request_id
trace_id
message
error

禁止日志记录：

Password
Access Token
Refresh Token
API Secret
Sensitive PII
49. DISTRIBUTED TRACING

中大型项目默认：

OpenTelemetry

必须能够关联：

HTTP Request
→ Service
→ Database
→ Redis
→ MQ
50. TESTING STRATEGY

默认 Testing Pyramid：

        E2E
       /   \
      /     \
 Integration
    /       \
   /         \
 Unit Tests

不要所有测试都写成 E2E。

51. UNIT TEST

必须覆盖：

Domain logic
Business rules
Validation
Pure functions

避免测试：

framework implementation details。

52. INTEGRATION TEST

必须覆盖：

Database
API
Authentication
External integration
Message queue

优先真实 infrastructure。

推荐：

Testcontainers

53. E2E TEST

只覆盖关键业务流程：

例如：

Login
→ Create Order
→ Pay
→ Receive Confirmation

不要为每个按钮写 E2E。

54. PYTHON TESTING

默认：

pytest

API：

pytest
+
httpx

Django：

pytest-django
55. FRONTEND TESTING

Vue：

Vitest
Playwright

React：

Vitest / Jest
Playwright

E2E：

Playwright

56. GO TESTING

默认：

go test

配合：

table-driven tests
integration tests
Testcontainers
57. JAVA TESTING

默认：

JUnit
Mockito
Testcontainers

Integration：

Spring Boot Test

58. CODE QUALITY
Python

默认：

Ruff
Mypy
Pytest
TypeScript

默认：

TypeScript
ESLint
Prettier
Vitest
Go

默认：

gofmt
go vet
golangci-lint
go test
Java

默认：

Checkstyle / Spotless
JUnit

根据团队标准调整。

59. PACKAGE MANAGEMENT

Python：

优先：

uv

Node：

pnpm

Go：

Go Modules

Java：

Gradle

或：

Maven

根据 existing project 优先。

60. CONTAINERIZATION

默认：

Docker

生产环境：

Multi-stage build

必须：

non-root user where possible
small base image
pinned dependencies
healthcheck
graceful shutdown
61. DOCKER COMPOSE

适合：

Local development
Integration testing
Small deployment

例如：

services:
  api
  postgres
  redis
  worker
62. KUBERNETES
什么时候选
Multiple services
Autoscaling
High availability
Large organization
Existing Kubernetes platform
什么时候不要选
MVP
Small application
1–3 developers
Single service
No Kubernetes expertise

默认：

Docker > Kubernetes

63. CI/CD

默认：

GitHub Actions

Pipeline：

Push
 ↓
Lint
 ↓
Type Check
 ↓
Unit Test
 ↓
Integration Test
 ↓
Security Scan
 ↓
Build
 ↓
Deploy
64. DATABASE MIGRATION

必须使用 migration。

Python：

Alembic

Django：

Django migrations

Java：

Flyway / Liquibase

Node：

根据 ORM：

Prisma migration
Drizzle migration

禁止：

直接手工修改 production schema。

65. BACKUP

Production Database 必须考虑：

Backup
Retention
Restore
Disaster Recovery

不能只写：

“数据库自动备份”。

必须明确：

Backup Frequency
Retention
Restore Strategy
RPO
RTO
66. DATABASE DESIGN RULES

默认：

第三范式优先。

但为了读取性能可以合理反规范化。

禁止：

为了“灵活”而把所有字段塞进 JSON。

67. TRANSACTION RULES

涉及：

Money
Inventory
Permission
Critical state transition

必须考虑 transaction。

68. ID STRATEGY

默认：

UUID / UUIDv7 / database-generated ID

根据：

distributed generation
ordering
security
storage

选择。

不要暴露敏感业务序号作为安全边界。

69. TIME

所有后端：

UTC storage

API：

ISO 8601

用户显示：

local timezone

70. API ERROR FORMAT

统一：

{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Resource not found",
    "details": {}
  },
  "request_id": "..."
}

业务错误不要直接返回：

database exception。

71. PAGINATION

默认：

Cursor-based pagination

适合：

Large dataset
Real-time changing dataset

Offset pagination：

适用于：

Small dataset
Admin
Simple CRUD

72. RATE LIMITING

公开 API 默认考虑：

Rate Limiting

实现：

Redis when distributed.

必须定义：

limit
window
response
bypass policy
73. CACHING

Cache-aside 默认：

Application
    ↓
Redis
    ↓ miss
Database

必须定义：

TTL
invalidation
stale strategy
failure behavior
74. ASYNC ARCHITECTURE

只有明确需求才使用 async。

典型：

HTTP Request
 ↓
Create Job
 ↓
Queue
 ↓
Worker
 ↓
Database

不要把所有业务都异步化。

75. FRONTEND STATE MANAGEMENT

Vue：

默认：

Pinia

React：

优先：

React built-in state

需要 global state 时：

Zustand / Redux Toolkit 等。

不要默认 Redux。

76. UI COMPONENT LIBRARY

Agent 不应自动引入多个 UI library。

默认：

选择一个：

Ant Design
MUI
shadcn/ui
Element Plus
Naive UI

根据 frontend framework 和项目类型选择。

77. MONOREPO
什么时候选
Frontend + Backend
Shared types
Multiple applications
Shared packages

结构：

apps/
├── web
├── api
└── worker

packages/
├── types
├── ui
└── config
78. REPOSITORY STRUCTURE
Python FastAPI

默认：

project/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── models/
│   └── schemas/
├── tests/
├── migrations/
├── scripts/
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
79. Django
project/
├── config/
├── apps/
│   ├── users/
│   ├── orders/
│   └── payments/
├── tests/
├── manage.py
├── pyproject.toml
└── Dockerfile
80. Go
project/
├── cmd/
│   └── server/
├── internal/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── transport/
├── pkg/
├── migrations/
├── tests/
├── go.mod
├── Dockerfile
└── README.md

不要滥用：

pkg/

只有真正需要被外部复用的 package 才放这里。

81. NestJS
project/
├── src/
│   ├── modules/
│   │   ├── users/
│   │   ├── orders/
│   │   └── payments/
│   ├── common/
│   ├── config/
│   └── main.ts
├── test/
├── prisma/
├── package.json
└── Dockerfile
82. Spring Boot
project/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/app/
│   │   │       ├── domain/
│   │   │       ├── application/
│   │   │       ├── infrastructure/
│   │   │       └── api/
│   │   └── resources/
│   └── test/
├── build.gradle
└── Dockerfile
83. VUE
web/
├── src/
│   ├── components/
│   ├── views/
│   ├── layouts/
│   ├── stores/
│   ├── router/
│   ├── services/
│   ├── types/
│   └── utils/
├── tests/
├── public/
├── package.json
└── vite.config.ts
84. REACT
web/
├── src/
│   ├── components/
│   ├── features/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── stores/
│   ├── types/
│   └── utils/
├── tests/
├── package.json
└── vite.config.ts

推荐 Feature-oriented structure。

85. NEXT.JS
web/
├── app/
│   ├── (marketing)/
│   ├── dashboard/
│   ├── api/
│   └── layout.tsx
├── components/
├── features/
├── lib/
├── services/
├── types/
├── tests/
└── package.json
86. CONFIGURATION

环境配置：

.env
.env.local
.env.production

但：

Secrets 不允许提交 Git。

必须提供：

.env.example

例如：

DATABASE_URL=
REDIS_URL=
JWT_SECRET=
OPENAI_API_KEY=
87. SECRET MANAGEMENT

Production：

不要依赖 .env 文件长期存储 secrets。

优先：

Cloud Secret Manager
Vault
CI/CD secret store
88. VERSION STRATEGY

Agent 默认遵循：

Language

使用当前稳定版本。

Framework

使用当前稳定版本，但避免刚发布的 major version。

Database

使用当前主流稳定 major version。

Libraries

优先：

stable
maintained
compatible

避免：

abandoned
alpha
beta
deprecated
89. VERSION PINNING

Production dependencies 必须锁定。

Python：

uv.lock

Node：

pnpm-lock.yaml

Go：

go.mod
go.sum

Java：

gradle.lockfile

或：

Maven dependency management。

90. DEPENDENCY DECISION

引入第三方依赖之前必须问：

是否真的需要？
标准库能否解决？
现有依赖能否解决？
项目是否长期维护？
License 是否允许？
Security history 如何？
Agent 是否容易正确使用？
91. SPEC-DRIVEN DEVELOPMENT

Spec 是：

Source of Truth

而不是：

README 的附属文档。

92. SPEC ARTIFACTS

推荐：

docs/
└── specs/
    └── 001-feature-name/
        ├── context.md
        ├── requirements.md
        ├── technology-selection.md
        ├── design.md
        ├── decisions.md
        ├── tasks.md
        └── verification.md
93. PROJECT-LEVEL SPEC

项目级：

docs/
├── architecture.md
├── technology-selection.md
├── engineering-rules.md
└── specs/
94. TECHNOLOGY-SELECTION.MD

必须包含：

# Technology Selection

## Project Type

## Scale

## Architecture

## Backend

### Candidates

### Selected

### Reason

### Alternatives

### Rejected Because

## Frontend

## Database

## Cache

## Message Queue

## Search

## Storage

## Authentication

## Observability

## Deployment

## Testing
95. DECISION RECORD FORMAT

每一个重要技术决策：

## Decision: PostgreSQL

### Status

Accepted

### Decision

Use PostgreSQL as primary database.

### Context

The system contains relational transactional data.

### Alternatives

- MySQL
- MongoDB

### Why PostgreSQL

- Strong relational model
- ACID
- JSONB
- Mature ecosystem

### Why Not Alternatives

MySQL:
No existing infrastructure requirement.

MongoDB:
Domain is strongly relational.

### Consequences

The project depends on PostgreSQL.

### Reversibility

Medium
96. REQUIREMENTS

Functional requirements必须：

明确
可测试
可验证
不包含不必要的实现细节

推荐：

WHEN condition
THE SYSTEM SHALL behavior
97. ACCEPTANCE CRITERIA

每个核心需求必须有 Acceptance Criteria。

例如：

Given a valid invitation
When the user accepts it
Then the user becomes a member
98. DESIGN

Design 必须回答：

Component
Data flow
API
Database
Authentication
Error handling
Async processing
Failure handling
99. TASKS

Tasks 必须：

小
可执行
可验证
有依赖关系

不要：

Implement authentication system

应该拆：

Create user model
Create password hashing service
Create login endpoint
Create refresh token flow
Add authentication middleware
Add integration tests
100. IMPLEMENTATION RULE

Agent 实现代码之前：

必须读取：

Project Rules
Technology Selection
Relevant Spec
Design
Tasks
101. CHANGE MANAGEMENT

如果实现过程中发现：

Spec 错误

不要直接修改代码绕过 Spec。

流程：

发现问题
 ↓
确认 Spec 是否错误
 ↓
更新 Spec
 ↓
更新 Design
 ↓
更新 Tasks
 ↓
继续 Implementation
102. BROWNFIELD PROJECT

进入已有项目后：

先分析：

Repository
Architecture
Dependencies
Database
API
Tests
CI/CD
Deployment

不要立即写代码。

必须先生成：

project-discovery.md
103. BROWNFIELD TECHNOLOGY RULE

已有：

Python + Flask

不要自动迁移：

FastAPI

已有：

MySQL

不要自动迁移：

PostgreSQL

已有：

React

不要自动迁移：

Vue

除非用户明确要求。

104. FEATURE DEVELOPMENT FLOW
Requirement
 ↓
Explore
 ↓
Clarify
 ↓
Technology impact
 ↓
Spec
 ↓
Design
 ↓
Tasks
 ↓
Implementation
 ↓
Tests
 ↓
Review
 ↓
Verification
105. BUGFIX FLOW

Bugfix 不一定需要完整 Feature Spec。

最少：

Bug Description
 ↓
Root Cause
 ↓
Expected Behavior
 ↓
Fix Design
 ↓
Test
 ↓
Implementation
 ↓
Verification
106. REFACTOR FLOW
Current Architecture
 ↓
Problem
 ↓
Constraints
 ↓
Target Architecture
 ↓
Migration Strategy
 ↓
Incremental Tasks
 ↓
Tests
 ↓
Implementation

禁止：

一次性大规模重写。

107. AGENT QUESTION POLICY

如果关键架构信息未知：

不要编造。

优先：

Ask user

但不要为了无关紧要的问题阻塞开发。

108. QUESTIONS CLASSIFICATION
MUST ASK

影响架构：

用户规模
数据一致性
安全
合规
核心业务流程
部署环境
已有技术栈
性能要求
SHOULD ASK

影响实现：

Auth provider
Storage
Email provider
Search
Queue
CAN ASSUME

低风险：

Formatting
File naming
Test naming
Basic project structure

但假设必须记录。

109. TECHNOLOGY DECISION OUTPUT

生成 Spec 前必须输出：

Architecture:
Modular Monolith

Backend:
Python + FastAPI

Frontend:
Vue 3 + TypeScript + Vite

Database:
PostgreSQL

Cache:
None initially

Queue:
None initially

Search:
PostgreSQL Full Text Search

Storage:
S3-compatible Object Storage

Authentication:
OIDC / Cookie Session

API:
REST + OpenAPI

Testing:
pytest + Vitest + Playwright

Observability:
Structured Logging + OpenTelemetry

Deployment:
Docker

CI/CD:
GitHub Actions
110. DEFAULT TECHNOLOGY MATRIX
Category	Default	Alternatives
Architecture	Modular Monolith	Microservices
Backend	Python	Go / TS / Java
Python API	FastAPI	Django / Flask
Enterprise Backend	Spring Boot	NestJS
TS Backend	NestJS	Fastify / Hono
Frontend	Vue 3	React / Next.js
React SSR	Next.js	—
DB	PostgreSQL	MySQL / MongoDB
Cache	None	Redis
Queue	None	RabbitMQ
Streaming	None	Kafka
Search	PostgreSQL FTS	OpenSearch / Elasticsearch
Vector	pgvector	Qdrant / Milvus
API	REST	GraphQL / gRPC
Internal RPC	gRPC	REST
Object Storage	S3	Local
Auth	OIDC / Session	JWT
Python ORM	SQLAlchemy	Django ORM
Go DB	sqlc	GORM / Ent
Node ORM	Prisma	Drizzle / TypeORM
Java ORM	JPA	jOOQ
Python Test	pytest	unittest
Frontend E2E	Playwright	Cypress
Container	Docker	—
Local orchestration	Docker Compose	—
Production orchestration	Managed Container	Kubernetes
CI/CD	GitHub Actions	GitLab CI
Observability	OpenTelemetry	Vendor SDK
Python package	uv	Poetry
Node package	pnpm	npm / yarn
111. DEFAULT FULL STACK

对于没有特殊约束的中小型 SaaS：

Architecture:
Modular Monolith

Frontend:
Vue 3
TypeScript
Vite
Pinia

Backend:
Python
FastAPI
Pydantic
SQLAlchemy
Alembic

Database:
PostgreSQL

Cache:
None initially

Queue:
None initially

Search:
PostgreSQL Full Text Search

Storage:
S3-compatible Object Storage

API:
REST
OpenAPI

Authentication:
Cookie Session / OIDC

Testing:
pytest
Vitest
Playwright

Observability:
Structured Logging
OpenTelemetry

Container:
Docker
Docker Compose

CI/CD:
GitHub Actions
112. DEFAULT AI APPLICATION STACK
Frontend:
Next.js / React
TypeScript

Backend:
Python
FastAPI

Database:
PostgreSQL

Vector:
pgvector

Cache:
Redis when needed

Storage:
S3

LLM:
Provider abstraction

Background Jobs:
Celery / Queue

API:
REST + OpenAPI

Testing:
pytest
Vitest
Playwright

Observability:
OpenTelemetry
113. DEFAULT ENTERPRISE STACK
Frontend:
React / Vue

Backend:
Java/Kotlin
Spring Boot

Database:
PostgreSQL

Cache:
Redis

Messaging:
Kafka when event streaming is required

Search:
OpenSearch when required

Auth:
OIDC / SAML

API:
REST
gRPC internally

Observability:
OpenTelemetry

Deployment:
Kubernetes

CI/CD:
GitHub Actions / GitLab CI
114. DEFAULT HIGH-PERFORMANCE SERVICE
Language:
Go

Framework:
Chi / Gin

Database:
PostgreSQL

Cache:
Redis when justified

Internal API:
gRPC

Messaging:
Kafka when required

Observability:
OpenTelemetry

Deployment:
Docker / Kubernetes
115. TECHNOLOGY INTRODUCTION CHECKLIST

在引入任何新技术前回答：

[ ] What problem does it solve?
[ ] Is the problem real?
[ ] Can existing technology solve it?
[ ] What operational cost does it add?
[ ] What development cost does it add?
[ ] What failure modes does it introduce?
[ ] How will it be monitored?
[ ] How will it be tested?
[ ] How will it be backed up?
[ ] How will it be upgraded?
[ ] Can we remove it later?

如果无法回答：

不要引入。

116. ARCHITECTURE REVIEW CHECKLIST

生成 spec.md 前检查：

[ ] Project type identified
[ ] Scale estimated
[ ] Architecture selected
[ ] Backend selected
[ ] Frontend selected
[ ] Database selected
[ ] Cache decision made
[ ] Queue decision made
[ ] Search decision made
[ ] Storage decision made
[ ] Authentication selected
[ ] API style selected
[ ] Testing strategy defined
[ ] Observability defined
[ ] Deployment defined
[ ] CI/CD defined
[ ] Security considered
[ ] Backup considered
[ ] Risks documented
[ ] Open questions documented
117. FINAL SPEC REQUIREMENTS

最终 spec.md 至少包含：

1. Overview
2. Goals
3. Non-Goals
4. Users
5. Functional Requirements
6. Non-Functional Requirements
7. Scale
8. Architecture
9. Technology Decisions
10. Repository Structure
11. Data Model
12. API Design
13. Authentication
14. Authorization
15. Error Handling
16. Logging
17. Testing
18. CI/CD
19. Deployment
20. Security
21. Risks
22. Open Questions
23. Acceptance Criteria
118. FINAL AGENT BEHAVIOR

当用户说：

“帮我开发 XXX”

不要直接：

write code

应该：

1. Discover
2. Analyze
3. Select architecture
4. Select technology
5. Produce specification
6. Ask only critical questions
7. Produce design
8. Produce tasks
9. Implement
10. Test
11. Verify
119. GOLDEN RULE

永远遵循：

Requirement
    ↓
Decision
    ↓
Specification
    ↓
Design
    ↓
Task
    ↓
Code
    ↓
Test
    ↓
Verification

而不是：

Prompt
 ↓
Code
 ↓
More Prompt
 ↓
More Code
120. FINAL PRINCIPLE

技术不是目的。

架构不是目的。

Framework 不是目的。

SDD 也不是目的。

最终目标：

Correctness
+
Maintainability
+
Simplicity
+
Testability
+
Observability
+
Security
+
Evolvability

在没有明确需求时：

选择最简单、成熟、可维护、容易验证的方案。

在需求明确要求复杂架构时：

满足需求，并记录为什么复杂是必要的。

不要为了架构而架构。


---

## 我再给你一个关键建议

如果你准备**真的把这套东西长期用于 Claude Code / Cursor / Codex**，我不建议把上面 **120 条全部塞进一个 `CLAUDE.md`**。

更好的工程化方式是：

```text
agent-sdd/
│
├── CLAUDE.md                  # Agent 总入口，约 100～200 行
├── AGENTS.md                  # 通用 Agent 规则
│
├── .sdd/
│   ├── README.md
│   │
│   ├── knowledge/
│   │   ├── architecture.md
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   ├── database.md
│   │   ├── messaging.md
│   │   ├── api.md
│   │   ├── security.md
│   │   ├── testing.md
│   │   ├── deployment.md
│   │   └── observability.md
│   │
│   ├── decision-trees/
│   │   ├── architecture.md
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   ├── database.md
│   │   └── infrastructure.md
│   │
│   ├── templates/
│   │   ├── project-discovery.md
│   │   ├── technology-selection.md
│   │   ├── spec.md
│   │   ├── design.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── adr.md
│   │
│   └── workflows/
│       ├── new-project.md
│       ├── new-feature.md
│       ├── bugfix.md
│       └── refactor.md
│
└── specs/
    └── 001-project/
        ├── project-discovery.md
        ├── technology-selection.md
        ├── spec.md
        ├── design.md
        ├── tasks.md
        └── verification.md

其中 CLAUDE.md 只负责：

“什么时候读取什么”

而不是：

“把所有技术知识全部背下来”

例如：

# CLAUDE.md

## SDD REQUIRED

Before implementing a new project or major feature:

1. Read `.sdd/workflows/new-project.md`
2. Read `.sdd/knowledge/architecture.md`
3. Read `.sdd/decision-trees/backend.md`
4. Read `.sdd/decision-trees/frontend.md`
5. Read `.sdd/decision-trees/database.md`
6. Generate `technology-selection.md`
7. Generate `spec.md`
8. Do not implement until architecture decisions are resolved.

For existing projects:

1. Inspect existing architecture first.
2. Never replace an existing technology without explicit justification.
3. Prefer incremental changes.

这样有一个非常大的好处：

未来你更新技术栈时，不需要修改 Agent 的核心规则。

例如 2027 年你决定：

Python 默认版本变化
FastAPI 版本变化
Vue → React
PostgreSQL → 某种新方案

只需要修改：

.sdd/knowledge/backend.md
.sdd/decision-trees/backend.md

而：

CLAUDE.md
AGENTS.md

基本不动。

这实际上会形成一个更完整的体系：

                 ┌────────────────────┐
                 │    CLAUDE.md       │
                 │    AGENTS.md       │
                 │  Agent 行为规则     │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │    SDD Workflow    │
                 │                    │
                 │ Discovery          │
                 │ Decision           │
                 │ Spec               │
                 │ Design             │
                 │ Tasks              │
                 │ Implementation     │
                 │ Verification       │
                 └─────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   Architecture       Technology        Engineering
     Knowledge         Knowledge          Rules
          │                │                │
          ▼                ▼                ▼
      Backend          Database           Testing
      Frontend         Redis              Security
      API              Kafka              CI/CD
      Deployment       Storage            Observability
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    technology-selection.md
                           │
                           ▼
                       spec.md
                           │
                           ▼
                       design.md
                           │
                           ▼
                       tasks.md
                           │
                           ▼
                    Claude/Cursor/Codex
                           │
                           ▼
                         Code

我认为这才是你前面所说的“给 Agent 输入项目框架先验知识”的正确形态：不是告诉 Agent “Python + FastAPI + PostgreSQL 是最佳实践”，而是建立一套可解释的决策系统，让 Agent 根据项目上下文选择技术，并把选择结果固化进 technology-selection.md 和 spec.md。