# Knowledge: Data（数据工程 / 管道）

> 来源：知识库 §4.3（Data / AI Application）、§4.4（CLI / Automation）、§4.5（Worker / Background Job）；Matrix §28（Test Strategy Matrix 的 Data Pipeline 行）；`knowledge/architecture.md` §1（项目类型矩阵）。
> **重要说明**：三份源文档对"数据工程"覆盖很薄（仅项目类型归属、语言倾向、Worker 框架、测试策略四块）。
> 因此本文件中**只有明确标注来源的条目来自源文档，其余均标注「本仓补充」**——属于本仓增补的领域规则，不是源文档内容。
> 治理：`.sdd/decision-trees/decision-protocol.md`　AI 侧决策线：`.sdd/decision-trees/ai-llm.md`

---

## 1. 触发条件

```
IF project_type = Data Application / ETL / Data Pipeline / Recommendation / Analytics
THEN 读取本文件
```

## 2. 项目类型与默认形态（知识库 §4.3）

典型：Data Pipeline / Recommendation / Analytics。

```
Frontend → API / Job Service → { DB, Redis, Vector Store } → Object Storage
```

无前端的数据项目：可直接 `CLI / Job → 对象存储 / 数仓`（知识库 §4.4 的 CLI 形态）。

## 3. 语言与运行时（知识库 §4.3 / §4.4）

- 数据处理 / ETL / AI → **Python**
- 系统工具 / 网络工具 / DevOps / 高性能 CLI → **Go**
- **本仓补充**：能用 SQL 表达的数据变换不要写成 Python 循环；变换逻辑与调度解耦。

## 4. 编排与调度（本仓补充，源文档未覆盖 —— 最高优先级缺口）

```
IF 任务数 > 1 AND 存在依赖关系
THEN 需要编排器（不要用 cron + 脚本串联）
```

| 场景 | 选择 |
| --- | --- |
| 单机少量任务、无依赖 | cron / systemd timer |
| DAG 依赖 + 回填 + 重试 + 可视化 | Airflow（最成熟）/ Dagster（资产化）/ Prefect（轻量 Python） |
| 已用 Python、任务量小 | Celery Beat（见 `messaging.md` §5） |
| 云原生托管 | 云厂商 DAG 服务 |

**判据**：需要**回填（backfill）**与**依赖可视化**时才引入编排器；否则 cron 足够。
引入编排器 → 复杂度 **+1**（见 `decision-protocol §5.1`），须在 ADR 记录存在理由。

## 5. 转换层（本仓补充）

```
IF 转换逻辑超过少量 SQL
THEN 需要建模层：dbt（SQL 优先、可测试、有 lineage）或等价 Python 框架
```

禁止把业务变换散落在调度脚本里；变换逻辑必须可单元测试。

## 6. 批 vs 流（本仓补充）

```
IF latency_requirement = batch 可接受
THEN 批处理（默认）

IF 需要秒级/持续处理 AND (replay OR multiple_consumers)
THEN 流处理（Kafka + Flink / Spark Structured Streaming）
```

流处理是**重组件**（Kafka +2，见 `decision-protocol §5.1`），必须由明确的延迟指标驱动，不得因"未来可能实时"引入。

## 7. 存储分层（本仓补充）

| 层 | 用途 | 选择 |
| --- | --- | --- |
| Raw / Landing | 原样落地，不加工 | 对象存储（见 `database.md` §7） |
| Staging / ODS | 清洗、去重、标准化 | 数仓表 |
| Mart / 特征 | 面向消费 | 数仓表 + 特征存储 |

- 列式格式（Parquet）优先于 CSV。
- 分区字段必须与查询模式一致。
- 不要用 OLTP 库承担大规模分析负载（OLTP / OLAP 分离）。

## 8. 特征存储（本仓补充）

```
IF 训练与推理共用同一批特征 AND 存在训练-推理偏斜（training-serving skew）风险
THEN 需要特征存储或统一特征计算层
ELSE 直接落表（不要过早引入特征平台）
```

用户侧参考：C2C 推荐样本 / 特征工程类项目属此档。

## 9. 幂等 / 回填 / 数据质量（本仓补充）

- **幂等**：每个任务必须可重复执行且结果一致（按分区**覆盖写**，而非追加）。
- **回填**：必须能指定日期区间重跑；禁止"只能跑今天"的设计。
- **数据质量**：主键唯一性、空值率、行数波动（对比近 7 天）、枚举域；异常应**失败**而不是静默通过。
- **血缘**：任务输入输出必须可追踪。
- 涉及 Money / Inventory / Permission / 关键状态时，事务与一致性要求同 `database.md` §10。

## 10. 测试（Matrix §28）

Data Pipeline 行：**Unit High / Integration High / E2E Low**。

- Unit：变换函数（给定输入 → 期望输出）
- Integration：真实数据库 / 文件系统（Testcontainers 或临时 schema）
- E2E：只覆盖一条端到端关键链路，不追求覆盖面

## 11. 观测（见 `observability.md`）

必查指标：任务成功率 / 执行时长 / 重试次数 / **数据新鲜度（freshness）** / 行数波动 / 队列深度。
