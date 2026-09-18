我重新读取了你现在仓库的 main 分支。相比上一版，v1.3 的核心修正方向基本正确：Spec 前置、AUTO/RECOMMEND 不阻塞、P0A/P0B、Default = Candidate Prior、版本策略、真 Schema 校验等都已经进入文档体系。CHANGELOG.md 也明确记录了这些修复。

但是这次检查发现一个比较重要的情况：

你现在不是“还有一些小问题”，而是 v1.3 的部分修改已经写进 CLAUDE.md / AGENTS.md / CHANGELOG，但没有完整同步到 .sdd 的 canonical rule、workflow、template 和 validator。

因此目前仓库出现了新的 “上层 Agent 指令已经 v1.3，但底层规则仍残留 v1.1/v1.2 语义” 的状态。

我建议把下面的问题作为 v1.3.1 修复。

一、P0：decision-protocol.md 仍然存在旧规则

这是当前最严重的问题。

你在 CLAUDE.md / AGENTS.md 已经定义：

AUTO
→ 直接执行

RECOMMEND
→ 采用推荐方案继续，不阻塞

REQUIRE_CONFIRMATION
→ 必须人工确认

BLOCKED
→ 只有重大、不可逆、高风险且没有安全默认值才停止

但是 decision-protocol.md 仍然写着：

RECOMMEND → 提出方案，建议人确认

以及：

BLOCKED → 信息不足，停止，请求澄清

更严重的是，§8 的旧规则仍然写：

3. 用户明确要求是 Hard Constraint。

而你新的 P0A/P0B 已经明确不是这个语义。

最后 §9 又重新写回：

技术栈这类有长期锁定成本的决定，应先 Architecture Proposal → Human Confirmation

这和 v1.3 的核心修复再次冲突。

必须修改

建议直接重写 decision-protocol.md 的：

§6
§8
§9

尤其是 §6：

decision-protocol.md §6 决策状态替换内容
6. 决策状态（Decision Status）

每个架构 / 技术决策必须标记一个状态：

Status	含义	Agent 行为
AUTO	规则可以直接确定，风险低且可逆	直接决定并记录，不询问用户
RECOMMEND	存在合理选择，但推荐方案可安全采用	采用推荐方案继续执行，并记录 alternatives / assumptions / reversibility / review_triggers；不阻塞
REQUIRE_CONFIRMATION	对架构、合规、兼容性、长期锁定或高风险行为有重大影响	必须请求人工确认；未确认不得进入相关实现
BLOCKED	缺失信息导致重大、不可逆或高风险决策无法安全继续，且不存在安全可逆默认值	停止并请求最小必要澄清
6.1 RECOMMEND 与 REQUIRE_CONFIRMATION 的边界

RECOMMEND 不等于“等待用户确认”。

只有以下情况才升级为 REQUIRE_CONFIRMATION：

改变系统边界或部署拓扑；
引入长期运维责任；
改变认证 / 授权 / 合规边界；
改变公共 API 契约；
引入不可逆或高成本迁移；
涉及付款、数据驻留、法规或组织级约束；
用户明确要求人工审批；
规则库明确将该决策定义为 REQUIRE_CONFIRMATION。

普通语言、框架、ORM、测试工具、包管理器、缓存是否引入等，
只要满足 Hard Constraints 且属于 AUTO / RECOMMEND，Agent 不得为了免责而逐项询问用户。

6.2 BLOCKED 的使用条件

以下条件必须同时满足：

缺失的信息会改变重大架构 / 安全 / 合规 / 数据一致性 / 部署决策；
该决策具有明显不可逆或高风险后果；
没有安全的可逆默认方案。

否则不得使用 BLOCKED。

6.3 Assumptions

CAN_ASSUME 或 RECOMMEND 产生的假设必须记录在：

technology-selection.md
decision.json

必要时同步到 spec.md 的 Assumptions。

只有该假设本身构成重要 Architecture Decision 时，才需要 ADR。

6.4 默认 REQUIRE_CONFIRMATION

