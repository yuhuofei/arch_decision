# Knowledge: Database（数据库）

> 来源：res.md §22-§27, §39, §40, §66-§69
> 决策树：`.sdd/decision-trees/database.md`

## 1. Database Decision（§22）

候选：PostgreSQL / MySQL / SQLite / MongoDB / Redis / Specialized DB。

## 2. PostgreSQL（§23, DEFAULT Primary Database）

新项目默认 PostgreSQL。
选：SaaS / ERP / CRM / E-commerce / Enterprise / 金融类事务系统 / 复杂关系数据 / JSONB 需求。
不选：仅当存在明确理由（已有 MySQL 基础设施 / Vendor 要求 / 特殊负载）。
优势：ACID / Relational / JSONB / Full-text search / Extensions / 成熟生态。

**Agent 提问**：数据是否复杂关系？是否需要事务？JSON？全文搜索？强一致性？

## 3. MySQL（§24）

选：已有 MySQL 生态 / 已有 DBA 专长 / 已有应用迁移 / Vendor 要求。新项目无约束 → PostgreSQL 优先。

## 4. SQLite（§25）

选：CLI / Desktop / Local-first / Prototype / Test / Embedded。
不选：多实例生产 API / 高写并发 / 分布式后端。

## 5. MongoDB（§26）

选：Document-oriented / Dynamic schema / Nested document / Event·document 存储 / 特定 Mongo 生态。
不选：强关系数据 / 金融事务 / 复杂 join / 强一致性为核心。默认 PostgreSQL > MongoDB，除非 domain 明确适合 document model。

## 6. Redis（§27）

**不是 Primary Database。** 用途：Cache / Session / Rate limit / Distributed lock / Pub-Sub / Temporary state。
选：Hot data / 频繁读 / Rate limiting / 分布式锁 / Session / Temporary state。
不选：如果只是"以后可能缓存"。必须定义 TTL / invalidation / cache miss strategy / Redis failure 行为 / 是否允许 stale data。

## 7. Vector Search（§39）

AI/RAG 默认优先 `PostgreSQL + pgvector`。仅当规模与查询特征明确需要时引入 Qdrant / Weaviate / Milvus / Pinecone。

## 8. Object Storage（§40）

文件默认对象存储（S3-compatible）。不要把大文件直接存 PostgreSQL。数据库保存 object_key / filename / mime_type / size / metadata。

## 9. DB Design Rules（§66）

默认第三范式优先；为读性能可合理反规范化。**禁止**为"灵活"把所有字段塞进 JSON。

## 10. Transaction Rules（§67）

涉及 Money / Inventory / Permission / 关键状态转移 → 必须考虑 transaction。

## 11. ID Strategy（§68）

默认 UUID / UUIDv7 / DB-generated ID（按分布式生成/排序/安全/存储选择）。不要暴露敏感业务序号作为安全边界。

## 12. Time（§69）

所有后端 UTC 存储；API 用 ISO 8601；用户显示用 local timezone。
