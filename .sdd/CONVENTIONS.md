# CONVENTIONS.md — 引用与命名约定

> 本文件与 `.sdd/LAYOUT.md` 配套：LAYOUT 管"东西放哪里"，本文件管"怎么引用、怎么命名"。
> 目的：**消除 `§N` 歧义**。此前全仓混用两套编号体系，且同一数字在两套体系中含义不同
> （例：`res.md` §67 = Transaction；`spec.md` §10 = Acceptance Criteria）。

---

## 1. 引用编号约定（强制）

**禁止裸写 `§N`。** 每个 `§` 必须带来源前缀：

| 引用对象 | 正确写法 | 示例 |
| --- | --- | --- |
| 源规则 `res.md` | `res.md §N` / `res.md §N.M` | `res.md §67`（Transaction）、`res.md §2.1`（Business） |
| `AI Architecture Decision Matrix.md` | `Matrix §N` / `Matrix §N.M` | `Matrix §32`（复杂度预算）、`Matrix §6.1`（Python） |
| `AI Coding SDD …知识库.md` | `知识库 §N` / `知识库 §N.M` | `知识库 §71`、`知识库 §4.5` |
| `mod_gpt.md`（v1.3 可执行性评审） | `mod_gpt.md §N` | `mod_gpt.md §1`（Spec 前置）、`§4`（design 按需） |
| `modv2.md`（v1.4 复核评审） | `modv2.md §N` | `modv2.md §14`（四态追溯）、`§22`（归属矩阵） |
| 本仓规则文件 | `<文件名> §N` | `decision-protocol §6`、`spec.md §10` |
| 指代当前文件自身 | `本文件 §N` / `本模板 §N` | `本文件 §1` |

**两条硬规则**：
1. **不带小数点的 `§N`，若无前缀，一律视作 `res.md` §N。** 新增引用仍应显式写 `res.md §N`。
2. **带小数点的 `§N.M` 必须带前缀**——因为 `res.md`（1.1-1.5、2.1-2.5、4.1…）与 `Matrix`（5.1-5.3、6.1-6.5、8.1-8.4…）**都有小数编号**，不带前缀无法判定。

**源文档路径**：源文档已归档到 `sources/v1.0/`，因此 `res.md` 等价于 `sources/v1.0/res.md`，其余同理。

**紧凑写法（允许，工具会展开）**：同一来源的多个条号可缩写，归属规则是「每个 `§N` 归属其前方最近的来源名」。

| 写法 | 展开为 |
| --- | --- |
| `Matrix §24,§25,§45` | §24、§25、§45（逗号后**必须**重写 `§`） |
| `res.md §50-§58` | §50…§58（区间两侧**必须**都带 `§`） |
| `res.md §1.2-§1.4` | §1.2、§1.3、§1.4（同主号的小数区间） |
| `res.md §60-§65,§86；Matrix §24,§25` | 分号分隔的两组，各归各自来源 |

区间两端**必须**都写 `§`：只写一次（形如 `50-58`）不被识别——它会与「条号 50 带领 58 项」这类叙述冲突。
跨主号的小数区间（形如 `1.2` 跨到 `3.4`）语义不唯一，也不展开。

### 1.1 各来源的"条号从哪来"

| 来源 | 条目识别方式 | 条数 |
| --- | --- | --- |
| `res.md` | `# N. TITLE` 标题，或**全大写英文**的裸 `N. TITLE`（内部中文编号列表借"含 CJK"排除） | 121 顶层 + 11 子条目 |
| `Matrix` | Markdown 标题（`#` 开头） | 45 + 14 |
| `知识库` | Markdown 标题（`#` 开头） | 89 + 14 |
| `mod_gpt.md` | **严格递增的行首编号**（`N. P0：…`）；编号回退（重启）的行视作正文子枚举，忽略 | 9 |
| `modv2.md` | **行首中文序数**（`一、P0：…` … `二十二、…`）；正文代码块里的 `6.` / `6.1` 等阿拉伯编号**不参与**识别 | 22 |

> `mod_gpt.md` 是散文式评审而非标题编号规范文档，正文里有 3 处**从 1 重新开始**的列表
> （"A default: 1. …"、"Default priority: 1. …"、"DEFINITION OF DONE: 1. …"）。
> 若不做递增过滤，同一个条号（如第 1、2 条）会被重复登记，条号集合与标题都会张冠李戴。
>
> `modv2.md` 同样是散文式评审，但改用中文序数编号（22 条）。中文序数天然唯一且递增，故无需递增过滤；
> 只因它正文的代码块里含多处阿拉伯编号小节（`6.` / `6.1`），若混用模型会互相污染，故按来源分派不同正则。

---

## 2. 文件命名约定

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 规则文件 | kebab-case `.md` | `decision-protocol.md`、`technology-selection.md` |
| 项目实例目录 | `specs/<3 位序号>-<kebab-name>/` | `specs/001-order-management/` |
| 机器可读决策契约 | `specs/<id>/decision.json`（固定名） | `specs/001-project/decision.json` |
| ADR | `specs/<id>/adr/ADR-<3 位序号>-<kebab-topic>.md` | `ADR-001-postgres.md` |
| 模板 | `.sdd/templates/<产物名>.md`（与产物同名） | `.sdd/templates/plan.md` |
| 章节标题 | `## N. 标题`（阿拉伯数字 + 点 + 空格） | `## 5. 复杂度预算` |

