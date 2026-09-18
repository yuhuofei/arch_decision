# Decision Tree: Backend（后端语言与框架选型）

> 配套知识：`.sdd/knowledge/backend.md`

## 起点：选哪种语言？

```
工作负载主要是 AI / Data / LLM / RAG / 数据处理 / 快速 MVP？
├─ 是 ──→ Python
│         └─ API 服务？ → FastAPI（默认）
│             ├─ 强依赖 Django Admin / CMS / ORM-heavy / server-rendered → Django
│             └─ 已有 Flask 且极简/高度定制 → Flask（新项目仍优先 FastAPI）
├─ 否 ──→ 高并发 / 网络服务 / Gateway / Proxy / Infrastructure / Cloud Native / CLI？
│         └─ 是 ──→ Go（Chi 默认 / Gin / Echo）
├─ 否 ──→ 全栈 TypeScript / Web-first / BFF / Realtime / 团队偏好 TS？
│         └─ 是 ──→ TypeScript + NestJS（Enterprise/模块化/DI）
├─ 否 ──→ Enterprise / Banking / ERP / 大型组织 / 已有 JVM 生态 / 复杂事务？
│         └─ 是 ──→ Java 或 Kotlin + Spring Boot
└─ 否 ──→ 微软生态？ → C#
```

## 关键判定

### Python（§6）
- 选：AI / LLM / RAG / Data / Automation / API / SaaS / Internal Tool / MVP / CRUD
- 不选（考虑 Go/Java/Rust）：极端低延迟 / 极端高并发 / CPU-heavy / 网络基础设施

### FastAPI vs Django vs Flask（§7-§9）
- 新 Python API → **FastAPI** 默认
- Admin-heavy / CMS / Enterprise CRUD / server-rendered → Django
- 已有 Flask / 极简 / 高度定制 → Flask

### Go framework（§11）
- Lightweight / 标准库优先 / 最小抽象 → Chi（默认）
- REST / 快速开发 / 成熟生态 → Gin
- Lightweight service → Echo

### TS backend（§13）
- Enterprise TS / 模块化 / DI / 大团队 → NestJS
- 极简 API / 极轻量 serverless → 不引入框架

### Java/Kotlin（§15）
- Enterprise / 复杂业务 / 大团队 / 长生命周期 → Spring Boot

## 用户显式指定（§1.5）
用户指定 `Python + FastAPI + PostgreSQL` → 最高优先级，不得擅自改。`Go + Gin + MySQL` 即使 Agent 认为更好也照做，可记录风险。

## 输出
写入 `technology-selection.md` 的 Backend 段：Candidates / Selected / Reason / Alternatives / Rejected Because。
