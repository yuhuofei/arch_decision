# Verification — 001-project（示例实例）

> 验证实现是否符合 Spec（res.md §117 Acceptance Criteria / res.md §97）。本文件为 Verification 记录模板。

## Verification Checklist
- [ ] 所有 Acceptance Criteria（spec.md §10）已覆盖测试
- [ ] Unit Tests 通过（res.md §51）
- [ ] Integration Tests 通过（res.md §52，优先真实 infrastructure / Testcontainers）
- [ ] E2E 关键流程通过（res.md §53）
- [ ] 代码 / 架构 / Spec 三者一致（res.md §0）
- [ ] 安全 baseline 满足（res.md §45）
- [ ] 日志未泄露敏感信息（res.md §48）
- [ ] CI/CD 流水线绿（res.md §63）

## Acceptance Criteria 结果
| # | Criteria | Status | Evidence |
| --- | --- | --- | --- |
| AC1 | Given valid invitation When accepts Then becomes member | ☐ | <test/report> |

## Open Issues / Risks
<待填写>

## Convergence
实现符合 Spec 且测试通过 → 收敛。若发现 Spec 错误，按 res.md §101 回流更新。
