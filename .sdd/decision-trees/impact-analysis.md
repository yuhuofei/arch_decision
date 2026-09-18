# Decision Tree: Impact Analysis（影响面分析）

> 来源：`res.md §101`（Change Management）、`res.md §102-§103`（Brownfield Project / Technology Rule）、
> `res.md §115`（Technology Introduction Checklist）、`Matrix §34-§35`（Existing Project Decision Matrix / Existing Stack Conflict）；
> `modv2.md §20`（本决策树为结构缺口补齐）。
> 定位：**`new-feature.md` 的前置步骤**，也可在 `bugfix.md` / `refactor.md` 前使用。
> 解决的问题：现有 workflow 只回答"我要做什么"，**没有回答"这个改动会影响什么"**——
> Brownfield 项目里后者才是风险来源。
> 治理：`.sdd/decision-trees/decision-protocol.md`

---

## 1. 触发条件

```
IF 任一成立 THEN 先做本分析，再进 new-feature / bugfix / refactor：
  - 改动落在存量系统（Brownfield）
  - 改动可能触及 API / DB schema / 认证授权 / 部署
  - 不确定影响范围
```

**纯新增、零耦合的新项目不需要本步骤**（无既有面可影响）。

## 2. 检查清单（逐项给出结论，不留空）

| 面 | 要回答 | 输出 |
| --- | --- | --- |
| 受影响模块 | 哪些模块/包/服务的代码会改 | 列表 |
| 受影响 API | 契约是否变化？是否 breaking？ | `none` / `modified` / `breaking` |
| 受影响 DB 表 | 是否改 schema / 加索引 / 回填 | `none` / `migration required` |
| 受影响外部集成 | 对方契约、回调、对账是否受影响 | 列表 |
| 受影响认证/授权 | 角色、权限判定、会话行为是否变 | `none` / `changed` |
| 受影响测试 | 哪些既有测试会失败或需改 | 列表 |
| 受影响部署 | 是否需要新配置、新环境变量、新资源 | 列表 |
| 受影响可观测 | 指标/日志/告警是否需同步调整 | 列表 |
| 迁移需求 | 数据迁移、双写、兼容窗口 | `none` / `required` |
| 向后兼容 | 旧客户端/旧数据是否仍可用 | `yes` / `no` |

> `受影响的测试` 与 `受影响的可观测` 最常被漏，而它们决定"改完能不能被发现出问题"。

## 3. 标准输出格式

```yaml
impact:
  architecture: none        # none / affected / breaking
  database:     none        # none / affected / migration required
  api:          none        # none / affected / breaking
  security:     none        # none / affected / breaking
  deployment:   none
  observability: none
  migration:    none        # none / required
  backward_compatibility: yes
  affected_modules: []
  affected_tests: []
  decision_status: AUTO     # 见 decision-protocol.md §6；breaking 类默认 REQUIRE_CONFIRMATION
```

该块写入 `spec.md`（增量特性）或 `plan.md`；`decision_status` 为非 `AUTO` 时按协议处理。

## 4. 判定规则（与决策协议衔接）

```
IF api = breaking OR database = migration required OR security = breaking
THEN decision_status = REQUIRE_CONFIRMATION（decision-protocol.md §6.4）
     不得静默实施（res.md §101 变更管理）

IF 影响面跨越 ≥2 个模块 AND 无法在单个 task 内闭环
THEN 拆分为多个 task，并在 tasks.md 标注依赖顺序

IF 影响面无法确定（不知道谁会受影响）
THEN 标 BLOCKED，按 decision-protocol.md §6.2 提最小必要问题集
     禁止"先改了再看"
```

## 5. 与 Brownfield 约束的关系

存量项目的既有技术栈优先复用（`res.md §103`、`decision-protocol.md` §3.1 的 P0B）。
**影响分析的作用之一就是暴露"改动会迫使迁移"**——此时应回到 `Matrix §35`（Existing Stack Conflict）
判断是真必要迁移，还是可以缩小改动范围避免迁移。

```
优先选择：影响面更小的实现
只有当"影响面小"与"需求正确性"冲突时，才选大影响面方案并记录理由
```

## 6. 与验证的衔接

`verification.md` 的 Consistency Check 节中的 `No undocumented architecture changes`
即对应本分析：**实际改动超出本表声明的范围 = 未登记的架构变更**，必须补登并重新评估。
