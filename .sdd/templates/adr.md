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
<!-- CAN ASSUME / RECOMMEND 的假设以 technology-selection.md + decision.json 为准（decision-protocol §6.3）；
     此处只写与本决策直接相关的假设，不必复制全部 -->
- <假设 1>

### Evidence
<!-- modv2.md §15：决策依据必须可指向来源，不得只写"因为更好" -->
- type: <requirement / constraint / team / documentation>
  claim: <依据内容>
  source: <spec.md#FR-00X / 官方文档 URL / 团队现状>
  verified_at: <YYYY-MM-DD 或 —>

### Review Triggers
<!-- modv2.md §16：AUTO 不是永久结论；写明什么条件出现时重评 -->
- <条件>

### Consequences
<!-- 采用后的影响与依赖；Reversibility：Low/Medium/High -->

---

## 索引
- adr-001-<topic>.md — <一句话>
- adr-002-<topic>.md — <一句话>
