# AGENTS.md — General Agent Engineering Rules

> 通用 Agent 软件工程与 Spec-Driven Development 规则。详细知识库见 `.sdd/`。
> 来源：`sources/v1.0/res.md`（顶层 121 条 + 子条目 11）+ `Matrix`（45 + 14）+ `知识库`（89 + 14）+ `mod_gpt.md`（9 条可执行性改进）+ `modv2.md`（22 项复核）；Agent 总指令见 `知识库 §87`。
> **规则归属**：本文件与 `CLAUDE.md` 是 Agent 入口，**只引用、不重新定义**行为语义（见 `.sdd/CANONICAL.md`）。
> 引用约定见 `.sdd/CONVENTIONS.md`；目录约定见 `.sdd/LAYOUT.md`。
> 本文件定位：**规则摘要 + 目录索引（table of contents）**，不追求穷尽 —— 细节在 `.sdd/`。

## 0. READ ORDER（读什么、什么顺序）

**任何新项目 / 重大特性，实现前必须按序读取**（顺序按 `mod_gpt.md §1` 修正：Spec 前置）：

1. `.sdd/LAYOUT.md`（目录约定）+ `.sdd/CONVENTIONS.md`（引用约定）
2. `.sdd/workflows/new-project.md`（流程细则）
3. 用 `.sdd/templates/project-discovery.md` 生成 `project-discovery.md`
4. 基于 Discovery 生成 **Draft `spec.md`**（WHAT/WHY/NFR/Hard Constraints/Acceptance Criteria/Open Questions，**不写技术实现**）
5. **Draft Spec 足以支撑架构判断后**，才读决策材料：
   - `.sdd/decision-trees/decision-protocol.md`（**约束模型 / 优先级 / 评分标尺 / 复杂度预算 / 决策状态 / 确认门槛 / 决策循环 / 30 条规则**）
   - `.sdd/knowledge/architecture.md` + `.sdd/decision-trees/architecture.md`
   - `.sdd/decision-trees/backend.md` / `frontend.md` / `database.md` / `infrastructure.md`
   - **按项目类型追加**：
     - AI / LLM / RAG / Agent → `.sdd/knowledge/ai-llm.md` + `.sdd/decision-trees/ai-llm.md`
     - Data / ETL / Pipeline → `.sdd/knowledge/data.md`
     - 涉及缓存或全文检索 → `.sdd/knowledge/caching.md`
     - 任何新项目（版本问题）→ `.sdd/knowledge/versioning.md`
     - 存量系统改动 / 影响面不明 → `.sdd/decision-trees/impact-analysis.md`
     - SaaS 多租户 → `.sdd/knowledge/multi-tenancy.md`
     - 可用性 / RPO·RTO / 容错重试 → `.sdd/knowledge/reliability.md`
     - PII / 留存删除 / 合规驻留 → `.sdd/knowledge/data-lifecycle.md`
     - 外部系统集成（第三方 API / 回调） → `.sdd/knowledge/integration.md`
     - 配置与密钥 → `.sdd/knowledge/configuration.md`
     - 引入第三方依赖 → `.sdd/knowledge/dependency-management.md`
6. 生成 `technology-selection.md` + `decision.json`（Hard Constraint elimination → Candidates → Decision Status → Complexity Budget）
7. 对 `REQUIRE_CONFIRMATION` 项请求人工确认（其余状态不阻塞）
8. 完成 Final `spec.md`（`Accepted`）→ `plan.md` → `design.md`（按需）→ `adr/`（按需）→ `tasks.md`
9. **未解决 `BLOCKED` / `REQUIRE_CONFIRMATION` 决策前，不得实现代码。**

其他入口：
| 场景 | 流程 |
| --- | --- |
| 新特性 | `.sdd/workflows/new-feature.md`（**Impact Analysis 前置**） |
| 小改动（见阈值） | `.sdd/workflows/small-change.md` |
| 缺陷修复 | `.sdd/workflows/bugfix.md` |
| 重构 | `.sdd/workflows/refactor.md` |
| 存量项目 | 先按 `res.md §102` 生成 `project-discovery.md`，**不要立即写代码** |

## CORE MISSION（res.md §0）
理解需求 → 识别类型/规模 → 架构决策 → 可解释技术选型 → Spec → Design → Plan → Tasks → 实现 → 验证 → 收敛。保持代码/架构/Spec 一致。

