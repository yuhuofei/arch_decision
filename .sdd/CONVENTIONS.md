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
| 本仓规则文件 | `<文件名> §N` | `decision-protocol §6`、`spec.md §10` |
| 指代当前文件自身 | `本文件 §N` / `本模板 §N` | `本文件 §1` |

**两条硬规则**：
1. **不带小数点的 `§N`，若无前缀，一律视作 `res.md` §N。** 新增引用仍应显式写 `res.md §N`。
2. **带小数点的 `§N.M` 必须带前缀**——因为 `res.md`（1.1-1.5、2.1-2.5、4.1…）与 `Matrix`（5.1-5.3、6.1-6.5、8.1-8.4…）**都有小数编号**，不带前缀无法判定。

**源文档路径**：源文档已归档到 `sources/v1.0/`，因此 `res.md` 等价于 `sources/v1.0/res.md`。

---

## 2. 文件命名约定

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 规则文件 | kebab-case `.md` | `decision-protocol.md`、`technology-selection.md` |
| 项目实例目录 | `specs/<3 位序号>-<kebab-name>/` | `specs/001-order-management/` |
| ADR | `specs/<id>/adr/ADR-<3 位序号>-<kebab-topic>.md` | `ADR-001-postgres.md` |
| 模板 | `.sdd/templates/<产物名>.md`（与产物同名） | `.sdd/templates/plan.md` |
| 章节标题 | `## N. 标题`（阿拉伯数字 + 点 + 空格） | `## 5. 复杂度预算` |

---

## 3. 枚举值（保持拼写完全一致，便于机器校验）

| 概念 | 取值 |
| --- | --- |
| Decision Status | `AUTO` / `RECOMMEND` / `REQUIRE_CONFIRMATION` / `BLOCKED` |
| ADR Status | `Proposed` / `Accepted` / `Rejected` / `Superseded` |
| 约束优先级 | `P0`（Hard）/ `P1`（Strong）/ `P2`（Preference）/ `P3`（Weak） |
| Confidence | `0–5` 整数 |
| 复杂度预算档 | `MVP 5` / `Internal 6` / `Small SaaS 8` / `Enterprise SaaS 12` / `Distributed 20+`（计分口径见 `decision-protocol §5.1`） |

---

## 4. 未知值处理

| 场景 | 写法 |
| --- | --- |
| 数值未知 | `UNKNOWN`（**不编造精确数字**） |
| 级别未知 | `LOW` / `MEDIUM` / `HIGH` |
| 未定项 | `<待填写>`（模板占位符） |

详见 `.sdd/templates/project-discovery.md`。

---

## 5. 变更规则

1. 新增引用来源 → 先在本文件 §1 登记前缀，再使用。
2. 迁移脚本：`scripts/migrate_refs.py`（一次性迁移 + 可复跑校验）。
3. 校验脚本：`scripts/validate_rules.py`。
