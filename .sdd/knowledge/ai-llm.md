# Knowledge: AI / LLM / RAG / Agent（AI 应用）

> 来源：Matrix §29（AI Application Matrix）、§30（LLM Provider Architecture）、§31（RAG Matrix）；知识库 §4.3（Data / AI Application）、§60（AI / RAG SaaS）。
> 决策树：`.sdd/decision-trees/ai-llm.md`　治理：`.sdd/decision-trees/decision-protocol.md`
> **标注说明**：未标注「本仓补充」的条目直接来自上述来源；「本仓补充」表示源文档未覆盖、由本仓增补。

---

## 0. 触发条件

```
IF llm = true OR rag = true OR agent = true
THEN 读取本文件，并把 §1 的 10 项检查结果写入 technology-selection.md
```

## 1. AI Application Matrix（Matrix §29）

只要 `llm = true`，**自动检查**以下 10 项，逐项在 `technology-selection.md` 中给出结论：

| # | 检查项 | 必须回答 |
| --- | --- | --- |
| 1 | model_provider | 用哪个供应商 / 哪个模型 |
| 2 | prompt_management | prompt 存在哪、如何版本化 |
| 3 | token_cost | 成本上限与计量方式 |
| 4 | retry | 失败重试策略（次数、退避） |
| 5 | timeout | LLM 调用超时（必须显式设置） |
| 6 | streaming | 是否流式返回 |
| 7 | structured_output | 是否需要结构化输出（JSON schema / tool call） |
| 8 | evaluation | 如何评估输出质量 |
| 9 | fallback | 主供应商不可用时的降级路径 |
| 10 | observability | 调用可观测（trace / token / latency） |

## 2. LLM Provider Architecture（Matrix §30）

```
IF 只有一个模型供应商
THEN direct SDK = acceptable

IF multiple_providers OR provider_switching_expected OR model_evaluation_required
THEN LLM Provider Abstraction
```

**不要**为了"未来支持多个模型"提前建立过度复杂的 abstraction（Matrix §30 明确警告）。这与 `architecture.md` §4「不为未来假设需求增加复杂度」一致。

## 3. RAG Matrix（Matrix §31）

```
IF document_knowledge = true AND semantic_search = true
THEN RAG = true
```

进一步：

```
relational_data AND vector_scale = moderate       → PostgreSQL + pgvector（默认）
vector_scale = large OR vector_workload = dominant → Dedicated Vector DB
```

向量库细则见 `database.md` §6。计分见 `decision-protocol §5.1`：**pgvector 作为 PostgreSQL 扩展不额外计分；独立向量库 +2**。

## 4. AI / RAG SaaS 默认栈（知识库 §60）

```
Frontend        Next.js + TypeScript
Backend         Python + FastAPI
Database        PostgreSQL
Vector          pgvector
Cache           Redis
Object Storage  S3
LLM             Provider abstraction
Observability   OpenTelemetry
Testing         pytest + Playwright
Deployment      Docker
```

> 这是**默认值，不是强制值**。任一项被 Hard Constraint 覆盖时按 `decision-protocol §3` 处理。
> **Cache 需注意**：本清单列出 Redis，但仍须通过 `caching.md` §1 的条件检查（Matrix §23）——无读密集/低变更/命中收益时不应仅因本清单而引入 Redis。

## 5. Agent 工程（本仓补充，源文档未覆盖）

三份源文档未给出 Agent（多轮工具调用）的工程规则，以下为本仓增补，属"AI 应用必查"：

- **工具调用**：每个 tool 必须有输入 schema 与超时；**禁止无上限循环**，必须设 `max_steps`。
- **幂等**：写操作类 tool 必须幂等，或携带幂等键。
- **成本上限**：单次请求 token 上限 + 每会话累计上限；超限即中止（对应本文件 §1 的 `token_cost`）。
- **Prompt 版本化**：prompt 视为代码，纳入版本控制；语义变更走 `.sdd/workflows/new-feature.md`。
- **可观测**：记录每次调用的 provider / model / prompt_version / tokens / latency / 工具轨迹。
- **评估（eval）**：至少一组固定 case 作为回归集；prompt 或模型变更必须跑 eval 后才可上线。
- **数据边界**：发送给外部模型的用户数据范围必须明确（涉及合规 → `REQUIRE_CONFIRMATION`）。

## 6. 不得自行决定（知识库 §71 + Matrix §44 规则 20）

以下决策**不得静默做出**，一律 `REQUIRE_CONFIRMATION`：

- 引入/更换 LLM 供应商
- 数据出境 / 数据驻留（data residency）
- 把用户数据用于模型训练
- 自建推理集群（涉及 GPU 与运维成本）

## 7. 复杂度预算

```
LLM 供应商 API（外部托管）        → 不计分
自建推理服务（需独立部署）        → +1
独立向量库                        → +2
pgvector（PostgreSQL 扩展）       → 0
```

计分口径见 `decision-protocol §5.1`。
