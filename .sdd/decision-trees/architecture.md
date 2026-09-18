# Decision Tree: Architecture（架构选型）

> 配套知识：`.sdd/knowledge/architecture.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## Step 0：项目类型（Matrix §4）
```
API+CRUD+Web UI        → SaaS / Business
AI/LLM/RAG             → AI Application
数据处理/ETL           → Data Application
CLI/SDK/Library        → CLI / Library
高吞吐网络             → High-Concurrency Backend
内部管理系统           → Internal Tool
多服务业务平台         → Distributed System
多类型命中：Primary=业务价值，Secondary=技术特征
```

## Step 1：规模（`knowledge/architecture.md` §1 / `res.md` §3）
```
user_count < 100k AND team_size <= 10 → Small/Medium
否则 Large
```

## Step 2：Monolith vs Modular Monolith vs Microservices（Matrix §5）
```
IF user_count < 100000 AND team_size <= 10
   AND independent_scaling = false AND deployment_complexity low
→ Monolith

IF application_complexity >= medium AND service_independence = low AND team_size <= 20
→ Modular Monolith        # 新企业应用默认 ✅ AUTO

IF (independent_scaling OR independent_deployment OR team_ownership
    OR technology_boundary OR failure_isolation OR workload differs)
   AND microservices_benefit > operational_complexity
→ Microservices           # ⚠️ REQUIRE_CONFIRMATION
ELSE → Modular Monolith
```

**Microservices 检查项**（知识库 §65）：服务边界/团队边界/独立部署/独立扩缩/故障隔离/不同技术栈/单体已成瓶颈——多数为 No → Modular Monolith。

## Step 3：复杂度预算（Matrix §32）
按 `decision-protocol.md` **§5.1 计分表**计算 `complexity_score`：
```
计入：主数据库 +1 / 缓存 +1 / MQ +1 / 对象存储 +1 / 独立调度器 +1
      Kafka +2 / ES·OpenSearch +2 / 专用向量库 +2 / K8s +3 / Microservices +3
不计：语言 / 框架 / ORM / Docker / CI-CD / gRPC / 部署平台
pgvector 作为 PG 扩展 → 不额外计分（独立向量库才 +2）
```
```
MVP 5 / Internal 6 / Small SaaS 8 / Enterprise SaaS 12 / Distributed 20+
IF score > budget → 重新评估，降级组件
```

## Step 4：进阶模式（默认关闭）
Event-Driven / CQRS / Event Sourcing / DDD — 仅当满足知识库 §66-§69 明确条件。否则不引入。

## Step 5：多租户（Matrix §22）
```
users belong to orgs AND isolation required → multi_tenant
默认 Shared DB + tenant_id；强隔离→schema；合规→DB；极端→infra
```

## Step 6：前后端分离（Matrix §9）
SaaS/多终端/Mobile+Web/多 client/大型前端 → 分离；简单 CRUD/SEO/MVP/内部工具 → 可合并（Next.js Full Stack）。

## 输出
写入 `technology-selection.md` 的 Architecture 段；Microservices / K8s / Multi-region 标 `REQUIRE_CONFIRMATION`（decision-protocol §6）。复杂必要性用 ADR 记录。
