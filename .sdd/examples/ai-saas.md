# Example: AI SaaS（AI / RAG 应用）

> 来源：Matrix §38；知识库 §60。

## Input
```yaml
project_type: SaaS
ai: true
rag: true
relational_data: true
vector_scale: moderate
frontend: web
team_size: 5
```

## 决策
```
Architecture → Modular Monolith
Frontend    → Next.js + TypeScript        # React 全栈，适合 AI Web
Backend     → FastAPI                     # Python AI 生态
Database    → PostgreSQL
Vector      → pgvector                    # moderate 规模，不引专用向量库
Cache       → Redis only if cache/session/rate-limit required
Object Storage → S3-compatible
API        → REST
Testing    → pytest + frontend tests + E2E
Observability → structured logging + metrics
```

## 依据
- AI/LLM/RAG → Python + FastAPI（backend.md §1）。
- 关系型 + 中等向量 → PostgreSQL + pgvector（database.md §6；不引 Qdrant/Milvus）。
- LLM Provider：单一供应商用 direct SDK；多供应商/需评估才建 Provider Abstraction（Matrix §30，勿为"未来多模型"过度抽象）。

## 决策状态
- Architecture / Backend / DB / Vector → `AUTO`
- 若引入专用向量库（规模超标）→ `RECOMMEND`
- 若 RAG 涉及数据合规/驻留 → `REQUIRE_CONFIRMATION`

## 复杂度预算（口径见 decision-protocol §5.1）
```
PostgreSQL(1) + pgvector(0，PG 扩展不额外计分) + 对象存储(1) = 2  ≤ Small SaaS 预算 8   ✅
只有"独立部署的专用向量库"才 +2；Redis 未确认时不计分。
```
