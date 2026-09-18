# Knowledge: Versioning（版本选择策略）

> 来源：res.md §88（VERSION STRATEGY）,§89（VERSION PINNING）,§64；mod_gpt.md §8（生命周期化改写，本仓采纳）
> 决策树：无独立决策树 —— 版本不是"选哪个技术"，而是"该技术的哪个版本"，由本文件唯一规定。
> **被引用方**：`knowledge/backend.md`、`knowledge/frontend.md`、`knowledge/database.md`、`knowledge/deployment.md`
> 都只引用本文件，**不各自维护版本策略**（否则又会漂移）。
> 治理：`.sdd/decision-trees/decision-protocol.md`

---

## 1. 原则

**版本选择是生命周期决策，不是流行度决策。**

```
不因为"最新"而选最新。
不因为"稳定"而永远不动。
```

版本与其他技术属性受同一套约束模型管辖（`decision-protocol §2`）：

| 情形 | 等级 | 处理 |
| --- | --- | --- |
| 存量项目已锁定版本，且仍在支持期 | **Hard Constraint（P0B）** | 不得擅自升级（`decision-protocol §3.1`） |
| 存量项目版本已 EOL / 有安全漏洞 | **P0A** | 必须升级，且"保持不动"不是可选项 |
| 新项目版本 | 通常 `AUTO` | 按本文件 §3 判定，记录进 `decision.json` 的 `versions` |
| 版本升级属"重大技术迁移" | `REQUIRE_CONFIRMATION` | 见 `decision-protocol §6` |

> 版本策略**不写死具体版本号**。任何"Python = 3.13 所以永远用 3.13"的写法都会很快过期，
> 且会让 Agent 忽略"已在支持期"这一唯一有意义的判据。

---

## 2. 存量项目（Brownfield）

**保持现有 major/minor 版本**，除非满足以下任一（满足才允许升级）：

```
- 安全支持已终止（security support ended）
- 上游社区支持已终止（EOL）
- 所需依赖与之不兼容
- 用户显式要求升级
- 有文档化需求必须升级
```

与 `CLAUDE.md` §4 / `knowledge/backend.md` §6 一致：**未经授权不得擅自升级**。
反过来说，"EOL 就是不升级"同样不可接受 —— 它属 P0A（安全/可行），高于用户的"我不想动"（P0B）。

---

## 3. 新项目（Greenfield）

**默认优先级（从上到下）**：

```
1. Supported stable release      # 仍在支持期的稳定版
2. Active ecosystem support      # 生态活跃（有在维护的库/插件）
3. Dependency compatibility      # 与项目其他依赖兼容
4. Deployment/runtime support    # 目标部署平台/运行时支持
5. Team/toolchain compatibility  # 团队与工具链能覆盖
6. Latest release                # 最新发布 —— 优先级最低
```

具体倾向：

| 类别 | 取值 |
| --- | --- |
| 语言运行时 | 当前被广泛支持的 stable 或 LTS |
| Java | supported LTS |
| Node.js | **Active LTS**（非 Current） |
| 数据库 | 目标平台上可用的 supported stable major |
| 框架 | 最新 stable major，且生态支持已成熟 |

**默认避免**：

```
alpha / beta / RC
刚发布且依赖兼容性未解决的 major 版本
EOL 版本
目标部署平台上不可用的版本
```

> 与 `res.md §88` 一致：框架"用当前稳定版本，但避免刚发布的 major version"。

---

## 4. 核实与记录（强制）

新项目的版本号 **MUST** 在有网络访问时对着上游官方文档核实（`res.md §88` 的意图）。
**禁止编造精确版本号**；未核实时写 `UNKNOWN`（见 `.sdd/CONVENTIONS.md` §3）。

记录进 `specs/<id>/decision.json` 的 `versions` 数组（Schema 见 `.sdd/schema/decision.schema.json`）：

```json
"versions": [
  { "technology": "Python",     "selected": "x.y", "support_status": "supported",
    "verified_at": "<YYYY-MM-DD>", "reason": "..." },
  { "technology": "PostgreSQL", "selected": "x",   "support_status": "supported",
    "verified_at": "<YYYY-MM-DD>", "reason": "..." }
]
```

`support_status` 取值：`supported` / `LTS` / `maintenance` / `EOL` / `UNKNOWN`。
`versions` 为**按需**：无法核实就显式记 `UNKNOWN` 并写清理由，**不要省略整项**。

---

## 5. 锁定（Locking，res.md §89）

```
Application dependencies：
  - 精确 lock 文件（Python: uv.lock / Node: pnpm-lock.yaml / Go: go.mod+go.sum / Java: gradle.lockfile）
  - 可复现安装（reproducible install）

Runtime：
  - pin major/minor
  - patch 更新按项目更新策略执行

Container images：
  - 禁止 `latest`
  - 必须 pin 运行时版本
```

> 与 `knowledge/deployment.md`（`res.md §60-§65` 的镜像规则）一致：本文件规定"钉什么"，
> `deployment.md` 规定"怎么构建"。

---

## 6. 与本仓其他文件的关系

| 文件 | 关系 |
| --- | --- |
| `knowledge/backend.md` | 语言/框架选型；版本指向本文件 |
| `knowledge/frontend.md` | 前端框架选型；版本指向本文件 |
| `knowledge/database.md` | 数据库选型；版本指向本文件 |
| `knowledge/deployment.md` | 镜像与 CI；锁定规则指向本文件 §5 |
| `decision-protocol §6` | 版本升级若属"重大技术迁移"则 `REQUIRE_CONFIRMATION` |
