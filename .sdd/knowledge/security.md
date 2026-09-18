# Knowledge: Security（安全与认证）

> 来源：res.md §41-§46, §87

## 1. Authentication（§41, 默认优先成熟方案）

**禁止**：自己设计密码加密 / 自己设计 OAuth / 自己设计 JWT 算法 / 自己实现密码 hash / 自己实现 session crypto。

## 2. Session（§42）

传统 Web：Cookie + Server-side Session。

## 3. JWT（§43）

适用：API / Mobile / 分布式认证 / 无状态服务。必须考虑：expiration / refresh / revocation / key rotation / token storage / CSRF·XSS。
**不要因为"JWT 流行"而默认 JWT。**

## 4. OIDC / OAuth（§44）

第三方登录（Google / Microsoft / GitHub / Enterprise SSO）优先 OIDC。企业可能需 SAML + OIDC。

## 5. Security Baseline（§45）

默认：HTTPS / Secrets 在源码外 / 成熟库做密码 hash / Input validation / Output encoding / CSRF 防护（适用处）/ Rate limiting / Authorization 检查 / Audit logging（按需）。
**禁止**：`password = plaintext`；`secret = "hard-coded-secret"`。

## 6. Authorization（§46）

不要把 Authentication 与 Authorization 混为一谈。默认 RBAC；复杂系统考虑 ABAC / Policy-based。

## 7. Secret Management（§87）

生产环境不要依赖 `.env` 长期存 secrets。优先：Cloud Secret Manager / Vault / CI-CD secret store。
