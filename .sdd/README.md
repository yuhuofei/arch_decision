# .sdd — Spec-Driven Development Rule Library

本目录是 Agent 在 SDD 模式下进行项目框架选择与技术选型的**可解释决策系统**。
它不是"把 Python+FastAPI+PostgreSQL 当最佳实践硬塞给 Agent"，而是一套让 Agent 依据项目上下文选择技术、并把选择固化进 `decision.json` / `technology-selection.md` / `spec.md` 的规则库（定位与 `知识库 §1` 的「文档目标」一致）。

## 设计原则（res.md §120 FINAL PRINCIPLE / 知识库 §2,§2.1）
技术、架构、Framework、SDD 都不是目的；目标是 Correctness / Maintainability / Simplicity / Testability / Observability / Security / Evolvability。
无明确需求 → 最简单、成熟、可维护、易验证的方案；复杂需求 → 满足需求并**记录必要性**。

**v1.3 的三条执行语义修正**（`mod_gpt.md`）：
1. **Spec 前置** —— 先 Draft Spec（WHAT/WHY），再架构/技术决策（`mod_gpt.md §1`）。
2. **确认收窄** —— 只有 `REQUIRE_CONFIRMATION` 阻塞；`AUTO`/`RECOMMEND` 自行决定并记录（`mod_gpt.md §2`）。
3. **默认值 = 候选先验** —— `DEFAULT does not mean SELECTED`（`mod_gpt.md §7`）。

## 目录结构

```
.sdd/
├── README.md                 # 本文件
├── LAYOUT.md                 # ⭐ 目录约定唯一权威（4 套来源约定的取舍 + design/ADR 按需判据）
├── CONVENTIONS.md            # ⭐ 引用编号与命名约定（避免 §N 歧义；含两级 Schema 校验的区分）
├── TRACEABILITY.md           # ⭐ 4 份来源 → 落点文件反向索引（脚本生成，勿手改；见 知识库 §86）
├── schema/                   # 机器可读契约（JSON Schema draft 2020-12）
│   └── decision.schema.json  # 由 scripts/mini_schema.py 对 decision.json 做**真校验**
├── knowledge/                 # 技术知识库（"选什么、何时选"的参考）—— 14 个
│   ├── architecture.md        # 项目类型矩阵 / Monolith·Modular·Microservices / 复杂度预算 / 多租户 / 进阶模式
│   ├── backend.md             # 语言矩阵(Python/Go/TS/Java/Rust) / 框架 / ORM / Worker
│   ├── frontend.md            # Vue/React/Next.js/Angular / Tailwind / UI 库 / 状态 / API Client
│   ├── database.md            # PG/MySQL/SQLite/Redis / 向量 / 对象存储 / 多租户
│   ├── caching.md             # Redis 引入条件 / Cache 策略 / Search 决策线
│   ├── messaging.md           # MQ(Rabbit/Kafka/Redis) / 后台任务
│   ├── api.md                 # REST/GraphQL/gRPC / OpenAPI / Contract
│   ├── security.md            # 认证矩阵(No Auth/Session/JWT/OIDC) / 授权 / API 安全
│   ├── testing.md             # 测试金字塔 / 按项目类型的 Test Strategy Matrix
│   ├── deployment.md          # Docker / K8s 决策规则 / CI-CD / 备份
│   ├── observability.md       # 日志 / 指标 / 追踪
│   ├── ai-llm.md              # AI/LLM/RAG/Agent：provider / prompt / token 成本 / eval / fallback
│   ├── data.md                # 数据工程：调度 / dbt / 批流 / 特征存储 / 数据质量 / 回填
│   └── versioning.md          # ⭐ 版本选择策略**唯一实现**（不写死版本号；存量为 Hard Constraint）
├── decision-trees/            # 决策树（"什么情况选什么"的判断逻辑）—— 7 个
│   ├── decision-protocol.md   # ⭐ 元治理：约束模型(P0A/P0B/P1-P3)/评分标尺/复杂度预算/决策状态/确认门槛/默认值语义/决策循环/30条规则
│   ├── architecture.md
│   ├── backend.md             # 语言与框架的**候选先验**（不是断言结论）
│   ├── frontend.md
│   ├── database.md
│   ├── ai-llm.md              # AI/LLM/RAG 决策线
│   └── infrastructure.md      # Auth/MQ/Search/API/Deploy/Observability
├── templates/                 # 文档模板 —— 7 个
│   ├── project-discovery.md
│   ├── technology-selection.md  # 人读版（Decision Contract 的 YAML 镜像 + 决策状态 + 复杂度预算 + Versions）
│   ├── spec.md                  # 14 节（含 Status: Draft→Accepted 与 res.md §117 映射表）
│   ├── design.md                # **按需**；只写 plan 装不下的细节
│   ├── plan.md                  # 16 节技术架构模板
│   ├── tasks.md
│   └── adr.md                   # **按需**；含 Status / Confidence / Decision Status
├── workflows/                 # 流程 —— 5 个
│   ├── new-project.md          # Spec 前置的 canonical order + 收窄后的确认门槛 + 15 步决策循环
│   ├── new-feature.md
│   ├── small-change.md         # 轻量改动档（跳过全流程的显式阈值）
│   ├── bugfix.md
│   └── refactor.md
└── examples/                 # 已决策示例（来自 Matrix / 知识库）—— 5 个
    ├── saas.md
    ├── ai-saas.md
    ├── internal-tool.md
    ├── high-concurrency.md
    └── brownfield.md
```

