# Implementation Plan — 002-demo-todo-cli（演示实例）

> 按 `.sdd/templates/plan.md` 填写。描述 HOW、架构与技术选择。
> 技术选型来自 `technology-selection.md`；本演示无 `design.md`（`plan.md` 已装得下，判据见 `.sdd/LAYOUT.md` §1.2）。

## 1. Architecture
### Architecture Style
Monolith（单进程命令行程序）。

### Component Diagram
```
终端 ──> main.py(argparse) ──> tasks.py(领域操作) ──> db.py(SQLite) ──> todo.db
```

### Data Flow
命令解析 → 调用领域函数 → 经仓储层读写 SQLite → 返回文本结果。

## 2. Technology Stack
- 语言：Python 3（versioning.md：实现前核对 stable major，本演示写 UNKNOWN）
- CLI：argparse（标准库）
- 持久化：SQLite（标准库 `sqlite3`）
- 测试：pytest

## 3. Project Structure
```
todo_cli/
  __init__.py
  main.py        # argparse 子命令入口
  db.py          # 连接 + 建表
  tasks.py       # 增删改查领域函数
tests/
  test_tasks.py
todo.db          # SQLite 文件（应 gitignore）
pyproject.toml   # 打包 / 入口
```

## 4. Backend Design
- `db.py`：`init_db()` 建 `tasks` 表；返回连接。
- `tasks.py`：`add/ list/ done/ rm` 纯函数，接收连接。
- `main.py`：`argparse` 注册四个子命令，调用 `tasks.py`。

## 5. Frontend Design
无（CLI）。

## 6. Database
```sql
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  done INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```
无迁移策略（v1 单表，后续变更走 `new-feature.md`）。

## 7. API
CLI 子命令（非 REST）：
- `todo add <title>`
- `todo list [--all]`
- `todo done <id>`
- `todo rm <id>`

错误模型：未知 ID → 退出码 1 + stderr `task not found`。

## 8. Async Processing
无。

## 9. Cache
无。

## 10. Security
本地文件 `~/.todo/todo.db`，依赖文件系统权限；不解析网络输入。

## 11. Testing
- Unit（High）：`tasks.py` 各函数 + 临时内存库。
- Integration（Low）：`main.py` 子命令端到端。
- E2E（Low）：仅关键路径。

## 12. Observability
`logging` INFO 级记录 add/done/rm。

## 13. Deployment
`pip install .` 暴露 `todo` 命令；或 `python -m todo_cli`。无容器。

## 14. Architecture Decisions
### ADR-001 SQLite
Decision: 采用嵌入式 SQLite / Reason: 单用户本地持久化，零运维 / Alternatives: PostgreSQL / Rejected: 需独立服务 / Status: AUTO / Confidence: 5

## 15. Risks
- 并发写入：单用户单实例可接受；文档说明勿多实例同时跑。

## 16. Migration
v1 单表，暂无。
