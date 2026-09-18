# Knowledge: API（接口风格）

> 来源：res.md §29-§33, §70-§73

## 1. API Style（§29, DEFAULT: REST）

## 2. REST（§30）

选：Public API / Web backend / Mobile backend / CRUD / 标准 HTTP 服务。
默认要求：Resource-oriented URL / HTTP methods / HTTP status codes / Pagination / Filtering / Sorting / Error schema / Versioning strategy。

## 3. GraphQL（§31）

选：Multiple clients / 高度可变数据需求 / 复杂前端数据组合 / Client-driven querying。
不选：简单 CRUD / 单一前端 / 简单 API / 团队不熟悉 GraphQL。默认 REST > GraphQL。

## 4. gRPC（§32）

选：Internal service-to-service / 高性能 / Streaming / 强类型 / Polyglot services。
不选：Browser public API / 简单 CRUD API。默认 `Public API → REST`；`Internal 高性能 → gRPC`。

## 5. OpenAPI（§33）

所有 REST API 默认用 OpenAPI。必须定义：Request schema / Response schema / Error schema / Authentication / Pagination / Examples。

## 6. API Error Format（§70）

统一：

```json
{
  "error": { "code": "RESOURCE_NOT_FOUND", "message": "Resource not found", "details": {} },
  "request_id": "..."
}
```

业务错误不要直接返回 database exception。

## 7. Pagination（§71）

- Cursor-based（默认）：大表 / 实时变化数据集。
- Offset：小表 / Admin / 简单 CRUD。

## 8. Rate Limiting（§72）

公开 API 默认考虑 Rate Limiting。分布式用 Redis 实现。必须定义 limit / window / response / bypass policy。

## 9. Caching（§73）

Cache-aside 默认：`Application → Redis → miss → Database`。必须定义 TTL / invalidation / stale strategy / failure behavior。
