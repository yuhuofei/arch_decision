# Changelog

本文件记录 `.sdd/` 规则库的版本变更。约定见 `.sdd/CONVENTIONS.md` §5。

> 版本号唯一来源是 `.sdd/VERSION`；本文件的最新版本标题必须与它一致（`scripts/validate_rules.py` 会核对）。

---

## [v1.5] — 2026-09-19

**主题：Agent Entry 瘦身 —— 让 Canonical 硬规则 1 从"已声明"变成"已落实"**。

### 问题：v1.4 声明了原则，但入口文件没遵守

`v1.4` 新增的 `.sdd/CANONICAL.md` 硬规则 1 写明"**Agent 入口只引用，不重新定义**行为语义"，
但当时的 `CLAUDE.md` §5 与 `AGENTS.md` 仍然各写了一份完整的决策语义：

- 约束优先级 `P0A` / `P0B` / `P1`–`P3` 的**定义**
- 复杂度计分的**口径与数值**（组件 +1、Kafka/ES +2、K8s +3、预算档 5/6/8/12/20+）
- 决策状态 `AUTO` / `RECOMMEND` / `REQUIRE_CONFIRMATION` / `BLOCKED` 的**定义**
- 评分**公式**（`Requirement Fit×40 + Maintainability×20 + …`）
- **默认技术矩阵**（22 行 Default / Alternatives 表）
- `REQUIRE_CONFIRMATION` 的**默认清单**（与 `decision-protocol.md` §6.4 逐字重复）

即：同一份语义在 `CLAUDE.md`、`AGENTS.md`、`decision-protocol.md` 存在 **三份定义** —— 这正是 v1.3 的 rule drift 成因。

### 处置：入口文件退化为"路由"，语义回归唯一权威

| 语义 | 唯一权威（改动后） | 入口文件现在的写法 |
| --- | --- | --- |
| 约束优先级 / 硬软约束 / 默认值语义 | `decision-protocol.md` §2 / §3.1 / §3.4 | 路由表一行 |
| 评分公式与 rubric | `decision-protocol.md` §4 / §4.1 | 路由表一行 |
| 复杂度计分与预算 | `decision-protocol.md` §5 / §5.1 / §5.2 | 路由表一行 |
| 决策状态与确认门槛 | `decision-protocol.md` §6 | 路由表一行 |
| 默认选型（候选先验） | `.sdd/decision-trees/` 各领域文件 | 路由一行（**不再复制矩阵**） |
| 流程步序 | `.sdd/workflows/new-project.md` | `CLAUDE.md` §2 只列"读什么"，步序指向权威 |
| 提问策略 `MUST/SHOULD/CAN ASSUME` | `decision-protocol.md` §6 / §6.2 / §6.3 | `CLAUDE.md` §6 只给位置 |

**两份入口文件的新定位**（已登记进 `.sdd/CANONICAL.md` §1）：

- `CLAUDE.md` = **读取路由**：什么时候读什么、按什么顺序读（Step 0–8 + 按规模 / 按项目类型的追加读取表）。
- `AGENTS.md` = **通用工程规则 + 语义路由表 + DEFINITION OF DONE**。

**"要判断 X → 去读 Y"的路由表全局只有一份**，放在 `AGENTS.md` §4；`CLAUDE.md` §5 只指向它。
初稿曾把这张表同时写在两个文件里 —— 那是**这轮修复本身制造的新重复**，已合并。
`CLAUDE.md` 只保留"按顺序读哪些文件 / 追加读什么"（§2 / §3），与"去哪查语义"（`AGENTS.md` §4）职责分离。

同时去掉两份入口文件之间的重复：`FINAL PRINCIPLE`（`res.md §120`）此前两边都有，现只留 `AGENTS.md`；
读取顺序此前两边都有，现只留 `CLAUDE.md`。

### 顺带修正：入口文件里"看起来只是摘要"的重复

- `AGENTS.md` 的"最重要的规则"由 12 条改为 **6 条原则**。原第 4/5/6/7/8/9 条
  （Modular Monolith 默认、PostgreSQL 默认、Redis 非默认、REST 默认、TS/Python/Go 语言倾向）
  是**默认值的第二种写法**，与默认矩阵同源 —— 一并移出，指向 `.sdd/decision-trees/`。
  保留的 6 条是真正的工程原则（不追流行 / 不预支复杂度 / 复用存量栈 / 记录理由 / 追溯链 / Spec 前置）。
- `AGENTS.md` 的"禁止（不得静默决定）"清单与 `decision-protocol.md` §6.4 逐字重复 → 改为指针。
- `.sdd/README.md` 的"使用方式"第 3 条曾复述确认门槛与 `AUTO`/`RECOMMEND` 语义 → 改为指针。

