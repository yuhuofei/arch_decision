# Example: Internal Tool（小型内部工具）

> 来源：AI Coding SDD 知识库 §63。演示"不要默认复杂架构"。

## 场景
内部订单查询/小工具，团队 2-3 人，用户少，无高并发。

## 可选方案
```
Option A: Next.js + PostgreSQL          # 全栈单体，最简单
Option B: FastAPI + Vue + PostgreSQL     # 前后端分离，团队偏 Python
```
两者均可，**不要默认** Microservices / Kafka / Kubernetes / Elasticsearch / Redis。

## 决策依据
- 复杂度 budget：MVP/Internal 预算 5-6；引入 MQ/ES/K8s 会轻易超限。
- 前后端合并可接受（architecture.md §6）：简单 CRUD / 内部工具 → Next.js Full Stack 合理。
- 若已有 Vue 专长 → Option B 保持一致性（Soft Constraint，团队熟悉度）。

## 决策输出（节选）
```yaml
architecture: { style: Monolith, reason: "small internal tool, no scaling need" }
backend: { language: Python, framework: FastAPI }   # 或 Next.js（Option A）
frontend: { framework: Vue 3 + Vite }                # 或 Next.js（Option A）
database: { primary: PostgreSQL }
cache: { enabled: false }
messaging: { enabled: false }
deployment: { strategy: Docker Compose }
```

## 决策状态
`AUTO`（无 REQUIRE_CONFIRMATION 项）。禁止为"以后可能"预置 Redis/Kafka/ES。
