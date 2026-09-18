# Example: Brownfield（存量项目决策）

> 来源：Matrix §34-§35；知识库 §71,§75。演示"存量优先保留"。

## 场景
现有项目：
```
Existing:
  Backend:  Django + PostgreSQL
  Frontend: React
```

## Knowledge Base 推荐（但此为 Brownfield）
```
Recommended (greenfield): FastAPI + PostgreSQL + Vue
```

## 决策结果
```yaml
existing_stack:
  backend: Django
  frontend: React
  database: PostgreSQL

recommended_action:
  preserve_existing_stack: true

migration:
  required: false
```

**DO NOT migrate automatically.** 不把 Django→FastAPI、React→Vue。
仅当：
```
existing_stack_problem = demonstrated   # 安全/EOL/严重性能/无法满足业务/无法维护
OR migration_requested = true          # 用户明确要求
```
才允许迁移，且迁移必须成为独立 ADR（`REQUIRE_CONFIRMATION`）。

## 决策状态
- preserve existing stack → `AUTO`（Hard Constraint 优先）
- 任何技术迁移 → `REQUIRE_CONFIRMATION`

## 延伸
进入存量项目先生成 `project-discovery.md`（§102）分析现有栈，不立即写代码。