### 修正：`CANONICAL.md` 曾登记两个不存在的检查项

v1.4 的归属矩阵在"机器校验"列写了 `check_decision_status_semantics` 与 `check_agent_entry_no_redefine`，
**这两个检查项在 `scripts/validate_rules.py` 里并不存在** —— 等于宣称了不存在的机器验证。
现已改为显式登记在 `.sdd/CANONICAL.md` §4「尚未实现的机器校验」，
并写明现状：**硬规则 1 目前只靠 `check_forbidden_semantics` 挡住旧句回流，挡不住"用新措辞再写一遍"，因此依赖 code review。**

### 影响面（引用同步）

- `CLAUDE.md` / `AGENTS.md`：重写。
- `.sdd/CANONICAL.md`：归属矩阵新增 `Default matrix` 行，`Agent entry` 拆为两行，新增 §4。
- `scripts/validate_rules.py`：`CANONICAL_TOPICS` 同步（新增 `Default matrix` 与两条 Agent entry）。**未新增任何检查项。**
- `.sdd/README.md`：上层文件说明 + 使用方式第 3 条。
- `.sdd/workflows/small-change.md`：入口由 `AGENTS.md` §0 改为 `CLAUDE.md` §3。
- `.sdd/decision-trees/decision-protocol.md` §7：不再以 `CLAUDE.md` §2 为流程顺序的依据。

### 未做（有意）

1. **未扩展 validator**：按约定先瘦身、再决定检查判据 —— 在"还没定义清楚什么叫重复"时固化检查项容易误报。
2. **未删除任何语义**：移出入口文件的内容全部已在权威文件中有落点（见上表），
   因此 5 份来源的"未引用"计数在本版仍为 0（由 `gen_traceability.py` 核对）。

---

## [v1.4] — 2026-09-19

**主题：Rule Drift 治理 + 决策契约补全**。
来源：`sources/v1.0/modv2.md`（22 项复核），逐项处置见 `REVIEW-2026-09-19.md` 的四审章节。

### 先说明：`modv2.md` 的 P0 清单多为旧快照误判

`modv2.md` 声称 `decision-protocol` / `new-project` / `LAYOUT` / `validate_rules` / `plan` /
`README` / `.sdd/README` 仍停留在 v1.1–v1.2 语义。逐条核实后，**这些判断不成立**：
该文档复核时读到的版本早于 v1.3 提交（它自己也注意到「公开页面显示 main 最新提交只有 2 个 commit」）。
核实证据：

| modv2 指控 | 实测 |
| --- | --- |
| `modv2.md` §1 `decision-protocol` §6/§8/§9 仍是旧语义 | 已是 v1.3 语义，文件内有「修正点（此前自相矛盾）」标注 |
| `modv2.md` §2 `new-project.md` 仍是旧流程 | 已是 `Discovery → Draft Spec → 决策 → Decision Status → Final Spec` |
| `modv2.md` §3 `LAYOUT.md` 把 `design.md` / `adr/` 标回必填 | 自 v1.3 即为**按需**，文件内有「v1.3 变更」标注 |
| `modv2.md` §5 `validate_rules.py` 没调用 `mini_schema` | 第 129 行已在调用（`check_decision_json`） |
| `modv2.md` §6 `versions` 未进入 Schema properties | 早已存在 |
| `modv2.md` §9 `plan.md` 仍是 Human Confirmation 旧语义 | 已是「仅 `REQUIRE_CONFIRMATION` 需先确认」 |
| `modv2.md` §12 root `README` 仍写 v1.1 ／ `modv2.md` §13 `.sdd/README` 旧流程 | 均为 v1.3 语义 |

**结论：本次不按「修旧语义」处理这些项；改为按「防回流 + 补真实缺口」处理。**

### 第一层：真实缺口修复（P0）

1. **新增 `templates/verification.md`**（`modv2.md §4`）
   `LAYOUT.md` 一直声明 `verification.md` 必填，但 `.sdd/templates/` 只有 7 个模板，没有它 —— 真结构缺口。
   新增 8 节模板（Status / AC 验证 / 需求追溯 / 测试结果 / NFR / 一致性检查 / Known Issues / Final Verdict）
   + `.sdd/schema/verification.schema.json` + `specs/001-project/verification.json`（机器实例）。
   `specs/001-project/verification.md` 同时从旧 4 节升级为新 8 节结构。

2. **`decision-protocol.md` §7 决策循环 15 步 → 21 步**（`modv2.md §10`）
   旧循环只覆盖「决策」子过程，缺 Draft Spec / Final Spec / 确认门槛 / 按需设计 / 验证。
   新循环到第 21 步「Spec → Plan → Tasks → Code → Tests consistency check」。

