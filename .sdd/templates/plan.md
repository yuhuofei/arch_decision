# Template: Plan（实施计划）

> 用途：Implementation Plan，衔接 Design 与 Tasks（res.md §99, §100）。
> 实现前必须读取：Project Rules / Technology Selection / Relevant Spec / Design / Tasks（§100）。

# Implementation Plan: <feature-name>

## Pre-Implementation Checklist（§100）
- [ ] 已读 Project Rules（CLAUDE.md / AGENTS.md）
- [ ] 已读 Technology Selection
- [ ] 已读 Relevant Spec
- [ ] 已读 Design
- [ ] 已读 Tasks

## Phase 1 — Foundation
- 仓库结构 / 依赖 / CI 基础 / 配置（§86）

## Phase 2 — Core Domain
- 领域模型 / ORM / Migration（§64）

## Phase 3 — API & Integration
- 端点 / 认证 / 错误格式 / 外部集成

## Phase 4 — Cross-cutting
- 日志 / 观测 / 安全 / 缓存 / 队列

## Phase 5 — Verification
- Unit / Integration / E2E（§50-§53）

## Change Management（§101）
发现 Spec 错误 → 更新 Spec → Design → Tasks → 继续实现，不直接绕过。