---

## 3. 枚举值（保持拼写完全一致，便于机器校验）

| 概念 | 取值 |
| --- | --- |
| Decision Status | `AUTO` / `RECOMMEND` / `REQUIRE_CONFIRMATION` / `BLOCKED` |
| Spec Status | `Draft` / `Accepted`（Draft 不得含技术实现，见 `CLAUDE.md` §2） |
| ADR Status | `Proposed` / `Accepted` / `Rejected` / `Superseded` |
| 约束优先级 | `P0A`（安全/合规/可行性/平台不可能）/ `P0B`（用户不可协商约束·现有系统硬兼容）/ `P1`（Strong）/ `P2`（Preference）/ `P3`（Weak） |
| Support Status（版本） | `supported` / `LTS` / `maintenance` / `EOL` / `UNKNOWN`（见 `knowledge/versioning.md` §4） |
| Verification Status | `Draft` / `Passed` / `Passed with Known Issues` / `Failed`（见 `templates/verification.md`） |
| Verification Verdict | `PASS` / `PASS WITH KNOWN ISSUES` / `FAIL` |
| AC 结果 | `PASS` / `FAIL` / `NOT RUN` |
| `cost.within_budget` | `true`（已知在预算内）/ `false`（明确超预算）/ `null`（无预算数据，无法判断）；**`cap` 未知时不得为 `true`**（`modv2.md §7`） |
| Confidence | `0–5` 整数 |
| 评分标尺（0–5） | 见 `decision-protocol §4.1` 的 rubric |
| 复杂度预算档 | `MVP 5` / `Internal 6` / `Small SaaS 8` / `Enterprise SaaS 12` / `Distributed 20+`（计分口径见 `decision-protocol §5.1`） |

> **`P0A` > `P0B`**：两者都是 Hard Constraint，但 P0A 不可被用户偏好覆盖（`decision-protocol §2`）。
> 引用时请写全 `P0A`/`P0B`；笼统写 `P0` 只在无法区分时才可接受。

---

## 4. 未知值处理

| 场景 | 写法 |
| --- | --- |
| 数值未知 | `UNKNOWN`（**不编造精确数字**） |
| 版本未核实 | `selected: "UNKNOWN"` + `support_status: "UNKNOWN"` |
| 级别未知 | `LOW` / `MEDIUM` / `HIGH` |
| 未定项 | `<待填写>`（模板占位符） |

详见 `.sdd/templates/project-discovery.md` 与 `.sdd/knowledge/versioning.md` §4。

---

## 5. 变更规则

1. 新增引用来源 → 先在本文件 §1 登记前缀，再使用。
2. **引用解析只有一处实现**：`scripts/sdd_refs.py`（`gen_traceability.py` 与 `validate_rules.py` 共用）。
   改解析规则、扫描范围或条号模型时**只改这个文件**——两份实现必然漂移，这正是 2026-09-19
   漏报 44/42 条「未引用」的根因。新增来源的条号模型分歧见 §1.1。
3. **Schema 校验有两级，语义不同**（不要混称"机器可校验"）：
   - `specs/<id>/decision.json` → **真 JSON Schema 校验**（`scripts/mini_schema.py`，纯标准库子集实现）
   - `specs/**/*.md` 的 YAML 代码块 → **structural validation**（只查必填键存在；YAML 无标准库解析器）
4. 迁移脚本：`scripts/migrate_refs.py`（一次性迁移 + 可复跑校验）。
5. 校验脚本：`scripts/validate_rules.py`（裸引用 / 条号存在性 / 文件引用 / Decision Schema 两级 / 复杂度预算）。
6. 索引生成：`scripts/gen_traceability.py`（改完引用后必须重跑，否则 `TRACEABILITY.md` 过期）。
   两个脚本的扫描范围也由 `sdd_refs.targets()` 统一，避免一边扫根目录文档、一边不扫。
7. **版本号只有一个来源**：`.sdd/VERSION`。`README.md` / `.sdd/README.md` / `CHANGELOG.md` 都引用它，
   由自检脚本核对三处一致（`modv2.md §12`）。
8. **规则归属只有一个权威**：见 `.sdd/CANONICAL.md`；`CLAUDE.md` / `AGENTS.md` 作为 Agent 入口
   **只引用、不重新定义**行为语义（`modv2.md §22`）。
9. **审计报告 `REVIEW-*.md` 豁免引用写法检查** —— 它的职责就是引用缺陷原文；
   它仍参与落点统计，但在四态模型中只记为 `MAPPED`（描述层）。
10. 机器可读索引：`scripts/gen_traceability.py` 同时产出 `.sdd/traceability.json`。
11. 收尾标准见 `AGENTS.md` 的 **DEFINITION OF DONE**（含"改了 A 就要同步 B"的对照表）。
