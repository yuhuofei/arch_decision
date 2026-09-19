# arch_decision + Spec Kit + OpenSpec + Claude Code：完整落地方案

我重新梳理了一遍。你这次把 Claude Code 加进来以后，四者的关系就非常清晰了。

我认为最合理的定位不是：

arch_decision + Spec Kit + OpenSpec 三套 SDD 框架叠在一起。

而是：

arch_decision = 架构决策治理层
Spec Kit / OpenSpec = 规格与变更工作流层
Claude Code = Agent 执行层

其中还有一个非常关键的设计：

Spec Kit 和 OpenSpec 不应该在同一个 Feature 上同时跑完整流程。

它们应该承担不同生命周期阶段。

## 1. 四个工具的正确分工
```text
                         人
                         │ Requirement / Change Request
                         ▼
              ┌───────────────────────┐
              │    arch_decision      │
              │                       │
              │ Architecture         │
              │ Technology Selection  │
              │ Constraints           │
              │ Complexity Budget     │
              │ Decision Status       │
              │ Human Confirmation    │
              └───────────┬───────────┘
                   ACCEPTED DECISION
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        ┌───────────┐           ┌───────────┐
        │ Spec Kit  │           │ OpenSpec  │
        │           │           │           │
        │ 新项目/   │           │ 已有系统/ │
        │ 新 Feature│           │ 变更管理  │
        └─────┬─────┘           └─────┬─────┘
              │                       │
              └───────────┬───────────┘
                          ▼
                  ┌──────────────┐
                  │ Claude Code  │
                  │              │
                  │ Read         │
                  │ Reason       │
                  │ Edit         │
                  │ Execute      │
                  │ Test         │
                  └──────┬───────┘
                         ▼
                    Verification
```

你的 arch_decision 当前 README 本身就是这个方向：要求 Agent 先经过 Discovery、Draft Spec、约束提取、候选淘汰、必要时评分、决策状态和确认，再形成 technology-selection.md / decision.json，最后才进入 Final Spec 和代码实现。

而当前 AGENTS.md 也已经把这个边界写得比较清楚：Agent Entry 负责路由，不负责重新定义决策语义；架构决策、约束优先级、决策状态、评分等由 .sdd/decision-trees/ 等 Canonical 文件负责。

## 2. 最重要的一点：不要让 Spec Kit 再重新选技术栈

这是四者结合时最容易出现的问题。

当前 Spec Kit 的官方流程是：

```text
/speckit.constitution
        ↓
/speckit.specify
        ↓
/speckit.clarify
        ↓
/speckit.plan
        ↓
/speckit.checklist
        ↓
/speckit.tasks
        ↓
/speckit.analyze
        ↓
/speckit.implement
        ↓
/speckit.converge
```

其中官方文档明确说明 /speckit.plan 是进入技术实现方案、技术栈和架构细节的阶段。

这和 arch_decision 有一个天然重叠。

所以不能直接：

```text
arch_decision
      ↓
Spec Kit
      ↓
/speckit-plan
```

然后让 /speckit-plan 自己重新决定：

PostgreSQL → MongoDB
FastAPI → Django
Monolith → Microservices

这样就把 arch_decision 绕过去了。

正确方式是：

```text
arch_decision
      ↓
Architecture Accepted
      ↓
Spec Kit
      ↓
Plan = implementation plan
```

即：

arch_decision 决定“采用什么”；Spec Kit 决定“基于已经采用的东西怎么实现”。

## 3. OpenSpec 的位置也不一样

OpenSpec 当前的核心流程是：

```text
Explore
   ↓
Propose
   ↓
Review
   ↓
Apply
   ↓
Archive
```

官方文档明确把它设计成变化驱动的工作流：先探索，再生成 change proposal，审查 proposal 后才 Apply，完成后 Archive 并把变化合并回主规格。

典型结构：

```text
openspec/
├── specs/
│   └── ...
└── changes/
    ├── add-auth/
    │   ├── proposal.md
    │   ├── specs/
    │   ├── design.md
    │   └── tasks.md
    └── archive/
```

所以我建议：

新项目
```text
arch_decision
       ↓
Spec Kit
       ↓
Claude Code
已有项目增加/修改功能
arch_decision
       ↓
OpenSpec
       ↓
Claude Code
不推荐
arch_decision
       ↓
Spec Kit
       ↓
OpenSpec
       ↓
Claude Code
```

