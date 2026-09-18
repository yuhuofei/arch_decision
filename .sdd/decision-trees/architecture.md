# Decision Tree: Architecture（架构选型）

> 配套知识：`.sdd/knowledge/architecture.md`

## 起点：选 Modular Monolith 还是 Microservices？

```
是否需要"独立部署"某个模块？
├─ 否 ─┐
│      ├── 是否有不同团队负责不同模块？
│      │     ├─ 否 ─┐
│      │     │      ├── 是否存在不同语言/runtime 需求？
│      │     │      │     ├─ 否 ─┐
│      │     │      │     │      ├── 是否需要独立扩容？
│      │     │      │     │      │     ├─ 否 ─┐
│      │     │      │     │      │     │      ├── 是否有强故障隔离需求？
│      │     │      │     │      │     │      │     ├─ 否 → ✅ Modular Monolith（默认）
│      │     │      │     │      │     │      │     └─ 是 → ⚠️ 评估 Microservices
│      │     │      │     │      │     │      └─ ...
│      │     │      │     │      └─ 是 → ⚠️ 评估 Microservices
│      │     │      │     └─ 是 → ⚠️ 评估 Microservices
│      │     └─ 是 → ⚠️ 评估 Microservices
│      └─ ...
```

## 判定规则

### ✅ 默认选 Modular Monolith（§4.1）
满足以下任一即默认：
- MVP / SaaS / CRUD / Admin / Enterprise App / 中小型系统
- 业务边界尚未稳定
- 小团队（1-3 人）
- 单一业务域

### ⚠️ 仅当满足强条件才选 Microservices（§4.2）
至少满足一个：
- 独立部署
- 独立扩缩容
- 独立 team ownership
- 故障隔离
- 明确 bounded context
- 极高吞吐
- 不同技术栈

### ❌ 绝对不要优先选 Microservices
- MVP / 1-3 人团队 / CRUD / 业务边界不明确 / 无独立部署需求

## 选中后必答（Microservices 场景）

1. 为什么不能 Modular Monolith？
2. 哪些服务必须独立部署 / 扩容？
3. 分布式事务如何处理？
4. observability / service discovery / retry / idempotency 如何处理？

## 前后端是否分离（§21）

- 分离：Web + Mobile / API consumers > 1 / 前端复杂度 medium+
- 不分离：小型内部工具 / 简单 CRUD / 简单 CMS / MVP / server-rendered

## 输出
将结论写入 `specs/<id>/technology-selection.md` 的 Architecture 段，复杂必要性用 ADR 记录（`.sdd/templates/adr.md`）。
