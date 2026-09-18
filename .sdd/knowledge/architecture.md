# Knowledge: Architecture（架构）

> 来源：res.md §1.1, §3, §4, §21, §77
> 决策树：`.sdd/decision-trees/architecture.md`

## 1. Simple Before Complex（§1.1）

默认优先级：

```
Modular Monolith  >  Monolith  >  Microservices
```

仅在存在**明确需求**时引入复杂组件：

- Microservices、Kubernetes、Kafka、Elasticsearch、Redis、GraphQL、gRPC、Event Sourcing、CQRS、Service Mesh、Distributed Transactions。

**禁止**因以下理由增加技术组件：

- "以后可能需要" / "方便扩展" / "这是大厂架构" / "性能更好" / "比较现代" / "业界流行"。

## 2. Project Scale Classification（§3）

| 规模 | 典型特征 | 默认架构 |
| --- | --- | --- |
| Small | 1-3 人 / <10k 用户 / <100 RPS / <10GB 主库 / 单一业务域 | Modular Monolith + PostgreSQL + Docker（Redis 可选） |
| Medium | 3-10 人 / 10k-1M 用户 / 100-2000 RPS / 10GB-1TB | Modular Monolith + PG + Redis(按需) + 对象存储 + 后台 Worker |
| Large | >10 人 / >1M 用户 / >2000 RPS / >1TB / 多业务域 | 考虑服务拆分、读副本、分布式缓存、MQ、搜索集群、K8s（逐项证明必要性） |

## 3. Modular Monolith（§4.1, DEFAULT）

新项目默认。推荐结构：

```
src/
├── modules/
│   ├── users/
│   ├── orders/
│   ├── payments/
│   └── notifications/
├── shared/
├── infrastructure/
└── main/
```

每个 Module：

```
module/
├── domain/
├── application/
├── infrastructure/
├── api/
└── tests/
```

**什么时候选**：MVP / SaaS / CRUD / Admin / Enterprise App / 中小型系统 / 业务边界尚未稳定 / 小团队。
**什么时候不要选**：存在明确独立扩容、独立部署、独立团队、强故障隔离、极高吞吐、不同运行时需求。

**Agent 提问**：是否有必须独立部署的模块？不同团队负责不同模块？不同语言/runtime？是否需要独立扩容？

## 4. Microservices（§4.2）

**不是默认架构。** 至少满足一个强条件才选：独立部署 / 独立扩缩容 / 独立 team ownership / 故障隔离 / 明确 bounded context / 极高吞吐 / 不同技术栈。

**绝对不要优先选**：MVP / 1-3 人团队 / CRUD / 业务边界不明确 / 无独立部署需求。

**Agent 提问**：为什么不能 Modular Monolith？哪些服务必须独立部署/扩容？如何做分布式事务？observability？service discovery？retry？idempotency？

## 5. Frontend/Backend Coupling（§21）

- 需要前后端分离：Web + Mobile / API consumers > 1 / 前端复杂度 medium+。
- 不需要分离：小型内部工具 / 简单 CRUD / 简单 CMS / MVP / server-rendered app。不要为"架构标准"强行分离。

## 6. Monorepo（§77）

什么时候选：Frontend + Backend / 共享类型 / 多应用 / 共享包。

```
apps/
├── web
├── api
└── worker
packages/
├── types
├── ui
└── config
```
