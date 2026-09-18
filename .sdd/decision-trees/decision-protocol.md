# Decision Protocol（决策治理协议）

> 本文件是跨领域决策的"元规则"，应用于所有 decision-trees 与 knowledge 文件。
> 来源：Matrix §1-§2, §32, §36, §40-§44；知识库 §71-§73, §81, §85。
> 引用约定见 `.sdd/CONVENTIONS.md`：`Matrix §N` = Matrix 文档章节；`res.md §N` = res.md 规则条号。
> 配套：`.sdd/decision-trees/*.md`（领域树）、`.sdd/templates/technology-selection.md`（输出 schema）。

---

## 1. Agent 总决策协议（Matrix §1）

Agent **不允许**直接从技术栈名称开始决策。顺序：

```
INPUT
  ↓
Project Classification
  ↓
Hard Constraints
  ↓
Architecture Decision
  ↓
Backend → Frontend → Data → Infrastructure
  ↓
Testing / Observability / Security
  ↓
Architecture Validation（含复杂度预算）
  ↓
ADR
  ↓
plan.md
```

每个重大技术决策必须输出（Matrix §1）：

```yaml
decision:
reason:
evidence:
alternatives:
rejected:
constraints:
risks:
confidence:
```

---

## 2. 决策优先级（Matrix §2）

规则冲突时按以下优先级执行：

| Priority | Rule | 类型 |
| --- | --- | --- |
| P0 | Existing system constraints | Hard Constraint |
| P0 | Security / Compliance | Hard Constraint |
| P0 | Explicit user requirement | Hard Constraint |
| P0 | Deployment / platform constraint | Hard Constraint |
| P1 | Functional requirements | Strong Constraint |
| P1 | Performance requirements | Strong Constraint |
| P1 | Data characteristics | Strong Constraint |
| P1 | Team expertise | Strong Constraint |
| P2 | Maintainability | Preference |
| P2 | Testability | Preference |
| P2 | Operational simplicity | Preference |
| P3 | Ecosystem maturity | Preference |
| P3 | Developer popularity | Weak Preference |

**禁止：**

```
Popularity > Requirement
Framework preference > Existing system
Personal preference > Explicit requirement
Architecture fashion > Simplicity
```

---

## 3. Hard / Soft Constraint（Matrix §3）

### 3.1 Hard Constraint（不允许 Agent 自行覆盖）
满足任一即 Hard Constraint：用户明确指定 / 现有系统强依赖 / 法规合规 / 部署平台限制 / 数据库兼容 / 必须支持的第三方系统 / 性能 SLA / 安全要求 / 组织标准。

### 3.2 Soft Constraint（可比较，不能覆盖 Hard）
团队熟悉度 / 开发效率 / 生态成熟度 / 维护成本 / 学习成本 / 社区活跃度 / 性能余量 / 未来扩展性。

### 3.3 消除与评分
1. 先**消除**所有违反 Hard Constraint 的候选；
2. 在剩余候选中用 `decision-protocol §4` 评分，选**最简单满足需求**者（`decision-protocol §8` 规则 6）。

---

## 4. 技术选型评分（Matrix §36 / 知识库 §72）

多个候选都满足 Hard Constraint 时：

```
Score =
  Requirement Fit        × 40
+ Maintainability        × 20
+ Team Fit              × 15
+ Operational Simplicity × 15
+ Ecosystem             × 10
```

每项 0–5。**Hard Constraint 失败 = 直接淘汰**，不是降分。
### 4.1 Cost 复核（本仓补充，源文档未覆盖）

Matrix §36 的评分未含成本维度。为避免"选出技术上最优但成本失控"的方案，追加以下**复核步骤（不改动上式权重）**：

```
IF 方案的持续成本（托管服务费 / GPU / 存储 / 出网流量）超出项目预算档
THEN 视为 Soft 否决：
     必须 (a) 在 ADR 写明成本上限与计费方式，或 (b) 降级方案
     不得静默选择更贵的方案
```

- **个人 / 小预算项目**：Cost 可升为 **P1 Strong Constraint**（与性能、团队专长同级）。
- 计费口径必须可量化（按 token / 按 GB / 按小时），禁止"大概不贵"这类判断。
- 与复杂度预算（`decision-protocol §5`）的分工：**复杂度预算管"多不多"，本节（Cost 复核）管"贵不贵"**，两者都要过。


---

## 5. 架构复杂度预算（Matrix §32）

### 5.1 计分表（唯一口径）

**计分原则：只有"新增一个需要独立部署、独立运维、独立故障域的基础设施组件"才 +1。**
语言、框架、打包方式、协议、设计模式**一律不计分**——它们不增加运维面。