## 决策治理（decision-protocol.md，核心）

- **约束优先级 P0A / P0B / P1 / P2 / P3**（`decision-protocol.md` §2）：
  - **P0A**：安全 / 法规合规 / 技术可行性 / 平台不可能性 —— 不可违反，**用户偏好不能覆盖**。
  - **P0B**：用户显式不可协商约束 / 现有系统硬兼容 —— Agent 不得自行覆盖。
  - P1 功能·性能·数据特征·团队能力；P2 可维护性·简单性·成本；P3 生态·流行度·个人偏好。
- **用户表达分级**：用户说"偏好 / 熟悉 / 倾向 / 最好用" → **Preference**（P3/P2），**不构成 Hard Constraint**；
  只有"必须 / 不得 / 组织标准 / 不可改变"才升级为 Hard Constraint（`decision-protocol.md` §3.1）。
  反例（不应照做）：用户要求 EOL 框架、SQLite 承担高并发写、明文存 token、禁止备份 —— 这些撞 P0A，必须提出异议。
- **复杂度预算**：只有"新增需独立部署/运维/故障域的基础设施组件"才计分（组件 +1；Kafka/ES/专用向量库 +2；K8s/Microservices +3；**Docker/框架/ORM/gRPC 不计分**；pgvector 作为 PG 扩展不额外计分）。计分表见 `decision-protocol.md` §5.1；预算：MVP 5 / Internal 6 / Small SaaS 8 / Enterprise SaaS 12 / Distributed 20+。超限重评。
- **决策状态**（`decision-protocol.md` §6）：`AUTO` 直接执行并记录；`RECOMMEND` **采用推荐方案继续执行**，同时记录 alternatives / assumptions / reversibility，**不阻塞**；`REQUIRE_CONFIRMATION` 必须人确认；`BLOCKED` 仅在缺失信息会导致重大、不可逆或高风险决策且**无安全可逆默认值**时才停止。
- **默认值语义**（`decision-protocol.md` §3.4）：`DEFAULT does not mean SELECTED.`
  默认值 = **候选先验（candidate prior）**，不是决策结果；它必须让位于现有栈与团队已证实专长，且不得绕过 Hard Constraint 淘汰。
- **评分（`Matrix §36` 原始公式，权重不变）**：`Requirement Fit×40 + Maintainability×20 + Team Fit×15 + Operational Simplicity×15 + Ecosystem×10`；
  每项 0–5，**必须按 `decision-protocol.md` §4.1 的 rubric 打分**；**Hard Constraint 失败 = 直接淘汰，不是降分**；
  且**评分是 tie-break/比较工具，不是决策本身** —— 仅在消除后仍 ≥2 候选且规则无法区分时才评分，不为用公式而制造候选。
- **版本策略**（`knowledge/versioning.md`）**只有一处实现**：语言/框架/数据库/镜像的版本选择都查它，
  各领域文件不自建版本策略；**不写死版本号**，不编造版本，未核实写 `UNKNOWN`。
- **Cost 复核（本仓补充，源文档未覆盖）**：若方案引入的持续成本（托管费 / GPU / 存储 / 出网流量）超出项目预算档，视为 Soft 否决——必须在 ADR 中写明成本上限与计费方式，或降级方案；**不得静默选择更贵的方案**。个人 / 小预算项目可将 Cost 升为 P1 Strong Constraint。（`decision-protocol.md` §4.2）
- **冲突仲裁顺序**：`decision-protocol` > `decision-trees` > `knowledge` > 默认值（见 `decision-protocol.md` §10）。

## 默认技术矩阵（res.md §110 / 知识库 §59,§82）
> res.md §110 的落地版。**读法见 `decision-protocol.md` §3.4：下表是 candidate prior，不是 SELECTED。**
> 它有四个作用：进入候选集 / 无区分度时兜底 / 与现有栈或团队专长冲突时让位 / 不得绕过 Hard Constraint 淘汰。
> 此前漏掉 `Enterprise Backend` 与 `TS Backend` 两行，导致语言判定可输出 TypeScript（`decision-trees/backend.md` §1）却无框架可依 —— 见 `res.md §13,§81`。

