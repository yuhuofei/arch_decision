# ADR-003: Session-based Authentication

> 模板：`.sdd/templates/adr.md`　所属实例：`specs/001-project/`

## Status
Accepted

## Decision Status
`AUTO`
> 注意：`decision-protocol §6` 将 **Authentication architecture 变更**列为 `REQUIRE_CONFIRMATION`。
> 本决策属"初始选型"而非"变更"，且落在 `Matrix §20` 的 Session 明确分支上，故标记 `AUTO`；
> **此后若要改为 JWT / OIDC，必须升为 `REQUIRE_CONFIRMATION`。**

## Confidence
4 / 5 —— 场景判定清晰；扣分项为未来多客户端需求可能推翻。

## Decision
采用 **Session（Cookie + 服务端存储）** 作为认证方案。

## Context
面向运营人员的订单管理后台，同域 Web 应用，仅浏览器客户端，无对外开放 API、无移动端。

## Constraints
| 类型 | 内容 |
| --- | --- |
| P0 Hard | 禁止自研密码加密 / 会话加密 / JWT 算法（`知识库 §33`） |
| P1 Strong | 需要可立即失效的会话（后台系统需要强制下线能力） |
| P2 Preference | 实现与运维简单 |

## Alternatives
- Session（Cookie + Server-side）
- JWT / Token-based
- OAuth / OIDC

## Why Session
- 命中 `Matrix §20` 的 Session 分支：`traditional_web_application AND browser_only`
- 会话可**服务端立即撤销**，满足后台强制下线需求
- 无跨域/多客户端场景，无需为 JWT 承担过期/刷新/吊销/密钥轮换的复杂度
- 不暴露 token 到前端存储，减少 XSS 攻击面

## Why Not Alternatives
- **JWT**：适用于多客户端 / 无状态 API / 移动端（`Matrix §20` JWT 分支）。本例均不满足；`知识库 §33` 明确反对"因 JWT 流行而默认 JWT"
- **OAuth / OIDC**：适用于企业 SSO / 社交登录 / 外部身份提供方（`Matrix §20`）。当前无此需求

## Risks
- 后续若新增移动端或对外 API，Session 方案不再合适 → 缓解：一旦出现多客户端需求，立即走 `REQUIRE_CONFIRMATION` 评审 JWT/OIDC

## Assumptions
- 部署于同一域名下（无跨站 Cookie 问题）
- 后端为有状态部署（会话存储可随应用扩展，必要时接 Redis —— 届时应按 `knowledge/caching.md` §2 计分）

## Consequences
- 需要服务端会话存储；水平扩展时会话需共享（此时才考虑 Redis）
- 认证架构变更 → `REQUIRE_CONFIRMATION`
- **Reversibility：Medium**
