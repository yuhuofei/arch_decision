# Knowledge: Multi-Tenancy（多租户）

> 来源：`Matrix §22`（Multi-Tenant Matrix，四档隔离策略与默认值）、`知识库 §21`（PostgreSQL 多租户）、
> `Matrix §5`（Architecture Decision Matrix 的 organization/isolation 判据）、`res.md §67`（关键状态与事务）。
> `modv2.md §19` 列为缺失决策维度（此前散落在 `database.md` / `architecture.md`）。
> **重要说明**：`Matrix §22` 提供策略表，但**租户隔离的授权、迁移、备份、配置等运营细节源文档未覆盖**——
> 这些条目标注「本仓补充」。治理：`.sdd/decision-trees/decision-protocol.md`　相邻：`knowledge/database.md`、`knowledge/security.md`

---

## 1. 触发条件（`Matrix §22`）

```
IF users belong to organizations AND data isolation required
THEN multi_tenant = true → 读取本文件
```

**单一用户群体、无组织概念的项目不引入租户抽象** —— 无用抽象会污染每张表与每个查询。

## 2. 隔离策略四档（`Matrix §22`，唯一口径）

| 需求 | 策略 | 隔离强度 | 复杂度 | 成本 |
| --- | --- | --- | ---: | --- |
| Small/medium SaaS | **Shared DB + `tenant_id`**（默认） | 逻辑隔离 | +0 | 最低 |
| Strong isolation | Separate schema | 中 | +0 | 中 |
| Regulatory isolation | Separate database | 高 | +1 | 高 |
| Extreme isolation | Separate infrastructure | 最高 | +3 | 最高 |

```
DEFAULT = Shared DB + tenant_id      # 除非存在明确隔离要求
```

> 与 `decision-protocol.md` §3.4 一致：**默认是多租户策略的候选先验，不是结论**。
> 存在合规 / 数据驻留要求时直接跳到高隔离档，且属 `REQUIRE_CONFIRMATION`（`decision-protocol.md` §6.4）。

**分档判据（本仓补充）**：出现下列任一即不得停留在默认档 ——
监管/合同要求物理隔离、租户可自行指定数据存储地、单租户数据量级差异极大（大客户独占实例更划算）。

## 3. `Shared DB + tenant_id` 的强制纪律（本仓补充）

默认档**只有在纪律被强制执行时才安全**，否则是数据泄漏的温床：

```
1. 每张业务表必须含非空 tenant_id（无默认值）
2. 所有查询必须带 tenant_id 过滤 —— 由 ORM 全局作用域 / RLS 强制，不靠人记得写
3. 唯一约束必须含 tenant_id（否则跨租户撞键）
4. 禁止用自增 id 作为对外标识（会泄漏租户规模并便于枚举）
5. 迁移脚本必须在多租户数据上演练
```

> **PostgreSQL 优先用 RLS（Row Level Security）兜底**（`知识库 §21`）：把"忘记加 WHERE"从
> 潜在泄漏降级为显式报错。RLS 是扩展内能力，**不计复杂度预算**。

## 4. 授权边界（本仓补充）

多租户 = **两层授权**，缺一层即越权：

```
第一层：租户边界（用户属于哪个 tenant？）
第二层：租户内角色（RBAC/ABAC，见 knowledge/security.md）
```

跨租户访问（如管理员看所有租户）**必须显式建模**，不能靠"角色够高就放行"——
它是 `REQUIRE_CONFIRMATION` 级别的授权模型变更（`decision-protocol.md` §6.4）。

## 5. 迁移 / 备份 / 配置（本仓补充）

```
迁移
  Shared DB / Separate schema → 单次迁移影响全部租户，必须可回滚窗口内完成
  Separate database / infra   → 需多轮分批迁移 + 版本兼容期（双写或兼容读写）

备份 / 恢复
  Shared DB            → 恢复 = 全部租户一起回滚，必须事先告知影响面
  Separate db / infra   → 可按租户粒度恢复（这是高隔离档的主要收益）

租户级配置
  租户可变配置（品牌/限额/开关）走数据表或 feature flag，不走环境变量
  环境变量只能承载"进程级"配置（见 knowledge/configuration.md）
```

## 6. 复杂度与成本口径

- **默认档（Shared DB + tenant_id）不加组件，计 0 分** —— 多租户不因"是 SaaS"而自动增加复杂度。
- Separate database 档若导致"每租户一个实例"，按新增的基础设施组件计（`decision-protocol.md` §5.1）。
- Extreme isolation 档常等于 Multi-region / 多云，属 `REQUIRE_CONFIRMATION`。

## 7. 与验证的衔接

`verification.md` 的 Security 节必须包含**跨租户越权测试**（用 A 租户身份访问 B 租户资源应失败）。
只测"登录成功"不构成多租户验证。
