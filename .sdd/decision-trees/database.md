# Decision Tree: Database（数据库选型）

> 配套知识：`.sdd/knowledge/database.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## 1. 主数据库（Matrix §10-§12）

```
IF relational_data = true AND no_specific_constraint
→ PostgreSQL                      # 默认主数据库 AUTO

IF existing_mysql OR org_standard = MySQL OR ecosystem_dependency = MySQL
→ MySQL                           # Hard Constraint

IF single_instance AND low_concurrency AND scale = small
→ SQLite                          # CLI/Prototype/Local/Desktop/Tests
   不选：多实例生产 API / 高写并发 / 分布式后端

IF document-oriented AND dynamic_schema AND nested_document
   AND domain clearly fits document model
→ MongoDB                         # 否则 PostgreSQL > MongoDB
```

## 2. Redis（Matrix §13）
```
IF cache OR session OR rate_limit OR distributed_lock
   OR queue OR stream OR hot_data OR temporary_state
→ Redis = true
ELSE Redis = false                # Redis 不是默认数据库
```

## 3. 向量库（Matrix §18）
```
IF vector_search AND relational_data AND vector_scale = moderate
→ PostgreSQL + pgvector           # 默认

IF vector_scale = large OR workload = dominant OR specialized features
→ Qdrant / Weaviate / Milvus      # RECOMMEND
```

## 4. 对象存储（Matrix §19）
```
IF file_storage AND size/volume > local limit
→ S3-compatible (S3/MinIO/R2/OSS/COS)
小型本地文件 → local filesystem
DB 只存 object_key/url/metadata/mime_type/size
```

## 5. 多租户（Matrix §22）
```
users belong to orgs AND isolation required → multi_tenant
默认 Shared DB + tenant_id；强隔离→schema；合规→DB；极端→infra
```

## 6. 设计约束（res.md §66-§69）
第三范式优先；事务覆盖 Money/Inventory/Permission/关键状态；ID 默认 UUID/UUIDv7；时间 UTC。

## 输出
写入 `technology-selection.md` 的 Database / Cache / Vector / Storage / Multi-tenant 段。
