# Template: Technology Selection（技术选型）

> 用途：固化技术决策（res.md §94, §109）。每个重要决策配 ADR（`.sdd/templates/adr.md`）。
> 生成前必须读：`.sdd/decision-trees/*.md` 与 `.sdd/knowledge/*.md`。

# Technology Selection

## Project Type
<!-- MVP / Production / Internal / Public / SaaS / Enterprise -->

## Scale
<!-- Small / Medium / Large -->

## Architecture
<!-- Modular Monolith / Microservices -->

### Candidates
### Selected
### Reason
### Alternatives
### Rejected Because

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

---

## 决策输出速填（§109 示例）

```
Architecture:        Modular Monolith
Backend:             Python + FastAPI
Frontend:            Vue 3 + TypeScript + Vite
Database:            PostgreSQL
Cache:               None initially
Queue:               None initially
Search:              PostgreSQL Full Text Search
Storage:             S3-compatible Object Storage
Authentication:      OIDC / Cookie Session
API:                REST + OpenAPI
Testing:            pytest + Vitest + Playwright
Observability:       Structured Logging + OpenTelemetry
Deployment:          Docker
CI/CD:              GitHub Actions
```

## 决策记录（§95 ADR 索引）
- [ ] PostgreSQL → adr-001-postgres.md
- [ ] FastAPI → adr-002-fastapi.md
- ...
