# Decision Tree: Infrastructure（基础设施选型：Cache / Queue / Search / API / Auth / Deploy / CI-CD）

> 配套知识：`.sdd/knowledge/messaging.md` · `api.md` · `security.md` · `deployment.md` · `observability.md`

## Message Queue（§34, 默认 NONE）
```
是否需要 Async processing / Retry / Event-driven / Decoupling / High throughput / Background jobs？
├─ 否 ──→ 不引入消息队列
├─ 是 ──→ 简单任务队列 / 业务事件 / 中等规模 / 传统企业集成 → RabbitMQ（§35）
│         └─ Event streaming / 高吞吐 / Event replay / 数据管道 / 多 consumer → Kafka（§36）
后台任务（§37）：Python→Celery；轻量→FastAPI BackgroundTasks（注意≠分布式可靠队列）
```

## Search（§38, 默认 PostgreSQL FTS）
```
是否需要 Fuzzy / Faceted / 复杂排序 / 大索引？
├─ 否 ──→ PostgreSQL Full Text Search
└─ 是 ──→ Elasticsearch / OpenSearch / Meilisearch / Typesense（禁止无需求引入 ES）
```

## API Style（§29, 默认 REST）
```
Public API / Web / Mobile / CRUD / 标准 HTTP → REST + OpenAPI（§30,§33）
多 client / 高度可变数据 / Client-driven → GraphQL（§31，默认 REST>GraphQL）
Internal 高性能 / Streaming / 强类型 / Polyglot → gRPC（§32）
```

## Authentication（§41, 优先成熟方案）
```
传统 Web → Cookie + Server-side Session（§42）
API / Mobile / 分布式 / 无状态 → JWT（须考虑 expiration/refresh/revocation，§43，勿因流行而默认）
第三方登录 → OIDC（企业可能 SAML+OIDC，§44）
禁止自研密码加密 / OAuth / JWT 算法 / session crypto
```

## Deployment（§60, 默认 Docker）
```
Local dev / 集成测试 / 小部署 → Docker Compose（§61）
多服务 / Autoscaling / 高可用 / 大型组织 / 已有 K8s → Kubernetes（§62，默认 Docker>K8s）
CI/CD → GitHub Actions（§63，Push→Lint→TypeCheck→Unit→Integration→Security→Build→Deploy）
```

## Observability（§47, 默认结构化日志+Metrics+Health+Error）
```
中大型 → OpenTelemetry 统一 Logs/Metrics/Traces（§49）
日志禁止记录 Password/Token/Secret/PII（§48）
```

## 技术规范引入检查表（§115）
引入任何新技术前回答：解决什么问题？问题是否真实？现有能否解决？运维/开发成本？失败模式？如何监控/测试/备份/升级？能否移除？无法回答则不引入。

## 输出
写入 `technology-selection.md` 的 Cache / Queue / Search / API / Authentication / Observability / Deployment / CI-CD 段。
