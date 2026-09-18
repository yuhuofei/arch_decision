# Example: High-Concurrency Service（高并发网络服务）

> 来源：Matrix §39；知识库 §61。

## Input
```yaml
project_type: network_service
concurrency: very_high
latency_requirement: strict
service_to_service: true
```

## 决策
```
Language        → Go                         # 高并发/网络/低延迟
HTTP            → net/http / Gin             # 小服务 net/http；普通 API Gin
Protocol        → REST externally
                → gRPC internally if justified
Database        → PostgreSQL if relational
Cache           → Redis if required
Architecture    → Modular Monolith initially
Microservices    → only if independent scaling/deployment required
```

## 依据
- 高并发/延迟严格/网络服务 → Go（backend.md §1，Matrix §6.2）。
- Go 标准库 `net/http` 已足够小服务；仅高级 middleware/routing 引 Gin（backend.md §3）。
- 外部 REST，内部 service-to-service 低延迟/强类型 → gRPC（api.md §3）。
- 不要因"Go 性能好"就默认 Microservices；先 Modular Monolith，确有独立扩缩/部署才拆。

## 决策状态
- Language/Framework → `AUTO`
- 若引入 gRPC / Redis / Microservices / K8s → 对应 `RECOMMEND` 或 `REQUIRE_CONFIRMATION`

## 复杂度预算（口径见 decision-protocol §5.1）
```
PostgreSQL(1) + [Redis(1) 若启用] = 1 ~ 2  ≤ Small SaaS 预算 8   ✅
gRPC 不计分（进程内协议）；Docker 不计分（打包方式）。
⚠️ 若进一步引入 Microservices(+3) + K8s(+3) → 7 ~ 8，逼近预算上限，必须重评并触发 REQUIRE_CONFIRMATION。
```
