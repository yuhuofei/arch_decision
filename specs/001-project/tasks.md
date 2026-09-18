# Tasks — 001-project（示例实例）

> 按 `.sdd/templates/tasks.md` 填写（§99）。任务须小、可执行、可验证、有依赖。

## Task List

| ID | Task | Depends On | Verification |
| --- | --- | --- | --- |
| T1 | 初始化仓库结构与依赖（res.md §86） | — | 项目可本地启动 |
| T2 | 创建领域模型 + Migration（res.md §64） | T1 | Migration 可应用 |
| T3 | 实现认证（密码 hash / 登录 / refresh） | T2 | 单元测试 + 集成测试（res.md §51,§52） |
| T4 | 实现核心 API 端点（OpenAPI res.md §33） | T3 | 集成测试通过 |
| T5 | 日志 / 观测接入（res.md §47-§49） | T4 | 结构化日志输出 |
| T6 | E2E 关键流程（res.md §53） | T5 | Playwright 通过 |

## Verification Mapping
- Unit：Domain logic / Business rules / Validation
- Integration：DB / API / Auth
- E2E：仅关键业务流程（如 Login → Create → Pay → Confirm）