3. **`decision-protocol.md` §6 重排为 6.1–6.4**（`modv2.md §6`）
   - §6.1 `RECOMMEND` 与 `REQUIRE_CONFIRMATION` 的**边界**（8 条升级条件 + 不得为免责逐项询问）
   - §6.2 `BLOCKED` 的**三条件**与澄清模板（原 §6.1 模板移入）
   - §6.3 **Assumptions 记录位置**（`technology-selection.md` + `decision.json`，**不要求 ADR**）
   - §6.4 默认 `REQUIRE_CONFIRMATION` 清单（原 §6.0）

4. **`CAN_ASSUME` 不再要求 ADR**（`modv2.md §11`）
   `CLAUDE.md` §6、`decision-protocol` §6.3/§6.2、`adr.md` 同步；ADR 自 v1.3 起即为按需。

### 第二层：决策契约补全（P1）

5. **`decision.schema.json` 增结构化字段**（`modv2.md §6,§15-§18`）
   新增 `evidence`（**必填，minItems 1**）/ `constraints` / `alternatives` / `scores` /
   `deferred` / `review_triggers` / `decision_history`；`versions[]` 增 `source_url`；
   `cost.within_budget` 改为 `["boolean","null"]` 并增 `budget_basis`。
   `evidence` 是本次**理念上最重要的一条**：决策从「规则驱动的推荐」升级为「有据可查的判断」——
   `reason: PostgreSQL is preferred` 这类不可复核的理由不再足够。

6. **`cost` 逻辑矛盾修正**（`modv2.md §7`）
   两个实例均为 `cap: UNKNOWN` + `within_budget: true`——预算上限未知却判定「在预算内」。
   001 改为 `within_budget: null` + `budget_basis: null` 并把「预算上限未定」写入 `risks`；
   002 补 `budget_basis`。新增自检项 `check_cost_consistency` 防复发。

7. **`technology-selection.md` 模板**（`modv2.md §8`）
   删除 `Architecture Summary` 标题里的「先输出给人确认」残留（它与同文件下一段自相矛盾）；
   新增 Evidence / Deferred / Review Triggers / Decision History 四节与 YAML 镜像字段。

8. **`plan.md` / `.sdd/README.md` 的确认语义**（`modv2.md §9,§13`）
   核实后**无需修改**（已是收窄后语义）；`.sdd/README.md` 已重写以反映 v1.4 结构与四态追溯。

9. **`.sdd/VERSION` 单一版本来源**（`modv2.md §12`）
   新增 `.sdd/VERSION`（内容 `1.4`）；`README.md` / `.sdd/README.md` / `CHANGELOG.md` 引用它，
   自检项 `check_version_consistency` 强制三处一致（原来人工维护两处必然漂移）。

10. **两个实例的 `decision.json` / `technology-selection.md` YAML 镜像**同步新字段。

### 第三层：能力增强

11. **`CANONICAL.md` 规则归属矩阵**（`modv2.md §22`）
    16 个主题 → 唯一权威的对照表；配套自检项 `check_canonical_registry`、
    `check_workflow_order`、`check_forbidden_semantics`、`check_artifact_requiredness`。

12. **TRACEABILITY 升级为四态**（`modv2.md §14`）
    `MAPPED → IMPLEMENTED → VERIFIED`：`IMPLEMENTED` 由落点路径自动判定（是否落在实现层），
    `VERIFIED` 由人工登记的检查项决定（`VERIFIED_BY`，只登记真实存在的检查项）。
    同时产出机器可读的 `.sdd/traceability.json`。
    **`VERIFIED` 不等于内容正确** —— 与「引用率 ≠ 覆盖率」一起写进文件说明。

13. **6 个缺失知识域**（`modv2.md §19`）
    新增 `multi-tenancy` / `reliability` / `data-lifecycle` / `integration` / `configuration` /
    `dependency-management`。其中 `multi-tenancy` 接 `Matrix §22`、`dependency-management` 接
    `res.md §90`、`configuration` 接 `res.md §86,§87` 与 `知识库 §36`，其余条目标注「本仓补充」。
    **动机**：`Compliance` / `Data residency` 已被列为默认 `REQUIRE_CONFIRMATION`，
    若没有对应知识，Agent 只会「知道要问」却不知道「问什么」。

14. **`impact-analysis.md` 决策树 + `new-feature.md` 前置**（`modv2.md §20`）
    回答 Brownfield 的真正问题：「这个改动会影响什么」。

15. **`small-change.md` 增 Behavioral Risk Check**（`modv2.md §21`）
    行数不是风险指标；触及对外行为 / 授权判定 / 持久化语义 / 错误语义 / 事务边界 / 并发 /
    重试 / 默认业务行为即升级。

### 第 5 来源接入