## 上层文件
- `README.md`：仓库总览（人 + 非 Claude 的 Agent 入口）。
- `CLAUDE.md`：Agent 总入口，只负责"什么时候读取什么"（含 Spec 前置流程）。
- `AGENTS.md`：通用 Agent 工程规则摘要（读取顺序、默认矩阵、最重要的规则、**DEFINITION OF DONE**）。
- `sources/v1.0/`：源文档归档，**只读，Agent 决策时不读取**。
- `specs/`：项目实例目录（如 `specs/001-project/`，含 `decision.json`）。

## 使用方式
1. **先看约定**：目录约定见 `.sdd/LAYOUT.md`，引用编号与命名见 `.sdd/CONVENTIONS.md`（引用的 `§` 必须带来源前缀：`res.md` / `Matrix` / `知识库` / `mod_gpt.md` / `<文件名>`）。
2. 新项目：`CLAUDE.md` §2 → Discovery → **Draft Spec** → 读 decision-protocol + knowledge + decision-trees → 填 template 到 `specs/<id>-<name>/` → 写 `decision.json`。
3. **人工确认门槛（已收窄）**：只有标 `REQUIRE_CONFIRMATION` 的决策（Microservices / K8s / DB migration / Auth architecture 等）需 `Architecture Proposal → Human Confirmation`；
   其余（语言、框架、ORM、测试工具、缓存是否引入）属 `AUTO`/`RECOMMEND`，**自行决定并记录，不阻塞**。
4. 小改动：走 `.sdd/workflows/small-change.md`，不跑全流程。
5. 更新技术栈：仅改 `knowledge/` 与 `decision-trees/`；`CLAUDE.md`/`AGENTS.md` 基本不动。
   版本变化一律改 `knowledge/versioning.md` 的**策略**，不写死版本号。版本变更记入 `CHANGELOG.md`。

## 校验
```bash
python3 scripts/gen_traceability.py   # 重建 4 份来源 → 落点的反向索引（改引用后必跑）
python3 scripts/validate_rules.py     # 引用完整性 + decision.json 真 Schema 校验 + 复杂度预算
```
收尾标准（0 错误 0 警告 + 同步矩阵）见 `AGENTS.md` 的 **DEFINITION OF DONE**。

## 来源
- `sources/v1.0/res.md`（AGENT PROJECT ENGINEERING & SPEC-DRIVEN DEVELOPMENT RULES v1.0，120 条）
- `sources/v1.0/AI Architecture Decision Matrix.md`（约束模型 / 正式决策矩阵 / 复杂度预算 / 决策状态 / 30 条规则）
- `sources/v1.0/AI Coding SDD 项目技术架构与框架选择知识库.md`（中文知识库 / 模板 / 默认技术栈 / 与 Spec Kit 衔接）
- `sources/v1.0/mod_gpt.md`（v1.3 可执行性评审：Spec 前置 / 确认收窄 / 约束分级 / design 按需 / 真 Schema 校验 / 评分标尺 / 默认值语义 / 版本策略 / DoD）
