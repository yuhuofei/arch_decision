# Template: ADR（Architecture Decision Record）

> 用途：固化每一个重要技术决策（res.md §95；Matrix §1,§18；知识库 §73）。
> 文件名建议 `ADR-NNN-<topic>.md`；放 `specs/<id>/adr/`。
> **按需**：没有重要 Architecture Decision 就不建，不要为了满足目录规范制造 ADR（`.sdd/LAYOUT.md` §1.2）。

## Decision: <技术/方案名>

### Status
<!-- Accepted / Rejected / Superseded / Proposed -->

### Decision Status（decision-protocol §6）
<!-- AUTO / RECOMMEND / REQUIRE_CONFIRMATION / BLOCKED -->

### Confidence
<!-- overall 0-5；及各项依据 -->

### Decision
<!-- 一句话结论，如：Use PostgreSQL as primary database. -->

### Context
<!-- 为什么做这个决定；系统/项目背景约束 -->

### Constraints
<!-- Hard / Soft Constraint（P0A / P0B / P1-P3，见 CONVENTIONS.md §3） -->

### Alternatives
- <备选 A>
- <备选 B>

### Why <Selected>
- <优势 1>
- <优势 2>

### Why Not Alternatives
- <备选 A>: <理由>
- <备选 B>: <理由>

### Risks
- <风险 1>（含缓解）

### Assumptions
- <假设 1（CAN ASSUME 须记录）>

### Consequences
<!-- 采用后的影响与依赖；Reversibility：Low/Medium/High -->

---

## 索引
- adr-001-<topic>.md — <一句话>
- adr-002-<topic>.md — <一句话>