对同一个 Feature这么串，会产生重复 Spec、重复 Plan、重复 Task。

## 4. 四者最终的生命周期

可以把它定义成：

```text
┌─────────────────────────────────────────────┐
│                  Project                    │
└─────────────────────────────────────────────┘

                新项目
                   ▼
          ┌─────────────────┐
          │ arch_decision   │
          │                 │
          │ Discovery       │
          │ Draft Spec      │
          │ Constraints     │
          │ Architecture    │
          │ Technology      │
          │ Decision        │
          └────────┬────────┘
             ACCEPTED
                   ▼
             ┌──────────┐
             │ Spec Kit │
             └────┬─────┘
          Specify / Clarify
                  ▼
                Plan
                  ▼
                Tasks
                  ▼
             Claude Code
                  ▼
             Implementation
                  ▼
              Converge
                  ▼
               Release
```

以后发生变化：

```text
Change Request
      ▼
arch_decision
      ├── No architecture impact
      │        │
      │        ▼
      │     OpenSpec
      └── Architecture impact
               ▼
         Architecture
         Re-decision
               ▼
            OpenSpec
               ▼
          Claude Code
               ▼
             Archive
```

这个结构非常重要。

## 5. 用一个真实项目完整走一遍

下面假设我们创建：

企业内部 AI Knowledge Base

需求：

用户上传 PDF / Markdown
自动解析
建立知识库
RAG 查询
Web UI
50～100 用户
内网部署
单租户
第一版不要求高可用
希望低运维成本

最终假设我们得到：

Architecture:

Modular Monolith

Backend:

Python + FastAPI

Frontend:

Vue + TypeScript

Database:

PostgreSQL + pgvector

Cache:

None initially

Deployment:

Docker Compose

Authentication:

Company OIDC

注意：

这些不是预先告诉 Agent 的答案。

它们应该由 arch_decision 根据项目约束产生。

## 6. 第一步：初始化新项目
```bash
mkdir enterprise-ai-kb
cd enterprise-ai-kb
git init
```

然后引入 arch_decision。

推荐项目结构：

```text
enterprise-ai-kb/
├── AGENTS.md
├── CLAUDE.md
├── .sdd/
│   ├── VERSION
│   ├── CANONICAL.md
│   ├── LAYOUT.md
│   ├── CONVENTIONS.md
│   ├── decision-trees/
│   ├── knowledge/
│   ├── templates/
│   └── workflows/
├── scripts/
│   └── validate_rules.py
├── specs/
├── openspec/
├── src/
└── tests/
```

你的 arch_decision 当前 README 就是按这种模式组织的：.sdd/ 是规则库，specs/ 是具体项目实例，scripts/ 是校验和迁移工具。

## 7. 第二步：安装 Spec Kit

当前 Spec Kit 的 CLI 可以初始化项目并选择 Agent integration；官方文档也明确支持 Claude integration。

例如：

```bash
uv tool install specify-cli
specify init . --integration claude
```

然后：

```bash
claude
```

## 8. 第三步：安装 OpenSpec

OpenSpec 当前支持 Claude Code，并且 openspec init 会在项目里安装对应的 skills / commands。

例如：

```bash
npm install -g @fission-ai/openspec@latest
openspec init
```

最终 Claude Code 中会出现类似：

```bash
/opsx:explore
/opsx:propose
/opsx:apply
/opsx:archive
```

OpenSpec 当前官方文档说明，Claude Code 的 command 是这些 workflow 的快捷入口，底层对应 OpenSpec skills。

## 9. 第四步：让 Claude Code 先执行 arch_decision

这里是整个体系最关键的地方。

第一次进入 Claude Code：

```bash
claude
```

然后不要：

帮我写这个项目

而应该：

这是一个全新项目。

现在不要写任何业务代码。

请先执行 arch_decision 的 New Project workflow。

严格遵守：

- AGENTS.md
- CLAUDE.md
- .sdd/CANONICAL.md
- .sdd/LAYOUT.md
- .sdd/decision-trees/decision-protocol.md
- .sdd/workflows/new-project.md

执行目标：