以下决策默认属于 REQUIRE_CONFIRMATION：

Microservices
Kubernetes
Multi-region
Database migration
Authentication architecture
Authorization model
Payment architecture
Data residency
Compliance
Cloud provider lock-in
Event-driven architecture
CQRS
Event Sourcing
Distributed transaction
Public API contract
Breaking API change
Major technology migration
用户明确要求人工审批的决策

该列表之外，不得仅因为“长期锁定成本”而自动升级为 REQUIRE_CONFIRMATION。

然后把 §8 的旧规则：

3. 用户明确要求是 Hard Constraint。

改成：

3. 用户明确表达“必须 / 不得 / 组织标准 / 不可改变”时，视为 P0B Hard Constraint；
   “偏好 / 熟悉 / 倾向 / 最好用”默认属于 Preference。
4. P0A（安全 / 合规 / 技术不可行 / 平台不可能）高于 P0B。
二、P0：new-project.md 还是旧流程

这是另一个非常明显的遗漏。

你现在 CLAUDE.md 已经是：

Requirement
→ Discovery
→ Draft Spec
→ Decision
→ Technology Selection
→ Confirmation
→ Final Spec
→ Plan
→ Design
→ Tasks

但 .sdd/workflows/new-project.md 仍然是：

Discovery
→ Architecture Decision
→ Technology Selection
→ Human Confirmation
→ Specification
→ Design / Plan
→ Tasks

这意味着 Agent 如果严格按照 CLAUDE.md 执行是一套行为，严格按照 workflow 执行又是另一套行为。

修改 new-project.md

建议把整个 §1/流程骨架统一成：

new-project.md canonical workflow
Agent 决策流程
User Requirement
      ↓
1. Project Discovery
      ↓
2. Draft Specification
   - WHAT / WHY
   - Functional Requirements
   - NFR
   - Constraints
   - Acceptance Criteria
   - Open Questions
      ↓
3. Decision Protocol
   - Project Classification
   - Hard / Soft Constraints
   - Existing Stack
   - Candidate Generation
   - Hard Constraint Elimination
      ↓
4. Architecture + Technology Selection
   - Architecture
   - Backend
   - Frontend
   - Database
   - Infrastructure
   - Testing
   - Observability
      ↓
5. Decision Status
   - AUTO → continue
   - RECOMMEND → continue
   - REQUIRE_CONFIRMATION → ask human
   - BLOCKED → ask minimum clarification
      ↓
6. Final Specification
   Draft → Accepted
      ↓
7. Plan
      ↓
8. Design（按需）
      ↓
9. ADR（按需）
      ↓
10. Tasks
      ↓
11. Implementation
      ↓
12. Tests
      ↓
13. Verification
      ↓
14. Consistency / Traceability Check
重要规则

technology-selection.md 不得反向定义需求。

如果技术选型过程中发现 Draft Spec 缺少影响架构的重要需求：

Decision
   ↓
发现需求缺口
   ↓
回到 Spec
   ↓
补充 / 修正 Requirement
   ↓
重新执行受影响的 Decision

不得为了让某个技术方案成立而修改需求。

Decision Status

只有 REQUIRE_CONFIRMATION 和 BLOCKED 会阻塞实现。

AUTO 与 RECOMMEND 不阻塞。

Final Spec

技术选型完成后，将 Draft Spec 更新为 Accepted。

Accepted Spec 是实现阶段的需求基准。

如果实现过程中发现 Spec 错误：

Code → 不得直接绕过 Spec
Spec → Plan / Design → Tasks → Code

必须先更新上游产物，再继续实现。

三、P0：LAYOUT.md 又和 v1.3 冲突了

这个问题很容易被忽略。

CHANGELOG v1.3 明确说：

design.md 与 adr/ 改为按需。

但是 LAYOUT.md 当前仍然写：

design.md       # 必填
adr/            # 必填
    ADR-001...

这实际上又把 v1.3 的改动推翻了。

