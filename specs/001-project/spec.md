# Spec — 001-project（示例实例）

> 按 `.sdd/templates/spec.md` 填写。Spec 是 Source of Truth（res.md §91），描述 WHAT/WHY。

## 1. Overview
### Problem
<待填写：当前订单管理痛点>
### Goal
<待填写：达成什么>
### Non-Goals
<待填写>
### Users
<引用 project-discovery.md §2>

## 2. Context
### Existing System
<Greenfield / 或现有系统>
### Business Context
<订单流转业务背景>
### Constraints
<硬约束：合规/部署/已有栈等>

## 3. User Stories
### US-001
As a 运营人员 / I want 创建并跟踪订单 / So that 掌握履约状态

## 4. Functional Requirements
### FR-001
The system SHALL 创建订单并持久化。
#### Scenario
- GIVEN 合法下单请求 WHEN 提交 THEN 订单创建成功并返回订单号

## 5. Non-Functional Requirements
### Performance
<如 p95 < 200ms>
### Security / Availability / Scalability / Observability
<引用 project-discovery.md §5>

## 6. Data Requirements
### Entities
orders / order_items / users
### Relationships / Constraints
<待填写>

## 7. API Requirements
### Endpoint
POST /api/v1/orders
### Request / Response / Error
<按 api.md 统一错误格式>

## 8. Integration Requirements
### External Services / Authentication / Retry / Timeout
<待填写>

## 9. Architecture Constraints
- Must use PostgreSQL（技术选型结论）
- Must not introduce Microservices without justification

## 10. Acceptance Criteria
- [ ] AC-001 Given 合法下单 When 提交 Then 订单创建成功
- [ ] AC-002 Given 无效商品 When 提交 Then 返回校验错误

## 11. Assumptions
<如单区域部署>

## 12. Open Questions
<待确认：是否需要多租户>

## 13. Out of Scope
<如报表分析 v2>

## 14. Traceability
| Requirement | Design | Task | Test |
| --- | --- | --- | --- |
| FR-001 | D-001 | T-001 | TEST-001 |
| FR-002 | D-002 | T-002 | TEST-002 |