`modv2.md` 用**中文序数**编号（`一、` … `二十二、`），与前三份及 `mod_gpt.md` 都不同。
其正文代码块含 `6.` / `6.1` 等阿拉伯编号小节，若混用模型会互相污染，
故 `scripts/sdd_refs.py` 按来源分派**三种条号模型**，`modv2.md` 取行首中文序数（得 1–22）。
登记于 `.sdd/CONVENTIONS.md` §1.1。

### 自检脚本新增 9 项检查

`check_cost_consistency` / `check_verification_json` / `check_verification_artifact` /
`check_verification_mirror` / `check_version_consistency` / `check_canonical_registry` /
`check_workflow_order` / `check_forbidden_semantics` / `check_artifact_requiredness`。

> 其中 `check_forbidden_semantics` 是**回归防护**：把 `modv2.md` 提到的旧语义写成禁止短语表，
> 一旦回流即报错。解释了历史需要保留旧原文时，在该行标注 `【已废弃】` 即可。
> `CHANGELOG.md` 与 `REVIEW-*.md` 天然豁免（它们必须能引用旧原文）。

---


### 第三层：文档一致性清理

- **`new-project.md` 移除冲突的"第二套步骤"**：原"Agent 决策循环"小节标题写"已升级为 21 步"，
  正文却只列 15 步，与 `decision-protocol.md §7` 的权威 21 步直接冲突。现改为**只指向
  `decision-protocol.md §7` 作为唯一权威**，本文件仅描述该循环在 new-project workflow 中的
  入口、阶段边界与产物，不再复制步骤（避免双份维护漂移）。符合"规则归属唯一权威"（`CANONICAL.md`）。
- **`decision.schema.json` 写清 `alternatives` / `rejected` 语义边界**：原描述「alternatives 保留理由、
  rejected 是淘汰结论」含混，导致 `MySQL` 在 `specs/001-project/decision.json` 里**同时**出现在两处。
  现明确：`alternatives` = 仍成立的**可行备选**；`rejected` = **淘汰结论**；**同一候选只应出现在二者之一**。
  同步修正 001 示例（`MySQL` 仅保留于 `alternatives`）。`rejected.minItems=1` 的设计债另记于
  `REVIEW-2026-09-19.md` 的「四审未做的事」，本轮**不改 Schema 结构**。
- **ADR 不再被写成"固定产物"**（3 处）：`LAYOUT.md §1.2` 自 v1.3 起即定 `adr/` **按需**，但以下三处
  仍把 ADR 与 `plan.md` / `decision.json` 并列为确认后的固定产物，与 LAYOUT 冲突：
  `.sdd/workflows/new-project.md`（确认门槛示意图）、`README.md`（流程总览）、
  `.sdd/decision-trees/decision-protocol.md`（§9 关键门槛——**与本文件 §2 已写的"ADR（按需）"自相矛盾**）。
  现统一为「固化 `decision.json` + `plan.md`；**如存在重要 Architecture Decision 再创建 `adr/`（按需）**」，
  并指向 `LAYOUT.md §1.2` 判据。避免 Agent 为满足流程而制造空 ADR。

## [v1.3] — 2026-09-19

**主题：Agent 可执行性优化**（不新增技术知识文件，只修执行语义）。
来源：`sources/v1.0/mod_gpt.md`（9 项评审意见），逐项落点见 `REVIEW-2026-09-19.md` 的三审章节。

### 修复（P0 — 流程与决策语义自相矛盾）

1. **Spec 前置，修正 canonical workflow**（`mod_gpt.md §1`）
   - 旧流程 `Discovery → Decision Protocol → Architecture → Backend/Frontend/Database → Technology Selection → Spec`
     把技术选型排在 Spec 之前，实际退化成 `Prompt → Tech Stack → Spec`，与 `spec.md` 声明的
     "Spec 是 Source of Truth" 冲突。
   - 新顺序：`Requirement → Discovery → **Draft Spec** → 决策材料 → Technology Selection →
     Human Confirmation（仅 CONFIRMATION）→ Final Spec（Accepted）→ plan → design(按需) → tasks`。
   - 落点：`CLAUDE.md` §2/§7、`.sdd/workflows/new-project.md`、`.sdd/templates/spec.md`
     （新增 `Status: Draft → Accepted` 与"不写具体技术实现"约束）、`decision-protocol §1/§9`、
     `AGENTS.md` READ ORDER、`CONVENTIONS.md` §3 新增 Spec Status 枚举。

