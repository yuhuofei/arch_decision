# sources — 源文档归档（只读）

> **Agent 在做技术决策时【不读取】本目录。** 本目录仅用于溯源、审计与影响面评估。
> 规则库的正式内容在 `.sdd/`；本目录是它的"原料"。

---

## 文件清单

| 版本 | 文件 | 内容 |
| --- | --- | --- |
| v1.0 | `v1.0/res.md` | AGENT PROJECT ENGINEERING & SPEC-DRIVEN DEVELOPMENT RULES（120 条工程与 SDD 规则） |
| v1.0 | `v1.0/AI Architecture Decision Matrix.md` | 约束模型 / 正式决策矩阵 / 复杂度预算 / 技术评分 / Decision Output Schema / 决策状态 / 15 步决策循环 / 30 条规则 |
| v1.0 | `v1.0/AI Coding SDD 项目技术架构与框架选择知识库.md` | 中文知识库 / 默认技术栈（9 场景）/ spec·plan 模板 / 与 Spec Kit 衔接 / 最重要 15 条规则 |
| v1.0 | `v1.0/mod_gpt.md` | **v1.3 可执行性评审**（9 项：Spec 前置 / 确认收窄 / 约束分级 / design 按需 / 真 Schema 校验 / 评分标尺 / 默认值语义 / 版本策略 / Definition of Done）。性质是"对本仓的评审意见"，不是原始技术规范。 |

---

## 引用写法（见 `.sdd/CONVENTIONS.md` §1）

| 前缀 | 等价于 |
| --- | --- |
| `res.md §N` / `res.md §N.M` | `sources/v1.0/res.md` 第 N 条 / 第 N.M 小节 |
| `Matrix §N` / `Matrix §N.M` | `sources/v1.0/AI Architecture Decision Matrix.md` 第 N 节 |
| `知识库 §N` | `sources/v1.0/AI Coding SDD 项目技术架构与框架选择知识库.md` 第 N 节 |
| `mod_gpt.md §N` | `sources/v1.0/mod_gpt.md` 第 N 条建议（N = 1–9） |

> `mod_gpt.md` 的条目识别方式与前三份不同：它是散文，正文里嵌着 3 处**从 1 重新开始**的子枚举，
> 故只认**严格递增**的行首编号（详见 `.sdd/CONVENTIONS.md` §1.1）。

---

## 重要提示：源文档之间存在冲突

源文档给出的**产物目录约定互不兼容**（共 4 套），见 `.sdd/LAYOUT.md` §2 的映射表：

| 来源 | 约定 | 状态 |
| --- | --- | --- |
| `res.md`（L2099-2112） | `docs/specs/<id>/{context,requirements,...}.md` | superseded |
| `res.md`（L2113-2121） | `docs/{architecture,technology-selection,engineering-rules}.md` | superseded |
| `res.md` 结尾建议 | `.sdd/{knowledge,decision-trees,templates,workflows}` + `specs/` | **adopted** |
| `Matrix` §45（L1996-2030）<br>`知识库` §89（同一套） | `ai-architecture-kb/...` | superseded |
| `知识库` §78（L2368-2384） | `specs/<id>/{spec,plan,tasks,research,...}.md` + `adr/` | 部分 adopted |
| `mod_gpt.md` §4 | `design.md` / `adr/` 曾被视为必填 | 已改为**按需**（`LAYOUT.md` §1.2） |

**Agent 若直接阅读源文档，会得到互相矛盾的落点。** 因此本仓要求：决策只读 `.sdd/`，源文档仅用于溯源。

---

## 更新源文档时

1. 新版本放 `sources/v<major>.<minor>/`（不要原地覆盖旧版本）。
2. 若新增来源，先在 `.sdd/CONVENTIONS.md` §1 登记前缀，再在 `scripts/sdd_refs.py` 的 `SOURCES` 登记路径与**条目识别方式**。
3. 运行 `python3 scripts/gen_traceability.py`（重建索引）→ `python3 scripts/validate_rules.py`（自检 0 错误 0 警告）。
4. 在 `CHANGELOG.md` 记录，并在 `.sdd/TRACEABILITY.md` 更新映射。
5. 收尾标准见 `AGENTS.md` 的 **DEFINITION OF DONE**。
