# Technology Selection — 002-demo-todo-cli（演示实例）

> 按 `.sdd/templates/technology-selection.md` 填写。生成前读 `.sdd/decision-trees/*.md`、`.sdd/knowledge/*.md`、`.sdd/knowledge/versioning.md`。
> **机器可读契约：同目录 `decision.json`**（真 JSON Schema 校验由 `scripts/validate_rules.py` 执行）。

## Project Type
Internal Tool / CLI（Greenfield，单人本地工具）

## Scale
Small（单人、单文件、无并发压力）

## Architecture
### Candidates
- Monolith（单进程 CLI）
- Microservices（不适用）
### Selected
Monolith（单进程脚本/包）
### Reason
无独立扩缩/部署/所有权需求；CLI 本质是单一可执行进程。
### Alternatives
（无合理替代）
### Rejected Because
Microservices 不满足强条件，纯属为架构而架构（`decision-protocol` 规则 7/30）。

## Backend
### Selected
Python 3 + argparse（标准库）
### Reason
本地工具/脚本类场景，Python 为默认候选先验；CRUD 类本地操作无需 Web 框架。argparse 满足子命令解析。
### Rejected Because
FastAPI/Django 引入 HTTP 服务与额外依赖，对本场景是过度设计。

## Database
SQLite（嵌入式文件）
### Reason
单用户本地持久化；嵌入式、零独立部署、零运维，满足需求的最简方案。
### Rejected Because
PostgreSQL/MySQL 需独立服务进程，违反「不得引入常驻服务」约束（`spec.md` §9），且 +1 基础设施复杂度无收益。

## Cache / Message Queue / Search / Vector / Object Storage
全部 None（无对应需求，不引入）。

## Authentication / Authorization
None（单用户本地，文件系统权限即足够）。

## Observability
基础 logging（INFO 级关键操作）。

## Deployment
`pip install .` 或 `python -m todo_cli`，无需容器/编排。

## Testing
pytest（Unit High / Integration Low / E2E Low）。

---

## 决策状态（decision-protocol §6）
- Architecture=Monolith → `AUTO`
- Backend=Python+argparse → `AUTO`
- Database=SQLite → `AUTO`
- Auth=None → `AUTO`
- **本实例无任何 `REQUIRE_CONFIRMATION` 项** → 无需人工确认门槛，Agent 直接执行并记录。

## 复杂度预算（decision-protocol §5）
```
SQLite 为嵌入式文件，无独立部署/运维/故障域 → 不计入复杂度（0 分）
Python / argparse 属语言与框架，不计分
score = 0  ≤  Internal Tool 预算 6   ✅
```

## 决策输出 Schema（镜像 decision.json）
```yaml
architecture_decision:
  project: { type: "Internal Tool / CLI", scale: Small, team_size: 1, deployment: "Local" }
  architecture: { style: Monolith, reason: "single-process CLI, no scaling/deployment need" }
  backend: { language: Python, framework: "argparse (stdlib)", reason: "local CLI tooling" }
  database: { primary: "SQLite (embedded file)", reason: "single-user local persistence, zero ops" }
  cache: { enabled: false }
  messaging: { enabled: false }
  search: { enabled: false }
  vector: { enabled: false }
  object_storage: { enabled: false }
  authentication: { strategy: None }
  authorization: { strategy: "single-user local" }
  observability: { logging: true, metrics: false, tracing: false }
  testing: { unit: High, integration: Low, e2e: Low }
  deployment: { strategy: "pip install / python -m" }
  cost: { recurring: "none (developer machine)", cap: "0", budget_basis: "项目预算为 0，仅使用本机资源", within_budget: true }
  evidence:
    - { type: requirement, claim: "本地单用户的增删改查命令行需求", source: "spec.md#FR-001", verified_at: null }
    - { type: documentation, claim: "标准库 argparse 足以覆盖子命令与参数解析", source: "res.md §90（依赖决策七问）", verified_at: null }
  constraints:
    - "P1: 单用户本地运行，无并发写压力"
    - "P2: 零运维面（不引入独立部署组件）"
    - "P2: 成本必须为 0"
  alternatives:
    - { option: "Typer / Click", reason: "标准库 argparse 已满足，引入即产生依赖维护义务" }
    - { option: "JSON 文件持久化", reason: "失去事务与查询能力；SQLite 内置且无部署成本" }
    - { option: DuckDB, reason: "分析型更强，但本工具是事务型小数据读写" }
  scores: []
  deferred:
    - { decision: "Cloud sync / multi-device", reason: "当前无需求；出现即需服务端与认证，属架构级变更", trigger: ["多设备或多用户协作", "云端备份诉求"] }
  review_triggers:
    - "出现多用户或共享同一数据文件 → 重评 SQLite 并发写"
    - "出现网络访问/API 需求 → 重新决策 backend 与 authentication"
  decision_history: []
  rejected:
    - { option: "Web framework (FastAPI/Django)", reason: "no HTTP server / multi-client need" }
    - { option: "PostgreSQL/MySQL server", reason: "embedded SQLite suffices; server adds unjustified +1" }
    - { option: "React/Vue frontend", reason: "no UI; CLI is sufficient" }
  confidence: { overall: 5 }
```

## Versions（见 knowledge/versioning.md）
| Technology | Selected | Support Status | Reason |
| --- | --- | --- | --- |
| Python | UNKNOWN | UNKNOWN | 实现前须联网核对目标环境可用的 supported stable major，禁止编造版本号 |

> 与 `decision.json` 保持一致；本演示未联网核对，按 versioning.md 规则写 `UNKNOWN`。