2. **AUTO/RECOMMEND 不再阻塞**（`mod_gpt.md §2`）
   - 旧文同时写着"只有重大架构决定属 REQUIRE_CONFIRMATION"和"技术栈类决定有长期锁定成本 → 必须 Human Confirmation"，
     于是语言/框架/数据库/Docker 都要问用户，`AUTO` 失去意义。
   - 现明确：`AUTO` 直接执行并记录；`RECOMMEND` **采用推荐方案继续执行**并记录
     alternatives / assumptions / reversibility，**不阻塞**；`BLOCKED` 仅在"缺失信息会导致重大、不可逆或
     高风险决策且无安全可逆默认值"时才停止。反向也禁止：不得把 AUTO/RECOMMEND 升格为"要人确认"以求免责。
   - 删除"技术栈类决定有长期锁定成本 → Human Confirmation"共 6 处：
     `decision-protocol §6/§9`、`CLAUDE.md` §5、`workflows/new-project.md`、`.sdd/README.md`、
     `templates/technology-selection.md`、`templates/plan.md`。

3. **约束优先级分级 P0A / P0B**（`mod_gpt.md §3`）
   - 旧规则"Explicit user requirement = P0 Hard Constraint"+"用户显式要求高于以上全部"过于绝对：
     用户要求 EOL 框架 / SQLite 承担高并发写 / 明文存 token / 禁止备份时，Agent 按旧规则都应照做。
   - 新分级：**P0A**（Safety·Legal·Compliance；Technical feasibility·Platform impossibility）**高于 P0B**
     （显式不可协商的用户约束；现有系统硬兼容）；P0A 不可被用户偏好覆盖，冲突时标 `BLOCKED` 并按模板澄清。
   - 新增**用户表达分级**：说"偏好 / 熟悉 / 倾向 / 最好用" → Preference（P3/P2）；
     只有"必须 / 不得 / 组织标准 / 不可改变"才升级为 Hard Constraint。
   - 落点：`decision-protocol §2/§3.1/§8`、`CLAUDE.md` §5、`AGENTS.md`、
     `decision-trees/backend.md`、`knowledge/backend.md`、`CONVENTIONS.md` §3 枚举。

### 修复（P1 — 结构与工程化）

4. **`design.md` 与 `adr/` 改为按需**（`mod_gpt.md §4`）
   - `plan.md`（16 节）与 `design.md` 覆盖内容高度重叠，且两份都在写"缓存 TTL"这类数值时
     Agent 无法判断 Source of Truth。
   - 现规定：`design.md` **只写 plan 装不下的细节**（复杂领域模型 / 状态机 / 并发 / 异步 /
     多外部集成 / 分布式一致性 / 复杂契约 / 安全敏感流程 / 需显式设计的算法），否则 plan 足够；
     `adr/` 无重要 Architecture Decision 就不建。并给出**文档职责边界表**（who answers what）。
   - 落点：`.sdd/LAYOUT.md` §1.1/§1.2/§2（含 mod_gpt.md 映射行）、`templates/design.md`（重写）、
     `templates/plan.md`、`templates/technology-selection.md`、`templates/adr.md`、
     `workflows/new-project.md`、`CLAUDE.md` §2。

5. **Schema 校验从"名义"变为"真校验"**（`mod_gpt.md §5`）
   - 旧实现只用正则检查"键名在不在"，`backend: 123` / `database: []` / `confidence: foo` 都能通过。
   - 现新增 `specs/<id>/decision.json`（**机器可读 Decision Contract**）+
     `scripts/mini_schema.py`（纯标准库 JSON Schema **子集**校验器，支持 type/enum/required/
     properties/additionalProperties/items/数值与长度边界/oneOf 等）；
     `validate_rules.py` 对它做**真校验**。
   - 保留 Markdown 里的 YAML 块，但**明确降级为 structural validation**（YAML 无标准库解析器，
     无法类型校验）——文档中"机器可校验 Schema"的说法全部改为
     "机器可读 Decision Contract + 真 Schema validation"，不再混称。
   - 子集校验器遇到不认识的 Schema 关键字**报错而非静默跳过**，防止再次退化为名义校验。
   - 反例验证：`mod_gpt.md §5` 给出的坏数据现已能被抓出 6 处违规。

6. **评分标尺（0–5 rubric）与适用门槛**（`mod_gpt.md §6`）
   - 公式有权重但无标尺，两个 Agent 会对同一对候选给出无法复核的分数（"伪精确评分"）。
   - 现给出 0–5 的统一标尺 + **各维度 3/4/5 的判定锚点**，并明确
     **Scoring is a tie-break / comparison tool, not the decision itself**；
     仅在"消除后仍 ≥2 候选且规则无法区分"时才评分，不为用公式而制造候选。
   - 落点：`decision-protocol §3.3/§4.1`、`templates/technology-selection.md`、`AGENTS.md`、`CLAUDE.md` §5。

