# ADR-001: Use PostgreSQL as Primary Database

> 模板：`.sdd/templates/adr.md`　所属实例：`specs/001-project/`
> 命名约定见 `.sdd/CONVENTIONS.md` §2。

## Status
Accepted

## Decision Status
`AUTO`（未触发 `decision-protocol §6` 的 `REQUIRE_CONFIRMATION` 项）

## Confidence
5 / 5 —— 新关系型项目的默认选择（`知识库` Rule 5、`Matrix §10`），无既有栈约束。

## Decision
使用 **PostgreSQL** 作为主数据库。

## Context
订单管理系统，核心数据为订单 / 订单项 / 用户，存在明确的关系与事务要求（下单、支付的状态流转）。
项目为 Greenfield，无既有数据库迁移成本。

## Constraints
| 类型 | 内容 |
| --- | --- |
| P0 Hard | 无既有数据库约束（Greenfield） |
| P0 Hard | 事务完整性要求覆盖 Money 与关键状态（`res.md §67`） |
| P1 Strong | 需要 JSON 字段与全文检索能力（避免为此单独引入组件） |
| P3 Weak | 团队熟悉度 |

## Alternatives
- PostgreSQL
- MySQL
- MongoDB

## Why PostgreSQL
- 强关系模型与完整事务（ACID），匹配订单/支付的强一致需求
- JSONB 兼顾半结构化字段，减少额外组件
- 内置全文检索，满足 `knowledge/caching.md` §5 的默认搜索档，**无需引入 Elasticsearch**
- 扩展生态丰富（如需向量检索可直接 pgvector，见 `knowledge/ai-llm.md` §3）
- 新关系型项目默认（`知识库` Rule 5）

## Why Not Alternatives
- **MySQL**：无既有组织标准或生态依赖（`Matrix §11` 的触发条件均不成立），Greenfield 下 PostgreSQL 能力更优
- **MongoDB**：领域强关系型（订单 ↔ 订单项 ↔ 用户），文档模型不匹配（`Matrix §12`）

## Risks
- 单实例写入瓶颈 → 缓解：先索引与读写分离；**在有证据前不引入缓存或分库**

## Assumptions
- 单区域部署，暂无数据驻留 / 合规要求（CAN ASSUME，须记录，见 `decision-protocol` §3）
- 数据量在中小规模（未接近需要分区的量级）

## Consequences
- 项目依赖 PostgreSQL 生态（Alembic 迁移、psycopg 驱动）
- 后续若改用其它数据库 = 架构级变更 → `REQUIRE_CONFIRMATION`
- **Reversibility：Low**（数据迁移成本高）

---

## 索引
- `ADR-001-postgres.md` — 主数据库选 PostgreSQL
- `ADR-002-fastapi.md` — 后端框架选 FastAPI
- `ADR-003-session-auth.md` — 认证采用 Session