1. Discovery
2. Draft Spec
3. Constraint Classification
4. Architecture Candidate Generation
5. Candidate Elimination
6. Technology Selection
7. Complexity Budget
8. Decision Status
9. Human Confirmation
10. Final Accepted Architecture

当前项目：

企业内部 AI Knowledge Base。

需求：

- 用户上传 PDF / Markdown
- 自动解析文档
- 建立知识库
- 支持 RAG
- Web UI
- 50~100 用户
- 公司内部部署
- 单租户
- 第一版不要求高可用
- 低运维成本

不要写业务代码。

完成后停在 Architecture Decision 阶段。
## 10. Claude Code 此时应该做什么

根据你当前 arch_decision 的设计，Agent 应该先走：

```text
Requirement
    ↓
Discovery
    ↓
Draft Spec
    ↓
Constraints
    ↓
Candidates
    ↓
Elimination
    ↓
Score if needed
    ↓
Simplest sufficient architecture
    ↓
Decision Status
```

你的 AGENTS.md 当前也明确要求：

理解需求 → 识别类型/规模 → 架构决策 → 可解释技术选型 → Spec → Design → Plan → Tasks → 实现 → 验证 → 收敛。

## 11. 第一次人机交互

Claude：

我需要先完成 Discovery。

### Q1

预计用户规模是多少？

你：

第一阶段 50~100 人。

Claude：

### Q2

部署环境？

你：

公司内部 Ubuntu Server。

Claude：

### Q3

是否公网访问？

你：

不公网开放。

Claude：

### Q4

认证方式？

目前不知道公司是否已经提供 OIDC。

你：

公司有统一 OIDC。
## 12. Claude Code 进入架构决策

它可能生成：

Architecture Decision

## Architecture

Candidates:

A. Microservices
B. Modular Monolith

Constraints:

- 50~100 users
- single tenant
- internal deployment
- low operational complexity

Microservices introduces additional operational complexity
without a current requirement.

Decision:

Modular Monolith

Status:

AUTO

然后：

Backend:

Python
Go
TypeScript

AI/RAG ecosystem is a significant requirement.

Decision:

Python

Status:

RECOMMEND

然后：

Web Framework:

FastAPI
Django
Flask

Requirement:

API-first backend + AI/RAG.

Decision:

FastAPI

Status:

RECOMMEND

然后：

Database:

PostgreSQL
MySQL
MongoDB

Requirement:

- relational metadata
- transactions
- vector search

Candidates:

PostgreSQL + pgvector
PostgreSQL + Qdrant
PostgreSQL + Milvus

Complexity analysis:

Qdrant introduces another infrastructure component.

Milvus introduces substantially more operational complexity.

Decision:

PostgreSQL + pgvector

Status:

AUTO
## 13. 什么时候必须停下来问人？

比如：

Authentication

Candidates:

A. Existing company OIDC
B. Application-managed session
C. JWT

Company OIDC appears available.

However, the requirement does not explicitly state
whether integration is mandatory.

Decision:

REQUIRE_CONFIRMATION

Claude 必须停。

请确认：

A. 强制使用公司 OIDC
B. 不使用公司 OIDC
C. 先保留认证抽象，暂不决定

你：

A

Claude：

Authentication:

Company OIDC

Decision Status:

ACCEPTED
## 14. Architecture Accepted

最终 Claude 应该生成：

specs/001-project/

```text
├── project-discovery.md
├── technology-selection.md
├── decision.json
├── plan.md
└── verification.md
```

如果有重要架构决策，再生成：

adr/

你的当前规则已经明确 ADR 是按需产生，而不是所有决策都强制创建 ADR。

## 15. 到这里才进入 Spec Kit

现在告诉 Claude：

Architecture Decision 已完成并 Accepted。

现在切换到 Spec Kit workflow。

重要：

arch_decision 已经是 Architecture 和 Technology Selection 的唯一决策来源。

Spec Kit 不得重新选择：

- programming language
- backend framework
- frontend framework
- database
- vector store
- deployment architecture
- authentication architecture

现在执行：

```bash
/speckit.specify
```

目标：

将已经确认的产品需求转换为正式 Feature Specification。

重点描述：

WHAT
WHY
Acceptance Criteria

不要重新进行技术选型。

如果发现需求与 Architecture Decision 冲突：

停止并报告：

