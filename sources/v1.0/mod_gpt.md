我检查了当前 main 分支的 README.md、CLAUDE.md、AGENTS.md、.sdd/README.md、LAYOUT.md、decision-protocol.md、核心 templates/workflows、decision.schema.json 和 validate_rules.py。整体上，v1.1 已经把你上一轮评审里的大部分结构性问题修好了；现在剩下的问题主要不是“缺知识”，而是执行语义仍有几处会让 Claude/Codex/Cursor 得到不同结果。

其中最值得改的是下面 8 项。

1. P0：SDD 主流程顺序仍然自相矛盾

这是当前最重要的问题。

spec.md 明确规定：

Spec 是 Source of Truth，描述 WHAT / WHY；Plan 描述 HOW。

但 CLAUDE.md 当前流程却是：

Discovery
→ Decision Protocol
→ Architecture
→ Backend / Frontend / Database
→ Technology Selection
→ Spec

也就是先选架构和技术，再正式形成需求 Spec。

这会产生一个典型的 Agent 偏差：

用户：开发一个订单系统

Agent：
“这是 CRUD”
→ Python
→ FastAPI
→ PostgreSQL
→ Vue
→ 然后开始写 spec

这实际上还是：

Prompt → Tech Stack → Spec

而不是 SDD。

建议统一成
Requirement
    ↓
Discovery
    ↓
Draft Spec（WHAT / WHY / NFR / Constraints）
    ↓
Architecture + Technology Decision
    ↓
Human Confirmation（仅 REQUIRE_CONFIRMATION）
    ↓
Finalize Spec
    ↓
Plan
    ↓
Design（需要时）
    ↓
Tasks
    ↓
Code

这里 Spec 可以分成 Draft/Accepted 两个状态，不需要增加文件。

修改 CLAUDE.md

把当前 §2 替换为：

## 2. SDD REQUIRED（新项目 / 重大特性）

实现新项目或重大特性前，必须按顺序完成：

  0. 读 `.sdd/LAYOUT.md` 与 `.sdd/CONVENTIONS.md`
  1. 读 `.sdd/decision-trees/decision-protocol.md`
- 2. 读 `.sdd/workflows/new-project.md`
- 3. 读 `.sdd/knowledge/architecture.md` + `.sdd/decision-trees/architecture.md`
- 4. 读 backend / frontend / database / infrastructure 决策树
- 5. 按项目类型追加领域知识
- 6. 生成 project-discovery.md
- 7. 生成 technology-selection.md
- 8. 生成 spec.md 与 plan.md
+ 2. 读 `.sdd/workflows/new-project.md`
+ 3. 用 `.sdd/templates/project-discovery.md`
+    生成 `project-discovery.md`
+ 4. 基于 Discovery 生成 Draft `spec.md`
+    - 明确 WHAT / WHY
+    - Functional Requirements
+    - NFR
+    - Hard Constraints
+    - Acceptance Criteria
+    - Open Questions
+    - 不写具体技术实现
+ 5. 只有 Draft Spec 足以支撑架构判断后，读取：
+    - `.sdd/knowledge/architecture.md`
+    - `.sdd/decision-trees/architecture.md`
+    - backend / frontend / database / infrastructure 决策树
+    - 与项目类型有关的领域知识
+ 6. 生成 `technology-selection.md`
+    - Hard Constraint elimination
+    - Candidate comparison
+    - Decision Status
+    - Complexity Budget
+ 7. 对 `REQUIRE_CONFIRMATION` 决策请求人工确认
+ 8. 根据已确认决策完成：
+    - Final spec.md
+    - plan.md
+    - 必要时 design.md
+    - ADR
+    - tasks.md
+ 9. 未解决的 BLOCKED / REQUIRE_CONFIRMATION 决策不得进入相关实现。

同时修改 Golden Rule：

- Requirement → Decision → Specification → Design → Task → Code → Test → Verification
+ Requirement
+ → Discovery
+ → Specification
+ → Architecture Decision
+ → Plan / Design
+ → Task
+ → Code
+ → Test
+ → Verification
2. P0：AUTO/RECOMMEND 和“技术栈必须人工确认”互相打架

decision-protocol.md 有四种状态：

AUTO
RECOMMEND
REQUIRE_CONFIRMATION
BLOCKED

只有重大架构决定属于 REQUIRE_CONFIRMATION。

但是 CLAUDE.md 又写：

技术栈类决定有长期锁定成本 → 先 Architecture Proposal → Human Confirmation。

new-project.md 更直接：

技术栈类决定有长期锁定成本，不得静默决定。

于是 Agent 很可能认为：

Python? 问用户
FastAPI? 问用户
PostgreSQL? 问用户
Vue? 问用户
Docker? 问用户

