# Workflow: Refactor（重构）

> 来源：res.md §106。入口：CLAUDE.md §3。

## 流程（禁止一次性大规模重写）
```
1. Current Architecture   → 记录现状
   ↓
2. Problem                → 重构动因（可维护性/性能/复杂度）
   ↓
3. Constraints            → 约束（兼容/停机/风险）
   ↓
4. Target Architecture    → 目标形态
   ↓
5. Migration Strategy     → 迁移策略
   ↓
6. Incremental Tasks      → 拆为小步增量任务
   ↓
7. Tests                  → 每步有测试守护（res.md §50-§53）
   ↓
8. Implementation         → 增量落地，可随时回退
```

## 注意
- **禁止**一次性大规模重写（res.md §106）。
- 每步可验证、可回退（Reversibility，见 adr.md）。
- 重构不改变对外行为；若改变，按 new-feature 流程走 Spec。
- Brownfield 进入已有项目先生成 project-discovery.md（§102），不立即写代码。
