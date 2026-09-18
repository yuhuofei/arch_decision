# Template: Design（设计）

> 用途：Design 必须回答以下（res.md §98）。实例见 `specs/001-project/design.md`。

# Design: <feature-name>

## Component
<!-- 模块 / 服务划分，组件职责与边界 -->

## Data Flow
<!-- 请求从入口到落库的流转；含 async 分支（§74） -->

## API
<!-- 端点、Request/Response schema（OpenAPI, §33）、错误格式（§70）、分页（§71） -->

## Database
<!-- 表 / 集合设计，第三范式优先（§66），事务边界（§67），ID 策略（§68） -->

## Authentication
<!-- Cookie Session / JWT / OIDC（§41-§44） -->

## Error Handling
<!-- 统一错误格式（§70）；业务错误不暴露 DB exception -->

## Async Processing
<!-- 仅在明确需求时（§74）；HTTP→Job→Queue→Worker→DB -->

## Failure Handling
<!-- 重试 / 幂等 / 降级 / Redis failure 行为（§73） -->
