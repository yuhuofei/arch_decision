# Decision Tree: AI / LLM（AI 应用决策线）

> 配套知识：`.sdd/knowledge/ai-llm.md`、`database.md` §6、`caching.md`
> 治理：`.sdd/decision-trees/decision-protocol.md`
> 本文件只做判断，知识与理由见配套知识文件。

---

## Step 0：触发

```
IF llm = true OR rag = true OR agent = true
THEN 走本决策线（并与 architecture / backend / frontend / database 决策线并联执行）
```

## Step 1：供应商架构（Matrix §30）

```
IF 单供应商
THEN direct SDK                       # AUTO
IF 多供应商 OR 需切换 OR 需模型评估
THEN LLM Provider Abstraction         # RECOMMEND
```

> 不要为"未来多模型"预设复杂抽象。

## Step 2：成本与可靠性（Matrix §29）

必须输出：`model_provider` / `token_cost` / `timeout` / `retry` / `fallback`。

```
无成本上限设计                         → BLOCKED（信息不足，先澄清）
数据出境 / 数据驻留 / 用于训练          → REQUIRE_CONFIRMATION
无 timeout 设置                        → BLOCKED（LLM 调用必须显式设超时）
```

## Step 3：RAG 与向量（Matrix §31）

```
IF document_knowledge = true AND semantic_search = true
THEN RAG = true

relational_data AND vector_scale = moderate → PostgreSQL + pgvector          # AUTO
vector_scale = large OR workload = dominant → 专用向量库 Qdrant/Weaviate/Milvus  # RECOMMEND（+2）
```

## Step 4：调用形态（Matrix §29）

```
需流式交互 → streaming = true
需程序消费 → structured_output = true（JSON schema / tool call）
两者都要   → 同时定义，并**各自**定义失败行为（流中断 / 解析失败）
```

## Step 5：评估与观测（Matrix §29）

```
无 evaluation 方案 → 不得进入实现阶段
```

观测必须包含：provider / model / prompt_version / tokens / latency / 工具轨迹（见 `ai-llm.md` §5）。

## Step 6：Agent 工程（本仓补充，见 `ai-llm.md` §5）

```
IF 多轮工具调用
THEN 必须定义 max_steps / tool timeout / 幂等键 / 每会话成本上限
```

## Step 7：合规复查

```
IF 涉及用户数据外发
THEN 标记 REQUIRE_CONFIRMATION，并在 technology-selection.md 记录数据边界
```

## 输出

- 写入 `technology-selection.md` 的 AI 段（含 `decision-protocol §6` 的 Decision Status）
- 写入 `plan.md` 的 §2 Technology Stack 与 §10 Security
- 只有 `REQUIRE_CONFIRMATION` 项先 `Architecture Proposal → Human Confirmation` 再固化（`decision-protocol §9`）；
  其余按 `AUTO`/`RECOMMEND` 直接执行并记录，不阻塞
- ADR **按需**（`.sdd/templates/adr.md`）：只记录重要 Architecture Decision，不为凑目录制造 ADR
