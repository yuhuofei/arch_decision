# LAYOUT.md — 产物目录约定（Canonical Layout）

> **本文件是目录约定的唯一权威。** 当 `res.md` / `Matrix` / `知识库` 给出不同目录结构时，**一律以本文件为准**。
> 解决对象：源文档共给出 **4 套互不兼容**的约定，此前仓库只落地其中一套却未声明取舍。
> 相关：`.sdd/CONVENTIONS.md`（引用与命名约定）、`.sdd/README.md`（规则库总览）。
> v1.3 变更：`specs/` 的 `design.md` 与 `adr/` 由「必填」改为**按需**，新增 `decision.json`（`mod_gpt.md §4`）。
> v1.4 变更：新增 `.sdd/VERSION` / `.sdd/CANONICAL.md` / `.sdd/traceability.json` 与
> `verification.schema.json`；`verification.md` 明确为必填（`modv2.md §3-§4`）。

---

## 1. 采纳的约定（唯一）

### 1.1 目录树

```
<repo>/
├── README.md                     # 仓库总览（人 + 非 Claude 的 Agent 入口）
├── CLAUDE.md                     # Agent 行为规则 + 读取顺序（"什么时候读什么"）
├── AGENTS.md                     # 通用工程规则 + 读取顺序 + DEFINITION OF DONE
├── CHANGELOG.md                  # 规则库版本变更
│
├── sources/                      # 【只读】源文档归档，Agent 决策时【不读取】
│   ├── README.md
│   └── v1.0/
│       ├── res.md
│       ├── AI Architecture Decision Matrix.md
│       ├── AI Coding SDD 项目技术架构与框架选择知识库.md
│       ├── mod_gpt.md            # v1.3 可执行性评审（9 项改进）
│       └── modv2.md              # v1.4 复核评审（22 项；四态追溯 / 归属矩阵）
│
├── .sdd/                         # 规则库（跨项目复用、随版本演进）
│   ├── VERSION                   # 规则库版本号**唯一来源**（README/CHANGELOG 引用它）
│   ├── LAYOUT.md                 # 本文件：目录约定
│   ├── CONVENTIONS.md            # 引用编号与命名约定
│   ├── CANONICAL.md              # 规则归属矩阵：同一语义只有一个权威定义
│   ├── TRACEABILITY.md           # 5 份来源 → 落点文件反向索引（四态；脚本生成，勿手改）
│   ├── traceability.json         # 同上，机器可读版（脚本生成）
│   ├── README.md
│   ├── knowledge/                # 参考知识（"选什么、何时选"）
│   ├── decision-trees/           # 判断逻辑（"什么情况选什么"）
│   ├── templates/                # 文档骨架
│   ├── workflows/                # 执行流程
│   ├── examples/                 # 已决策示例
│   └── schema/                   # 机器可读契约（JSON Schema）
│
└── specs/                        # 项目实例（每个项目 / 大型特性一个目录）
    └── <id>-<name>/
        ├── project-discovery.md      # 必填
        ├── technology-selection.md   # 必填（人读）
        ├── decision.json             # 必填（机器可读 Decision Contract，真 Schema 校验）
        ├── spec.md                   # 必填（14 节，WHAT/WHY；Status: Draft → Accepted）
        ├── plan.md                   # 必填（16 节，HOW/架构/技术栈）
        ├── design.md                 # 按需：只有 plan 装不下的细节才写（判据见 §1.2）
        ├── tasks.md                  # 必填
        ├── verification.md           # 必填
        └── adr/                      # 按需：存在重要 Architecture Decision 时创建
            └── ADR-001-<topic>.md
```

**其他按需产物**（大型特性才建，Spec Kit 风格）：`research.md` / `data-model.md` / `api-contract.md` / `architecture.md`。
`verification.json` 为**可选**的机器可读版验证报告（契约见 `.sdd/schema/verification.schema.json`）；
存在时必须与 `verification.md` 的 Status / Verdict / AC 集合一致（自检脚本会核对）。

### 1.2 design.md 与 adr/ 的创建判据

**design.md 只写"对 plan.md 来说太细"的内容**。它**不是第二份 plan**：任何在 `plan.md` 已写的架构、
技术栈、模块划分、缓存 TTL 之类内容，**不得**在 `design.md` 重述 —— 两份都写同一件事时，
Agent 无法判断哪份是 Source of Truth（例如 `plan.md: TTL=10min` 与 `design.md: TTL=30min`）。

`design.md` SHOULD be created when one or more apply（`mod_gpt.md §4`）：

```
- complex domain model                （复杂领域模型）
- non-trivial state machine           （状态机）
- concurrency                         （并发）
- async workflow                      （异步流程）
- multiple external integrations      （多外部集成）
- distributed consistency             （分布式一致性）
- complex API contract                （复杂接口契约）
- security-sensitive flow             （安全敏感流程）
- algorithm requires explicit design  （算法需要显式设计）
```

否则 **`plan.md` 足够，不创建 `design.md`**。

`adr/` 同理：**没有重要的 Architecture Decision 就不建** —— 不要为了满足目录规范制造 ADR。
`ADR` 只需记录进入 `decision.json` 的那几条决策（含 `REQUIRE_CONFIRMATION` 项）；
**CAN ASSUME / RECOMMEND 的假设不要求 ADR**（写入 `technology-selection.md` + `decision.json` 即可，`decision-protocol` §6.3）。

`verification.md` 是**必填**产物（与上两者不同）：它是"实现确实满足 Accepted Spec"的唯一证据，
结构见 `.sdd/templates/verification.md`（8 节）。缺它即视为未验证。

**文档职责边界（唯一权威划分）**：

