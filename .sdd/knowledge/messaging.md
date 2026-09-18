# Knowledge: Messaging（消息队列与后台任务）

> 来源：res.md §34-§37, §74
> 决策树：`.sdd/decision-trees/infrastructure.md`

## 1. Message Queue（§34, DEFAULT: NONE）

默认**无消息队列**。仅当存在以下需求才引入：Async processing / Retry / Event-driven / Decoupling / High throughput / Background jobs。

## 2. RabbitMQ（§35）

选：Task queue / Business events / Job processing / Moderate scale / 传统企业集成。
不选：Event streaming platform / 海量 replay 需求。

## 3. Kafka（§36）

选：Event streaming / High throughput / Event replay / Data pipeline / 多 consumer / Event-driven 架构。
不选：简单后台任务 / 简单邮件队列 / 小 CRUD 应用。

默认：`Simple Queue → RabbitMQ`；`Event Streaming → Kafka`。

## 4. Background Jobs（§37）

- Python：Celery，或轻量场景 FastAPI BackgroundTasks。
- **注意**：BackgroundTasks ≠ 分布式可靠队列。若需 Retry / Persistence / Distributed workers / Scheduling → 用真正的 task queue。

## 5. Async Architecture（§74）

只有明确需求才用 async。典型：`HTTP Request → Create Job → Queue → Worker → Database`。**不要把所有业务都异步化**。
