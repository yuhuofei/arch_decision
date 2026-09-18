# Design — 001-project（示例实例）

> 按 `.sdd/templates/design.md` 填写（`res.md §98`、`知识库 §80`）。
> **按需产物**：本实例命中「复杂接口契约 + 安全敏感流程（支付）+ 异步流程」，故保留（`.sdd/LAYOUT.md` §1.2）。
> **本文件只写 `plan.md` 装不下的细节**，不得重述 plan 已写的架构 / 技术栈 / 模块划分 / 缓存 TTL。
> 与 `plan.md` 冲突时以 `plan.md` 为准 —— 需要改 plan 的内容就改 `plan.md` 本身。

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