7. **默认值语义：Default = Candidate Prior**（`mod_gpt.md §7`）
   - 旧句式 `IF … THEN language = Python` / `THEN Vue 3 + TypeScript` 是**断言结论**，
     等于跳过候选淘汰；叠加"几乎任何 Web 后端都满足 CRUD/API"，任何 SaaS 都收敛到
     `Vue + FastAPI + PostgreSQL` —— 正是本仓要避免的"答案库"效果。
   - 现统一改为候选句式：`THEN Python SHOULD be included as a candidate` /
     `THEN Vue 3 + TypeScript SHOULD be considered`，并新增四条统一规则
     （进入候选集 / 无区分度时才可为 AUTO / 让位于现有栈与团队专长 / 不得绕过淘汰）。
   - 落点：`decision-protocol §3.4`、`knowledge/{backend,frontend}.md`、
     `decision-trees/{backend,frontend}.md`、`workflows/new-project.md`、`AGENTS.md` 默认矩阵。

8. **新增 `knowledge/versioning.md`（版本选择策略唯一实现）**（`mod_gpt.md §8`）
   - 此前只有 `Python 3.x` / `Vue 3` / `pinned deps`，回答不了 Agent 最实际的问题
     （3.12 还是 3.13？PG 17 还是 18？Node 哪个 LTS？），且把具体版本号写死必然过期。
   - 新增：原则（生命周期决策，不是流行度决策）/ 存量项目保持版本的 5 个例外 /
     新项目 6 级默认优先级 / 明确避免 alpha·beta·RC·EOL·平台不可用 / **强制核对上游官方文档**
     （未核实写 `UNKNOWN`，禁止编造）/ 锁定规则（lockfile、pin major·minor、镜像禁 `latest`）。
   - backend / frontend / database / deployment 只**引用**它，不各自维护版本策略；
     `decision.json` 新增 `versions` 字段（Schema 同步扩展）。

9. **`AGENTS.md` 新增 DEFINITION OF DONE**（`mod_gpt.md §9`）
   - 明确改本规则库的"完成"标准：先 `gen_traceability.py` 再 `validate_rules.py`，
     必须 0 错误 0 警告 / 无失效文件引用 / 无互相冲突的 canonical rules；
     并给出"改了 A 就要同步 B"的对照表（Layout / Decision semantics / Technology rule /
     User-facing behavior / Rule source mapping / Public rule behavior / 版本策略 / 新增来源）。
   - `CLAUDE.md` §9 指向该节。

### 溯源与工程化

10. **接入第 4 份来源 `mod_gpt.md`**
    - `.sdd/CONVENTIONS.md`：§1 登记 `mod_gpt.md §N` 前缀，并新增 `CONVENTIONS.md` §1.1「各来源的条号从哪来」。
    - `scripts/sdd_refs.py` 增加该来源与**专用条目模型**：它是散文式评审，正文含 3 处
      **从 1 重新开始**的子枚举，故只认严格递增的行首编号（得到 9 条）。
    - `sources/README.md` 补文件清单、引用前缀与"更新源文档时"的步骤（含登记条目识别方式）。

### 已知限制（未解决，勿误读）

- **引用率 ≠ 内容覆盖率**：`TRACEABILITY.md` 全绿只说明"每条源规则都至少被一处声明为来源"。
- **裸 `§N` 检查是"按分句回看标签"实现的**：若同一分句里出现任何白名单标签
  （如文件名 `design.md`），该分句内的裸 `§N` 会被放过（本次已顺手修掉一处实例：
  `specs/001-project/design.md` 的 `§98` → `res.md §98`）。收紧该规则会牵连全仓，留待下次评估。

---

## [v1.2] — 2026-09-19

二审：追踪矩阵本身失准，且 TS 后端线存在选型死胡同。

### 修复（P1 — 追踪矩阵漏报，误导"该规则可安全删除"）

1. **引用解析合并为唯一实现**
   - 新增 `scripts/sdd_refs.py`，`gen_traceability.py` 与 `validate_rules.py` 共用。
     此前两个脚本各自维护一份 `(res\.md|Matrix|知识库) §(\d+)` 正则，只认「来源名 + 紧随其后的单个条号」，
     漏掉三类合法写法：逗号压缩 `Matrix §24,§25,§45`、区间 `res.md §50-§58`、子条目 `知识库 §6.1`。
     库内共 **69 处压缩/区间写法、30+ 处子条目引用**被截断。
   - **后果一（严重）**：`TRACEABILITY.md` 误报「（未引用）」。修复前 res.md 覆盖率 **64%**、知识库 **53%**；
     修复后 **100% / 100% / 100%**。一份把 `Matrix §45` 标成"无人引用"的索引，会让源文档升级时的
     影响面评估直接失效。
   - **后果二**：校验脚本同样漏检压缩写法中的越界条号——**已抓到 1 处**（见下）。

