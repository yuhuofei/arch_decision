# Tasks — 002-demo-todo-cli（演示实例）

> 按 `.sdd/templates/tasks.md` 填写。任务须小、可执行、可验证、有依赖。

## Task List

| ID | Task | Depends On | Verification |
| --- | --- | --- | --- |
| T1 | 初始化仓库结构与 `pyproject.toml` | — | `todo --help` 可运行 |
| T2 | 实现 `db.py`：建 `tasks` 表 | T1 | 表存在且字段正确 |
| T3 | 实现 `tasks.py`：add/list/done/rm | T2 | 单元测试通过 |
| T4 | 实现 `main.py`：argparse 四个子命令 | T3 | `todo add/list/done/rm` 端到端通过 |
| T5 | 接入 logging（INFO 级关键操作） | T4 | 关键操作有日志输出 |
| T6 | 编写 pytest 单测并达 Unit High | T3 | `pytest` 全绿 |

## Verification Mapping
- Unit：领域逻辑 / 校验（tasks.py）
- Integration：CLI 子命令（main.py）
- E2E：仅关键业务路径（add → list → done → rm）
