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

---

## 引用写法（见 `.sdd/CONVENTIONS.md` §1）

| 前缀 | 等价于 |
| --- | --- |
| `res.md §N` / `res.md §N.M` | `sources/v1.0/res.md` 第 N 条 / 第 N.M 小节 |
| `Matrix §N` / `Matrix §N.M` | `sources/v1.0/AI Architecture Decision Matrix.md` 第 N 节 |
| `知识库 §N` | `sources/v1.0/AI Coding SDD 项目技术架构与框架选择知识库.md` 第 N 节 |

---

## 重要提示：源文档之间存在冲突

三份源文档给出的**产物目录约定互不兼容**（共 4 套），见 `.sdd/LAYOUT.md` §2 的映射表：

| 来源 | 约定 | 状态 |
| --- | --- | --- |
| `res.md`（L2099-2112） | `docs/specs/<id>/{context,requirements,...}.md` | superseded |
| `res.md`（L2113-2121） | `docs/{architecture,technology-selection,engineering-rules}.md` | superseded |
| `res.md` 结尾建议 | `.sdd/{knowledge,decision-trees,templates,workflows}` + `specs/` | **adopted** |
| `Matrix` §45（L1996-2030） | `ai-architecture-kb/...` | superseded |
| `知识库` §78（L2368-2384） | `specs/<id>/{spec,plan,tasks,research,...}.md` + `adr/` | 部分 adopted |

**Agent 若直接阅读源文档，会得到互相矛盾的落点。** 因此本仓要求：决策只读 `.sdd/`，源文档仅用于溯源。

---

## 更新源文档时

1. 新版本放 `sources/v<major>.<minor>/`（不要原地覆盖旧版本）。
2. 运行 `python3 scripts/validate_rules.py` 检查引用是否失效。
3. 在 `CHANGELOG.md` 记录，并在 `.sdd/TRACEABILITY.md` 更新映射。
