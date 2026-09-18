# Template: Tasks（任务拆分）

> 用途：Tasks 必须小、可执行、可验证、有依赖（res.md §99）。实例见 `specs/001-project/tasks.md`。

# Tasks: <feature-name>

## 原则
- 小（单点可完成）
- 可执行
- 可验证
- 有依赖关系

## ❌ 反例
```
Implement authentication system
```

## ✅ 正例
```
- [ ] Create user model
- [ ] Create password hashing service
- [ ] Create login endpoint
- [ ] Create refresh token flow
- [ ] Add authentication middleware
- [ ] Add integration tests
```

## Task List

| ID | Task | Depends On | Verification |
| --- | --- | --- | --- |
| T1 | | | |
| T2 | | | |
| T3 | | | |

## Verification Mapping
每个 Task 对应测试类型（§50-§53）：
- Unit：Domain logic / Business rules / Validation
- Integration：DB / API / Auth / MQ
- E2E：仅关键业务流程