2. **修正越界引用**
   - `.sdd/knowledge/architecture.md`：原先误引了 `Matrix` 的第 65–69 条（该区间实属 `知识库` 的
     微服务/EDA/CQRS/ES/DDD），且下一组 `知识库 §65-§70` 已正确覆盖。`Matrix` 最大条号为 §45。**已删除误并项**。

3. **扫描范围统一**
   - `gen_traceability.py` 原先只扫 `.sdd/` 与 `specs/`，漏掉根目录的 `README.md` / `AGENTS.md` / `CLAUDE.md` / `CHANGELOG.md`；
     而 `validate_rules.py` 是扫全仓的。范围改由 `sdd_refs.targets()` 统一提供。

4. **小数区间支持**
   - `§1.2-§1.4` 原先不展开（`§1.3` 因此被判"未覆盖"）。现支持同主号小数区间；跨主号小数区间语义不唯一，保留不展开。

### 修复（P1 — TS 后端选型死胡同）

5. **`AGENTS.md` 默认技术矩阵漏行**
   - 该表声明来源为 `res.md §110`，却漏掉 `Enterprise Backend`（Spring Boot / NestJS）与
     `TS Backend`（NestJS / Fastify / Hono）两行，以及 Queue / Streaming / Search / Object Storage / Internal RPC / Testing。
     `res.md §110` 原文为 `TS Backend → NestJS（默认）/ Fastify / Hono`。

6. **补齐 TS 后端判定**
   - `.sdd/decision-trees/backend.md` §4：原先只列 Next.js / React+Vite / Vue+Vite 三个**前端**框架，
     而 `decision-trees/backend.md` 的语言判定可以输出 `TypeScript` → **API-only 服务无框架可依**。现拆为两组：
     纯 TS 后端 → NestJS（默认）/ Fastify / Hono；含前端的 fullstack → Next.js。并写明"不要把 Next.js 当纯后端框架"。
   - `.sdd/knowledge/backend.md`：TypeScript 段补框架默认；`knowledge/backend.md` 的 Repository Structure 补 `res.md §78-§82`。

### 改进（引用完整性）

7. **补齐 10 处「内容已有、未标出处」**：`knowledge/architecture.md`（`res.md §4.1`、`知识库 §4.1-§4.2,§12.1`）、
   `knowledge/backend.md`（`知识库 §5.1,§6.1-§6.3,§8.1-§8.3`）、`knowledge/caching.md`（`res.md §38`、`知识库 §30`）、
   `decision-trees/decision-protocol.md`（`Matrix §3.1-§3.2`、`知识库 §64,§74`）、`.sdd/README.md`（`知识库 §2,§2.1,§86`）、
   `AGENTS.md`（`res.md §1.2-§1.4`、`知识库 §87`）、`CLAUDE.md`（`知识库 §87`）。

8. **`LAYOUT.md` 映射表补第 5 套约定的归属**：`知识库 §89` 规定的 `ai-architecture-kb/` 与 `Matrix §45` 是**同一套**，
   原表只归给了 `Matrix §45`。

9. **`CONVENTIONS.md` §1/§5**：登记紧凑写法（逗号压缩 / 区间 / 小数区间）的展开语义与归属规则；
   明确「引用解析只有一处实现」。

### 说明

- **引用率 ≠ 内容覆盖率**。三份源文档 100% 有落点，只证明「每条规则都至少被一处声明为来源」，
  不证明该条已被完整正确落地。`TRACEABILITY.md` 已写明该限制。

---

## [v1.1] — 2026-09-19

### 修复（P0 — 消除自相矛盾，避免 Agent 误判）

1. **目录约定统一**
   - 新增 `.sdd/LAYOUT.md`：声明唯一采纳的约定（`.sdd/` + `specs/<id>-<name>/`），
     并为源文档中另外 3 套约定（`res.md §92`/`§93` 的 `docs/`、`Matrix §45` 的 `ai-architecture-kb/`、`知识库 §78` 的部分产物）给出 **superseded 映射表**。
   - 清除 `.sdd/templates/spec.md` 中残留的 `docs/architecture.md` 等引用。

2. **spec 节数统一**
   - 明确以 `知识库 §79` 的 **14 节**为准（`res.md §117` 为 23 项）。
   - 在 `.sdd/templates/spec.md` 补 `res.md §117（23 项） → 14 节 / plan.md` **全量映射表**，并显式记录取舍理由（spec = WHAT/WHY，plan = HOW）。
   - 修正两处过期引用：`.sdd/workflows/new-feature.md`「不必全量 23 项」、`specs/001-project/verification.md`「spec.md §23」（实为 §10）。

