# Workflow: Small Change（轻量改动）

> 入口：`CLAUDE.md` §3（按改动规模分流的追加读取表）。
> 目的：**避免 Agent 对每个小改动都跑完整 SDD 流程**（流程成本 > 改动价值）。
> 治理：`.sdd/decision-trees/decision-protocol.md`

---

## 1. 判定阈值（**全部满足**才走本流程）

| 维度 | 阈值 |
| --- | --- |
| 涉及文件数 | ≤ 3 |
| 变更行数 | ≤ 100 行（不含纯格式化） |
| 触及架构 | **否** —— 不新增组件、不改分层、不改通信协议 |
| 触及接口 | **否** —— 不改公开 API 契约、不改 DB schema |
| 触及安全 | **否** —— 不涉及认证 / 授权 / 密钥 / 权限判定 |
| 触及业务规则 | **否** —— 不涉及 Money / Inventory / Permission / 关键状态（`res.md §67`） |
| 触及依赖 | **否** —— 不新增、不升级依赖 |

**任一条件不满足 → 退出本流程**，改走 `new-feature.md` / `bugfix.md` / `refactor.md`。

### 1.1 Behavioral Risk Check（行为风险检测；`modv2.md §21`）

> **行数不是风险指标。** 把 `if user.is_admin:` 改成 `if user.is_owner:` 只改一行，
> 却是权限规则变化。即使满足上表全部阈值，只要改变下列任一项，
> **立即升级**为 `new-feature.md` / `bugfix.md`，不得按轻量改动处理：

```
- externally observable behavior   （对外可观察行为）
- authorization result              （授权判定结果）
- persistence semantics             （持久化语义：存不存 / 存什么 / 删不删）
- error semantics                   （错误码 / 错误语义 / 异常类型）
- transaction boundary              （事务边界）
- concurrency behavior              （并发行为 / 加锁 / 幂等性）
- retry behavior                    （重试次数 / 重试条件）
- default business behavior         （默认业务行为 / 默认取值）
```

**`≤100 行` 与 `≤3 文件` 只是防止过度流程的成本门槛，不是安全门槛。**

---

## 2. 典型可走场景

- 文案 / i18n 文案调整
- 样式 / 布局微调
- 日志字段增补（**不含**敏感信息，`res.md §48`）
- 内部函数重命名、注释修正
- 补充测试用例（不改变行为）
- 非生产关键配置的默认值调整

## 3. 不可走（必须走完整流程）

| 情况 | 原因 |
| --- | --- |
| 任何 DB schema 变更 | migration 属 `REQUIRE_CONFIRMATION` 范畴（`res.md §64`） |
| 任何公开 API 契约变更 | `decision-protocol` §6 |
| 认证 / 授权相关改动 | Authentication architecture 变更属 `REQUIRE_CONFIRMATION` |
| 新增或升级依赖 | 须过 `res.md §90` 的依赖决策七问 |
| 涉及 Money / Inventory / Permission / 关键状态 | 事务与一致性要求（`res.md §67`） |
| 性能相关的结构调整 | 需实测证据（`decision-protocol` §5.1 检查表） |

---

## 4. 流程

```
1. 确认阈值      → 逐项对照本文件 §1 与 §1.1 行为风险；任一不满足即退出本流程
   ↓
2. 最小改动      → 不做"顺手重构"（禁止 res.md §106 式的大范围重写）
   ↓
3. 验证          → 至少保证现有测试全绿
   ↓
4. 记录          → 提交信息说明：改了什么、为何属于轻量改动
```

---

## 5. 注意

1. 本流程**免去** `spec.md` / `plan.md` / ADR 产出，但**不免去测试**。
2. 改动过程中若发现触及阈值外内容 → **立即升级**到对应流程，不要"改都改了"。
3. 轻量改动**不改变对外行为**；若改变了行为，按 `new-feature.md` 走 Spec，
   并按 `.sdd/decision-trees/impact-analysis.md` 重估影响面。
4. 单次会话中累计多个小改动仍按各自阈值判定；累计超过阈值即视为一次 new-feature。