修改为
LAYOUT.md specs 产物规则替换内容
1.1 Spec Instance Artifacts
specs/<id>-<name>/
├── project-discovery.md       # 必填
├── technology-selection.md    # 必填
├── decision.json              # 必填
├── spec.md                    # 必填
├── plan.md                    # 必填
├── tasks.md                   # 必填
└── verification.md            # 必填

design.md                      # 按需
adr/                           # 按需
research.md                    # 按需
data-model.md                 # 按需
api-contract.md                # 按需
architecture.md               # 按需
design.md

仅当 plan.md 无法清晰表达以下内容时创建：

复杂领域模型
状态机
并发控制
异步工作流
多外部系统集成
分布式一致性
复杂 API Contract
安全敏感流程
复杂算法
需要独立审查的详细设计

否则不创建。

adr/

只有存在需要长期保留的 Architecture Decision 时创建。

例如：

Microservices
Kubernetes
Database migration
Auth architecture
Event-driven architecture
CQRS / Event Sourcing
Distributed transaction
Public API contract
重大技术迁移

普通的 AUTO / RECOMMEND 技术选择不为了形式而创建 ADR。

verification.md

必须存在。

它记录：

Acceptance Criteria 验证结果
Test Results
Requirement → Test Traceability
Spec → Plan → Tasks → Code 一致性
未解决风险
未通过项及处理方式
四、P0：实际上缺少 templates/verification.md

这个问题是我这次新发现的，而且是一个真实的结构缺口。

LAYOUT.md 声明：

verification.md 必填

但 .sdd/templates/ 当前只有：

project-discovery
technology-selection
spec
design
plan
tasks
adr

没有 verification.md。.sdd/README.md 也只列这 7 个模板。

而 new-project 最终又明确需要 Verification。

应新增
.sdd/templates/verification.md

建议：

.sdd/templates/verification.md
Template: Verification

用途：证明实现结果满足 Accepted Spec、Plan、Tasks 和 Acceptance Criteria。

Verification: <Feature Name>
1. Verification Status
Status: Draft / Passed / Passed with Known Issues / Failed
Verified At:
Verified By:
Commit / Revision:
2. Acceptance Criteria
AC	Description	Verification Method	Result	Evidence
AC-001	
	Test / Manual / Inspection	PASS/FAIL	

AC-002	
	
	
	

3. Requirement Traceability
Requirement	Design	Task	Code	Test	Result
FR-001	D-001	T-001	
	TEST-001	PASS
4. Test Results
Unit
Command:
Result:
Integration
Command:
Result:
E2E
Command:
Result:
5. Non-Functional Verification
Performance
Target:
Actual:
Evidence:
Security
Checks:
Result:
Availability / Reliability
Checks:
Result:
Observability
Logs:
Metrics:
Tracing:
Result:
6. Consistency Check

Accepted Spec ↔ Plan consistent

Plan ↔ Tasks consistent

Tasks ↔ Code consistent

Requirements ↔ Tests traceable

No undocumented architecture changes

No unresolved REQUIRE_CONFIRMATION decision

No unresolved BLOCKED decision

7. Known Issues
Issue	Severity	Impact	Follow-up
8. Final Verdict

PASS

PASS WITH KNOWN ISSUES

FAIL

Evidence / Notes

同时 .sdd/README.md 的模板列表增加：

verification.md
五、P0：你说“真 Schema 校验”，但 validate_rules.py 目前实际上没有调用 mini_schema.py

这是我认为这轮审查中最值得重视的工程实现问题。

CHANGELOG v1.3 宣称：

validate_rules.py 对 decision.json 做真 Schema 校验。

而 mini_schema.py 确实已经存在，而且实现了真正的 JSON Schema 子集校验。

但是当前 validate_rules.py 里：

check_decision_schema(files)

检查的仍然是 Markdown 里的 YAML block：

YAML_BLOCK.findall(text)

然后只是：

for key in required:
    ...

即检查 key 是否存在。

它没有调用 mini_schema.validate()。