这样 AUTO 基本失去意义。

应明确为
AUTO
→ Agent 可直接决定 + 记录

RECOMMEND
→ Agent 选择推荐方案 + 记录 alternatives
→ 不必阻塞

REQUIRE_CONFIRMATION
→ 用户确认后继续

BLOCKED
→ 缺少的信息无法通过安全/可逆默认值解决
修改 decision-protocol.md §6
| Status | Agent 行为 |
| --- | --- |
| AUTO | 直接执行并记录 |
-| RECOMMEND | 提出方案，建议人确认 |
+| RECOMMEND | Agent 可采用推荐方案继续执行，同时记录 alternatives、assumptions 与 reversibility；不阻塞流程 |
| REQUIRE_CONFIRMATION | 必须人确认，不得静默决定 |
-| BLOCKED | 停止，请求澄清 |
+| BLOCKED | 缺失信息会导致重大、不可逆或高风险决策，且不存在安全可逆默认值时才停止 |

然后删除：

技术栈类决定有长期锁定成本 → Human Confirmation

改成：

只有标记为 REQUIRE_CONFIRMATION 的技术/架构决策必须人工确认。

普通语言、框架、ORM、测试工具、包管理器等，
在满足 Hard Constraints 且属于 AUTO/RECOMMEND 时，
Agent 应自行选择并记录，不应阻塞用户。

这会明显提高 Claude/Codex 实际使用体验。

3. P0：用户明确要求 = 最高 Hard Constraint 太绝对

当前协议写的是：

Explicit user requirement = P0 Hard Constraint

最后甚至规定：

用户显式要求高于以上全部。

而 backend 又再次写：

用户指定即 Hard Constraint，不得擅自改。

这会造成例如：

用户要求：
Python 3.7
已 EOL 的框架
SQLite + 高并发写
前端必须保存明文 token
禁止数据库备份

Agent 按当前规则理论上都应该服从。

更合理的是区分：

Requirement
Preference
Constraint

用户说“我比较喜欢 MySQL”不应该等价于：

MUST_USE_MYSQL = true
建议改优先级
P0A  Safety / Legal / Compliance
P0A  Technical feasibility / Platform impossibility

P0B  Explicit non-negotiable user constraint
P0B  Existing system hard compatibility

P1   Functional requirement
P1   Performance / Data / Team capability

P2   Maintainability / Simplicity / Cost

P3   Ecosystem / Popularity / preference

同时增加一句：

用户表达的“偏好、熟悉、倾向、最好使用”默认属于 Preference，
只有明确表达“必须 / 不得 / 组织标准 / 不可改变”时，
才升级为 Hard Constraint。

这样整个体系会稳很多。

4. P1：plan.md 和 design.md 职责高度重复

这是目前结构里第二大的冗余问题。

plan.md 已经包含：

architecture
component
data flow
backend
frontend
database
API
async
cache
security
testing
observability
deployment

而 design.md 又包含：

Component
Data Flow
API
Database
Authentication
Error Handling
Async Processing
Failure Handling

实际上差不多是第二份 Plan。

最危险的不是文档多，而是：

plan.md:
Redis cache TTL = 10min

design.md:
Redis cache TTL = 30min

Agent 不知道谁是 Source of Truth。

建议不要强制 design.md

我建议：

spec.md
    WHAT / WHY

technology-selection.md
    WHICH TECHNOLOGY / WHY

plan.md
    HOW at architecture level

design.md
    ONLY detailed design that is too detailed for plan
    Optional

tasks.md
    executable work
修改 .sdd/LAYOUT.md
specs/<id>-<name>/
    ├── project-discovery.md
    ├── technology-selection.md
    ├── spec.md
    ├── plan.md
-   ├── design.md                 # 必填
+   ├── design.md                 # 按需：复杂模块/协议/状态机/算法/跨组件流程
    ├── tasks.md
    ├── verification.md
-   └── adr/                      # 必填（至少 1 个 ADR）
+   └── adr/                      # 按需：存在 Architecture Decision 时创建

并增加：

design.md SHOULD be created when one or more apply:

- complex domain model
- non-trivial state machine
- concurrency
- async workflow
- multiple external integrations
- distributed consistency
- complex API contract
- security-sensitive flow
- algorithm requires explicit design

否则 plan.md 足够，不创建 design.md。

ADR 也一样：没有重要 Architecture Decision，不需要为了满足目录规范制造 ADR。

5. P1：现在所谓的 JSON Schema 校验实际上没有真正执行 Schema

这是一个工程层面的隐患。

你已经建立了很好的：

.sdd/schema/decision.schema.json

它定义了 architecture_decision。

