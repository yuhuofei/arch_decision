# Decision Tree: Infrastructure（基础设施：Auth / MQ / Search / API / Deploy / CI-CD / Observability）

> 配套知识：`.sdd/knowledge/{messaging,api,security,deployment,observability}.md`
> 治理：`.sdd/decision-trees/decision-protocol.md`

## 1. Authentication（Matrix §20，含 No Auth）
```
IF public_readonly AND user_identity_not_required
→ No Auth                         # 仅此场景

IF traditional_web AND browser_only
→ Session (Cookie + Server-side)  # AUTO

IF multiple_clients OR stateless_api OR mobile
→ JWT / token-based               # RECOMMEND（勿因流行默认）

IF enterprise_sso OR social_login OR external_idp
→ OAuth / OIDC                    # RECOMMEND
```
**禁止**自研密码加密/OAuth Server/JWT 算法/session crypto。
Authentication architecture 变更 = `REQUIRE_CONFIRMATION`（decision-protocol §6）。

## 2. Authorization（Matrix §21）
```
admin/user 两级            → RBAC
权限含 resource/org/tenant/ownership/attribute → RBAC + resource-level
仅复杂策略                → ABAC / Policy Engine
```

## 3. Message Queue（Matrix §16）
```
request_response 足够 AND background_work 低 → MQ = false
task_queue / business_event / routing → RabbitMQ
event_streaming AND (高吞吐 OR replay OR 多consumer OR stream) → Kafka
queue 简单 AND 已用 Redis → Redis Queue
```

## 4. Search（Matrix §17 → 细则见 `knowledge/caching.md` §5）
```
复杂全文/fuzzy/faceting/大规模/相关性关键 → OpenSearch/Elasticsearch   # +2，需实测证据
否则 → PostgreSQL Full Text Search        # 默认
```
> 不要因"以后可能搜索很多"提前引入搜索集群（Matrix §17）。

## 4b. Cache（Matrix §23 → 细则见 `knowledge/caching.md`）
```
read_heavy AND data_changes_less_frequently AND cache_hit_benefit_significant → cache = true   # +1
ELSE → cache = false
```
> Redis 不是默认组件；引入时必须在 ADR 中说明存在理由。

## 5. API Style（Matrix §15）
```
public/business/CRUD → REST + OpenAPI     # 默认
前端数据形状复杂 AND 多视图 → GraphQL（candidate）
service-to-service AND 低延迟/强类型 → gRPC
```

## 6. Deployment（Matrix §24-§25）
```
Local/MVP     → Docker Compose
Small Prod    → Docker + Managed DB + Managed Redis
Large Prod    → 仅 multiple_services/autoscaling/HA/multi_region/org K8s 标准 → K8s
否则 Docker / Managed Container Platform
K8s = REQUIRE_CONFIRMATION
```

## 7. CI/CD / Observability
- CI/CD → GitHub Actions（企业已有则 GitLab/Jenkins/Azure DevOps）。
- Observability → 生产默认 Logs+Metrics+Tracing；多服务/分布式 → OpenTelemetry。

## 8. 复杂度预算联动（Matrix §32）
每个引入的组件计入 `complexity_score`；超限必须重评（见 architecture.md §3）。

## 输出
写入 `technology-selection.md` 的 Authentication / Authorization / Queue / Search / API / Deployment / CI-CD / Observability 段。