更进一步，它也没有使用你已经写好的 sdd_refs.py，虽然 changelog 宣称两个脚本已经统一使用 sdd_refs.py。

所以这里实际上是：

CHANGELOG
    ↓
声称 v1.3 已完成

代码
    ↓
v1.2 的部分实现 + v1.3 新文件
建议直接修 validate_rules.py

核心逻辑应该变成：

from mini_schema import validate as validate_json_schema

def check_decision_json():
    schema_path = ROOT / ".sdd" / "schema" / "decision.schema.json"

    for decision_path in ROOT.glob("specs/*/decision.json"):
        data = json.loads(decision_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        errors = validate_json_schema(data, schema)

        for error in errors:
            errors.append(
                f"[Decision JSON Schema] {decision_path}: {error}"
            )

并且：

technology-selection.md
    ↓
YAML block

只做：

structural mirror check

而：

decision.json
    ↓
canonical machine-readable source
    ↓
mini_schema

做真正 Schema validation。

更重要的是：

decision.json 应成为机器权威来源。

你现在已经在 decision.json 自己写了：

权威可校验实例

这是正确方向。

六、P1：Schema 本身还没有完全覆盖 Decision Protocol

你现在的 Schema 已经不错，但还存在一个明显遗漏：

Decision Protocol 要求重大决策输出：

decision
reason
evidence
alternatives
rejected
constraints
risks
confidence

但是 decision.schema.json 目前核心字段里：

rejected
risks
assumptions
confidence

比较完整，却没有把：

evidence
constraints
alternatives
scores
versions

作为结构化 Contract 的正式字段。Schema 目前虽然有 decision_status、complexity、cost，但 versions 甚至没有进入 properties。

而实例 decision.json 已经有：

"versions": [...]

这意味着 Schema 与实例实际上又开始漂移。

建议 Schema 增加
"evidence": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["claim", "source"],
    "properties": {
      "claim": { "type": "string" },
      "source": { "type": "string" },
      "verified_at": { "type": ["string", "null"] }
    }
  }
},
"constraints": {
  "type": "array",
  "items": { "type": "string" }
},
"alternatives": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["option"],
    "properties": {
      "option": { "type": "string" },
      "reason": { "type": "string" }
    }
  }
},
"versions": {
  "type": "array",
  "items": {
    "type": "object",
    "required": [
      "technology",
      "selected",
      "support_status",
      "verified_at",
      "reason"
    ],
    "properties": {
      "technology": { "type": "string" },
      "selected": { "type": "string" },
      "support_status": {
        "type": "string",
        "enum": [
          "supported",
          "LTS",
          "maintenance",
          "EOL",
          "UNKNOWN"
        ]
      },
      "verified_at": {
        "type": ["string", "null"]
      },
      "source_url": {
        "type": ["string", "null"]
      },
      "reason": {
        "type": "string"
      }
    }
  }
}

特别推荐加：

source_url

因为你已经要求：

新项目版本必须对着上游官方文档核实。

那么应该把“核实过”变成可审计的数据，而不是一句自然语言。

七、P1：decision.json 的成本状态存在逻辑矛盾

你的示例：

"cost": {
  "recurring": "...",
  "cap": "UNKNOWN",
  "within_budget": true
}

这个逻辑其实有问题：

预算上限 UNKNOWN
       +
within_budget = true

Agent 是如何知道在预算内的？

而 decision-protocol 明确要求成本：

必须可量化，不能“大概不贵”。

修改 Schema

不要：

"within_budget": {
  "type": "boolean"
}

改成：

"within_budget": {
  "type": ["boolean", "null"]
}

语义：

true  = 已知预算范围内
false = 明确超预算
null  = 无预算数据，无法判断

同时增加：

"budget_basis": {
  "type": ["string", "null"]
}

例如：

{
  "recurring": "$80-120/month",
  "cap": "$150/month",
  "budget_basis": "project monthly infrastructure budget",
  "within_budget": true
}
八、P1：RECOMMEND 的语义在 technology-selection.md 仍然是旧版

模板目前仍写：

