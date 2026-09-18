# Knowledge: Reliability（可靠性 / 容错）

> 来源：`res.md §65`（BACKUP / RPO / RTO）、`res.md §2.5`（Non-functional Requirements）、
> `res.md §72`（RATE LIMITING）、`Matrix §26`（Observability Matrix，可靠性信号来源）；
> `知识库 §8`（Async Processing，含 idempotency）。`modv2.md §19` 列为缺失决策维度。
> **重要说明**：源文档对"可靠性"覆盖**很薄**（仅备份/RPO/RTO、限流、可观测三块）。
> 本文件中**只有标注来源的条目来自源文档，其余标注「本仓补充」**。
> 治理：`.sdd/decision-trees/decision-protocol.md`　相邻：`knowledge/observability.md`、`knowledge/deployment.md`

---

## 1. 触发条件

```
IF 任一成立 THEN 读取本文件：
  - 有可用性要求（用户能感知的服务中断）
  - 涉及支付 / 订单 / 关键状态写入
  - 有数据丢失容忍度要求（RPO / RTO）
  - 出现外部依赖调用（第三方 API / MQ / 对象存储）
  - 出现重试 / 并发 / 幂等相关问题
```

## 2. 指标先定义，再谈设计（本仓补充）

**没有指标就无法验证可靠性**，也就无法写 `verification.md` 的 NFR 节。开工前必须明确四个数：

```
SLA  = 对用户的承诺（对外）       例如 99.9%/月
SLO  = 内部目标（略严于 SLA）      例如 99.95%/月
SLI  = 实际测量的指标              例如 成功请求数 / 总请求数
错误预算 = 1 - SLO                 例如 0.05%/月 ≈ 21 分钟
```

> **禁止**写"高可用""尽量不丢数据"这类无法验证的表述（`res.md §2.5` 要求 NFR 可量化）。
> 未定的写 `UNKNOWN`，并在 `spec.md` §12 Open Questions 登记（`.sdd/CONVENTIONS.md` §4）。

## 3. 数据可靠性：RPO / RTO（`res.md §65`）

```
RPO（Recovery Point Objective）= 能容忍丢多少数据（时间维度）
RTO（Recovery Time Objective） = 能容忍停多久
```

| RPO / RTO 档 | 需要的机制 | 复杂度 / 成本 |
| --- | --- | --- |
| 小时级 | 每日全量备份 + 手工恢复 | 低 |
| 分钟级 | 主从复制 + 自动 failover | 中（+1 组件） |
| 秒级 / 接近 0 | 同步复制 / 多区域 | 高（Multi-region 属 `REQUIRE_CONFIRMATION`，`decision-protocol.md` §6.4） |

**必须先定要求，再选机制** —— 反过来会为了"看起来可靠"引入永久运维负担。
RPO/RTO 记入 `decision.json` 的 `risks` / `assumptions`，实现后用恢复演练验证。

## 4. 故障处理模式的引入门槛（本仓补充）

三条都被"缺了会真出事"驱动，**不是默认全上**：

```
Retry
  IF 调用外部依赖 AND 失败是瞬时的（网络抖动 / 5xx / 限流）
  THEN 指数退避 + 抖动（jitter）；必须设上限与总超时
  禁止：无上限重试（会放大故障）

Idempotency（知识库 §8）
  IF 有重试 OR 有消息重复投递 OR 支付/下单类写操作
  THEN 必须幂等键（idempotency key）或唯一约束
  否则重试 = 重复扣款 / 重复订单

Circuit Breaker
  IF 依赖某个下游 AND 其故障会拖垮本服务（线程/连接池耗尽）
  THEN 引入熔断 + 降级返回
  IF 下游非关键（如统计上报）
  THEN 直接异步化或忽略，不引入熔断器
```

> 熔断器**不计入**复杂度预算（进程内库，非独立组件，`decision-protocol.md` §5.1）。

## 5. 降级与限流（`res.md §72`）

```
Graceful degradation（本仓补充）
  明确"哪些功能可以先坏"：核心链路（下单/支付）> 次要功能（推荐/统计）
  降级必须是显式设计好的分支，不是 try/except 吞掉异常

Rate limiting（res.md §72）
  IF 对外暴露 API AND 存在滥用 / 爬取 / 成本放大风险 THEN 必做
  实现优先顺序：网关/反代层 → 应用中间件 → 存储层计数（Redis，+1）
```

## 6. 复杂度与成本口径

- **只有"独立故障域"才计复杂度**：多区域（+3 级）、独立副本集群按 `decision-protocol.md` §5.1 口径计。
- Retry / 幂等 / 熔断 / 超时**都是代码内模式，一律不计分**。
- 可靠性设计会拉高**持续成本**（多副本 / 跨区域流量）：按 `decision-protocol.md` §4.2 做 Cost 复核，
  不得静默选择更贵的高可用方案。

## 7. 与验证的衔接

`verification.md` §5 的 Availability / Reliability 节必须对着本节 §2 的 SLO 与实际测量值填写；
**未做恢复演练 / 未测故障注入的，如实写 `NOT VERIFIED`**，不得凭设计意图判 PASS。
