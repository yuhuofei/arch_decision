# Decision Protocol（决策治理协议）

> 本文件是跨领域决策的"元规则"，应用于所有 decision-trees 与 knowledge 文件。
> 来源：Matrix §1-§2,§3.1-§3.2,§32,§36,§40-§44；知识库 §64（MVP 默认）,§71-§74,§81,§85；
> mod_gpt.md §2（决策状态语义）,§3（约束优先级）,§6（评分标尺）,§7（默认值语义）。
> 引用约定见 `.sdd/CONVENTIONS.md`：`Matrix §N` = Matrix 文档章节；`res.md §N` = res.md 规则条号。
> 配套：`.sdd/decision-trees/*.md`（领域树）、`.sdd/templates/technology-selection.md`（人读输出）、
> `specs/<id>/decision.json`（机器可读契约）。

---

## 1. Agent 总决策协议（Matrix §1）

Agent **不允许**直接从技术栈名称开始决策。

> **进入时机**：本协议是"决策"这个子过程。它发生在 **Draft Spec 之后** —— 先有 WHAT/WHY，
> 再谈 HOW（`CLAUDE.md` §2 第 3–5 步）。跳过 Draft Spec 直接进本节，等于把 SDD 退化成
> `Prompt → Tech Stack → Spec`。

```
INPUT（= 已足以支撑架构判断的 Draft Spec）
  ↓
Project Classification
  ↓
Hard Constraints（P0A / P0B）
  ↓
Architecture Decision
  ↓
Backend → Frontend → Data → Infrastructure
  ↓
Testing / Observability / Security
  ↓
Architecture Validation（含复杂度预算）
  ↓
Decision Status →（仅 REQUIRE_CONFIRMATION）Human Confirmation
  ↓
ADR（按需）+ technology-selection.md + decision.json
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

## 2. 决策优先级（Matrix §2，分级按 `mod_gpt.md §3` 细化）

规则冲突时按以下优先级执行。**上位覆盖下位。**

| Priority | Rule | 类型 |
| --- | --- | --- |
| **P0A** | Safety / Legal / Compliance | Hard Constraint（不可覆盖） |
| **P0A** | Technical feasibility / Platform impossibility | Hard Constraint（不可覆盖） |
| **P0B** | Explicit **non-negotiable** user constraint | Hard Constraint |
| **P0B** | Existing system hard compatibility | Hard Constraint |
| P1 | Functional requirements | Strong Constraint |
| P1 | Performance requirements | Strong Constraint |
| P1 | Data characteristics | Strong Constraint |
| P1 | Team capability / expertise | Strong Constraint |
| P2 | Maintainability | Preference |
| P2 | Simplicity | Preference |
| P2 | Cost | Preference（个人/小预算项目可升 P1，见 §4.2） |
| P2 | Testability / Operational simplicity | Preference |
| P3 | Ecosystem maturity | Preference |
| P3 | Developer popularity / personal preference | Weak Preference |

**关键差异（此前版本的缺陷）**：

```
P0A ≻ P0B ≻ P1 ≻ P2 ≻ P3