| 计入 `complexity_score` | 分值 | 不计入 | 理由 |
| --- | ---: | --- | --- |
| 主数据库（PostgreSQL / MySQL） | +1 | 语言（Python/Go/TS/Java/Rust） | 非基础设施组件 |
| 缓存（Redis / Memcached） | +1 | 框架（FastAPI/Next.js/Gin/Spring） | 非基础设施组件 |
| 消息队列（RabbitMQ / Redis Queue 独立实例） | +1 | ORM（SQLAlchemy/Prisma/sqlc） | 代码内库 |
| 对象存储（S3/MinIO/R2/OSS/COS） | +1 | Docker / Docker Compose | **打包方式**，非新增组件 |
| 独立调度器（Airflow/Celery Beat/独立 Worker 集群） | +1 | CI/CD（GitHub Actions 等） | 构建期，不影响运行时架构 |
| Kafka | +2 | 部署平台（VM / Cloud Run / ECS / Docker） | 承载方式，非新增组件 |
| Elasticsearch / OpenSearch | +2 | gRPC | 进程内协议，非独立组件 |
| 专用向量库（Qdrant/Weaviate/Milvus） | +2 | 迁移工具（Alembic/Flyway） | 工具链 |
| Kubernetes | +3 | 第三方 SaaS（Auth0/Stripe 等托管服务） | 外部托管，不自运维 |
| Microservices（相对单体新增的部署单元数按 +3 计） | +3 | — | — |

**pgvector 归属规则（消除此前歧义）**：
```
pgvector 作为 PostgreSQL 扩展（同实例）        → 不额外计分（已计入主数据库 +1）
独立部署的向量数据库实例                        → +2
```

**同一组件只计一次**：多实例 / 主从 / 读写分离不重复计分。

### 5.2 预算对照

超过预算必须重新评估（降级组件或记录必要性）。

| Project | Budget |
| --- | ---: |
| MVP | 5 |
| Internal Tool | 6 |
| Small SaaS | 8 |
| Enterprise SaaS | 12 |
| Distributed System | 20+ |

> 这是**架构复杂度控制机制**，不是性能评分。

### 5.3 计分示例（口径示范）

```
Small SaaS：PostgreSQL(1) + 对象存储(1) = 2 / 预算 8          ✅
AI SaaS  ：PostgreSQL(1) + pgvector(0,扩展) + 对象存储(1) = 2 / 预算 8   ✅
高并发服务：PostgreSQL(1) + Redis(1) = 2 / 预算 8             ✅（gRPC 不计）
超限示例 ：PostgreSQL(1) + Redis(1) + Kafka(2) + ES(2) + K8s(3) = 9 > Small SaaS 8  ⚠️ 必须重评
```

> Docker / Docker Compose **不计分**——早期版本中曾有示例把 Docker 计入，已统一为本表口径。

### 基础设施引入检查表（Matrix §33 / 知识库 §83）
```
1. What requirement requires it?
2. Why existing components cannot satisfy it?
3. What operational cost does it introduce?
4. What happens if it fails?
5. How will it be tested?
6. How will it be monitored?
7. Can it be removed later?
```
无法回答 → REJECT。原则：**每个基础设施组件必须有文档化存在理由。**

---

## 6. 决策状态（Matrix §41）

每个决策必须标记：

| Status | 含义 | Agent 行为 |
| --- | --- | --- |
| `AUTO` | 可自动决定 | 直接执行并记录 |
| `RECOMMEND` | 可提方案 | 提出方案，建议人确认 |
| `REQUIRE_CONFIRMATION` | 重大架构影响 | **必须人确认，不得静默决定** |
| `BLOCKED` | 信息不足 | 停止，请求澄清 |

### 默认 REQUIRE_CONFIRMATION 的决策（Matrix §42）
Microservices / Kubernetes / Multi-region / Database migration / Authentication architecture / Authorization model / Payment / Data residency / Compliance / 主流云商 / Event-driven / CQRS / Event sourcing / Distributed transaction / Public API contract / Breaking API changes / 重大技术迁移。

> 规则：存在多个合理方案时，不假装只有唯一正确答案，应列出 Alternatives 与 Trade-offs（知识库 Rule 15）。
### 6.1 BLOCKED 澄清问题模板（本仓补充）

状态为 `BLOCKED`（信息不足）时，**不得猜测后继续**，也不得泛泛地问"能再详细说说吗"。按下列模板提出**最小必要问题集**：

```
【阻塞点】<一句话说明哪一项决策无法进行>
【为什么阻塞】<缺少哪个信息，导致哪个规则无法判定>
【需要你确认】（最多 3 个，每个给出选项）
  1. <问题>            A) ...  B) ...  C) 不确定
  2. <问题>            A) ...  B) ...  C) 不确定
  3. <问题>            A) ...  B) ...  C) 不确定
【若暂不确定的默认处理】<将按 [假设] 继续，并在 assumptions 中记录；影响架构时则必须等待>
```

判定标准（与 `res.md §108` 的 QUESTION POLICY 对应）：