ARCHITECTURE_CONFLICT

这里正好符合 Spec Kit 官方对 /speckit.specify 的定位：Specify 阶段应该描述 what/why，而不是技术实现。

## 16. Spec Kit Clarify

然后：

```bash
/speckit.clarify
```

或者：

请执行 Spec Kit Clarify。

重点检查：

1. 用户故事
2. 文档上传
3. 文档解析失败
4. 文档删除
5. RAG 查询
6. Citation
7. 权限
8. 错误处理
9. 数据生命周期
10. 验收标准

不要改变 Architecture Decision。
## 17. 最关键：Spec Kit Plan 怎么处理

这里必须特别改造默认思维。

Spec Kit 官方 /speckit.plan 本来就是技术规划阶段。

但在我们的组合里：

```text
arch_decision
       ↓
已经决定技术栈
       ↓
Spec Kit Plan
       ↓
只能做 implementation design
```

所以 Prompt 应该明确：

执行：

```bash
/speckit.plan
```

但是：

Architecture Decision 已经 Accepted。

以下文件是唯一技术架构事实来源：

specs/001-project/decision.json
specs/001-project/technology-selection.md

Plan 必须基于这些决策。

禁止重新选择：

- Language
- Framework
- Database
- Cache
- Message Queue
- Deployment Model
- Authentication

Plan 的职责是：

HOW TO IMPLEMENT THE ACCEPTED ARCHITECTURE

而不是：

WHICH ARCHITECTURE TO CHOOSE。

如果实现过程中发现当前 Architecture 无法满足 Spec：

不要自行改变技术。

输出：

ARCHITECTURE_CHANGE_REQUEST

并停止。

这是四个工具能够正确协作的核心 Prompt。

## 18. Spec Kit Checklist / Analyze

继续：

```bash
/speckit.checklist
```

然后：

```bash
/speckit.analyze
```

Spec Kit 官方把 analyze 定位为检查 spec.md、plan.md、tasks.md 之间的冲突、缺口和歧义，而且它是只读分析阶段。

所以这里非常适合作为第二道 Gate。

## 19. Tasks
```bash
/speckit.tasks
```

得到：

tasks.md

要求：

每个 Task 必须能够追溯：

```text
Requirement
    ↓
Spec
    ↓
Architecture Decision
    ↓
Plan
    ↓
Task
```

## 20. 最后才允许 Claude Code 写代码
```bash
/speckit.implement
```

但建议不要直接让它无限制执行。

Prompt：

执行 /speckit.implement。

执行前进行 Preflight：

1. Architecture = ACCEPTED
2. REQUIRE_CONFIRMATION = 0
3. BLOCKED = 0
4. Spec = VALID
5. Plan = VALID
6. Tasks = VALID
7. Analyze = PASS

如果任意条件不满足：

不要写代码。

否则按照 tasks.md 的依赖顺序实现。

每完成一个阶段：

- 运行测试
- 检查 Architecture Compliance
- 检查 Requirement Traceability
## 21. 最后 Converge
```bash
/speckit.converge
```

然后再要求：

同时执行 arch_decision verification。

检查：

Requirement
→ Spec
→ Architecture
→ Plan
→ Task
→ Code
→ Test

检查：

1. 是否存在未经批准的技术
2. 是否改变 Architecture
3. 是否增加未批准基础设施
4. 是否违反 Complexity Budget
5. 是否存在未实现 Requirement
6. 是否存在无测试 Requirement
7. Code 是否与 Accepted Architecture 一致

如果发现架构偏差：

不要直接修改 Architecture Decision。

报告：

ARCHITECTURE_DRIFT

Spec Kit 当前的 Converge 本身就是用来检查代码与 spec/plan/tasks 的一致性，并在发现缺口时补充任务，然后继续 implement/converge 循环。

## 22. 那么 OpenSpec 什么时候进入？

这才是你这个体系真正有意思的地方。

假设项目已经上线：

enterprise-ai-kb v1.0

现在用户提出：

增加企业微信登录。

这是一个 Change。

这时候不要重新跑完整的 Spec Kit：

❌ /speckit.specify
❌ /speckit.plan
❌ /speckit.tasks

而是：

OpenSpec
## 23. OpenSpec Explore

Claude Code：

```bash
/opsx:explore
```

Prompt：

