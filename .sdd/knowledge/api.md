# Knowledge: API（接口风格）

> 来源：res.md §29-§33,§70-§73；Matrix §15；知识库 §26-§28,§52,§53
> 决策树：`.sdd/decision-trees/infrastructure.md`

## 1. REST（res.md §30 / Matrix §15，默认）
```
IF public_api OR business_api OR CRUD THEN REST
```
默认 Resource-oriented URL / HTTP methods / status codes / Pagination / Filtering / Sorting / Error schema / Versioning。

## 2. GraphQL（res.md §31 / Matrix §15）
```
IF frontend_data_shape_complexity = high AND clients_need_different_views THEN GraphQL = candidate
```
不选：简单 CRUD / 单一前端 / 简单 API / 团队不熟。默认 REST > GraphQL（知识库 Rule 7）。不要因"更先进"默认 GraphQL。

## 3. gRPC（res.md §32 / Matrix §15）
```
IF service_to_service AND low_latency OR strongly_typed_contract THEN gRPC
```
不选：Browser public API / 简单 CRUD。默认 Public→REST，Internal 高性能→gRPC。
```
Browser → REST/JSON ; Service → Service → gRPC
```

## 4. OpenAPI（res.md §33）
所有 REST API 默认 OpenAPI 3.x。必须定义 Request/Response/Error schema / Authentication / Pagination / Examples。

## 5. API Contract → 生成 TS Client（知识库 §52-§53，新增）
```
Backend → OpenAPI → TypeScript Client → Frontend
```
前后端共享 API Contract，减少 response≠expectation。

## 6. API Error Format（res.md §70）
统一 `{ "error": { "code", "message", "details" }, "request_id" }`。业务错误不暴露 DB exception。

## 7. Pagination / Rate Limiting / Caching（res.md §71-§73）
- Cursor-based（默认，大表/实时）；Offset（小表/Admin/CRUD）。
- 公开 API 默认 Rate Limiting（分布式用 Redis），定义 limit/window/response/bypass。
- Cache-aside：`App → Redis → miss → DB`，定义 TTL/invalidation/stale/failure。
