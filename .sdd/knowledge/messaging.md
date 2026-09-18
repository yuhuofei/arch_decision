# Knowledge: Messaging（消息队列与后台任务）

> 来源：res.md §34-§37,§74；Matrix §16,§33；知识库 §4.5,§29,§34
> 决策树：`.sdd/decision-trees/infrastructure.md`

## 1. 是否需要 MQ（Matrix §16）
```
IF request_response = sufficient AND background_work = low THEN MQ = false
```
仅当 Async processing / Retry / Event-driven / Decoupling / High throughput / Background jobs 才引入。

## 2. RabbitMQ（res.md §35 / Matrix §16）
```
IF task_queue OR business_event OR routing = important THEN RabbitMQ
```
适合任务队列/业务事件/Job/中等规模/传统企业集成。

## 3. Kafka（res.md §36 / Matrix §16）
```
IF event_streaming AND (high_event_volume OR event_replay OR multiple_consumers OR stream_processing)
THEN Kafka
```
适合高吞吐事件流/日志/数据管道/Event Streaming。不要为"异步"自动用 Kafka。

## 4. Redis Queue（Matrix §16，新增）
```
IF queue_complexity = low AND Redis_already_required THEN Redis-based queue
```
适合中小型异步任务/简单 Job/已用 Redis 的系统。

## 5. Background Jobs / Worker（res.md §37 / 知识库 §4.5）
- Python：Celery / RQ / Arq + Redis / RabbitMQ。
- Go：Asynq / 自建 Worker + Redis。
- FastAPI BackgroundTasks ≠ 分布式可靠队列；需 Retry/Persistence/分布式/Scheduling 用真正 task queue。

## 6. Async Architecture（res.md §74）
只有明确需求才用 async：`HTTP → Create Job → Queue → Worker → DB`。不要所有业务都异步化。

## 7. Event-Driven（知识库 §66）
仅业务天然存在 Domain Event 时采用 Domain Event + Message Broker；否则不为"先进"引入 Event Bus。