我们准备增加：

企业微信 OAuth 登录。

请先探索，不要修改代码。

请检查：

1. 当前认证架构
2. 当前用户模型
3. 当前 session/token 机制
4. 当前 OIDC 集成
5. 数据库影响
6. API 影响
7. 前端影响
8. Security Boundary
9. 是否影响现有 Architecture Decision

重点：

如果这个 Change 会改变 Architecture Decision，
必须明确标记：

ARCHITECTURE_IMPACT

OpenSpec 的 Explore 当前就是只读的思考/调查阶段，不应该直接写代码。

## 24. 如果发现没有架构影响

例如：

当前已有：

Authentication abstraction

新增微信 OAuth
只是增加一个 Provider。

Architecture：

UNCHANGED

那么：

```text
OpenSpec
   ↓
Proposal
   ↓
Review
   ↓
Apply
   ↓
Archive
```

## 25. OpenSpec Propose
```bash
/opsx:propose add-wechat-login
```

OpenSpec 当前会生成：

openspec/changes/add-wechat-login/

```text
├── proposal.md
├── specs/
├── design.md
└── tasks.md
```

这是 OpenSpec 当前 spec-driven workflow 的标准 change artifact 结构。

## 26. Human Review

你检查：

proposal.md

然后：

specs/

再：

design.md

最后：

tasks.md

你可以告诉 Claude：

Review OpenSpec change：

add-wechat-login

发现：

1. 未覆盖账号绑定
2. 未覆盖已有账号冲突
3. 未覆盖取消授权
4. 未覆盖 OAuth callback failure

请修改 Proposal / Specs / Design / Tasks。

不要修改代码。
## 27. OpenSpec Apply

确认以后：

```bash
/opsx:apply
```

OpenSpec 会根据 tasks.md 执行实现，并逐项勾选任务。官方文档也明确说明 Apply 是从 change proposal 的 tasks 开始实现代码的阶段。

## 28. OpenSpec Verify

如果安装了 OpenSpec optional verify workflow，可以：

```bash
/opsx:verify
```

检查：

```text
Implementation
      ↓
OpenSpec Change
      ↓
Requirements
```

OpenSpec 当前把 verify 作为 optional workflow，而不是默认 core workflow。

## 29. OpenSpec Archive

完成以后：

```bash
/opsx:archive
```

或者 CLI：

```bash
openspec archive add-wechat-login
```

OpenSpec Archive 会把 change 移到：

openspec/changes/archive/

并根据 change 的 spec delta 更新主 specs。

## 30. 但是，如果 OpenSpec 发现架构真的变了呢？

这是整个体系最关键的一个场景。

例如用户说：

微信登录以后，还要支持 10 万并发用户。

OpenSpec Explore 发现：

当前：

Modular Monolith
Single Server

新增：

100k concurrent users
High Availability
Horizontal Scaling

这已经不是普通 Feature Change。

Agent 应该：

```text
OpenSpec Explore
       ▼
ARCHITECTURE_IMPACT
       ▼
STOP
       ▼
arch_decision
       ▼
重新进行 Architecture Decision
       ▼
Architecture Accepted
       ▼
OpenSpec Update
       ▼
Apply
```

## 31. 也就是说，OpenSpec 不应该拥有 Architecture 的最终决定权

这是我认为你 arch_decision 项目最值得坚持的一条原则：

OpenSpec design.md

```text
          ↓

只能提出 Architecture Change

          ↓

不能直接批准 Architecture Change
```

例如：

ARCHITECTURE_CHANGE_REQUEST

Reason:
Current modular monolith may not satisfy
100k concurrent users.

Affected:

- architecture
- deployment
- caching
- database
- reliability

Required:

arch_decision re-evaluation

然后回到：

arch_decision
## 32. 最终形成一个非常漂亮的闭环
```text
                       ┌───────────────┐
                       │     User      │
                       └───────┬───────┘
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
```

          New Project                  Existing Project
```text
                 │                           │
                 ▼                           ▼
```

         arch_decision                OpenSpec Explore
