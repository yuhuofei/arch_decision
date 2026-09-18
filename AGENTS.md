# AGENTS.md — 通用工程规则（General Engineering Rules）

> 本文件承载三样东西：**通用工程规则**、**语义路由表**、**DEFINITION OF DONE**。
> **它不定义决策语义** —— 约束优先级、决策状态、复杂度计分、评分公式、确认门槛的唯一权威是
> `.sdd/decision-trees/decision-protocol.md`；**默认选型（候选先验）**的唯一权威是 `.sdd/decision-trees/`。
> 读取顺序见 `CLAUDE.md` §2；归属矩阵见 `.sdd/CANONICAL.md`；引用约定见 `.sdd/CONVENTIONS.md`。
> 来源：`sources/v1.0/res.md`（顶层 121 条 + 子条目 11）+ `Matrix`（45 + 14）+ `知识库`（89 + 14）
> + `mod_gpt.md`（9 条可执行性改进）+ `modv2.md`（22 项复核）。
> **规则归属**：本文件与 `CLAUDE.md` 是 Agent 入口，**只引用、不重新定义**行为语义（`.sdd/CANONICAL.md`）。

## 1. CORE MISSION（`res.md §0`）

理解需求 → 识别类型/规模 → 架构决策 → 可解释技术选型 → Spec → Design → Plan → Tasks → 实现 → 验证 → 收敛。
保持代码 / 架构 / Spec 一致。

## 2. 工程原则（`知识库 §85` / `res.md §1.2-§1.4` 节选）

> **原则层**。本层只写"怎么想"。**具体默认值**（各语言 / 框架 / 数据库 / 中间体的默认与替代）
> 不在本文件复制 —— 见 `.sdd/decision-trees/` 各领域文件的 Default / Alternatives。

1. 不因技术流行而选技术。
2. 不为未来假设需求增加复杂度。
3. 存量项目优先保持已有技术栈。
4. 技术选型必须记录理由。
5. 架构决策追溯到 Requirement；Requirement 追溯到 Test；Code 追溯到 Spec。
6. **Spec 先于技术选型**：先 WHAT/WHY，再 HOW；不写技术实现的 Draft Spec 是正常产物，不是未完成品。

## 3. 通用工程约束

1. **存量项目**：先分析现有仓库 / 架构 / 依赖 / 数据库 / API / 测试 / CI-CD / 部署，
   **不要立即写代码**（`res.md §102`）；流程见 `.sdd/decision-trees/impact-analysis.md`。
2. **授权边界**：未经用户明确授权，不得擅自更换已有技术栈（`知识库 §71`）或升级版本
   （`.sdd/knowledge/versioning.md`）。必须迁移的例外情形及其优先级判定见 `decision-protocol.md` §2。
3. **记录理由**：架构决策的"为什么"写入 `specs/<id>/decision.json` 的 `evidence` 字段；
   该决策重要且需长期保留时才建 ADR（`.sdd/LAYOUT.md` §1.1）。
4. **追溯链**：`Requirement → Decision → Task → Code → Test` 必须可追；反向索引由
   `scripts/gen_traceability.py` 生成，**勿手改** `.sdd/TRACEABILITY.md`。
5. **不静默决定**：需要人工确认的决策清单见 `decision-protocol.md` §6.4 —— 本文件不复制该清单。

## 4. 语义路由表（**唯一一份**；`CLAUDE.md` §5 指向这里）

| 要判断的事 | 权威 |
| --- | --- |
| 约束优先级（P0A / P0B / P1–P3）的含义与覆盖关系 | `.sdd/decision-trees/decision-protocol.md` §2 |
| 硬约束 / 软约束 / 用户表达分级 | `decision-protocol.md` §3.1 / §3.2 |
| 默认值语义（`DEFAULT does not mean SELECTED`） | `decision-protocol.md` §3.4 |
| 评分公式、0–5 标尺、何时才评分 | `decision-protocol.md` §4 / §4.1 |
| 成本复核 | `decision-protocol.md` §4.2 |
| 复杂度计分口径与预算档 | `decision-protocol.md` §5 / §5.1 / §5.2 |
| 决策状态（`AUTO` / `RECOMMEND` / `REQUIRE_CONFIRMATION` / `BLOCKED`）的含义 | `decision-protocol.md` §6 |
| `RECOMMEND` 与 `REQUIRE_CONFIRMATION` 的边界 | `decision-protocol.md` §6.1 |
| `BLOCKED` 的使用条件与澄清模板 | `decision-protocol.md` §6.2 |
| Assumptions / 假设记录在哪里 | `decision-protocol.md` §6.3 |
| 哪些决策默认必须人工确认 | `decision-protocol.md` §6.4 |
| 决策循环步序 | `decision-protocol.md` §7 |
| 规则冲突时谁优先 | `decision-protocol.md` §10 |
| 流程顺序（Step 0–8）与"每一步读什么" | `CLAUDE.md` §2 / `.sdd/workflows/new-project.md` |
| 产物必填性与目录 | `.sdd/LAYOUT.md` §1.1 |
| 版本策略 | `.sdd/knowledge/versioning.md` |
| 候选选择与默认选型 | `.sdd/decision-trees/` 对应领域文件 |
| 技术知识 | `.sdd/knowledge/` 对应文件 |

