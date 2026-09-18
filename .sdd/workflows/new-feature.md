# Workflow: New Feature（新特性）

> 来源：res.md §104。入口：CLAUDE.md §3。

## 流程
```
Requirement
   ↓
1. Explore            → 理解现有代码/架构/相关 Spec
   ↓
2. Clarify            → 仅问 MUST ASK（§108）；无关紧要问题用 CAN ASSUME 并记录
   ↓
3. Technology impact  → 是否引入新技术？用 §115 检查表；影响架构必须 Ask
   ↓
4. Spec               → 用 templates/spec.md（可仅增量，不必全量 23 项）
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
- 技术影响评估：若需新增组件，按 decision-trees 与 §115 检查表论证必要性。
- 改动若触及既有 Spec 错误：按 §101 更新 Spec→Design→Tasks 再继续。