| 问题类型 | 处理 |
| --- | --- |
| 影响架构（规模 / 一致性 / 安全 / 合规 / 核心流程 / 部署 / 既有栈 / 性能） | **MUST ASK**，即 `BLOCKED`，停在原地等答复 |
| 影响实现（Auth / Storage / Email / Search / Queue） | **SHOULD ASK**，可给默认值并标记 `RECOMMEND` |
| 低风险（格式化 / 命名 / 基础结构） | **CAN ASSUME**，直接假设，但**必须写入 ADR 的 Assumptions** |

禁止：把 MUST ASK 的问题降级为 CAN ASSUME 以"加快进度"（`res.md §44` 规则 27-28）。


---

## 7. Agent 决策循环（Matrix §43）

```
1. Read requirements
2. Classify project
3. Extract hard constraints
4. Extract soft constraints
5. Detect existing stack
6. Generate candidates
7. Eliminate hard-constraint violations
8. Score remaining candidates
9. Select simplest sufficient architecture
10. Generate ADR
11. Mark confidence
12. Identify human-confirmation decisions
13. Generate plan.md
14. Generate tasks.md
15. Run consistency analysis (spec → plan → tasks)
```

---

## 8. 最终 Agent 规则（Matrix §44，节选核心 30 条）

1. 理解需求前不选技术。
2. 存量项目约束优先于通用默认值。
3. 用户明确要求是 Hard Constraint。
4. 安全/合规/部署/兼容约束是 Hard Constraint。
5. 淘汰违反 Hard Constraint 的候选。
6. 有效候选中选**最简单满足需求**的架构。
7. 优先 Modular Monolith，除非独立扩缩/部署/所有权/技术/故障隔离有明确收益。
8. 新关系型项目优先 PostgreSQL，除非具体需求偏向其他库。
9. 非 Cache/Session/限流/锁/队列/流/临时状态需要，不引入 Redis。
10. 非异步/事件驱动需求，不引入 Kafka/RabbitMQ。
11. 数据库搜索能力不足时才引入 ES/OpenSearch。
12. PostgreSQL+pgvector 满足时，不引入专用向量库。
13. 运维需求证明复杂度的才引入 K8s。
14. 存量项目保留现有技术，除非明确要求迁移或存在已证实问题。
15. 不为流行度优化。
16. 不为假设的未来需求优化。
17. 每个架构组件必须有文档化理由。
18. 每个重大决策记录 decision/reason/alternatives/rejected/risks/assumptions/confidence。
19. 决策分类为 AUTO/RECOMMEND/REQUIRE_CONFIRMATION/BLOCKED。
20. 不得静默做 REQUIRE_CONFIRMATION 决策。
21. spec.md 描述 WHAT 与 WHY。
22. plan.md 描述 HOW、架构与技术选择。
23. tasks.md 描述可执行实现工作。
24. 每个 Task 必须追溯到需求或设计决策。
25. 实现前校验 spec → plan → tasks 一致性。
26. 实现后校验 requirements → design → tasks → code → tests。
27. 歧义会实质改变架构 → 停下澄清。
28. 歧义不改变架构 → 显式假设并继续。
29. 优先可逆决策。
30. 目标是**最小且可靠满足需求**的架构，而非最先进架构。

---

## 9. 与 SDD 工具的衔接（知识库 §88）

本知识库作为 Architecture Knowledge Base 放在 SDD 的 **Plan / Architecture Decision** 阶段：

```
User → /speckit-specify → spec.md (WHAT/WHY)
        → Architecture KB → /speckit-plan → plan.md (HOW/Tech)
        → /speckit-tasks → tasks.md
        → /speckit-implement → Code
        → /speckit-converge
```

**关键门槛**：技术栈这类有长期锁定成本的决定，应先 `Architecture Proposal → Human Confirmation`，确认后固化进 plan.md 与 ADR，后续 Agent 默认不得擅自改变。

---

## 10. 规则冲突仲裁顺序（本仓补充）

当**本仓内部文件之间**给出不一致结论时（例如 `knowledge/` 的默认值与某次 `decision-trees/` 的判定相反），按以下顺序仲裁，**上位覆盖下位**：

```
1. decision-protocol.md        元治理：约束模型 / 优先级 / 复杂度预算 / 决策状态
2. decision-trees/*.md         领域判断逻辑
3. knowledge/*.md              参考知识与默认值
4. AGENTS.md 默认技术矩阵       兜底默认值
```

**与源文档的关系**：`sources/` 中的源文档**不参与仲裁**（只用于溯源）。
若本仓结论与源文档冲突，以本仓为准，并在 `.sdd/LAYOUT.md` / 对应文件的"取舍记录"中写明理由（例：spec 节数取 14 节而非 `res.md §117` 的 23 项，理由见 `templates/spec.md`）。

**与用户指令的关系**：用户显式要求 = P0 Hard Constraint，**高于以上全部**（`res.md §1.5`）。

