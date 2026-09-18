# Template: Verification（验证报告）

> 用途：证明实现结果满足 **Accepted Spec**、Plan、Tasks 与 Acceptance Criteria。
> 来源：`res.md §97`（Acceptance Criteria）、`res.md §50-§53`（Testing Strategy / Unit / Integration / E2E）、
> `res.md §116`（Architecture Review Checklist）；`Matrix §27-§28`（Testing Matrix / Test Strategy Matrix）；
> `知识库 §11`（Testing）；`modv2.md §4`（本模板为结构缺口补齐）。
> **本文件是 `specs/<id>/verification.md` 的必填产物**（见 `.sdd/LAYOUT.md` §1.1）。
> 机器可读契约：`.sdd/schema/verification.schema.json`。
> 引用约定见 `.sdd/CONVENTIONS.md`：**禁止裸写 `§N`**。

---

# Verification: &lt;Feature / Project Name&gt;

## 1. Verification Status

```
Status:        Draft / Passed / Passed with Known Issues / Failed
Verified At:   <YYYY-MM-DD>
Verified By:   <Agent / Human / CI job>
Commit:        <sha>
Spec:          specs/<id>/spec.md  (Status: Accepted)
```

> `Status` 取值与 `verification.schema.json` 的枚举一致，不得自造。

---

## 2. Acceptance Criteria

> 逐条对应 `spec.md` §10 的 Acceptance Criteria。**每一条都必须有结论**，
> 不允许留空 —— 未验证项写 `NOT RUN` 并说明原因。

| AC | 描述 | 验证方式 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| AC-001 | <描述> | Test / Manual / Inspection | PASS / FAIL / NOT RUN | `<测试名 / 命令 / 截图路径>` |
| AC-002 | | | | |

---

## 3. Requirement Traceability

> `Requirements ↔ Tests traceable`（`res.md §97`）。任一层留空即视为追溯断裂。

| Requirement | Design | Task | Code | Test | Result |
| --- | --- | --- | --- | --- | --- |
| FR-001 | D-001 | T-001 | `<文件:符号>` | TEST-001 | PASS |
| NFR-001 | | | | | |

---

## 4. Test Results

> 命令必须可复跑；不要写"已测试"这类不可复核的结论。

```
Unit
  Command:   <e.g. pytest tests/unit>
  Result:    <N passed / N failed / N skipped>

Integration
  Command:   <e.g. pytest tests/integration>
  Result:

E2E
  Command:   <e.g. npx playwright test>
  Result:
```

---

## 5. Non-Functional Verification

> NFR 必须对着 `spec.md` 的原始指标核，不写"性能良好"这类无数字结论（`knowledge/testing.md`）。

```
Performance
  Target:    <来自 spec.md 的 NFR>
  Actual:
  Evidence:  <压测命令 / 报告路径>
  Verdict:   PASS / FAIL / NOT VERIFIED

Security
  Checks:    <认证 / 授权 / 密钥 / 注入面 / 依赖漏洞扫描>
  Result:

Availability / Reliability
  Checks:    <见 knowledge/reliability.md>
  Result:

Observability
  Logs:      Metrics:      Tracing:
  Result:
```

---

## 6. Consistency Check

> 与 `decision-protocol.md` §7 的第 21 步对应。逐项勾选，不得整段跳过。

- [ ] Accepted Spec ↔ Plan consistent
- [ ] Plan ↔ Tasks consistent
- [ ] Tasks ↔ Code consistent
- [ ] Requirements ↔ Tests traceable
- [ ] No undocumented architecture changes
- [ ] No unresolved `REQUIRE_CONFIRMATION` decision
- [ ] No unresolved `BLOCKED` decision
- [ ] 实现未绕过 Spec（发现 Spec 错误时按 `new-feature.md` 先回改上游产物）

---

## 7. Known Issues

| Issue | Severity | Impact | Follow-up |
| --- | --- | --- | --- |
| | High / Medium / Low | | |

---

## 8. Final Verdict

```
PASS
PASS WITH KNOWN ISSUES    # 必须在上表逐条登记，且不得含 High
FAIL                      # 不得进入发布；退回 Plan / Tasks / Code
```

**Evidence / Notes**

<补充说明、未通过项的处理方式、复现命令>
