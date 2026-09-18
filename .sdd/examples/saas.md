# Example: SaaS（普通企业 Web SaaS）

> 来源：Matrix §37。演示 decision-protocol 落地。

## Input（需求）
```yaml
project:
  type: SaaS
users:
  expected: 5000
frontend:
  web: true
backend:
  api: true
data:
  relational: true
ai: false
concurrency: medium
team:
  size: 6
deployment:
  docker: true
```

## 候选架构
Microservices / Modular Monolith / Monolith

## 规则应用
```
team_size <= 10
independent_scaling = false
service_independence = low
```
→ Microservices **eliminated**（不满足强条件）。
候选：Monolith / Modular Monolith；复杂度 medium → **Modular Monolith selected**。

## 决策输出（Decision Output Schema）
```yaml
architecture_decision:
  project: { type: SaaS, scale: Small/Medium, team_size: 6, deployment: Docker }
  architecture: { style: Modular Monolith, reason: "no independent scaling/deployment need" }
  backend: { language: Python, framework: FastAPI, reason: "CRUD/API, non-extreme-perf" }
  frontend: { language: TypeScript, framework: Vue 3 + Vite, reason: "business admin app" }
  database: { primary: PostgreSQL, reason: "relational default" }
  cache: { enabled: false }
  messaging: { enabled: false }
  search: { enabled: false, technology: PostgreSQL FTS }
  object_storage: { enabled: true, technology: S3-compatible }
  authentication: { strategy: Session }
  authorization: { strategy: RBAC }
  observability: { logging: true, metrics: true, tracing: false }
  testing: { unit: High, integration: High, e2e: Medium }
  deployment: { strategy: Docker }
  rejected: [ { option: Microservices, reason: "no strong-condition satisfied" } ]
  confidence: { overall: 4 }
```

## 复杂度预算（口径见 decision-protocol §5.1）
```
PostgreSQL(1) + 对象存储(1) = 2  ≤ Small SaaS 预算 8   ✅
Docker 属打包方式，不计分。
```

## 决策状态
全部 `AUTO`（无 Microservices/K8s/Auth 架构变更等 REQUIRE_CONFIRMATION 项）。
