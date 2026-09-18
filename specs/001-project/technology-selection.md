# Technology Selection — 001-project（示例实例）

> 按 `.sdd/templates/technology-selection.md` 填写。生成前读 `.sdd/decision-trees/*.md` 与 `.sdd/knowledge/*.md`。

## Project Type
<!-- MVP / Production / Internal / Public / SaaS / Enterprise -->

## Scale
<!-- Small / Medium / Large -->

## Architecture
### Candidates
- Modular Monolith（默认）
- Microservices
### Selected
Modular Monolith
### Reason
无独立部署/独立 team/极高吞吐需求，业务边界尚未稳定，小团队。
### Alternatives
Microservices
### Rejected Because
不满足强条件（§4.2）；为架构而架构违背 FINAL PRINCIPLE（§120）。

## Backend
### Candidates
- Python + FastAPI（默认）
- Go
### Selected
Python + FastAPI
### Reason
<待填写>
### Alternatives
Go
### Rejected Because
<非高并发/网络基础设施场景>

## Frontend
<!-- Vue 3 + TypeScript + Vite（默认，Enterprise/Admin） -->

## Database
<!-- PostgreSQL（默认主数据库） -->

## Cache
None initially

## Message Queue
None initially

## Search
PostgreSQL Full Text Search

## Storage
S3-compatible Object Storage

## Authentication
OIDC / Cookie Session

## Observability
Structured Logging + OpenTelemetry

## Deployment
Docker

## Testing
pytest + Vitest + Playwright

## 决策输出速填（§109）
```
Architecture:   Modular Monolith
Backend:        Python + FastAPI
Frontend:       Vue 3 + TypeScript + Vite
Database:       PostgreSQL
Cache:          None initially
Queue:          None initially
Search:         PostgreSQL Full Text Search
Storage:        S3-compatible Object Storage
Authentication: OIDC / Cookie Session
API:           REST + OpenAPI
Testing:       pytest + Vitest + Playwright
Observability:  Structured Logging + OpenTelemetry
Deployment:     Docker
CI/CD:         GitHub Actions
```

## 决策记录（ADR 索引）
- [ ] PostgreSQL → adr-001-postgres.md
- [ ] FastAPI → adr-002-fastapi.md
