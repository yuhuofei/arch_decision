# Knowledge: Deployment（部署与运维）

> 来源：res.md §60-§65, §86, §87, §88, §89

## 1. Containerization（§60, DEFAULT: Docker）

生产：Multi-stage build。必须：non-root user（尽量）/ small base image / pinned dependencies / healthcheck / graceful shutdown。

## 2. Docker Compose（§61）

适合：Local dev / Integration testing / Small deployment（api + postgres + redis + worker）。

## 3. Kubernetes（§62）

选：多服务 / Autoscaling / 高可用 / 大型组织 / 已有 K8s 平台。不选：MVP / 小应用 / 1-3 人 / 单服务 / 无 K8s 专长。默认 Docker > Kubernetes。

## 4. CI/CD（§63, DEFAULT: GitHub Actions）

Pipeline：Push → Lint → Type Check → Unit Test → Integration Test → Security Scan → Build → Deploy。

## 5. Database Migration（§64）

必须用 migration（见 backend.md §12）。禁止直接手工改 production schema。

## 6. Backup（§65）

生产数据库必须明确：Backup Frequency / Retention / Restore Strategy / RPO / RTO。不能只写"数据库自动备份"。

## 7. Configuration（§86）

环境配置：`.env` / `.env.local` / `.env.production`。Secrets 不允许提交 Git。必须提供 `.env.example`（如 DATABASE_URL / REDIS_URL / JWT_SECRET / OPENAI_API_KEY）。

## 8. Secret Management（§87）

生产优先 Cloud Secret Manager / Vault / CI-CD secret store（见 security.md §7）。

## 9. Version Strategy（§88）& Pinning（§89）

见 backend.md §13 / §14。