| Category | Default（候选先验） | Alternatives |
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
| 版本 | 见 `.sdd/knowledge/versioning.md` | — |

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
12. **Spec 先于技术选型**：先 WHAT/WHY，再 HOW；不写技术实现的 Draft Spec 是正常产物，不是未完成品。

## 禁止（不得静默决定）
Microservices / Kubernetes / Multi-region / Database migration / Authentication architecture /
Authorization model / Payment / Data residency / Compliance / 云商 / Event-driven / CQRS /
Event Sourcing / Distributed transaction / Public API contract / Breaking API changes / 重大技术迁移（含破坏性版本升级）
—— 以上一律 `REQUIRE_CONFIRMATION`（`decision-protocol.md` §6）。

> 反向约束（`mod_gpt.md §2`）：**上述清单之外**的语言、框架、ORM、测试工具、包管理器、缓存是否引入等，
> 属 `AUTO`/`RECOMMEND`，Agent **应自行选择并记录，不应逐个征询用户**。把一切都升级为"要人确认"会让 AUTO 失去意义。

## DEFINITION OF DONE（修改本规则库时）
> 来源：`mod_gpt.md §9`。本仓是**规则库**，改动它的"完成"标准与写业务代码不同。

1. 运行：
   ```bash
   python3 scripts/gen_traceability.py      # 先重建索引（改了引用就必须重跑）
   python3 scripts/validate_rules.py        # 再自检
   ```
2. 必须达到：
   - **0 errors，0 warnings**
   - **无失效文件引用**（反引号内 `.md` / `specs/*/decision.json` 指向真实文件）
   - **无互相冲突的 canonical rules**（同一件事只能有一个权威文件，见 `.sdd/CANONICAL.md`）
   - **Canonical 不变量全部通过**（归属矩阵与登记表一致 / 流程顺序 / 决策状态旧语义未回流 / 必填产物有模板）
   - **版本号三处一致**（`.sdd/VERSION` ≡ `README.md` ≡ `CHANGELOG.md` 最新版本）
   - `TRACEABILITY.md` 与当前引用一致（否则就是过期索引，比缺失更有害）
3. 若修改了以下内容，**必须同步**：

   | 改了什么 | 必须同步 |
   | --- | --- |
   | Layout / 目录结构 | `.sdd/LAYOUT.md` |
   | Decision semantics（状态 / 优先级 / 评分 / 预算） | `.sdd/decision-trees/decision-protocol.md` |
   | Technology rule（某技术支持什么、默认是什么） | `.sdd/knowledge/` 与 `.sdd/decision-trees/` |
   | User-facing behavior（读取顺序、流程分流、确认门槛） | `CLAUDE.md` / `AGENTS.md` |
   | Rule source mapping（引用来源条号） | 重跑 `scripts/gen_traceability.py` 更新 `.sdd/TRACEABILITY.md` |
   | Public rule behavior（对外可见的规则变更） | `CHANGELOG.md` |
   | 版本策略 | `.sdd/knowledge/versioning.md`（**不要**在领域文件里另写一份） |
   | **规则库版本号** | `.sdd/VERSION`（唯一来源）→ 同步 `README.md` / `.sdd/README.md` / `CHANGELOG.md` |
   | **Canonical 归属**（哪份文件说了算） | `.sdd/CANONICAL.md` + `scripts/validate_rules.py` 的 `CANONICAL_TOPICS` |
   | Verification 结构 | `.sdd/templates/verification.md` + `.sdd/schema/verification.schema.json` |
   | 新增知识域 / 决策树 | `.sdd/README.md` 与 `.sdd/LAYOUT.md` 的目录清单（含数量） |
   | 新增引用来源 | 先在 `.sdd/CONVENTIONS.md` §1 登记前缀，再使用 |

4. 校验器不认识某条 Schema 关键字时会**报错而非静默跳过**（`scripts/mini_schema.py`）；
   遇到该报错应扩展 `SUPPORTED_KEYWORDS`，不要删检查。

## FINAL PRINCIPLE（res.md §120）
技术/架构/Framework/SDD 都不是目的。目标：Correctness + Maintainability + Simplicity + Testability + Observability + Security + Evolvability。无明确需求选最简单成熟方案；复杂需求记录必要性。不要为架构而架构。