RECOMMEND → 提出方案，建议人确认

而且：

Architecture Summary → 先输出给人确认。

这和 CLAUDE.md / AGENTS.md 的 v1.3 规则直接冲突。

修改

把：

RECOMMEND → 提出方案，建议人确认

改成：

RECOMMEND → Agent 采用推荐方案继续执行。
必须记录：
- alternatives
- assumptions
- reversibility
- review_triggers

不阻塞用户。

把：

Architecture Summary（先输出给人确认）

改成：

Architecture Summary

仅当其中存在 REQUIRE_CONFIRMATION 决策时，
才暂停并请求人工确认。

如果全部为 AUTO / RECOMMEND，
Agent 可以直接继续生成 Final Spec / Plan / Tasks。
九、P1：plan.md 仍然保留了旧的 Human Confirmation 语义

现在：

技术栈类决定建议先 Human Confirmation 再固化

这已经不应该存在。

修改
技术决策必须从 technology-selection.md 继承。

- AUTO → 直接固化
- RECOMMEND → 直接固化，并记录假设 / 可逆性
- REQUIRE_CONFIRMATION → 确认后固化
- BLOCKED → 不得固化并不得实现
十、P1：decision-protocol 的决策循环仍然没有真正升级到 v1.3

现在仍然：

1 Read requirements
2 Classify
3 constraints
...
10 Generate ADR
...
13 plan
14 tasks
15 consistency

缺：

Draft Spec
Final Spec
Human Confirmation Gate
Design optional
Verification
建议把 §7 改成
1. Read / capture requirements
2. Project Discovery
3. Draft Specification
4. Extract Hard Constraints
5. Extract Soft Constraints
6. Detect Existing Stack
7. Generate Candidates
8. Eliminate Hard-Constraint Violations
9. Select / Score remaining candidates
10. Validate Architecture Complexity / Cost
11. Mark Decision Status
12. Resolve REQUIRE_CONFIRMATION / BLOCKED
13. Finalize Accepted Spec
14. Generate Plan
15. Generate Design if required
16. Generate ADR if required
17. Generate Tasks
18. Implement
19. Test
20. Verify
21. Run Spec → Plan → Tasks → Code → Tests consistency check

这才和你现在的 CLAUDE.md 真正一致。

十一、P1：CAN_ASSUME 不应该要求 ADR

现在 CLAUDE.md：

CAN ASSUME
→ 假设必须写入 ADR

但你已经把 ADR 改成按需。

这是一个小但真实的冲突。

建议：

CAN_ASSUME
→ 必须写入 technology-selection.md / decision.json assumptions。

只有该假设产生重要 Architecture Decision 时，
才创建 ADR。

这个规则应该同步到：

CLAUDE.md
AGENTS.md
decision-protocol.md
adr.md
十二、P1：README / .sdd/README / CHANGELOG 版本号不一致

根 README 当前写：

当前规则库版本：v1.1

但是 CHANGELOG.md 已经有：

v1.3 — 2026-09-19

这属于非常典型的 release metadata drift。

修改 README
当前规则库版本：v1.3

同时 .sdd/README.md 也应：

当前规则库版本：v1.3

最好不要人工维护两个地方。

进一步建议：

VERSION

单独文件：

.sdd/VERSION

内容：

1.3

然后：

README
CHANGELOG
validation

都可以检查它。

十三、P1：.sdd/README.md 仍然是旧流程

当前：

新项目：
CLAUDE.md §2
→ read decision-protocol
→ workflow + knowledge + decision-trees
→ template

以及：

技术栈类决定先 Architecture Proposal → Human Confirmation。

这也是 v1.1/v1.2 遗留。

应该明确：

Requirement
→ Discovery
→ Draft Spec
→ Decision
→ Technology Selection
→ Decision Status
→ Final Spec
→ Plan
→ Design（optional）
→ ADR（optional）
→ Tasks
→ Implementation
→ Verification
十四、一个更隐蔽的问题：TRACEABILITY 目前仍然不是“内容覆盖率”

