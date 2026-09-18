# Knowledge: Database（数据库）

> 来源：res.md §22-§27,§39,§40,§66-§69；Matrix §10-§13,§18,§22；知识库 §20-§24,§31,§32
> 决策树：`.sdd/decision-trees/database.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## 1. 数据库分类（知识库 §20）
先按 关系型 / 文档型 / KV / 搜索 / 向量 / 时序 分类。

## 2. PostgreSQL（res.md §23 / Matrix §10，默认主数据库）
```
IF relational_data = true AND no_specific_constraint THEN PostgreSQL
```
适合 SaaS/ERP/CRM/订单/财务/工作流/多租户/复杂查询/JSON/地理/AI。新关系型项目默认（知识库 Rule 5）。优势：SQL 强/事务完整/JSONB/丰富类型/扩展强。

## 3. MySQL（res.md §24 / Matrix §11）
```
IF existing_mysql OR organization_standard = MySQL OR ecosystem_dependency = MySQL THEN MySQL
```
不要因"数据库都差不多"在已有 PG 项目切换（Greenfield→PG 优先；Existing→保持原库优先）。

## 4. SQLite（res.md §25 / Matrix §12）
```
IF single_instance AND low_concurrency AND database_scale = small THEN SQLite
```
典型 CLI/Prototype/Local/Desktop/Small Internal/Tests。不选：多实例生产 API / 高写并发 / 分布式后端。

## 5. Redis（res.md §27 / Matrix §13）
**不是默认数据库**，也不是"第二数据库"。
```
Redis = true 仅当 cache/session/rate_limit/distributed_lock/queue/stream/hot_data/temporary_state
IF none_of_above THEN Redis = false
```
原则：PostgreSQL/MySQL = Source of Truth；Redis = Performance/Temporary State。重要业务数据不要只放 Redis。

## 6. Vector Search（res.md §39 / Matrix §18 / 知识库 §31）
```
IF vector_search AND relational_data AND vector_scale = moderate THEN PostgreSQL + pgvector   # 默认
IF vector_scale = large OR vector_workload = dominant OR specialized_vector_features THEN Qdrant/Weaviate/Milvus
```
不要默认同时部署 PG+Redis+ES+Milvus（知识库 §31）。

## 7. Object Storage（res.md §40 / Matrix §19 / 知识库 §32）
文件/图片/视频/附件不直存 DB；默认 S3-compatible（AWS S3 / MinIO / Cloudflare R2 / 阿里云 OSS / 腾讯云 COS）。DB 只存 object_key/url/metadata/mime_type/size。小型本地文件可用 local filesystem。

## 8. 多租户（Matrix §22，详见 architecture.md §5）
Shared DB + tenant_id（默认）→ Separate schema → Separate DB → Separate infra。

## 9. DB Design Rules（res.md §66）
默认第三范式优先；为读性能合理反规范化。禁止为"灵活"把所有字段塞 JSON。

## 10. Transaction / ID / Time（res.md §67,§68,§69）
- 事务覆盖 Money/Inventory/Permission/关键状态。
- ID 默认 UUID/UUIDv7/DB-generated。
- 时间 UTC 存储；API ISO 8601；显示 local timezone。
