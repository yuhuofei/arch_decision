# Knowledge: Configuration（配置与密钥）

> 来源：`res.md §86`（CONFIGURATION）、`res.md §87`（SECRET MANAGEMENT）、`知识库 §36`（Configuration：
> Environment Variables + Config Object）、`res.md §45`（SECURITY）、`res.md §41`（AUTHENTICATION，含加密）、
> `res.md §48`（LOGGING，禁止泄露敏感信息）。`modv2.md §19` 列为缺失决策维度。
> **重要说明**：源文档只给了一条 Configuration 条目，本文件多数规则为「本仓补充」——
> 依据是"Agent 经常在这里犯错"（把密钥写进代码、把运行期配置编译进镜像、缺省值静默回退）。
> 治理：`.sdd/decision-trees/decision-protocol.md`　相邻：`knowledge/deployment.md`、`knowledge/security.md`

---

## 1. 触发条件

```
IF 项目包含以下任一 THEN 读取本文件：
  - 多环境部署（dev / staging / prod）
  - 存在密钥 / token / 证书
  - 存在需要运营期调整的开关或阈值
```

## 2. 三类配置必须分开（`知识库 §36` + 本仓补充）

| 类别 | 例子 | 存放 | 可热改 |
| --- | --- | --- | --- |
| 构建期配置 | 编译目标、包名、内嵌版本号 | 代码 / 构建脚本 | ❌ 需重新构建 |
| 运行期配置 | 端口、日志级别、外部服务 URL、阈值 | 环境变量 / ConfigMap / 配置服务 | 部分可 |
| 密钥 | DB 密码、API Key、签名私钥、JWT secret | **密钥管理服务** | 轮换即可 |

> **禁止**：把密钥写进代码、提交进仓库、打进镜像、放进前端产物、写进日志（`res.md §48`）。
> **禁止**：把运行期配置"编译"进镜像 —— 会导致同一个镜像无法跨环境复用，且改一个阈值就要重新发版。

## 3. 配置读取的强制规则（本仓补充）

```
1. 必需配置缺失 → 启动时失败（fail fast），不得用隐式默认值静默继续
   ❌ os.environ.get("DB_URL", "localhost")   # 生产环境连错库还不报错
   ✅ 启动即校验，缺失则退出并说明缺哪个变量

2. 默认值只能是"开发环境的显式默认"，且必须在启动日志里标注"使用了默认值"

3. 配置必须有单一入口（Config 对象 / Settings 类），禁止散落 os.environ 调用
   → 便于审计"这个服务到底依赖哪些配置"

4. 类型与范围校验在启动时做（端口是数字、URL 可解析、超时为正数）
```

## 4. Feature flag（本仓补充）

```
IF 需要灰度发布 / 快速关停某功能 / A/B THEN 引入 feature flag
IF 只是"以后可能要用" THEN 不引入 —— 未清理的 flag 是永久技术债
强制：每个 flag 必须登记"删除条件"（全量后多久清理），否则会永久累积
```

flag 存储优先复用已有组件（数据库 / Redis），**不为此新增组件**。

## 5. 密钥轮换（本仓补充）

```
必须支持在不重启全量服务的前提下轮换（双密钥并存窗口）
IF 无法轮换 THEN 视为已知风险，写入 decision.json 的 risks
```

## 6. 复杂度与成本口径

- 环境变量 / 配置文件 / Settings 类**一律不计分**（代码内机制）。
- 专用密钥管理服务（Vault 等）：属外部托管或新组件，按 `decision-protocol.md` §5.1 判定；
  云厂商托管密钥服务通常视为"平台能力"，不计分。
- 引入配置中心（独立部署）按 `+1` 计，并须过 `Matrix §33` 的基础设施引入检查表。

## 7. 与验证的衔接

`verification.md` 必须确认：**必需配置缺失时服务拒绝启动**（负向测试），
且仓库与镜像中不含明文密钥（secret 扫描）。