```text
                 │                           │
                 │                    Architecture Impact?
                 │                           │
                 │                    ┌──────┴──────┐
                 │                    │             │
                 │                   NO            YES
                 │                    │             │
                 │                    │             ▼
                 │                    │       arch_decision
                 │                    │             │
                 │                    │             ▼
                 │                    │       Architecture
                 │                    │        Accepted
                 │                    │             │
                 └────────────┬───────┴─────────────┘
                              ▼
                    ┌─────────────────┐
                    │ Spec / Change   │
                    │ Accepted        │
                    └────────┬────────┘
                             ▼
                       Claude Code
                             ▼
                        Implementation
                             ▼
                         Verification
                             ▼
                          Archive
```

## 33. Claude Code 在这里到底是什么？

这个问题也很重要。

Claude Code 不是第四个 Spec Framework。

它是：

Agent Runtime / Execution Engine

它负责：

```text
读取规则
   ↓
读取 Spec
   ↓
读取 Architecture
   ↓
分析代码
   ↓
修改文件
   ↓
执行命令
   ↓
运行测试
   ↓
提交结果
```

而：

arch_decision
Spec Kit
OpenSpec

负责定义：

应该怎么思考
应该产生什么 artifact
什么时候允许进入下一阶段

这四者组合以后就非常合理。

## 34. Claude Code 中最终会出现什么？

大致会有：

Claude Code

arch_decision:
    project workflow
    architecture rules
    technology decisions

Spec Kit:
```bash
    /speckit.constitution
    /speckit.specify
    /speckit.clarify
    /speckit.plan
    /speckit.checklist
    /speckit.tasks
    /speckit.analyze
    /speckit.implement
    /speckit.converge
```

OpenSpec:
```bash
    /opsx:explore
    /opsx:propose
    /opsx:apply
    /opsx:update
    /opsx:sync
    /opsx:archive
```

Spec Kit 和 OpenSpec 当前都已经把 workflow/skill 设计成 Agent 可调用的流程，而不是要求用户自己手动执行每个文件操作。

## 35. 最推荐的实际 Prompt 体系

我建议你以后不要让用户记几十条 Prompt。

只需要记住三个入口。

新项目
/arch-new-project

语义：

Discovery
→ Draft Spec
→ Architecture Decision
→ Technology Selection
→ Human Gate
→ Accepted Architecture

然后：

```bash
/speckit-specify
```

再：

```bash
/speckit-clarify
/speckit-plan
/speckit-checklist
/speckit-tasks
/speckit-analyze
/speckit-implement
/speckit-converge
```

已有项目新增 Feature
```bash
/opsx:explore
```

然后：

```bash
/opsx:propose
```

Review。

然后：

```bash
/opsx:apply
```

最后：

```bash
/opsx:verify
/opsx:archive
```

Feature 过程中发现架构变化

统一走：

ARCHITECTURE_CHANGE_REQUEST

然后：

```text
arch_decision
       ↓
Re-evaluate
       ↓
Accepted
       ↓
return to Spec Kit / OpenSpec
```

## 36. 我建议你给 arch_decision 增加一个“Agent Adapter”概念

这里是我看完你现在 v1.5 仓库以后，觉得下一步最值得做的地方。

现在你的 arch_decision 已经有：

.sdd/
AGENTS.md
CLAUDE.md
workflows/
decision-trees/
knowledge/
templates/
schema/
scripts/

并且当前 README 已经明确把 CLAUDE.md / AGENTS.md 定位成 Agent 入口，把 .sdd/ 定位成规则体系。

下一步可以增加：

```text
adapters/
├── claude-code/
│   ├── AGENTS.md
│   └── commands/
├── spec-kit/
│   ├── workflow.yml
│   └── instructions/
└── openspec/
    ├── config.yaml
    └── instructions/
```

这样：

```text
arch_decision
       ├── Claude Code Adapter
       ├── Spec Kit Adapter
       └── OpenSpec Adapter
```

而不是把 Spec Kit / OpenSpec 的规则直接复制进 .sdd/。

这与 Spec Kit 当前已经支持可组合 workflow 的机制尤其契合。Spec Kit 现在的 workflow 可以包含 command、shell、human gate、条件、循环等，并支持自定义 workflow；官方已经提供带 review gate 的完整 SDD workflow。

## 37. 最终可以做成一个“一键初始化”

理想状态下，新项目只需要：

```bash
arch-decision init enterprise-ai-kb
```

然后自动完成：

1. 初始化 Git

2. 安装 arch_decision v1.5

