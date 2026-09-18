# AGENTS.md — General Agent Engineering Rules

> 通用 Agent 软件工程与 Spec-Driven Development 规则。详细知识库见 `.sdd/`。
> 来源：`sources/v1.0/res.md`（顶层 121 条 + 子条目 11）+ `Matrix`（45 + 14）+ `知识库`（89 + 14）；Agent 总指令见 `知识库 §87`。
> 引用约定见 `.sdd/CONVENTIONS.md`；目录约定见 `.sdd/LAYOUT.md`。

## 0. READ ORDER（读什么、什么顺序）

**任何新项目 / 重大特性，实现前必须按序读取：**

1. `.sdd/LAYOUT.md`（目录约定）+ `.sdd/CONVENTIONS.md`（引用约定）
2. `.sdd/decision-trees/decision-protocol.md`（**约束模型 / 优先级 / 评分 / 复杂度预算 / 决策状态 / 确认门槛 / 决策循环 / 30 条规则**）
3. `.sdd/workflows/new-project.md`
4. `.sdd/knowledge/architecture.md` + `.sdd/decision-trees/architecture.md`
5. `.sdd/decision-trees/backend.md` / `frontend.md` / `database.md` / `infrastructure.md`
6. **按项目类型追加**：
   - AI / LLM / RAG / Agent → `.sdd/knowledge/ai-llm.md` + `.sdd/decision-trees/ai-llm.md`
   - Data / ETL / Pipeline → `.sdd/knowledge/data.md`
   - 涉及缓存或全文检索 → `.sdd/knowledge/caching.md`
7. 用 `.sdd/templates/` 生成 `specs/<id>-<name>/` 下的 `project-discovery.md` → `technology-selection.md` → `spec.md` → `plan.md` → `design.md` → `tasks.md`，并在 `adr/` 记录决策
8. **未解决架构决策前，不得实现代码。**

其他入口：
| 场景 | 流程 |
| --- | --- |
| 新特性 | `.sdd/workflows/new-feature.md` |
| 小改动（见阈值） | `.sdd/workflows/small-change.md` |
| 缺陷修复 | `.sdd/workflows/bugfix.md` |
| 重构 | `.sdd/workflows/refactor.md` |
| 存量项目 | 先按 `res.md §102` 生成 `project-discovery.md`，**不要立即写代码** |

## CORE MISSION（res.md §0）
理解需求 → 识别类型/规模 → 架构决策 → 可解释技术选型 → Spec → Design → Plan → Tasks → 实现 → 验证 → 收敛。保持代码/架构/Spec 一致。

## 决策治理（decision-protocol.md，核心）
- **约束优先级**：用户明确/现有系统/安全合规/部署平台 = P0 Hard Constraint，不可自覆盖；流行度仅 P3 Weak Preference。
- **复杂度预算**：只有"新增需独立部署/运维/故障域的基础设施组件"才计分（组件 +1；Kafka/ES/专用向量库 +2；K8s/Microservices +3；**Docker/框架/ORM/gRPC 不计分**；pgvector 作为 PG 扩展不额外计分）。计分表见 `decision-protocol.md` §5.1；预算：MVP 5 / Internal 6 / Small SaaS 8 / Enterprise SaaS 12 / Distributed 20+。超限重评。
- **决策状态**：每项 `AUTO`/`RECOMMEND`/`REQUIRE_CONFIRMATION`/`BLOCKED`；重大架构决定必须人确认（清单见 `decision-protocol.md` §6）。
- **评分（Matrix §36 原始公式，权重不变）**：`Requirement Fit×40 + Maintainability×20 + Team Fit×15 + Operational Simplicity×15 + Ecosystem×10`；每项 0–5；**Hard Constraint 失败 = 直接淘汰，不是降分**。
- **Cost 复核（本仓补充，源文档未覆盖）**：若方案引入的持续成本（托管费 / GPU / 存储 / 出网流量）超出项目预算档，视为 Soft 否决——必须在 ADR 中写明成本上限与计费方式，或降级方案；**不得静默选择更贵的方案**。个人 / 小预算项目可将 Cost 升为 P1 Strong Constraint。
- **冲突仲裁顺序**：`decision-protocol` > `decision-trees` > `knowledge` > 默认值（见 `decision-protocol.md` §10）。

## 默认技术矩阵（res.md §110 / 知识库 §59,§82）
> res.md §110 的落地版。此前漏掉 `Enterprise Backend` 与 `TS Backend` 两行，导致语言判定可输出 TypeScript（`decision-trees/backend.md` §1）却无框架可依 —— 见 `res.md §13,§81`。
| Category | Default | Alternatives |
| --- | --- | --- |
| Architecture | Modular Monolith | Microservices |
| Backend | Python（AI/Data/CRUD/API）| Go（高并发/Infra）/ TS / Java |
| Python API | FastAPI | Django / Flask |
| Enterprise Backend | Spring Boot | NestJS |
| Go API | net/http（小服务）/ Gin | Echo |
| TS Backend | **NestJS** | Fastify / Hono |
| Frontend | Vue 3 + TS + Vite | React / Next.js |
| React SSR | Next.js | — |
| DB | PostgreSQL | MySQL / SQLite / MongoDB |
| Cache | None | Redis |
| Vector | pgvector | Qdrant/Milvus |
| API | REST + OpenAPI | GraphQL / gRPC |
| Queue | None | RabbitMQ |
| Streaming | None | Kafka |
| Search | PostgreSQL FTS | OpenSearch / Elasticsearch |
| Object Storage | S3 | 本地磁盘 |
| Internal RPC | gRPC | REST |
| Auth | Session / OIDC | JWT |
| Testing | pytest + Vitest + Playwright | — |
| CI/CD | GitHub Actions | GitLab CI |
| Observability | OpenTelemetry | Vendor SDK |
| LLM | 单供应商 direct SDK | 多供应商 → Provider Abstraction |
| 数据编排 | 无依赖 → cron | 有 DAG/回填 → Airflow/Dagster/Prefect |

## 最重要的规则（知识库 §85 / res.md §1.2-§1.4，节选）
1. 不因技术流行而选技术。
2. 不为未来假设需求增加复杂度。
3. 存量项目优先保持已有技术栈。
4. 新项目优先 Modular Monolith。
5. PostgreSQL 是新关系型项目默认。
6. Redis 非默认数据库。
7. REST 是默认 API 风格。
8. TypeScript 是新 Web 前端默认语言。
9. Python 优先 AI/Data/CRUD/API；Go 优先高并发/Infra/Network。
10. 技术选型必须记录理由。
11. 架构决策追溯到 Requirement；Requirement 追溯到 Test；Code 追溯到 Spec。

## 禁止（不得静默决定）
Microservices / Kubernetes / Multi-region / Database migration / Authentication architecture /
Authorization model / Payment / Data residency / Compliance / 云商 / Event-driven / CQRS /
Event Sourcing / Distributed transaction / Public API contract / Breaking API changes / 重大技术迁移
—— 以上一律 `REQUIRE_CONFIRMATION`（`decision-protocol.md` §6）。

## FINAL PRINCIPLE（res.md §120）
技术/架构/Framework/SDD 都不是目的。目标：Correctness + Maintainability + Simplicity + Testability + Observability + Security + Evolvability。无明确需求选最简单成熟方案；复杂需求记录必要性。不要为架构而架构。
