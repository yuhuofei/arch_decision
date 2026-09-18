# Decision Tree: Database（数据库选型）

> 配套知识：`.sdd/knowledge/database.md`

## 起点：主数据库选什么？

```
数据主要是关系型 + 需要事务 / 强一致性 / 复杂关系 / JSONB？
├─ 是 ──→ 已有 MySQL 基础设施 / 已有 DBA 专长 / Vendor 要求？
│         ├─ 是 ──→ MySQL
│         └─ 否 ──→ PostgreSQL（默认主数据库）
├─ 否 ──→ Document-oriented / Dynamic schema / Nested document / 特定 Mongo 生态？
│         └─ 是 ──→ MongoDB（仅当 domain 明确适合 document model；否则仍 PostgreSQL）
└─ 否 ──→ CLI / Desktop / Local-first / Prototype / Test / Embedded？
          └─ 是 ──→ SQLite（不选：多实例生产 API / 高写并发 / 分布式后端）

AI / RAG 向量检索？
├─ 默认 ──→ PostgreSQL + pgvector
└─ 规模/查询特征明确需要 ──→ Qdrant / Weaviate / Milvus / Pinecone

文件存储？
└─ 始终 ──→ 对象存储（S3-compatible）；数据库只存 object_key/filename/mime_type/size/metadata
```

## Redis 是否作为 Cache（§27）
```
是否存在 Hot data / 频繁读 / Rate limiting / 分布式锁 / Session / Temporary state？
├─ 是 ──→ 引入 Redis（必须定义 TTL / invalidation / cache miss / failure 行为 / 是否允许 stale）
└─ 否 ──→ 不引入（"以后可能缓存"不是理由）
```
> 注意：Redis 不是 Primary Database。

## 关键判定
- PostgreSQL（§23）默认；MySQL（§24）仅当已有约束；SQLite（§25）仅本地/嵌入；MongoDB（§26）仅 document model。
- 设计默认第三范式（§66）；事务覆盖 Money/Inventory/Permission/关键状态（§67）。
- ID 默认 UUID/UUIDv7/DB-generated（§68）；时间 UTC 存储（§69）。

## 输出
写入 `technology-selection.md` 的 Database / Cache / Vector / Storage 段。