这个你自己在 CHANGELOG 已经意识到了：

引用率 ≠ 内容覆盖率。

这一点非常正确。

但是我建议下一版真正把它解决掉。

现在：

res.md §42
    ↓
某个文件引用 res.md §42

只能证明：

“这个规则有人提到了”

不能证明：

“这个规则真的被正确实现了”
建议把 Traceability 升级为 4 种状态
SOURCE
  ↓
MAPPED
  ↓
IMPLEMENTED
  ↓
VERIFIED

例如：

Source	Rule	Implemented	Verified	Canonical
res.md §23	PostgreSQL default	database.md	decision test	database.md
res.md §64	DB migration confirmation	decision-protocol.md	validator test	decision-protocol.md
res.md §88	Version strategy	versioning.md	schema test	versioning.md

这样以后你的规则库才真正具备：

Rule → Implementation → Verification

的闭环。

十五、目前还有一个重要的“内容遗漏”：没有把“证据”提升到一等公民

你的体系现在已经有：

decision
reason
alternatives
rejected
risks
confidence

但对于 Agent 架构决策来说，我认为还缺一个：

Evidence

这是下一阶段非常值得补的。

例如 Agent 说：

PostgreSQL > MySQL

不能只是：

reason:
  PostgreSQL is preferred

应该：

decision:
  selected: PostgreSQL

evidence:
  - type: requirement
    claim: relational transactional workload
    source: spec.md#FR-003

  - type: constraint
    claim: JSON querying required
    source: spec.md#NFR-004

  - type: team
    claim: team has existing PostgreSQL operational experience
    source: project-discovery.md#team

  - type: documentation
    claim: selected version is supported
    source: official documentation
    verified_at: 2026-09-19

这样你的决策系统会从：

Rule-based recommendation

进一步变成：

Evidence-backed decision

这是我认为 arch_decision 后续最有价值的升级方向之一。

十六、另一个遗漏：缺少“Decision Re-evaluation Trigger”

你已经有：

reversibility

这是好的。

但还缺：

什么时候重新评估？

例如：

Redis = 不引入

不是永久结论。

应该：

review_triggers:
  - p95 latency > 300ms
  - cache hit opportunity > 60%
  - session storage exceeds application memory
  - rate-limit requirement introduced

再例如：

Modular Monolith

可以：

review_triggers:
  - independent scaling requirement appears
  - team ownership split exceeds 2 teams
  - deployment coupling becomes release blocker
  - fault isolation becomes explicit requirement

建议在 decision.json 增加：

"review_triggers": []

这样你的：

AUTO

不是：

永远如此

而是：

在当前证据与约束下如此，满足某些条件时重新决策。

这会非常符合真正的架构治理。

十七、还建议补一类“架构负债 / Deferred Decision”

目前体系比较强调：

选什么

但实际项目里经常是：

现在不做
以后可能做

例如：

不引入 Redis
不引入 Kafka
不做 Microservices
不做 Multi-region
不做 Elasticsearch

这些不应该全部写成 Rejected。

应该区分：

REJECTED

和：

DEFERRED

例如：

deferred:
  - decision: Redis
    reason: current workload does not justify operational complexity
    trigger:
      - p95 latency > threshold
      - cache requirement appears

这样 Agent 下次继续项目时不会重新从零判断。

十八、建议补一个 decision-log.md 或直接增强 decision.json

当前：

technology-selection.md
decision.json
ADR

已经比较完整。

但随着项目演进：

v1:
PostgreSQL

v2:
Redis added

v3:
Kafka added

v4:
Microservice split

你需要知道：

为什么改变？
谁改变？
依据什么？
哪个旧决策被 invalidated？

所以我建议不一定新增文件，直接在 decision.json 增加：

"decision_history": [
  {
    "decision": "architecture",
    "from": "Modular Monolith",
    "to": "Microservices",
    "changed_at": "2027-...",
    "reason": "...",
    "trigger": "...",
    "supersedes": "ADR-001"
  }
]