| 文件 | 回答 |
| --- | --- |
| `spec.md` | **WHAT / WHY**（含 NFR / Acceptance Criteria） |
| `technology-selection.md` + `decision.json` | **WHICH technology / WHY**（含 alternatives / decision status / 复杂度预算） |
| `plan.md` | **HOW at architecture level** |
| `design.md`（按需） | **只有 plan 装不下的细节** |
| `tasks.md` | **可执行工作** |

---

## 2. 未采纳的约定与映射表

| 来源 | 原约定 | 状态 | 映射到本仓 |
| --- | --- | --- | --- |
| `res.md`（L2099-2112） | `docs/specs/001-feature-name/{context, requirements, technology-selection, design, decisions, tasks, verification}.md` | **superseded** | `context.md`→`project-discovery.md` + `spec.md` §2<br>`requirements.md`→`spec.md` §3-§5、§10<br>`decisions.md`→`adr/ADR-NNN-*.md`<br>`technology-selection.md`/`design.md`/`tasks.md`/`verification.md` 同名保留，路径改为 `specs/<id>/` |
| `res.md`（L2113-2121） | 项目级 `docs/{architecture.md, technology-selection.md, engineering-rules.md}` + `docs/specs/` | **superseded** | 规则层 `engineering-rules.md`→`CLAUDE.md` + `AGENTS.md` + `.sdd/`<br>项目层 `architecture.md`/`technology-selection.md`→`specs/<id>/plan.md`/`technology-selection.md`<br>顶层目录 `docs/` → 统一为 `specs/` |
| `res.md` 结尾建议 | `.sdd/{knowledge, decision-trees, templates, workflows}` + `specs/001-project/` | **✅ adopted** | 即本仓约定（本文件 §1） |
| `Matrix` §45（L1996-2030）<br>`知识库` §89（L2680 起，**同一套** `ai-architecture-kb/`） | `ai-architecture-kb/{README, principles, decision-matrix, decision-tree, scoring}.md` + `{languages, backend, frontend, database, infrastructure, architecture, security, testing, observability}/` + `templates/` + `examples/` | **superseded** | `principles.md`+`decision-matrix.md`+`scoring.md`→`.sdd/decision-trees/decision-protocol.md`<br>`decision-tree.md`→`.sdd/decision-trees/*.md`<br>`languages/`→`.sdd/knowledge/backend.md`<br>其余领域目录→`.sdd/knowledge/*.md`<br>`templates/`/`examples/`→`.sdd/templates/`/`.sdd/examples/` |
| `知识库` §78（L2368-2384） | `specs/001-order-management/{spec, plan, tasks, research, data-model, api-contract, architecture}.md` + `adr/ADR-00x-*.md` | **部分 adopted** | `spec.md`/`plan.md`/`tasks.md`/`adr/` = 采纳 ✅<br>`research.md`/`data-model.md`/`api-contract.md`/`architecture.md` = 降为**按需产物**（见 §1.1） |
| `mod_gpt.md` §4 | `design.md` 与 `adr/` 在示例目录中被标为「必填」 | **已修正** | 改为**按需**，判据见 §1.2 |
| `modv2.md` §3 | 称 `LAYOUT.md` 又把 `design.md` / `adr/` 标回「必填」 | **核实为旧快照误判** | 本文件 §1.1/§1.2 自 v1.3 起即为**按需**；`modv2.md` 复核时读到的版本早于 v1.3 提交 |
| `modv2.md` §4 | 缺少 `templates/verification.md` | **已补齐** | 新增 `.sdd/templates/verification.md`（8 节）+ `.sdd/schema/verification.schema.json` |

> **明确决策**：不再新建 `docs/` 或 `ai-architecture-kb/`。若同时在仓内存在两套结构，Agent 会读到互相矛盾的落点。

---

## 3. 分工边界（避免 `docs/` 与 `specs/` 语义重叠）

| 位置 | 角色 | 是否参与 Agent 决策 |
| --- | --- | --- |
| `sources/` | 原始来源归档，只读 | ❌ 不读取 |
| `.sdd/` | 规则库：跨项目复用，随知识演进版本化 | ✅ 读取 |
| `specs/<id>/` | 项目实例：单个项目/特性的产物 | ✅ 读写 |
| `docs/`（若项目自身需要） | 面向人的说明（onboarding、运维手册、FAQ） | ❌ 不承载 SDD 产物 |

**禁止**：把 `spec.md` / `plan.md` / ADR 放进 `docs/`。

**同一件事只能有一个权威文件**（"canonical rule" 唯一性）：完整对照表见 **`.sdd/CANONICAL.md`**
（规则归属矩阵，含机器校验项）。总原则：目录归属看本文件，引用写法看 `.sdd/CONVENTIONS.md`，
决策语义看 `.sdd/decision-trees/decision-protocol.md`，流程顺序看 `.sdd/workflows/*.md`，
版本策略看 `.sdd/knowledge/versioning.md`，版本号看 `.sdd/VERSION`。
其余文件遇到这些主题**只能引用，不能另立一份**；`CLAUDE.md` / `AGENTS.md` 作为 Agent 入口，
**只引用、不重新定义规则**（出现冲突时以权威文件为准，摘要视为 bug）。

---

## 4. 变更规则

1. 修改目录约定 → **先改本文件**，再改受影响模板与 `CLAUDE.md` / `AGENTS.md`。
2. 新增规则领域 → 在 `.sdd/knowledge/` 与 `.sdd/decision-trees/` 落点，并重跑 `scripts/gen_traceability.py` 登记来源编号。
3. 本文件本身不承载技术知识，只承载"东西放哪里"；"哪份文件说了算"见 `.sdd/CANONICAL.md`。
4. 改完按 `AGENTS.md` 的 DEFINITION OF DONE 收尾（重跑索引 + 自检 0 错误 0 警告）。
