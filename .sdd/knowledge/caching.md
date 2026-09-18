# Knowledge: Caching & Search（缓存与搜索）

> 来源：Matrix §23（Caching Matrix）、§17（Search Engine Matrix）、§13（Redis Matrix）；res.md §71-§73。
> 治理：`.sdd/decision-trees/decision-protocol.md`　决策树：`.sdd/decision-trees/infrastructure.md` §4
> 关联：`database.md` §5（Redis 条件）

---

## 1. Cache 决策（Matrix §23）

```
IF read_heavy = true
   AND data_changes_less_frequently = true
   AND cache_hit_benefit = significant
THEN cache = true
ELSE cache = false
```

**不要因为"Redis 很快"默认加入 Redis**（Matrix §23）。
Cache 不是"性能优化默认项"，而是有明确命中收益才引入的组件。

## 2. Redis 引入条件（Matrix §13 → `database.md` §5）

```
Redis = true 仅当 cache / session / rate_limit / distributed_lock / queue / stream / hot_data / temporary_state
IF none_of_above THEN Redis = false
```

原则：**PostgreSQL / MySQL 是 Source of Truth；Redis 只承载性能与临时状态。** 重要业务数据不得只放 Redis。

## 3. Cache 策略（res.md §73）

```
Cache-aside：App → Redis → miss → DB → 写回
```

引入缓存时**必须显式定义**以下五项：

| 项 | 必须回答 |
| --- | --- |
| **TTL** | 每个 key 的过期时间（禁止无 TTL 的永久缓存） |
| **Invalidation** | 写操作后如何失效（删除 key 优于更新 key） |
| **Stale 容忍** | 允许数据旧到什么程度 |
| **Failure 行为** | Redis 不可用时"回源"还是"失败"（必须显式选择） |
| **Key 设计** | 实体 + 版本 + 粒度；**禁止跨租户共享 key** |

## 4. 计分（`decision-protocol §5.1`）

Redis / Cache 组件 **+1**。无缓存需求时引入 Redis 会直接占用复杂度预算，须在 ADR 中说明存在理由。

## 5. Search 决策线（Matrix §17）

```
默认：PostgreSQL Full Text Search
```

只有满足任一条件才考虑 **OpenSearch / Elasticsearch**：

```
full_text_search = complex
OR fuzzy_search = important
OR search_scale = large
OR faceting = complex
OR search_relevance = critical
```

**不要因为"以后可能搜索很多"提前加入搜索集群**（Matrix §17）。
引入 ES / OpenSearch → **+2**（`decision-protocol §5.1`），且必须有"数据库搜索能力不足"的**实测证据**（`decision-protocol §5.1` 的基础设施引入检查表）。

## 6. 与其它文件的分工

| 问题 | 去哪看 |
| --- | --- |
| 要不要 Redis | 本文件 §1-§2 |
| Redis 怎么用（TTL/失效） | 本文件 §3 |
| 全文检索 vs 搜索引擎 | 本文件 §5 |
| Redis 作为队列 | `messaging.md` §4 |
| 向量检索 | `database.md` §6 / `ai-llm.md` §3 |
| 缓存中间件部署 | `deployment.md` |