但 validate_rules.py 并没有拿 YAML 数据去执行 JSON Schema validation。

它实际上只是：

required = schema["properties"]["architecture_decision"]["required"]

for key in required:
    regex search key

也就是说下面这种内容甚至可能通过：

architecture_decision:
  project: hello
  backend: 123
  database: []
  rejected: wrong
  confidence: foo

因为 key 都存在。

因此 README 中：

机器可校验 Schema

现在有一点“名义上 Schema 化，实际上 regex 化”。

推荐修改方式

我反而建议不要再维护 Markdown YAML 的弱解析器。

直接增加：

specs/<id>/
    technology-selection.md
    decision.json

其中：

technology-selection.md

给人和 Agent 阅读。

decision.json

给机器校验。

这样：

data = json.loads(...)
jsonschema.validate(data, schema)

如果你坚持纯 Python 标准库无依赖，那就把当前描述从：

机器可校验 Schema

修改成：

Machine-readable Decision Contract

并明确：

validate_rules.py 当前执行 structural validation，
不是完整 JSON Schema validation。

如果允许一个开发依赖，我更建议：

jsonschema

直接真校验。

6. P1：评分公式有权重，但没有评分标尺，Agent 会产生“伪精确评分”

现在公式是：

Requirement Fit ×40
Maintainability ×20
Team Fit ×15
Operational Simplicity ×15
Ecosystem ×10

每项 0–5。

问题不是公式，而是没有定义：

Requirement Fit = 3 和 4 到底差在哪里？
Maintainability = 4 是什么？
Ecosystem = 5 又意味着什么？

两个 Agent 很可能得到：

Claude:
FastAPI 435
Django 420

Codex:
FastAPI 395
Django 445

看起来很科学，其实都是主观数字。

在 decision-protocol.md §4 增加评分 rubric
0 = 明确不满足
1 = 严重不足，需要重大 workaround
2 = 部分满足，有明显 trade-off
3 = 满足核心需求
4 = 很好满足，仅有轻微 trade-off
5 = 与该需求高度匹配，有直接证据支持

另外增加：

Scoring is a tie-break/comparison tool, not the decision itself.

只有满足以下情况才评分：
- Hard Constraint elimination 后仍有 >= 2 个合理候选；
- 候选的 trade-off 无法直接通过规则判定。

不要为了使用公式而人为制造候选或评分。

这点很重要。

7. P1：默认技术矩阵仍然偏“答案库”，而不是“决策系统”

例如：

new-project.md 直接写：

中小 SaaS → Vue + FastAPI + PG
AI → Next.js + FastAPI + pgvector
企业 → Spring Boot

Backend 的 Python 规则甚至是：

IF AI OR ML OR Data Processing OR Automation OR CRUD/API
THEN Python

几乎任何 Web 后端都满足 CRUD/API。

Frontend 又规定 Vue 为 business app 默认。

这样最终很容易退化成：

SaaS
→ Vue
→ FastAPI
→ PostgreSQL

与你最初想避免的事情非常接近。

建议把 THEN 改为 CANDIDATE

例如：

IF AI OR ML OR Data Processing OR Automation OR CRUD/API
- THEN language = Python
+ THEN Python SHOULD be included as a candidate

Go：

IF concurrency = high ...
- THEN language = Go
+ THEN Go SHOULD receive strong preference as a candidate

Vue：

IF business_app = true AND frontend_complexity = medium
- THEN Vue 3 + TypeScript
+ THEN Vue 3 + TypeScript SHOULD be considered

然后添加统一规则：

DEFAULT does not mean SELECTED.

A default:
1. enters the candidate set;
2. may become AUTO only when no P0/P1 constraint differentiates candidates;
3. must yield to existing stack and demonstrated team expertise;
4. must not bypass candidate elimination.

我认为这是这个仓库理念上非常关键的一次调整：

Default 应该代表 candidate prior，而不是 decision result。

8. P1：你最初要求的“默认版本策略”目前还没有真正形成规则

Backend 目前只有：

Python 3.x
Vue 3

部署部分则说 pinned deps。

这没有回答 Agent 最实际的问题：

Python 3.12 / 3.13 / 3.14 到底选哪个？
PostgreSQL 17 / 18？
Node LTS？
Java LTS？
FastAPI / Django 主版本？

这里不应该在知识库里永久写死：

Python = 3.13

因为很快过期。

建议新增：

.sdd/knowledge/versioning.md

内容建议如下：

# Version Selection Policy

## Principle

Version selection is a lifecycle decision, not a popularity decision.

Never choose a version only because it is the newest release.

## Existing Project

Preserve the existing major/minor version unless:

