# Verification — 001-project（示例实例）

> 结构遵循 `.sdd/templates/verification.md`（8 节）；机器可读契约见 `.sdd/schema/verification.schema.json`。
> 证明实现结果满足 Accepted Spec / Plan / Tasks / Acceptance Criteria。
> 引用约定见 `.sdd/CONVENTIONS.md`（禁止裸写 `§N`）。

---

## 1. Verification Status

```
Status:        Draft
Verified At:   —
Verified By:   —
Commit:        —
Spec:          specs/001-project/spec.md  (Status: Accepted)
```

> 本示例未实际实现与运行，故为 `Draft`。**不得**用示例数据伪造 PASS。

---

## 2. Acceptance Criteria

> 逐条对应 `spec.md` §10。未验证的写 `NOT RUN` 并说明原因，不留空。

| AC | 描述 | 验证方式 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| AC-001 | Given 合法下单 When 提交 Then 订单创建成功 | Test | NOT RUN | 待 T4 完成后补 `tests/integration/test_order_create.py` |
| AC-002 | Given 无效商品 When 提交 Then 返回校验错误 | Test | NOT RUN | 待 T4 完成后补 `tests/integration/test_order_validation.py` |

---

## 3. Requirement Traceability

| Requirement | Design | Task | Code | Test | Result |
| --- | --- | --- | --- | --- | --- |
| FR-001（创建订单） | plan.md §6 | T2 / T4 | `<待实现>` | TEST-001 | NOT RUN |
| NFR（性能 / 安全 / 可观测） | plan.md §8-§10 | T5 / T6 | `<待实现>` | TEST-002 | NOT RUN |

> `Requirements ↔ Tests traceable`（`res.md §97`）：任一层留空即视为追溯断裂。

---

## 4. Test Results

```
Unit
  Command:   pytest tests/unit
  Result:    NOT RUN（示例实例未实现）

Integration
  Command:   pytest tests/integration
  Result:    NOT RUN

E2E
  Command:   npx playwright test
  Result:    NOT RUN
```

---

## 5. Non-Functional Verification

```
Performance
  Target:    <来自 spec.md §5 的 NFR 数字>
  Actual:    NOT VERIFIED
  Evidence:  —
  Verdict:   NOT VERIFIED

Security
  Checks:    认证 / 授权 / 密钥管理 / 依赖漏洞扫描（res.md §45）
  Result:    NOT RUN

Availability / Reliability
  Checks:    按 knowledge/reliability.md 的 SLA / 备份 / 降级检查
  Result:    NOT RUN

Observability
  Logs:  结构化日志（res.md §47）    Metrics:  —    Tracing:  —
  Result:    NOT RUN（日志不得泄露敏感信息，res.md §48）
```

---

## 6. Consistency Check

- [ ] Accepted Spec ↔ Plan consistent
- [ ] Plan ↔ Tasks consistent
- [ ] Tasks ↔ Code consistent
- [ ] Requirements ↔ Tests traceable
- [ ] No undocumented architecture changes
- [ ] No unresolved `REQUIRE_CONFIRMATION` decision
- [ ] No unresolved `BLOCKED` decision
- [ ] 实现未绕过 Spec（发现 Spec 错误时按 `res.md §101` 先回改上游产物）

---

## 7. Known Issues

| Issue | Severity | Impact | Follow-up |
| --- | --- | --- | --- |
| 示例实例未实现，全部验证项为 NOT RUN | Low | 不构成真实交付 | 真实项目实现后替换本文件 |

---

## 8. Final Verdict

```
FAIL    # 示例实例无实现，按定义不能判 PASS
```

**Evidence / Notes**

本文件是**结构与写法示例**，用于演示 `.sdd/templates/verification.md` 的 8 节骨架，
不代表任何真实验证结果。真实项目必须把每一条 `NOT RUN` 替换为可复跑的结论。
