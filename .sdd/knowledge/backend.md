# Knowledge: Backend（后端语言与框架）

> 来源：res.md §5-§15, §28, §54, §56, §57, §58, §59, §64, §88, §89
> 决策树：`.sdd/decision-trees/backend.md`

## 1. Backend Language Decision（§5）

| 候选 | 默认决策原则 |
| --- | --- |
| Python | AI / Data / LLM / RAG / 数据处理 |
| Go | 高并发 / 基础设施 / 网络服务 |
| TypeScript | 全栈 TypeScript |
| Java / Kotlin | 企业 Java 生态 |
| C# | 微软生态 |

## 2. Python（§6）

**推荐**：AI / LLM / RAG / Data Processing / Automation / API / SaaS / Internal Tool / MVP / CRUD。
**不优先**：极端低延迟 / 极端高并发 / CPU-heavy / 网络基础设施 → 考虑 Go/Java/Rust。
**默认版本**：使用项目开始时的当前稳定 Python 3.x；不要固定旧版本。必须记录 Python Version + Reason。

## 3. FastAPI（§7, DEFAULT Python API）

默认 `Python + FastAPI`。选：REST API / API-first / SaaS / AI backend / Async / Microservice / Mobile backend / BFF。
不选：强依赖 Django Admin / 大量传统 server-rendered / 已有成熟 Django。
默认 Stack：FastAPI + Pydantic + SQLAlchemy + Alembic + pytest + httpx。

## 4. Django（§8）

选：Admin-heavy / CMS / Enterprise CRUD / ORM-heavy / Server-rendered / 已有 Django。
不选：极简 API / AI microservice / 高度异步 / 极轻量 service。
默认 Stack：Django + Django ORM + PostgreSQL + pytest-django + Redis(按需) + Celery(按需)。

## 5. Flask（§9）

选：已有 Flask 项目 / 极简 API / 高度定制 / 团队已有 Flask 能力。新项目默认 FastAPI > Flask（非绝对）。

## 6. Go（§10）

选：高并发 / 网络服务 / Gateway / Proxy / Infrastructure / Cloud Native / 高性能 API / Microservice / CLI。
不选：AI-heavy / Data Science / 快速 ML 原型 / Python 生态为核心依赖。
默认 Stack：Go + Chi/Gin + PostgreSQL + Redis(按需) + OpenTelemetry + Docker。

## 7. Go Framework（§11）

- **Chi**：Lightweight API / 标准库优先 / 最小抽象（默认推荐）。
- **Gin**：REST API / 快速开发 / 成熟生态。
- **Echo**：REST API / Lightweight service。

## 8. TypeScript Backend（§12, §13）

选：Full-stack TS / Web-first / BFF / Realtime / SaaS / 团队偏好 TS。默认 **NestJS**。
**NestJS** 选：Enterprise TS / Modular backend / Large team / DI / 结构化架构 / REST·GraphQL。不选：极简 API / 极轻量 serverless。
默认 Stack：NestJS + TS + PostgreSQL + Prisma/TypeORM + Redis(按需) + Jest。

## 9. Java / Kotlin（§14, §15）

选：Enterprise / Banking / ERP / 大型组织 / 已有 JVM 生态 / 复杂事务处理。默认 **Java/Kotlin + Spring Boot**。
**Spring Boot** 选：Enterprise backend / 复杂业务 / 大团队 / JVM 生态 / 长生命周期生产系统。不选：tiny service / MVP / 1 人原型 / 简单 API。
默认 Stack：Spring Boot + Spring Web + Spring Security + Spring Data JPA + PostgreSQL + Redis/Kafka(按需) + JUnit + Testcontainers。

## 10. ORM（§28）

- Python：SQLAlchemy（FastAPI/复杂 domain/显式 SQL）；Django 项目用 Django ORM。
- Go：sqlc（SQL-centric/性能/强类型）/ GORM（CRUD 快速）/ Ent（强 schema/大项目）。
- TS：Prisma / Drizzle（按团队与复杂度）。
- Java：Spring Data JPA；复杂 SQL 用 jOOQ。

## 11. Package Management（§59）

Python → uv（优先）/ Node → pnpm / Go → Go Modules / Java → Gradle 或 Maven（按 existing project）。

## 12. DB Migration（§64）

必须用 migration：Python → Alembic / Django → Django migrations / Java → Flyway·Liquibase / Node → Prisma·Drizzle migration。**禁止**直接手工改 production schema。

## 13. Version Strategy（§88）

语言用当前稳定版；框架用当前稳定版但避免刚发布的 major；库优先 stable/maintained/compatible，避免 abandoned/alpha/beta/deprecated。

## 14. Version Pinning（§89）

生产依赖必须锁定：uv.lock / pnpm-lock.yaml / go.mod+go.sum / gradle.lockfile。

## 15. Agent 提问（通用）

- Python：是否 AI/Data-heavy？是否 CPU-bound？是否对启动时间/内存敏感？
- Go：是否真需要 Go runtime 优势？是否高并发？是否 network/infra service？是否有 Go 团队？
- NestJS：是否需要模块化/DI？团队是否熟悉 TS？是否需要 GraphQL？
- Spring Boot：是否 Enterprise？是否长生命周期生产系统？