如果未来规模扩大，再拆成 ADR。

十九、内容方面，我建议下一版补齐 6 个领域

目前知识库已经有：

architecture
backend
frontend
database
caching
messaging
api
security
testing
deployment
observability
ai-llm
data

这个覆盖面已经不错。

但是如果目标是：

让 Agent 可以从需求直接完成 Architecture Decision

我认为还缺以下几个独立的决策维度。

1. reliability.md

建议覆盖：

SLA / SLO / SLI
Availability
RPO / RTO
Backup
Restore
Failover
Graceful degradation
Retry
Circuit breaker
Idempotency
Disaster Recovery
2. multi-tenancy.md

目前 database/architecture 提到多租户，但建议独立出来：

Single tenant
Shared DB / Shared Schema
Shared DB / Separate Schema
Database per Tenant
Hybrid

并且定义：

tenant isolation
authorization
data leakage prevention
migration
backup/restore
tenant-specific configuration

这是 SaaS 架构非常核心的一条决策线。

3. data-lifecycle.md

覆盖：

Data retention
Deletion
Archive
PII
Encryption
Backup retention
Audit log
Export
Import
Data residency

尤其你已经把：

Compliance
Data residency

设成 REQUIRE_CONFIRMATION，那么必须有对应知识来源，否则 Agent 只能知道“要问”，却不知道“问什么”。

4. integration.md

现在 API / Messaging / Security 分散处理外部系统。

可以统一：

REST
Webhook
Polling
SFTP
OAuth
API Key
Message Queue
CDC
Retry
Timeout
Idempotency
Rate Limit
Circuit Breaker
5. configuration.md

覆盖：

Environment variables
Secrets
Config files
Secret manager
Feature flags
Runtime config
Build-time config

Agent 经常会在这里犯错。

6. dependency-management.md

现在 versioning 解决的是：

版本

但没有完整解决：

为什么引入一个第三方依赖？

建议明确：

Before adding dependency:

1. Standard library sufficient?
2. Existing dependency sufficient?
3. Internal implementation cheaper?
4. License acceptable?
5. Maintenance active?
6. Security history acceptable?
7. Bundle/runtime cost?
8. Can it be removed later?
二十、我认为还缺一个真正重要的 Agent 能力：Impact Analysis

现在 workflow 主要解决：

我要做什么？

但是 Brownfield 项目特别需要：

这个改动会影响什么？

建议在 new-feature.md 前面增加：

Impact Analysis

Before deciding:

- affected modules
- affected APIs
- affected DB tables
- affected external integrations
- affected auth/authz
- affected tests
- affected deployment
- affected observability
- migration requirement
- backward compatibility

最终输出：

impact:
  architecture: none
  database: affected
  api: affected
  security: none
  deployment: none
  migration: required

这比单纯的：

Technology impact → 是否引入新技术

更完整。

二十一、small-change 还需要一个“行为变化”检测，而不仅是行数

当前：

≤3 文件
≤100 行
不改架构
不改 API
不改安全
不改业务规则
不改依赖

这是一个很好的防止过度 SDD 的设计。

但：

100 行

不是风险指标。

比如：

if user.is_admin:

改成：

if user.is_owner:

可能只改一行，但属于权限规则变化。

你已经禁止了安全/业务规则变化，所以方向没问题。

建议增加：

Behavioral Risk Check

即使满足文件数 / 行数阈值，只要改变以下任一项：
- externally observable behavior
- authorization result
- persistence semantics
- error semantics
- transaction boundary
- concurrency behavior
- retry behavior
- default business behavior

立即升级为 new-feature / bugfix。

这样 Agent 不会被：

<=100 lines

误导。

二十二、最终我建议你把 v1.3.1 的修改分成三个层次
第一层：立即修复的 P0

这是现在必须做的：

1. decision-protocol.md
   ├── RECOMMEND 旧语义
   ├── BLOCKED 旧语义
   ├── 用户 Hard Constraint 旧语义
   ├── Agent decision loop 旧流程
   └── §9 Human Confirmation 旧语义

