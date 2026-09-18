# Knowledge: Observability（可观测性）

> 来源：res.md §47-§49

## 1. Observability（§47, DEFAULT）

默认：Structured logging / Metrics / Health check / Error tracking。中大型项目用 OpenTelemetry 统一 Logs / Metrics / Traces。

## 2. Logging（§48）

默认 JSON structured logs。至少包含：timestamp / level / service / request_id / trace_id / message / error。
**禁止**记录：Password / Access Token / Refresh Token / API Secret / Sensitive PII。

## 3. Distributed Tracing（§49）

中大型项目默认 OpenTelemetry。必须能关联：HTTP Request → Service → Database → Redis → MQ。
