# Knowledge: Dependency Management（第三方依赖治理）

> 来源：`res.md §90`（DEPENDENCY DECISION，七问）、`res.md §45`（SECURITY，含许可证与安全历史）、
> `knowledge/versioning.md`（版本策略）。`modv2.md §19` 列为缺失决策维度。
> **与 versioning.md 的分工**：`versioning.md` 管**"选哪个版本"**（LTS / supported / EOL），
> 本文件管**"要不要引入这个依赖"**。两者都要过，不得互相替代。
> 治理：`.sdd/decision-trees/decision-protocol.md`　相邻：`knowledge/versioning.md`、`knowledge/security.md`

---

## 1. 触发条件

```
IF 任一成立 THEN 读取本文件：
  - 准备新增第三方依赖（库 / SDK / 框架 / 工具）
  - 准备升级 major 版本
  - 准备移除或替换依赖
```

## 2. 引入前的强制七问（`res.md §90`）

**逐条回答，答不出即不引入**。这是本文件的核心，任何新增依赖都必须过：

```
1. 是否真的需要？                 （能否用现有能力满足）
2. 标准库能否解决？               （语言自带的优先）
3. 现有依赖能否解决？             （避免功能重叠的多个库）
4. 项目是否长期维护？             （最近提交 / 发版 / issue 响应）
5. License 是否允许？             （与项目分发方式兼容）
6. Security history 如何？        （历史 CVE / 维护者响应速度）
7. Agent / 团队是否容易正确使用？  （生态文档与示例质量）
```

> 七问的答案记入 `decision.json` 的 `rejected`（未采纳的候选）或 `assumptions`（已采纳的依据），
> 不只留在对话里。**依赖决策是"重大技术决策"的一种，同样需要有据可查。**

## 3. 引入后的成本（本仓补充）

```
新增依赖的真实代价：
  - 供应链攻击面（每个传递依赖都算）
  - 升级义务（跟随上游 breaking change）
  - 体积 / 启动时间（前端 bundle、容器镜像层）
  - 许可合规审计成本
```

**因此默认倾向是"少引入"**：能自己写 50 行且可维护的，不引入一个需要持续跟随的库；
但**不要重造标准库已经提供的东西**。

## 4. 版本升级的判定（本仓补充）

| 场景 | 处置 |
| --- | --- |
| patch / minor（无 breaking） | 常规升级，走 CI |
| major（含 breaking） | 按 `new-feature.md`，属**重大技术迁移** → 默认 `REQUIRE_CONFIRMATION`（`decision-protocol.md` §6.4） |
| 安全修复（CVE） | **P0A**，可越过"暂时不想动"的 P0B 约束（`decision-protocol.md` §2） |
| EOL 运行时 | **P0A**，必须迁移（`knowledge/versioning.md`） |

## 5. 移除与替换（本仓补充）

```
IF 依赖满足任一 THEN 计划移除：
  - 已 EOL / 无维护
  - 存在未修复高危 CVE
  - 功能重叠（两个库做同一件事）
  - 实际只用了它的一个函数
移除同样要走七问的逆过程：确认没有隐藏依赖与运行时行为耦合。
```

## 6. 复杂度与成本口径

- **依赖不计复杂度预算**（进程内代码，非独立组件，`decision-protocol.md` §5.1）。
- 但依赖会放大**供应链风险**，属 `risks` 字段必须记录的一类。
- 商业授权的依赖若产生费用，按 `decision-protocol.md` §4.2 做 Cost 复核。

## 7. 与验证的衔接

`verification.md` 的 Security 节必须包含**依赖漏洞扫描**结果（SCA），
并列出**与已知 CVE 对应的处置**（升级 / 缓解 / 接受并登记风险）。
"扫了没看"不构成验证。
