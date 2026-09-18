# Knowledge: Observability（可观测性）

> 来源：res.md §47-§49；Matrix §26；知识库 §37,§38
> 生产系统默认 Logs + Metrics + Tracing（知识库 §38）。

## 1. Logging（res.md §48 / 知识库 §37）
默认 JSON structured。必须含：timestamp / level / service / request_id / trace_id / user_id(if allowed) / message / error。
**禁止**记录：password / token / secret / 完整银行卡号 / 敏感 PII。

## 2. Metrics（Matrix §26 / 知识库 §38，新增）
```
IF production_service = true THEN metrics = true
```
建议监控：Request Count / Latency / Error Rate / CPU / Memory / DB Connections / Queue Depth / Cache Hit Rate。

## 3. Tracing（res.md §49 / Matrix §26）
```
IF multiple_services OR distributed_requests OR latency_debugging = important THEN distributed tracing = true
```
中大型项目默认 OpenTelemetry 统一 Logs/Metrics/Traces，能关联 HTTP→Service→DB→Redis→MQ。
