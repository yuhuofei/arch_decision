# Workflow: New Feature（新特性）

> 来源：res.md §104；影响面分析见 `modv2.md §20` 与 `.sdd/decision-trees/impact-analysis.md`。入口：CLAUDE.md §3。

## 流程
```
Requirement
   ↓
1. Explore            → 理解现有代码/架构/相关 Spec
   ↓
2. Clarify            → 仅问 MUST ASK（res.md §108）；无关紧要问题用 CAN ASSUME 并记录
   ↓
2.5 Impact Analysis   → 用 .sdd/decision-trees/impact-analysis.md 逐面评估：
                        受影响模块 / API / DB 表 / 外部集成 / 认证授权 / 测试 / 部署 / 可观测 / 迁移
                        api=breaking 或 database=migration required → decision_status = REQUIRE_CONFIRMATION
   ↓
3. Technology impact  → 是否引入新技术？用 res.md §115 检查表；影响架构必须 Ask
   ↓
4. Spec               → 用 templates/spec.md（14 节；增量特性可只填受影响小节）
   ↓
5. Design             → 用 templates/design.md
   ↓
6. Tasks              → 用 templates/tasks.md
   ↓
7. Implementation
   ↓
8. Tests
   ↓
9. Review
   ↓
10. Verification
```

## 注意
- 不重复 Discovery（已有项目上下文）。
- 技术影响评估：若需新增组件，按 decision-trees 与 res.md §115 检查表论证必要性。
- **影响面分析是硬前置**：不确定影响范围时，不得“先改了再看”（impact-analysis.md §4）。
- 实际改动**超出**影响面分析声明的范围 = 未登记的架构变更，必须补登并重评（impact-analysis.md §6）。
- 改动若触及既有 Spec 错误：按 res.md §101 更新 Spec→Design→Tasks 再继续。
