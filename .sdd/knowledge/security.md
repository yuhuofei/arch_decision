# Knowledge: Security（安全与认证）

> 来源：res.md §41-§46,§87；Matrix §20,§21,§42；知识库 §33-§36,§71
> 决策树：`.sdd/decision-trees/infrastructure.md`（认证矩阵）

## 1. Authentication Matrix（Matrix §20，含 No Auth）

### No Auth（仅当）
```
IF public_readonly = true AND user_identity_not_required = true THEN 无认证
```

### Session（Cookie + Server-side）（res.md §42）
```
IF traditional_web_application AND browser_only THEN Session-based auth
```
适用传统 Web / 后台 / 同域系统。

### JWT / Token（res.md §43）
```
IF multiple_clients OR stateless_api OR mobile_client THEN JWT/token-based
```
必须考虑 expiration/refresh/revocation/key rotation/token storage/CSRF·XSS。不要因"JWT 流行"默认 JWT。

### OAuth / OIDC（res.md §44）
```
IF enterprise_sso OR social_login OR external_identity_provider THEN OAuth/OIDC
```
第三方登录优先 OIDC；企业可能 SAML+OIDC；Keycloak/Auth0/云 IAM。

**禁止**自研：密码加密 / OAuth Server / JWT 算法 / session crypto（知识库 §33）。

## 2. Authorization Matrix（Matrix §21）
```
admin/user 两级 → RBAC
权限与 resource/organization/tenant/ownership/attribute 相关 → RBAC + resource-level authorization
仅复杂策略 → ABAC / Policy Engine
```
默认 RBAC（res.md §46）；复杂系统 ABAC。不要把 `if user.is_admin` 散落业务代码，用 RBAC + Policy（知识库 §34）。

## 3. API Security Baseline（res.md §45 / 知识库 §35）
所有 API 默认考虑：Authentication / Authorization / Input Validation / Rate Limit / CORS / CSRF / SQL Injection / XSS / SSRF / File Upload Security / Secrets / Audit Log。**Agent 不允许自行降低安全级别。**

## 4. Secret Management（res.md §87）
生产优先 Cloud Secret Manager / Vault / CI-CD secret store。禁止 `password=plaintext`、`secret="hard-coded-secret"`、密钥提交 Git。

## 5. Agent 不得自行改变（知识库 §71）
未授权不得自行改变 Authentication / Architecture / Database / Deployment Platform / Cloud Provider / Public API / Language。