> **硬规则**：本表是**路由**，不是摘要 —— 表中只允许出现"主题名 + 权威位置"。
> 任一行的语义（枚举 / 公式 / 数值 / 清单）**不得**抄进本文件或 `CLAUDE.md`（`.sdd/CANONICAL.md` 硬规则 1 / 2）。

## 5. DEFINITION OF DONE（修改本规则库时）

> 来源：`mod_gpt.md §9`。本仓是**规则库**，改动它的"完成"标准与写业务代码不同。

1. 运行：

   ```bash
   python3 scripts/gen_traceability.py      # 先重建索引（改了引用就必须重跑）
   python3 scripts/validate_rules.py        # 再自检
   ```

2. 必须达到：
   - **0 errors，0 warnings**
   - **无失效文件引用**（反引号内 `.md` / `specs/*/decision.json` 指向真实文件）
   - **无互相冲突的 canonical rules**（同一件事只能有一个权威文件，见 `.sdd/CANONICAL.md`）
   - **Canonical 不变量全部通过**（归属矩阵与登记表一致 / 流程顺序 / 决策状态旧语义未回流 / 必填产物有模板）
   - **版本号三处一致**（`.sdd/VERSION` ≡ `README.md` ≡ `CHANGELOG.md` 最新版本）
   - `.sdd/TRACEABILITY.md` 与当前引用一致（否则就是过期索引，比缺失更有害）
3. 若修改了以下内容，**必须同步**：

   | 改了什么 | 必须同步 |
   | --- | --- |
   | Layout / 目录结构 | `.sdd/LAYOUT.md` |
   | **决策语义**（状态 / 优先级 / 评分 / 预算 / 确认门槛） | `.sdd/decision-trees/decision-protocol.md`（**不得**写入入口文件） |
   | **默认选型 / 候选判断**（某技术的默认与替代） | `.sdd/decision-trees/` 对应领域文件（**不得**在入口文件另立矩阵） |
   | Technology rule（某技术支持什么、怎么用） | `.sdd/knowledge/` 对应文件 |
   | **读取路由**（读什么、什么顺序） | `CLAUDE.md` |
   | **工程规则 / DoD** | `AGENTS.md` |
   | Rule source mapping（引用来源条号） | 重跑 `scripts/gen_traceability.py` 更新 `.sdd/TRACEABILITY.md` |
   | Public rule behavior（对外可见的规则变更） | `CHANGELOG.md` |
   | 版本策略 | `.sdd/knowledge/versioning.md`（**不要**在领域文件里另写一份） |
   | **规则库版本号** | `.sdd/VERSION`（唯一来源）→ 同步 `README.md` / `.sdd/README.md` / `CHANGELOG.md` |
   | **Canonical 归属**（哪份文件说了算） | `.sdd/CANONICAL.md` + `scripts/validate_rules.py` 的 `CANONICAL_TOPICS` |
   | Verification 结构 | `.sdd/templates/verification.md` + `.sdd/schema/verification.schema.json` |
   | 新增知识域 / 决策树 | `.sdd/README.md` 与 `.sdd/LAYOUT.md` 的目录清单（含数量） |
   | 新增引用来源 | 先在 `.sdd/CONVENTIONS.md` §1 登记前缀，再使用 |

4. **新增一条"行为语义"时**：先在 `.sdd/CANONICAL.md` §1 登记它的唯一权威，再在权威文件里写；
   入口文件（`CLAUDE.md` / `AGENTS.md`）**只允许加指针**。同一语义的第二份定义视为 bug。
5. 校验器不认识某条 Schema 关键字时会**报错而非静默跳过**（`scripts/mini_schema.py`）；
   遇到该报错应扩展 `SUPPORTED_KEYWORDS`，不要删检查。

## 6. FINAL PRINCIPLE（`res.md §120`）

技术 / 架构 / Framework / SDD 都不是目的。目标：
Correctness + Maintainability + Simplicity + Testability + Observability + Security + Evolvability。
无明确需求选最简单成熟方案；复杂需求记录必要性。不要为架构而架构。