3. **复杂度预算计分口径统一**
   - `.sdd/decision-trees/decision-protocol.md` 新增 **§5.1 计分表**（唯一口径）：明确计入项、不计入项（Docker / 框架 / ORM / gRPC / 部署平台）、以及 **pgvector 作为 PostgreSQL 扩展不额外计分**。
   - 新增 §5.2 预算对照、§5.3 计分示例。
   - 统一此前口径不一致的算式：`.sdd/examples/saas.md`（原计入 Docker）、`high-concurrency.md`（原不计）、`ai-saas.md`（原 pgvector 计 2）；同步 `knowledge/architecture.md`、`decision-trees/architecture.md`、`templates/technology-selection.md`、`specs/001-project/technology-selection.md`、`CLAUDE.md`、`AGENTS.md`。

4. **引用编号统一（消除 `§N` 歧义）**
   - 新增 `.sdd/CONVENTIONS.md`：禁止裸写 `§N`，必须带来源前缀（`res.md` / `Matrix` / `知识库` / `<文件名>`）。
   - 新增 `scripts/migrate_refs.py`，迁移 **124 处**引用（28 个文件）。
   - 语义核查后修正 **3 处来源错配**：`new-project.md` 的 `Matrix §34` 与 `知识库 §59-§62`、`knowledge/ai-llm.md` 的 `Matrix §44 规则 20`（这些编号在 res.md 与其它来源中同时存在，机器无法自动判定）。
   - 统一来源标签写法 `AI Architecture Decision Matrix §N` → `Matrix §N`。
   - 校验结果：全仓裸 `§N` 残留 **0** 处。

### 新增（P1 — 补内容缺口）

- **`knowledge/ai-llm.md`** + **`decision-trees/ai-llm.md`**：AI / LLM / RAG / Agent 决策线。
  此前 `Matrix §29`（AI Application Matrix 10 项必查）、`§30`（LLM Provider Architecture）、`§31`（RAG Matrix）**完全未落地**，仅被 `examples/ai-saas.md` 一句话带过。
- **`knowledge/data.md`**：数据工程决策线（编排调度 / 转换层 / 批 vs 流 / 存储分层 / 特征存储 / 幂等回填 / 数据质量 / 测试策略）。
  此前项目类型已含 "Data Application / ETL"，但无对应知识文件。源文档对该领域覆盖薄，文件中已逐条标注「本仓补充」。
- **`knowledge/caching.md`**：缓存与搜索决策线。此前 `Matrix §23`（Caching Matrix）、`§17`（Search Engine Matrix）未落地，仓库仅 4 行 + 2 行残片。
- **`specs/001-project/plan.md`** 与 **`specs/001-project/adr/`**（`ADR-001-postgres.md`、`ADR-002-fastapi.md`、`ADR-003-session-auth.md`）：
  补齐此前缺失的实例产物（原 ADR 索引指向不存在的文件）。
- **`.sdd/TRACEABILITY.md`**：`res.md` 120 条 → 落点文件的反向索引（脚本生成）。
- **`README.md`**（根）：仓库总览（人 + 非 Claude 的 Agent 入口）。
- **`.gitignore`**、**`CHANGELOG.md`**（本文件）。
- **`sources/v1.0/`**：源文档归档为只读，并声明"Agent 决策时不读取"。

### 新增（P2 — 工程化增强）

- **`.sdd/schema/decision.schema.json`** + **`scripts/validate_rules.py`**：机器可校验（引用完整性 + Decision Schema 必填项 + 复杂度预算）。
- **技术选型评分补 `Cost` 维度**（原 5 维共 100 分 → 6 维共 100 分，适配小预算/个人项目）。
- **`decision-protocol.md` 补 BLOCKED 澄清问题模板**（与 QUESTION POLICY MUST/SHOULD/CAN ASK 对应）。
- **`decision-protocol.md` 补文件间冲突仲裁顺序**。
- **`workflows/small-change.md`**：轻量改动档（跳过全流程的显式阈值）。

### 变更

- `.workbuddy/` 移出版本控制（改为本地个人状态；磁盘文件保留）。
- `.sdd/README.md` 目录树同步更新。

---

## [v1.0] — 2026-09-18

- 由 `res.md`（120 条）生成初版规则库：`CLAUDE.md` / `AGENTS.md` / `.sdd/{knowledge,decision-trees,templates,workflows}` / `specs/001-project/`。
- 按 `Matrix` 与 `知识库` 增强治理能力：新增 `decision-trees/decision-protocol.md`（约束模型 / 评分 / 复杂度预算 / 决策状态 / 确认门槛 / 15 步决策循环 / 30 条规则）；
  扩充 knowledge 至 10 个文件、decision-trees 至 5 个；`spec` 改 14 节、`plan` 改 16 节；新增 `.sdd/examples/` 5 个已决策示例。
