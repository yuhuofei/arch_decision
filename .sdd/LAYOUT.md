# LAYOUT.md — 产物目录约定（Canonical Layout）

> **本文件是目录约定的唯一权威。** 当 `res.md` / `Matrix` / `知识库` 给出不同目录结构时，**一律以本文件为准**。
> 解决对象：源文档共给出 **4 套互不兼容**的约定，此前仓库只落地其中一套却未声明取舍。
> 相关：`.sdd/CONVENTIONS.md`（引用与命名约定）、`.sdd/README.md`（规则库总览）。

---

## 1. 采纳的约定（唯一）

```
<repo>/
├── README.md                     # 仓库总览（人 + 非 Claude 的 Agent 入口）
├── CLAUDE.md                     # Agent 行为规则 + 读取顺序（"什么时候读什么"）
├── AGENTS.md                     # 通用工程规则 + 读取顺序（Codex/Cursor 读此文件）
├── CHANGELOG.md                  # 规则库版本变更
│
├── sources/                      # 【只读】源文档归档，Agent 决策时【不读取】
│   ├── README.md
│   └── v1.0/
│       ├── res.md
│       ├── AI Architecture Decision Matrix.md
│       └── AI Coding SDD 项目技术架构与框架选择知识库.md
│
├── .sdd/                         # 规则库（跨项目复用、随版本演进）
│   ├── LAYOUT.md                 # 本文件：目录约定
│   ├── CONVENTIONS.md            # 引用编号与命名约定
│   ├── TRACEABILITY.md           # res.md 120 条 → 落点文件反向索引
│   ├── README.md
│   ├── knowledge/                # 参考知识（"选什么、何时选"）
│   ├── decision-trees/           # 判断逻辑（"什么情况选什么"）
│   ├── templates/                # 文档骨架
│   ├── workflows/                # 执行流程
│   ├── examples/                 # 已决策示例
│   └── schema/                   # 机器可校验的 JSON Schema
│
└── specs/                        # 项目实例（每个项目 / 大型特性一个目录）
    └── <id>-<name>/
        ├── project-discovery.md      # 必填
        ├── technology-selection.md   # 必填
        ├── spec.md                   # 必填（14 节，WHAT/WHY）
        ├── plan.md                   # 必填（16 节，HOW/技术栈）
        ├── design.md                 # 必填
        ├── tasks.md                  # 必填
        ├── verification.md           # 必填
        └── adr/                      # 必填（至少 1 个 ADR）
            └── ADR-001-<topic>.md
```

**按需产物**（大型特性才建，Spec Kit 风格）：`research.md` / `data-model.md` / `api-contract.md` / `architecture.md`。

---

## 2. 未采纳的约定与映射表

| 来源 | 原约定 | 状态 | 映射到本仓 |
| --- | --- | --- | --- |
| `res.md`（L2099-2112） | `docs/specs/001-feature-name/{context, requirements, technology-selection, design, decisions, tasks, verification}.md` | **superseded** | `context.md`→`project-discovery.md` + `spec.md` §2<br>`requirements.md`→`spec.md` §3-§5、§10<br>`decisions.md`→`adr/ADR-NNN-*.md`<br>`technology-selection.md`/`design.md`/`tasks.md`/`verification.md` 同名保留，路径改为 `specs/<id>/` |
| `res.md`（L2113-2121） | 项目级 `docs/{architecture.md, technology-selection.md, engineering-rules.md}` + `docs/specs/` | **superseded** | 规则层 `engineering-rules.md`→`CLAUDE.md` + `AGENTS.md` + `.sdd/`<br>项目层 `architecture.md`/`technology-selection.md`→`specs/<id>/plan.md`/`technology-selection.md`<br>顶层目录 `docs/` → 统一为 `specs/` |
| `res.md` 结尾建议 | `.sdd/{knowledge, decision-trees, templates, workflows}` + `specs/001-project/` | **✅ adopted** | 即本仓约定（本文件 §1） |
| `Matrix` §45（L1996-2030）<br>`知识库` §89（L2680 起，**同一套** `ai-architecture-kb/`） | `ai-architecture-kb/{README, principles, decision-matrix, decision-tree, scoring}.md` + `{languages, backend, frontend, database, infrastructure, architecture, security, testing, observability}/` + `templates/` + `examples/` | **superseded** | `principles.md`+`decision-matrix.md`+`scoring.md`→`.sdd/decision-trees/decision-protocol.md`<br>`decision-tree.md`→`.sdd/decision-trees/*.md`<br>`languages/`→`.sdd/knowledge/backend.md`<br>其余领域目录→`.sdd/knowledge/*.md`<br>`templates/`/`examples/`→`.sdd/templates/`/`.sdd/examples/` |
| `知识库` §78（L2368-2384） | `specs/001-order-management/{spec, plan, tasks, research, data-model, api-contract, architecture}.md` + `adr/ADR-00x-*.md` | **部分 adopted** | `spec.md`/`plan.md`/`tasks.md`/`adr/` = 采纳 ✅<br>`research.md`/`data-model.md`/`api-contract.md`/`architecture.md` = 降为**按需产物**（见 §1） |

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

---

## 4. 变更规则

1. 修改目录约定 → **先改本文件**，再改受影响模板与 `CLAUDE.md` / `AGENTS.md`。
2. 新增规则领域 → 在 `.sdd/knowledge/` 与 `.sdd/decision-trees/` 落点，并在 `.sdd/TRACEABILITY.md` 登记来源编号。
3. 本文件本身不承载技术知识，只承载"东西放哪里"。
