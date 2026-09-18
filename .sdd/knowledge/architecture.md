# Knowledge: Architecture（架构）

> 来源：res.md §1.1,§3,§4,§4.1,§21,§77；Matrix §3-§5,§22,§32；知识库 §3,§4.1-§4.2,§12.1,§65-§70
> 决策树：`.sdd/decision-trees/architecture.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## 0. 决策治理（先看）
- 约束优先级 P0–P3、Hard/Soft Constraint、复杂度预算、决策状态见 `decision-protocol.md`。
- **默认优先 Modular Monolith**（知识库 Rule 4）。

## 1. 项目类型矩阵（Matrix §4 / 知识库 §4）
| 条件 | Project Type |
| --- | --- |
| API + CRUD + Web UI | SaaS / Business Application |
| AI / LLM / RAG | AI Application |
| 数据处理 / ETL | Data Application |
| CLI / SDK / Library | CLI / Library |
| 高吞吐网络服务 | High-Concurrency Backend |
| 内部管理系统 | Internal Tool |
| Mobile / Realtime / IoT / Infra / Automation / 多服务 | 对应类型 |

多类型命中：`Primary = 主要业务价值`，`Secondary = 技术特征`（如 AI SaaS：Primary=SaaS，Secondary=AI/RAG）。

**类型 → 知识文件落点**：
| Project Type | 必读知识文件 |
| --- | --- |
| AI Application（AI/LLM/RAG/Agent） | `knowledge/ai-llm.md` + `decision-trees/ai-llm.md` |
| Data Application（ETL/Data Pipeline/Analytics） | `knowledge/data.md` |
| 需要缓存或搜索 | `knowledge/caching.md` |
| 其余类型 | `knowledge/{backend,frontend,database,api,...}.md` 对应部分 |

## 2. Architecture Decision Matrix（Matrix §5，正式条件）

### 2.1 Monolith（默认）
```
IF user_count < 100000 AND team_size <= 10
   AND independent_scaling = false AND deployment_complexity must_be_low
THEN architecture = Monolith
```
适用：MVP / 内部系统 / 普通 CRUD / 早期 SaaS / 管理后台 / 简单 API。

### 2.2 Modular Monolith（新企业应用默认）
```
IF application_complexity >= medium AND service_independence = low AND team_size <= 20
THEN architecture = Modular Monolith
```
部署：1 application + 1 database + multiple modules。模块示例：Auth/Users/Billing/Orders/Notifications/Reporting。
结构见 `backend.md` 的 Modular Monolith 推荐布局。

### 2.3 Microservices（非默认）
```
IF (independent_scaling OR independent_deployment OR team_ownership_boundary
    OR technology_boundary OR failure_isolation OR workload_profile differs)
   AND microservices_benefit > operational_complexity
THEN Microservices
ELSE → Modular Monolith（REJECT）
```
**不得**因"未来可能扩展"直接选 Microservices（知识库 Rule 2）。检查项：服务边界/团队边界/独立部署/独立扩缩/故障隔离/不同技术栈/单体已成实际瓶颈——多数为 No 则 Modular Monolith（知识库 §65）。

## 3. 复杂度预算（Matrix §32）
**计分口径见 `decision-protocol.md` §5.1（唯一权威）**：只有"新增需独立部署/运维/故障域的基础设施组件"才 +1（Kafka/ES/专用向量库 +2；K8s/Microservices +3）。
**不计分**：语言、框架、ORM、Docker/Docker Compose、CI/CD、gRPC、部署平台。
**pgvector 作为 PG 扩展不额外计分**；独立向量库才 +2。
预算：MVP 5 / Internal 6 / Small SaaS 8 / Enterprise SaaS 12 / Distributed 20+。超限必须重评。

## 4. 进阶架构模式（知识库 §66-§69，默认关闭）
- **Event-Driven**：仅业务天然存在 Domain Event 时（订单→库存→支付→物流→通知）；否则不为"先进"引入 Event Bus。
- **CQRS**：仅读写模型差异巨大 / 复杂查询 / 高读写不对称 / 事件驱动 / 审计需求。
- **Event Sourcing**：仅需完整不可变历史 + 状态可重建 + 审计。
- **DDD**：建模方法而非默认架构；仅复杂业务/领域模型/大量业务规则。简单 CRUD 不需要 Aggregate/Domain Event 等。
- 默认不要使用（知识库 §83）：Kubernetes / Kafka / ES / Service Mesh / CQRS / Event Sourcing / Microservices / GraphQL / gRPC / 专用 Vector DB / 多数据库 / 多缓存。

## 5. 多租户（Matrix §22）
`users belong to organizations AND data isolation required → multi_tenant = true`。
| 需求 | 策略 |
| --- | --- |
| Small/Medium SaaS | Shared DB + tenant_id（默认） |
| 强隔离 | Separate schema |
| 合规隔离 | Separate database |
| 极端隔离 | Separate infrastructure |

## 6. 前后端分离（res.md §21 / Matrix §9）
- 分离：SaaS / 多终端 / Mobile+Web / 多 client / 大型前端 / AI API+Web。
- 合并（可接受）：简单 CRUD / SEO 网站 / MVP / 内部工具 / Next.js Full Stack。

## 7. Monorepo（res.md §77 / 知识库 §54）
适用 frontend+backend / shared packages；工具 pnpm workspace / Turborepo / Nx。**不要为两个目录引入复杂 Monorepo 工具**。

## 8. Agent 不得自行做的决定（知识库 §71）
未授权不得自行改变：Database / Architecture / Authentication / Deployment Platform / Cloud Provider / Message Broker / Public API / Programming Language。
