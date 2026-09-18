# Design — 001-project（示例实例）

> 按 `.sdd/templates/design.md` 与 `.sdd/templates/plan.md` 填写（§98, 知识库 §80）。
> Design 描述 HOW（plan.md 亦承载技术栈/设计）。

## Component
Modular Monolith 模块：users / orders / payments / notifications（见 architecture.md §2.2）。

## Data Flow
创建订单：API → orders module (domain) → repository → PostgreSQL；事件发往 notifications module。

## API
REST + OpenAPI（res.md §33）；错误格式（res.md §70）；分页 cursor-based（res.md §71）。

## Database
orders / order_items 表；第三范式（res.md §66）；事务覆盖支付/库存（res.md §67）；ID UUIDv7（res.md §68）。

## Authentication
Session（Cookie + Server-side，res.md §42）；多 client 时改 JWT/OIDC（res.md §43）。

## Authorization
RBAC（res.md §46）。

## Error Handling
统一错误格式（res.md §70）；业务错误不暴露 DB exception。

## Async Processing
仅明确需求时（res.md §74）：订单创建 → Queue → Worker → 通知。

## Failure Handling
重试 / 幂等 / 降级；Redis failure 行为（res.md §73）。
