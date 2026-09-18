# ADR-002: Use Python + FastAPI for the Backend

> 模板：`.sdd/templates/adr.md`　所属实例：`specs/001-project/`

## Status
Accepted

## Decision Status
`AUTO`

## Confidence
4 / 5 —— 语言与框架匹配明确；扣分项为团队若更熟 Go 则需重评。

## Decision
后端使用 **Python + FastAPI**（配 Pydantic / SQLAlchemy / Alembic）。

## Context
订单管理系统以 CRUD + 业务 API 为主，无极端性能或高并发网络服务需求。
需要 OpenAPI 契约以驱动前端 TS Client 生成（`知识库 §52-§53`）。

## Constraints
| 类型 | 内容 |
| --- | --- |
| P0 Hard | 无既有后端栈约束（Greenfield） |
| P1 Strong | 需产出 OpenAPI 供前端生成 Client |
| P2 Preference | 可测试性（业务逻辑需可单测） |

## Alternatives
- Python + FastAPI
- Python + Django
- Python + Flask
- Go + net/http / Gin

## Why FastAPI
- 语言匹配：CRUD/API 且非极端性能 → Python（`Matrix §6.1`）
- 框架匹配：General / Async / AI API → FastAPI（`Matrix §7` Python 分支默认）
- 原生 OpenAPI 生成，直接满足前端契约需求（`res.md §33`）
- 依赖注入 + Pydantic 校验，利于分层与单测

## Why Not Alternatives
- **Django**：适用于 Admin-heavy / CMS / ORM-heavy / server-rendered 场景（`Matrix §7`），本项目非此定位
- **Flask**：新 API 项目下 FastAPI 优于 Flask（`knowledge/backend.md` §2，非绝对）
- **Go**：仅在并发高 / 网络服务 / 基础设施 / 延迟严格 / CPU 效率重要时才更优（`Matrix §6.2`），本例均不满足

## Risks
- Python 运行时性能上限低于 Go → 缓解：本项目规模下非瓶颈；确有成瓶颈证据时再评估热点服务拆分

## Assumptions
- 无 CPU 密集型在线计算需求（重计算会走离线/异步，见 `plan.md` §8）

## Consequences
- 工具链绑定：uv + Ruff + mypy/pyright + pytest（`知识库 §47`）
- 后端语言变更 = 架构级变更 → `REQUIRE_CONFIRMATION`
- **Reversibility：Medium**
