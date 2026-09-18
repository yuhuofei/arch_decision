# Design — 001-project（示例实例）

> 按 `.sdd/templates/design.md` 填写（§98）。

## Component
<模块划分：参考 Modular Monolith 结构（knowledge/architecture.md §3）>

## Data Flow
<请求入口 → 领域 → 基础设施 → 落库；含 async 分支（§74）>

## API
<端点 / Request-Response schema（OpenAPI §33）/ 错误格式（§70）/ 分页（§71）>

## Database
<表设计，第三范式优先（§66）；事务边界（§67）；ID 策略（§68）>

## Authentication
<Cookie Session / JWT / OIDC（§41-§44）>

## Error Handling
<统一错误格式（§70）；业务错误不暴露 DB exception>

## Async Processing
<仅明确需求（§74）：HTTP → Job → Queue → Worker → DB>

## Failure Handling
<重试 / 幂等 / 降级 / Redis failure 行为（§73）>
