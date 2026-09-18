# Changelog

本文件记录 `.sdd/` 规则库的版本变更。约定见 `.sdd/CONVENTIONS.md` §5。

---

## [v1.1] — 2026-09-19

### 修复（P0 — 消除自相矛盾，避免 Agent 误判）

1. **目录约定统一**
   - 新增 `.sdd/LAYOUT.md`：声明唯一采纳的约定（`.sdd/` + `specs/<id>-<name>/`），
     并为源文档中另外 3 套约定（`res.md §92`/`§93` 的 `docs/`、`Matrix §45` 的 `ai-architecture-kb/`、`知识库 §78` 的部分产物）给出 **superseded 映射表**。
   - 清除 `.sdd/templates/spec.md` 中残留的 `docs/architecture.md` 等引用。

2. **spec 节数统一**
   - 明确以 `知识库 §79` 的 **14 节**为准（`res.md §117` 为 23 项）。
   - 在 `.sdd/templates/spec.md` 补 `res.md §117（23 项） → 14 节 / plan.md` **全量映射表**，并显式记录取舍理由（spec = WHAT/WHY，plan = HOW）。
   - 修正两处过期引用：`.sdd/workflows/new-feature.md`「不必全量 23 项」、`specs/001-project/verification.md`「spec.md §23」（实为 §10）。

3. **复杂度预算计分口径统一**
   - `.sdd/decision-trees/decision-protocol.md` 新增 **§5.1 计分表**（唯一口径）：明确计入项、不计入项（Docker / 框架 / ORM / gRPC / 部署平台）、以及 **pgvector 作为 PostgreSQL 扩展不额外计分**。
   - 新增 §5.2 预算对照、§5.3 计分示例。
   - 统一此前口径不一致的算式：`.sdd/examples/saas.md`（原计入 Docker）、`high-concurrency.md`（原不计）、`ai-saas.md`（原 pgvector 计 2）；同步 `knowledge/architecture.md`、`decision-trees/architecture.md`、`templates/technology-selection.md`、`specs/001-project/technology-selection.md`、`CLAUDE.md`、`AGENTS.md`。

4. **引用编号统一（消除 `§N` 歧义）**
   - 新增 `.sdd/CONVENTIONS.md`：禁止裸写 `§N`，必须带来源前缀（`res.md` / `Matrix` / `知识库` / `<文件名>`）。
   - 新增 `scripts/migrate_refs.py`，迁移 **124 处**引用（28 个文件）。
   - 语义核查后修正 **3 处来源错配**：`new-project.md` 的 `Matrix §34` 与 `知识库 §59-§62`、`knowledge/ai-llm.md` 的 `Matrix §44 规则 20`（这些编号在 res.md 与其它来源中同时存在，机器无法自动判定）。
   - 统一来源标签写法 `AI Architecture Decision Matrix §N` → `Matrix §N`。
   - 校验结果：全仓裸 `§N` 残留 **0** 处。

### 新增（P1 — 补内容缺口）

- **`knowledge/ai-llm.md`** + **`decision-trees/ai-llm.md`**：AI / LLM / RAG / Agent 决策线。
  此前 `Matrix §29`（AI Application Matrix 10 项必查）、`§30`（LLM Provider Architecture）、`§31`（RAG Matrix）**完全未落地**，仅被 `examples/ai-saas.md` 一句话带过。
- **`knowledge/data.md`**：数据工程决策线（编排调度 / 转换层 / 批 vs 流 / 存储分层 / 特征存储 / 幂等回填 / 数据质量 / 测试策略）。
  此前项目类型已含 "Data Application / ETL"，但无对应知识文件。源文档对该领域覆盖薄，文件中已逐条标注「本仓补充」。
- **`knowledge/caching.md`**：缓存与搜索决策线。此前 `Matrix §23`（Caching Matrix）、`§17`（Search Engine Matrix）未落地，仓库仅 4 行 + 2 行残片。
- **`specs/001-project/plan.md`** 与 **`specs/001-project/adr/`**（`ADR-001-postgres.md`、`ADR-002-fastapi.md`、`ADR-003-session-auth.md`）：
  补齐此前缺失的实例产物（原 ADR 索引指向不存在的文件）。
- **`.sdd/TRACEABILITY.md`**：`res.md` 120 条 → 落点文件的反向索引（脚本生成）。
- **`README.md`**（根）：仓库总览（人 + 非 Claude 的 Agent 入口）。
- **`.gitignore`**、**`CHANGELOG.md`**（本文件）。
- **`sources/v1.0/`**：源文档归档为只读，并声明"Agent 决策时不读取"。

### 新增（P2 — 工程化增强）

- **`.sdd/schema/decision.schema.json`** + **`scripts/validate_rules.py`**：机器可校验（引用完整性 + Decision Schema 必填项 + 复杂度预算）。
- **技术选型评分补 `Cost` 维度**（原 5 维共 100 分 → 6 维共 100 分，适配小预算/个人项目）。
- **`decision-protocol.md` 补 BLOCKED 澄清问题模板**（与 QUESTION POLICY MUST/SHOULD/CAN ASK 对应）。
- **`decision-protocol.md` 补文件间冲突仲裁顺序**。
- **`workflows/small-change.md`**：轻量改动档（跳过全流程的显式阈值）。

### 变更

- `.workbuddy/` 移出版本控制（改为本地个人状态；磁盘文件保留）。
- `.sdd/README.md` 目录树同步更新。

---

## [v1.0] — 2026-09-18

- 由 `res.md`（120 条）生成初版规则库：`CLAUDE.md` / `AGENTS.md` / `.sdd/{knowledge,decision-trees,templates,workflows}` / `specs/001-project/`。
- 按 `Matrix` 与 `知识库` 增强治理能力：新增 `decision-trees/decision-protocol.md`（约束模型 / 评分 / 复杂度预算 / 决策状态 / 确认门槛 / 15 步决策循环 / 30 条规则）；
  扩充 knowledge 至 10 个文件、decision-trees 至 5 个；`spec` 改 14 节、`plan` 改 16 节；新增 `.sdd/examples/` 5 个已决策示例。