2. new-project.md
   └── 整体流程仍是旧流程

3. LAYOUT.md
   ├── design.md 仍标必填
   └── adr/ 仍标必填

4. templates/verification.md
   └── 实际不存在

5. validate_rules.py
   └── 没真正接入 mini_schema.py
第二层：P1 工程一致性
6. technology-selection.md
   └── RECOMMEND / Human Confirmation 旧语义

7. plan.md
   └── Human Confirmation 旧语义

8. .sdd/README.md
   └── 旧流程 + 旧确认规则

9. README.md
   └── v1.1 → v1.3

10. decision.schema.json
    ├── versions 没有正式 schema
    ├── evidence 缺失
    ├── constraints 缺失
    ├── alternatives 缺失
    └── scores 缺失

11. decision.json
    └── cost.cap=UNKNOWN 但 within_budget=true
第三层：v1.4 能力增强

我建议不要继续往 knowledge/*.md 里无休止增加技术知识，而是增加：

.sdd/
├── knowledge/
│   ├── reliability.md
│   ├── multi-tenancy.md
│   ├── data-lifecycle.md
│   ├── integration.md
│   ├── configuration.md
│   └── dependency-management.md
│
├── decision-trees/
│   ├── impact-analysis.md
│   └── ...
│
├── schema/
│   ├── decision.schema.json
│   ├── verification.schema.json
│   └── traceability.schema.json
│
└── templates/
    ├── verification.md
    └── ...

同时把决策模型升级成：

Requirement
     ↓
Discovery
     ↓
Draft Spec
     ↓
Impact Analysis
     ↓
Constraints
     ↓
Candidates
     ↓
Elimination
     ↓
Evidence
     ↓
Decision
     ↓
Status
     ↓
Review Triggers
     ↓
Final Spec
     ↓
Plan
     ↓
Tasks
     ↓
Code
     ↓
Tests
     ↓
Verification
     ↓
Traceability
最后一个很重要的判断

你这次更新以后，核心理念已经基本正确。现在最需要控制的不是“继续增加规则”，而是：

Canonical Rule Consistency。

也就是同一个语义，在仓库里只能存在一个权威定义。

目前至少有这些重复定义：

Decision Status
    decision-protocol.md
    CLAUDE.md
    AGENTS.md
    technology-selection.md
    new-project.md
    plan.md

Workflow
    CLAUDE.md
    AGENTS.md
    decision-protocol.md
    new-project.md
    .sdd/README.md

Artifact Required/Optional
    LAYOUT.md
    CLAUDE.md
    new-project.md
    templates/*.md

Schema
    decision.schema.json
    technology-selection.md YAML
    decision.json
    validate_rules.py
    mini_schema.py

这正是你现在最容易发生 rule drift 的地方。

我建议下一步不要再手工修改十几个文件，而是建立一个非常明确的：

Canonical Rule Ownership Matrix

例如：

主题	唯一权威
Workflow	.sdd/workflows/*.md
Decision semantics	decision-protocol.md
Directory	LAYOUT.md
Reference syntax	CONVENTIONS.md
Technology knowledge	knowledge/*.md
Candidate selection	decision-trees/*.md
Machine contract	decision.schema.json
Machine instance	decision.json
Human-readable decision	technology-selection.md
Spec structure	templates/spec.md
Verification	templates/verification.md
Agent entry	CLAUDE.md / AGENTS.md 只引用，不重新定义规则

然后让 validate_rules.py 不仅检查“有没有引用”，还检查这些 canonical invariants。

这样 arch_decision 才会从“很完整的一套 SDD 文档”真正进入下一阶段：

一个可以被 Agent 稳定执行、可以被机器校验、可以持续演进而不发生规则漂移的 Architecture Decision System。

另外，我注意到当前仓库的公开页面显示 main 最新提交只有 2 个 commit，而 CHANGELOG 已经写到 v1.3；这本身也值得在下一次提交时确认是否只是 GitHub 页面缓存/当前分支状态差异。