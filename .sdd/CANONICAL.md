# CANONICAL.md — 规则归属矩阵（Canonical Rule Ownership）

> **本文件规定"同一个语义，在仓库里只能有一个权威定义"。**
> 来源：`modv2.md §22`（Canonical Rule Ownership Matrix）。
> 动机：v1.3 的教训是——同一语义被复制到 `CLAUDE.md` / `AGENTS.md` / `workflows/` / `templates/`
> 后，只改其中一处就产生 **rule drift**（上层已是新语义，底层仍是旧语义）。
> 相关：`.sdd/LAYOUT.md`（东西放哪里）、`.sdd/CONVENTIONS.md`（怎么引用）。

---

## 1. 归属矩阵

| 主题 | 唯一权威 | 允许的引用者 | 机器校验 |
| --- | --- | --- | --- |
| Workflow order（流程顺序） | `.sdd/workflows/new-project.md` | 全部（**入口文件只路由，不抄步序**） | `check_workflow_order` |
| Decision semantics（约束优先级 / 决策状态 / BLOCKED 条件 / 评分 / 复杂度预算 / 确认门槛） | `.sdd/decision-trees/decision-protocol.md` | 全部（**只引用，不重述行为语义**） | `check_forbidden_semantics`（防旧语义回流） |
| Default matrix（全栈默认选型 / 候选先验） | `.sdd/decision-trees/` 各领域文件 | 入口文件只路由 | — |
| Complexity budget（复杂度计分口径） | `.sdd/decision-trees/decision-protocol.md` §5.1 | 模板与知识文件只引用口径 | — |
| Artifact required/optional（产物必填性） | `.sdd/LAYOUT.md` §1.1 | `CLAUDE.md`、`workflows/*`、`templates/*` | `check_artifact_requiredness` |
| Directory（目录约定） | `.sdd/LAYOUT.md` | 全部 | — |
| Reference syntax（引用写法） | `.sdd/CONVENTIONS.md` §1 | 全部 | `check_bare_refs` / `check_source_refs` |
| Technology knowledge（技术知识） | `.sdd/knowledge/*.md` | `decision-trees/*`、`templates/*` | — |
| Candidate selection（候选判断） | `.sdd/decision-trees/*.md` | `knowledge/*` | — |
| Version strategy（版本策略） | `.sdd/knowledge/versioning.md` | `backend/frontend/database/deployment` **只引用** | — |
| Release version（规则库版本号） | `.sdd/VERSION` | `README.md`、`.sdd/README.md`、`CHANGELOG.md` | `check_version_consistency` |
| Machine contract（机器可读契约） | `.sdd/schema/decision.schema.json` | `decision.json`、`verification.md` | `check_decision_json` / `check_verification_json` |
| Machine instance（机器实例） | `specs/<id>/decision.json` | `technology-selection.md`（人读镜像，**不得与之矛盾**） | `check_decision_contract` |
| Human-readable decision | `.sdd/templates/technology-selection.md` | — | — |
| Spec structure（spec 节数） | `.sdd/templates/spec.md` | `workflows/*` | — |
| Verification（验证报告结构） | `.sdd/templates/verification.md` | `workflows/*` | `check_verification_artifact` |
| Traceability（反向索引） | `.sdd/TRACEABILITY.md`（**脚本生成，勿手改**） | 全部 | `check_traceability_fresh` |
| **Agent entry — 读取路由**（读什么、什么顺序） | `CLAUDE.md` | `AGENTS.md` 指向它 | —（见 §4） |
| **Agent entry — 工程规则 + DoD**（通用规范、"改完"标准） | `AGENTS.md` | `CLAUDE.md` 指向它 | —（见 §4） |
| **Semantic routing**（"要判断 X 去读 Y"的路由表） | `AGENTS.md` §4（**只有一份**） | `CLAUDE.md` §5 指向它 | —（见 §4） |

---

## 2. 三条硬规则

1. **Agent 入口只路由，不重新定义。**
   `CLAUDE.md` 承载**读取路由**，`AGENTS.md` 承载**通用工程规则 + DoD**。
   凡是"行为语义"——决策状态的含义、约束优先级、复杂度计分、评分公式、确认门槛、默认选型——
   都必须**指向权威文件**，不得成为第二份定义。
   判据（可操作）：**只要入口文件里出现"枚举 / 公式 / 数值 / 清单"形态的语义内容，即为 bug**。
   摘要与权威冲突时，**以权威为准**，且摘要视为 bug。

2. **同一个数只能写在一处。**
   复杂度计分表、决策状态枚举、spec 节数、版本号、流程步序、默认选型表，只允许有一个字面定义。
   其他位置引用它，不得复制数值 —— **包括"看起来很自然地复述一遍"**。

3. **机器优先。**
   能机器校验的（本表"机器校验"列非空）由 `scripts/validate_rules.py` 检查；
   剩下的靠本文件 + code review。**新增重复定义时，先在这里登记权威，再决定是否需要新检查项。**

---

## 3. 与"引用率 ≠ 内容覆盖率"的关系

本矩阵管的是 **"定义不要复制"**；`.sdd/TRACEABILITY.md` 管的是 **"源规则有没有落点"**；
`modv2.md §14` 提出的 `SOURCE → MAPPED → IMPLEMENTED → VERIFIED` 四态进一步区分
"被引用"与"被实现"与"被机器验证"。三者互补，都不能单独证明规则库正确。

> **注意**：本文件自身不承载规则内容，只承载"哪份文件说了算"。修改归属须同步
> `scripts/validate_rules.py` 里的 `CANONICAL_TOPICS` 登记表（`check_canonical_registry` 会检查两边一致）。

---

## 4. 尚未实现的机器校验（诚实登记）

硬规则 1（入口文件不得重新定义语义）目前**没有**机器检查。以下检查项**被计划但未实现**，
**不得**在别处（含本表旧版）宣称存在：

| 计划中的检查 | 应检查什么 | 现状 |
| --- | --- | --- |
| `check_decision_status_semantics` | 入口文件是否复述了决策状态 / 优先级语义 | **未实现** |
| `check_agent_entry_no_redefine` | 入口文件是否出现枚举 / 公式 / 数值 / 清单 | **未实现** |

当前**唯一**的机器防线是 `check_forbidden_semantics`（禁止短语表），它只能挡住**旧版原句回流**，
**挡不住"用新措辞再写一遍"**。因此硬规则 1 现阶段**依赖 code review**。

> 为什么先不实现：先把入口文件瘦身到位（v1.5），再决定这些检查的判据——
> 否则会在"还没想清楚什么叫重复"的时候先固化一个容易误报的检查。见 `CHANGELOG.md` `[v1.5]`。
