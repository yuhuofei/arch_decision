# Knowledge: Deployment（部署与运维）

> 来源：res.md §60-§65,§86,§87,§88,§89；Matrix §24,§25,§45；知识库 §44-§46,§47-§48
> 决策树：`.sdd/decision-trees/infrastructure.md`

## 1. Deployment Matrix（Matrix §24）
- **Local / MVP** → Docker Compose（api + postgres + redis + worker）
- **Small Production** → Docker + Managed DB + Managed Redis(if needed)
- **Large Production** → 仅当出现 `multiple_services OR autoscaling OR high_availability OR multi_region OR organization_kubernetes_standard` 才考虑 K8s

## 2. Kubernetes Decision Rule（Matrix §25 / 知识库 §45）
```
IF deployment_complexity_requirement <= medium THEN Kubernetes = false
IF autoscaling = required AND service_count >= multiple AND operational_team = available THEN Kubernetes = candidate
ELSE Docker / Managed Container Platform 优先
```
小项目用 Docker + VM / Cloud Run / ECS / App Service 通常更简单。不要默认 K8s。

## 3. CI/CD（res.md §63 / 知识库 §46，默认 GitHub Actions）
Pipeline：Lint → Type Check → Unit Test → Integration Test → Build → Security Scan → Deploy。
企业已有：GitLab CI / Jenkins / Azure DevOps。

## 4. Containerization（res.md §60，默认 Docker）
生产 Multi-stage build；必须 non-root / small base / pinned deps / healthcheck / graceful shutdown。
镜像**禁止 `latest`**，必须 pin 运行时版本；依赖锁定规则见 `.sdd/knowledge/versioning.md` §5（本文件不另写一份）。

## 5. Database Migration（res.md §64）
必须用 migration（Python Alembic / Django migrations / Java Flyway·Liquibase / Node Prisma·Drizzle）。禁止手工改 production schema。

## 6. Backup（res.md §65）
生产 DB 明确 Backup Frequency / Retention / Restore Strategy / RPO / RTO。不能只写"自动备份"。

## 7. Configuration / Secret（res.md §86,§87）
`.env` / `.env.local` / `.env.production`；Secrets 不提交 Git；提供 `.env.example`。生产优先 Cloud Secret Manager / Vault / CI-CD secret store。

## 8. Multi-region / 高可用
属 REQUIRE_CONFIRMATION 决策（decision-protocol §6），需人确认。