3. 安装 Spec Kit

4. 初始化 OpenSpec

5. 配置 Claude Code

6. 创建 AGENTS.md

7. 创建 CLAUDE.md

8. 创建 .sdd/

9. 创建 specs/

10. 创建 openspec/

11. 安装 Agent Skills

12. 配置 Architecture Gate

最终：

```text
enterprise-ai-kb/
├── .sdd/
├── .specify/
├── openspec/
├── specs/
├── .claude/
├── AGENTS.md
├── CLAUDE.md
├── src/
└── tests/
```

然后用户只需要：

```bash
claude
```

第一句话：

创建这个项目：
企业内部 AI Knowledge Base。

先不要写代码。
执行 Architecture Decision。

之后 Agent 自动完成：

```text
                    User
                      ▼
               arch_decision
             Architecture Gate
                      ▼
              ACCEPTED / STOP
                      ▼
                Spec Kit
       Specify → Clarify → Plan
                      ▼
                 Tasks
                      ▼
               Claude Code
                      ▼
               Implement
                      ▼
                Converge
                      ▼
                  Release
```

以后发生需求变化：

```text
User
 ▼
OpenSpec Explore
 ├── 普通 Change ──────────────┐
 │                            │
 │                            ▼
 │                         Propose
 │                            │
 │                            ▼
 │                          Apply
 │                            │
 │                            ▼
 │                         Archive
 └── Architecture Impact
             ▼
       arch_decision
             ▼
       Re-Architecture
             ▼
       OpenSpec Apply
```

## 38. 最终职责边界，我建议固定成这张表
| 阶段 | arch_decision | Spec Kit | OpenSpec | Claude Code |
| --- | --- | --- | --- | --- |
| Discovery | 主责 |  | Explore | 执行 |
| 需求理解 | 主责 | Specify | Explore | 执行 |
| WHAT / WHY | 参与 | 主责 | 主责 Change | 执行 |
| Architecture | 唯一决策者 | 消费 | 提出影响 | 执行 |
| Technology Selection | 唯一决策者 | 消费 | 消费 | 执行 |
| Spec | 提供约束 | 主责 | Change Spec | 执行 |
| Plan | 提供 Architecture | 主责 | Design | 执行 |
| Tasks | 约束 | 主责 | 主责 Change | 执行 |
| Implementation | Gate | 调度 | 调度 | 主责 |
| Verification | Architecture Verification | Converge | Verify | 执行 |
| Change | 判断 Architecture Impact | 可选 | 主责 | 执行 |
| Archive | 决策记录 | Spec history | 主责 | 执行 |
| Human Gate | 主责 | 可有 review gate | Proposal review | 执行 |

## 39. 最核心的设计原则

如果把整个方案压缩成 5 条规则，我建议就是：

Rule 1

arch_decision 决定 Architecture 和 Technology。

Spec Kit / OpenSpec 不得静默推翻 Accepted Architecture。


Rule 2

Spec Kit 主要用于：

New Project / New Feature

OpenSpec 主要用于：

Change / Evolution


Rule 3

Claude Code 是执行 Agent，不是架构决策权威。


Rule 4

任何工具发现 Architecture 不再满足需求：

ARCHITECTURE_CHANGE_REQUEST

→ 回到 arch_decision。


Rule 5

Architecture Accepted 是进入 Implementation 的 Gate。

最终你这个项目的定位就非常明确了：

arch_decision 不是另一个 Spec Kit，也不是另一个 OpenSpec。

它是位于 Requirement 与 SDD Workflow 之间的 Architecture Governance Layer。

而且这套定位和你现在 v1.5 的设计已经相当吻合：当前仓库已经把决策语义、默认选型、流程顺序、Canonical ownership、Verification 等分别放在 .sdd/ 的权威位置，而 AGENTS.md / CLAUDE.md 只负责 Agent 路由。

我认为下一步最值得做的不是继续往 arch_decision 里堆规则，而是做一个 Claude Code + Spec Kit + OpenSpec Adapter，把上面这套流程真正变成 Agent 可以一键执行的 workflow。 Spec Kit 当前已经提供可编排的 workflow/gate 机制，OpenSpec 也已经提供 Claude Code 的 skills/commands 机制，因此技术上非常适合往这个方向落地

