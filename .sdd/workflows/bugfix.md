# Workflow: Bugfix（缺陷修复）

> 来源：res.md §105。入口：CLAUDE.md §3。

## 流程（Bugfix 不一定需要完整 Feature Spec）
```
1. Bug Description      → 现象 / 影响范围
   ↓
2. Root Cause           → 根因分析（勿臆测，用测试/日志复现）
   ↓
3. Expected Behavior    → 期望行为
   ↓
4. Fix Design           → 最小修复设计
   ↓
5. Test                 → 先写复现测试（红→绿）
   ↓
6. Implementation
   ↓
7. Verification         → 确认测试通过 + 无回归
```

## 注意
- 不必生成完整 spec.md / design.md，但 Root Cause 与 Fix Design 必须记录。
- 若修复暴露 Spec/设计错误，按 §101 回流更新。
- 涉及 Money/Inventory/Permission/关键状态（§67）须保证事务一致性。