- security support ended;
- upstream support ended;
- required dependency is incompatible;
- user explicitly requests upgrade;
- upgrade is necessary for a documented requirement.

## New Project

Default priority:

1. Supported stable release
2. Active ecosystem support
3. Dependency compatibility
4. Deployment/runtime support
5. Team/toolchain compatibility
6. Latest release

Prefer:

- language runtimes: current widely-supported stable or LTS
- Java: supported LTS
- Node.js: Active LTS
- databases: supported stable major release available on target platform
- frameworks: latest stable major that has mature ecosystem support

Avoid by default:

- alpha / beta / RC
- newly released major versions with unresolved dependency compatibility
- EOL releases
- versions unavailable on target deployment platform

## Verification

For new projects, version numbers MUST be verified against current official upstream
documentation when network access is available.

Record:

| Technology | Selected | Support Status | Reason |
|---|---|---|---|
| Python | x.y | supported | ... |
| PostgreSQL | x | supported | ... |

## Locking

Application dependencies:
- exact lock file
- reproducible install

Runtime:
- pin major/minor
- patch updates allowed according to project update policy

Container images:
- never use `latest`
- pin runtime version

然后在 backend/frontend/database/deployment 都只引用它，不自己维护版本策略。

9. 我建议顺手调整 AGENTS.md

当前 AGENTS.md 作为“规则摘要 + 目录索引”的方向其实是对的，而且 81 行并不算长。OpenAI 当前也明确建议 AGENTS.md 保持简洁，把它当作 Agent 的 persistent context / table of contents，并包含运行方式、测试、lint、约束以及“完成”的定义。

当前缺少一个特别重要的部分：

## DEFINITION OF DONE

修改本规则库后：

1. 运行：
   python3 scripts/validate_rules.py

2. 必须：
   - 0 errors
   - 0 warnings
   - 无失效文件引用
   - 无互相冲突的 canonical rules

3. 如果修改：
   - Layout → 同步 LAYOUT.md
   - Decision semantics → 同步 decision-protocol.md
   - Technology rule → 更新 knowledge / decision-tree
   - User-facing behavior → 检查 CLAUDE.md / AGENTS.md
   - Rule source mapping → 更新 TRACEABILITY.md
   - Public rule behavior → 更新 CHANGELOG.md

这样 Codex 实际修改这个仓库的时候，会更稳定。

最值得做的结构调整

如果把这轮修改压缩成一个 v1.2，我建议最终变成：

User Requirement
       ↓
Project Discovery
       ↓
Draft Specification
       │
       ├── Functional Requirements
       ├── NFR
       ├── Constraints
       └── Acceptance Criteria
       ↓
Decision Protocol
       ↓
Generate Candidates
       ↓
Hard Constraint Elimination
       ↓
Decision Tree
       ↓
Score only if necessary
       ↓
Simplest Sufficient Solution
       ↓
Decision Status
       ├── AUTO ───────────────┐
       ├── RECOMMEND ──────────┤
       ├── REQUIRE_CONFIRMATION → Human
       └── BLOCKED ─────────────→ Clarify
                               │
       ↓                       ↓
Technology Selection / ADR
       ↓
Final Spec
       ↓
Plan
       ↓
Design (optional)
       ↓
Tasks
       ↓
Implementation
       ↓
Tests
       ↓
Verification

这比现在最大的变化其实只有三个：

Spec 前置、Confirmation 收窄、Design/ADR 按需。

但这三个变化会显著减少真实 Agent 使用中的摩擦。

我对当前项目的结论

当前 v1.1 已经可以使用，之前“目录混乱、引用冲突、缺 AI/Data/Caching、复杂度预算口径不一致”等问题基本已经处理掉了。

现在真正应该进入的是 v1.2「Agent 可执行性优化」，而不是继续增加技术知识文件。

我会把优先级排成：

优先级	文件	修改
P0	CLAUDE.md	Spec 前置，修正 canonical workflow
P0	decision-protocol.md	修正 AUTO / RECOMMEND / CONFIRM / BLOCKED 语义
P0	new-project.md	与 canonical workflow 对齐
P0	AGENTS.md	与新流程同步，增加 Definition of Done
P1	LAYOUT.md	design.md / ADR 改为按需
P1	decision-protocol.md	增加 0–5 scoring rubric
P1	backend/frontend	THEN SELECT 改成 candidate/preference
P1	schema + validator	真正 Schema validation，或明确只是 structural validation
P1	新增 knowledge/versioning.md	统一动态版本选择策略

这轮修改以后，这个仓库会更接近一个真正的 Architecture Decision Engine，而不是“组织得很好的技术最佳实践文档库”。尤其是把 Default 从结果改成 Prior/Candidate，我认为是下一版最核心的理念升级。