"用户明确要求" 不再是无条件的第一优先级。
只有 P0B（不可协商的用户约束）才享 Hard Constraint 地位；
P0A（安全 / 合规 / 可行性）永远在其之上。
```

**禁止：**

```
Popularity > Requirement
Framework preference > Existing system
Personal preference > Explicit requirement
Architecture fashion > Simplicity
User preference > Safety / Compliance / Feasibility      # 新增（P0A 不可被 P0B 覆盖）
```

---

## 3. Hard / Soft Constraint（Matrix §3）

### 3.1 Hard Constraint（不允许 Agent 自行覆盖）

满足任一即 Hard Constraint：

| 类别 | 例子 | 分级 |
| --- | --- | --- |
| 安全 / 合规 | 数据主权、加密要求、审计、许可证冲突、明文存 token | **P0A** |
| 技术可行性 / 平台不可能 | 已 EOL 的运行时、目标平台不支持、SLA 物理不可达、SQLite 承担高并发写 | **P0A** |
| 用户**不可协商**约束 | "必须用 MySQL"、"不得引入 Redis"、"组织标准是 Java" | **P0B** |
| 现有系统硬兼容 | 已绑定的数据库 / 协议 / 部署环境 / 第三方契约 | **P0B** |

> 注意"组织标准"属 P0B（用户/组织明确声明为组织规范），但若该标准要求的是**不合规或不可行**的做法，
> 则撞 P0A，须提出异议而非照做。

**用户表达分级（强制，`mod_gpt.md §3`）**：

```
用户说："偏好 / 喜欢 / 熟悉 / 倾向 / 最好用 / 如果能…"     → Preference（P3 或 P2）
用户说："必须 / 不得 / 不允许 / 组织标准 / 不可改变 / 已经定了" → Hard Constraint（P0B）
```

**禁止把偏好升格为硬约束**。用户说"我比较喜欢 MySQL" **不**等价于 `MUST_USE_MYSQL = true`；
它只是让 MySQL 在候选集中获得先验优势（见 §3.4）。

**遇到 P0A × P0B 冲突**：不得静默服从任一方，标 `BLOCKED` 并按 §6.1 模板提出最小必要问题集。
反例（不应照做）：用户要求 EOL 框架、SQLite 承担高并发写、前端保存明文 token、禁止数据库备份。

### 3.2 Soft Constraint（可比较，不能覆盖 Hard）

团队熟悉度 / 开发效率 / 生态成熟度 / 维护成本 / 学习成本 / 社区活跃度 / 性能余量 / 未来扩展性。

### 3.3 消除与评分

```
1. 先【消除】所有违反 Hard Constraint（P0A/P0B）的候选；
2. 若消除后【只剩 1 个】候选 → 直接选它，不评分；
3. 若消除后【仍有 ≥2 个】且规则（decision-trees / knowledge）无法直接区分 → 才用本文件 §4 评分；
4. 在可区分的情况下，选【最简单满足需求】者（本文件 §8 规则 6）。
```

> **评分有门槛**：不要为了"用上公式"而人为制造候选或强行打分（§4.1）。

### 3.4 默认值语义：Default = Candidate Prior（本仓补充，`mod_gpt.md §7`）

本仓多处给出"默认技术矩阵"（`AGENTS.md`、`knowledge/*.md`、`.sdd/examples/*.md`）。
**默认值不是决策结果**，它只是候选先验：

```
DEFAULT does not mean SELECTED.

A default:
1. enters the candidate set;                      # 进入候选集
2. may become AUTO only when no P0/P1 constraint differentiates candidates;
3. must yield to existing stack and demonstrated team expertise;
4. must not bypass candidate elimination.
```

因此规则写作必须区分两种句式：

| 写法 | 含义 | 是否允许 |
| --- | --- | --- |
| `IF … THEN language = Python` | 断言结论，等于跳过候选淘汰 | ❌ 旧写法，已修正 |
| `IF … THEN Python SHOULD be included as a candidate` | 候选先验，仍走 §3.3 流程 | ✅ |

**为什么改**：旧句式下 `IF AI OR ML OR CRUD/API THEN Python` 覆盖了几乎所有 Web 后端，
前端又规定 Vue 为 business app 默认 —— 于是任何 SaaS 都收敛到 `Vue + FastAPI + PostgreSQL`，
正是本仓要避免的"答案库"效果。默认值应表达**"哪个候选更可能赢"**，而不是**"答案是什么"**。

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

### 4.1 评分标尺（0–5 rubric）与适用门槛（本仓补充，`mod_gpt.md §6`）

**没有标尺的评分是"伪精确"**：两个 Agent 会对同一对候选给出 435 与 395 这类无法复核的分数。
故每项打分必须落到下列标尺：

```
0 = 明确不满足
1 = 严重不足，需要重大 workaround
2 = 部分满足，有明显 trade-off
3 = 满足核心需求
4 = 很好满足，仅有轻微 trade-off
5 = 与该需求高度匹配，有直接证据支持
```

**各维度的 3 / 4 / 5 判定锚点**（避免"感觉不错就打 4"）：

| 维度 | 3（满足核心） | 4（很好） | 5（高度匹配，有证据） |
| --- | --- | --- | --- |
| Requirement Fit | 覆盖主要功能需求，有 1 处需绕行 | 覆盖全部功能需求，无需绕行 | 有同规模同类型的落地证据 / 官方推荐场景 |
| Maintainability | 团队能维护，生态常规 | 类型/测试/文档齐备，改动局部化 | 与团队既有代码风格与工具链一致 |
| Team Fit | 有人写过 | 团队多数成员熟练 | 是团队现有主力栈 |
| Operational Simplicity | 运维面已知、可接受 | 与现有组件同源，不新增知识 | 不需要新增运维动作 |
| Ecosystem | 生态够用 | 生态活跃，常见问题有解 | 与项目其他依赖天然协同 |

**适用门槛（强制）**：只有**同时**满足以下两条才评分 ——

```
- Hard Constraint elimination 后仍有 >= 2 个合理候选
- 候选之间的 trade-off 无法由 decision-trees / knowledge 的规则直接判定
```

> **Scoring is a tie-break / comparison tool, not the decision itself.**
> 不要为了使用公式而人为制造候选或评分；无区分度时应直接选"最简单满足需求"者。

### 4.2 Cost 复核（本仓补充，源文档未覆盖）

Matrix §36 的评分未含成本维度。为避免"选出技术上最优但成本失控"的方案，追加以下**复核步骤（不改动上式权重）**：

```
IF 方案的持续成本（托管服务费 / GPU / 存储 / 出网流量）超出项目预算档
THEN 视为 Soft 否决：
     必须 (a) 在 ADR 写明成本上限与计费方式，或 (b) 降级方案
     不得静默选择更贵的方案
```

- **个人 / 小预算项目**：Cost 可升为 **P1 Strong Constraint**（与性能、团队专长同级，见本文件 §2）。
- 计费口径必须可量化（按 token / 按 GB / 按小时），禁止"大概不贵"这类判断。
- 与复杂度预算（本文件 §5）的分工：**复杂度预算管"多不多"，本节管"贵不贵"**，两者都要过。
- 成本记录进 `decision.json` 的 `cost` 字段（`recurring` / `cap` / `within_budget`）。

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

## 6. 决策状态（Matrix §41；语义按 `mod_gpt.md §2` 修正）

每个决策必须标记：

| Status | 含义 | Agent 行为 |
| --- | --- | --- |
| `AUTO` | 可由规则直接判定 | **直接执行并记录**，不向用户征询 |
| `RECOMMEND` | 存在多个合理方案，但默认值/规则给出推荐 | **Agent 可采用推荐方案继续执行**，同时记录 alternatives、assumptions 与 reversibility；**不阻塞流程** |
| `REQUIRE_CONFIRMATION` | 重大架构影响 | **必须人确认，不得静默决定** |
| `BLOCKED` | 缺失信息会导致重大、不可逆或高风险决策，且**不存在安全可逆默认值** | 停止，按 §6.1 请求澄清 |

> **修正点（此前自相矛盾）**：旧版本要求"技术栈类决定有长期锁定成本 → 必须先 `Human Confirmation`"，
> 与 `AUTO` 的存在直接冲突 —— 若语言、框架、数据库、Docker 都要问用户，`AUTO` 就失去了意义。
> 现统一为：**只有标记为 `REQUIRE_CONFIRMATION` 的技术/架构决策必须人工确认。**
> 普通语言、框架、ORM、测试工具、包管理器、缓存是否引入等，在满足 Hard Constraint 且属
> `AUTO`/`RECOMMEND` 时，Agent **应自行选择并记录，不应阻塞用户**。
>
> 反向也禁止：**不得**把 `AUTO`/`RECOMMEND` 升格为"要人确认"以求免责（`mod_gpt.md §2`）。

### 6.0 默认 REQUIRE_CONFIRMATION 的决策（Matrix §42）
Microservices / Kubernetes / Multi-region / Database migration / Authentication architecture / Authorization model / Payment / Data residency / Compliance / 主流云商 / Event-driven / CQRS / Event sourcing / Distributed transaction / Public API contract / Breaking API changes / 重大技术迁移（含破坏性版本升级）。

> 规则：存在多个合理方案时，不假装只有唯一正确答案，应列出 Alternatives 与 Trade-offs（知识库 Rule 15）。

### 6.1 BLOCKED 澄清问题模板（本仓补充）

状态为 `BLOCKED` 时，**不得猜测后继续**，也不得泛泛地问"能再详细说说吗"。按下列模板提出**最小必要问题集**：

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
| 影响实现（Auth / Storage / Email / Search / Queue） | **SHOULD ASK**，可给默认值并标记 `RECOMMEND`，**不阻塞** |
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
8. Score remaining candidates          # 仅当消除后仍 >= 2 且规则无法区分（§4.1）
9. Select simplest sufficient architecture
10. Generate ADR                       # 按需（LAYOUT.md §1.2）
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
3. 用户**不可协商**的要求是 Hard Constraint（P0B）；用户偏好不是（§3.1）。
4. 安全/合规/部署/兼容约束是 Hard Constraint（P0A 不可被 P0B 覆盖）。
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
20. 不得静默做 REQUIRE_CONFIRMATION 决策；也不得把 AUTO/RECOMMEND 升格为需人确认。
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

本知识库作为 Architecture Knowledge Base 放在 SDD 的 **Draft Spec 之后、Plan 之前**的阶段：

```
User
  → /speckit-specify              → spec.md（WHAT/WHY，Status: Draft）
  → Architecture KB + Decision    → technology-selection.md + decision.json
  → Human Confirmation            （仅 REQUIRE_CONFIRMATION 项）
  → Finalize spec.md（Status: Accepted：把已确认的约束回填到 Constraints/Acceptance）
  → /speckit-plan                 → plan.md（HOW/Tech）
  → design.md（按需）
  → /speckit-tasks                → tasks.md
  → /speckit-implement            → Code
  → /speckit-converge
```

**关键门槛（已收窄）**：只有标记为 `REQUIRE_CONFIRMATION` 的决定需要先 `Architecture Proposal → Human Confirmation`，
确认后固化进 `plan.md` + `decision.json` + ADR，后续 Agent 默认不得擅自改变。
其余决策按本文件 §6 的 `AUTO` / `RECOMMEND` 语义**直接执行并记录，不阻塞**。

---

## 10. 规则冲突仲裁顺序（本仓补充）

当**本仓内部文件之间**给出不一致结论时（例如 `knowledge/` 的默认值与某次 `decision-trees/` 的判定相反），按以下顺序仲裁，**上位覆盖下位**：

```
1. decision-protocol.md        元治理：约束模型 / 优先级 / 复杂度预算 / 决策状态
2. decision-trees/*.md         领域判断逻辑
3. knowledge/*.md              参考知识与默认值（**默认值只是候选先验**，§3.4）
4. AGENTS.md 默认技术矩阵       兜底默认值（同样只是候选先验）
```

**与源文档的关系**：`sources/` 中的源文档**不参与仲裁**（只用于溯源）。
若本仓结论与源文档冲突，以本仓为准，并在 `.sdd/LAYOUT.md` / 对应文件的"取舍记录"中写明理由
（例：spec 节数取 14 节而非 `res.md §117` 的 23 项，理由见 `templates/spec.md`）。

**与用户指令的关系**：用户**不可协商**的显式约束 = **P0B** Hard Constraint，Agent 不得自行覆盖（`res.md §1.5`）；
但 **P0B 不能让 Agent 产出违反 P0A（安全/合规/可行性）的方案** —— 遇到此类冲突必须标 `BLOCKED`
并按 §6.1 提出最小必要问题集，不得静默服从任一方（`mod_gpt.md §3`）。
用户表达的"偏好/倾向/最好用"只是 §3.4 意义上的候选先验，不构成约束。
