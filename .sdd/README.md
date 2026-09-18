# .sdd — Spec-Driven Development Rule Library

本目录是 Agent 在 SDD 模式下进行项目框架选择与技术选型的**可解释决策系统**。
它不是"把 Python+FastAPI+PostgreSQL 当最佳实践硬塞给 Agent"，而是一套让 Agent 依据项目上下文选择技术、并把选择固化进 `decision.json` / `technology-selection.md` / `spec.md` 的规则库（定位与 `知识库 §1` 的「文档目标」一致）。

当前规则库版本：**v1.5**（版本号唯一来源：`.sdd/VERSION`，由 `scripts/validate_rules.py` 核对与根 `README.md` / `CHANGELOG.md` 三处一致。）

## 设计原则（res.md §120 FINAL PRINCIPLE / 知识库 §2,§2.1）
技术、架构、Framework、SDD 都不是目的；目标是 Correctness / Maintainability / Simplicity / Testability / Observability / Security / Evolvability。
无明确需求 → 最简单、成熟、可维护、易验证的方案；复杂需求 → 满足需求并**记录必要性**。

**v1.3 的三条执行语义修正**（`mod_gpt.md`）：
1. **Spec 前置** —— 先 Draft Spec（WHAT/WHY），再架构/技术决策（`mod_gpt.md §1`）。
2. **确认收窄** —— 只有 `REQUIRE_CONFIRMATION` 阻塞；`AUTO`/`RECOMMEND` 自行决定并记录（`mod_gpt.md §2`）。
3. **默认值 = 候选先验** —— `DEFAULT does not mean SELECTED`（`mod_gpt.md §7`）。

**v1.4 的四条工程一致性修正**（`modv2.md`）：
1. **归属唯一化** —— 新增 `CANONICAL.md`：同一语义只有一个权威定义，入口文件只引用不重定义（`modv2.md §22`）。
2. **验证补全** —— `templates/verification.md`（8 节）+ `verification.schema.json`（`modv2.md §4`）。
3. **决策契约补全** —— `evidence` / `constraints` / `alternatives` / `scores` / `review_triggers` / `deferred` / `decision_history` 进入 Schema（`modv2.md §6,§15-§18`）。
4. **追溯四态** —— `MAPPED → IMPLEMENTED → VERIFIED`，区分"被提到"与"被实现"与"被机器验证"（`modv2.md §14`）。

> **注意**：`modv2.md` 的 P0 清单中，关于 `decision-protocol` / `new-project` / `LAYOUT` / `validate_rules`
> 的"仍是旧语义"判断，经逐条核实**属于旧快照误判**（该文档复核时读到的版本早于 v1.3 提交）。
> 完整核实结论见 `REVIEW-2026-09-19.md` 的四审章节。

## 目录结构

```
.sdd/
├── README.md                 # 本文件
├── VERSION                   # ⭐ 规则库版本号唯一来源
├── LAYOUT.md                 # ⭐ 目录约定唯一权威（来源约定的取舍 + design/ADR 按需判据）
├── CONVENTIONS.md            # ⭐ 引用编号与命名约定（避免 §N 歧义；含两级 Schema 校验的区分）
├── CANONICAL.md              # ⭐ 规则归属矩阵（同一语义只有一个权威定义）
├── TRACEABILITY.md           # ⭐ 5 份来源 → 落点四态索引（脚本生成，勿手改）
├── traceability.json         # 同上，机器可读版
├── schema/                   # 机器可读契约（JSON Schema draft 2020-12）
│   ├── decision.schema.json      # 由 scripts/mini_schema.py 对 decision.json 做**真校验**
│   └── verification.schema.json  # 同上，对 verification.json 做真校验
├── knowledge/                 # 技术知识库（"选什么、何时选"的参考）—— 20 个
│   ├── architecture.md        # 项目类型矩阵 / Monolith·Modular·Microservices / 复杂度预算 / 进阶模式
│   ├── backend.md             # 语言矩阵(Python/Go/TS/Java/Rust) / 框架 / ORM / Worker
│   ├── frontend.md            # Vue/React/Next.js/Angular / Tailwind / UI 库 / 状态 / API Client
│   ├── database.md            # PG/MySQL/SQLite/Redis / 向量 / 对象存储
│   ├── caching.md             # Redis 引入条件 / Cache 策略 / Search 决策线
│   ├── messaging.md           # MQ(Rabbit/Kafka/Redis) / 后台任务
│   ├── api.md                 # REST/GraphQL/gRPC / OpenAPI / Contract
│   ├── security.md            # 认证矩阵(No Auth/Session/JWT/OIDC) / 授权 / API 安全
│   ├── testing.md             # 测试金字塔 / 按项目类型的 Test Strategy Matrix
│   ├── deployment.md          # Docker / K8s 决策规则 / CI-CD / 备份
│   ├── observability.md       # 日志 / 指标 / 追踪
│   ├── ai-llm.md              # AI/LLM/RAG/Agent：provider / prompt / token 成本 / eval / fallback
│   ├── data.md                # 数据工程：调度 / dbt / 批流 / 特征存储 / 数据质量 / 回填
│   ├── versioning.md          # ⭐ 版本选择策略**唯一实现**（不写死版本号；存量为 Hard Constraint）
│   ├── multi-tenancy.md       # 多租户：隔离四档（Matrix §22）/ RLS / 租户级迁移备份
│   ├── reliability.md         # SLA·SLO·SLI / RPO·RTO / Retry·幂等·熔断 / 降级限流
│   ├── data-lifecycle.md      # 数据分级 / 留存删除 / 加密审计 / 数据驻留
│   ├── integration.md         # 外部系统接入契约（超时/重试/幂等/回调验签）
│   ├── configuration.md       # 配置三分类 / 密钥管理 / feature flag / fail fast
│   └── dependency-management.md # 依赖引入七问（res.md §90）/ 升级移除 / SCA
├── decision-trees/            # 决策树（"什么情况选什么"的判断逻辑）—— 8 个
│   ├── decision-protocol.md   # ⭐ 元治理：约束模型(P0A/P0B/P1-P3)/评分标尺/复杂度预算/决策状态/21步循环/30条规则
│   ├── impact-analysis.md     # ⭐ 影响面分析（new-feature 前置；Brownfield 风险来源）
│   ├── architecture.md
│   ├── backend.md             # 语言与框架的**候选先验**（不是断言结论）
│   ├── frontend.md
│   ├── database.md
│   ├── ai-llm.md              # AI/LLM/RAG 决策线
│   └── infrastructure.md      # Auth/MQ/Search/API/Deploy/Observability
├── templates/                 # 文档模板 —— 8 个
│   ├── project-discovery.md
│   ├── technology-selection.md  # 人读版（Decision Contract 镜像 + Evidence + Deferred + Review Triggers）
│   ├── spec.md                  # 14 节（含 Status: Draft→Accepted 与 res.md §117 映射表）
│   ├── design.md                # **按需**；只写 plan 装不下的细节
│   ├── plan.md                  # 16 节技术架构模板
│   ├── tasks.md
│   ├── verification.md          # **必填**；8 节验证报告（modv2.md §4）
│   └── adr.md                   # **按需**；含 Evidence / Review Triggers / Reversibility
├── workflows/                 # 流程 —— 5 个
│   ├── new-project.md          # Spec 前置的 canonical order + 收窄后的确认门槛 + 21 步决策循环
│   ├── new-feature.md          # 含 Impact Analysis 前置
│   ├── small-change.md         # 轻量改动档（文件/行数阈值 + **Behavioral Risk Check**）
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
- `CLAUDE.md`：Agent **读取路由** —— 只回答"什么时候读什么"（Step 0–8）；**只路由，不定义语义**。
- `AGENTS.md`：**通用工程规则 + 语义路由表 + DEFINITION OF DONE**；**不定义决策语义、不复制默认选型**。
- `sources/v1.0/`：源文档归档，**只读，Agent 决策时不读取**。
- `specs/`：项目实例目录（如 `specs/001-project/`，含 `decision.json` 与 `verification.md`）。

## 使用方式
1. **先看约定**：目录约定见 `.sdd/LAYOUT.md`，引用编号与命名见 `.sdd/CONVENTIONS.md`，
   "哪份文件说了算"见 `.sdd/CANONICAL.md`（引用的 `§` 必须带来源前缀：`res.md` / `Matrix` / `知识库` / `mod_gpt.md` / `modv2.md` / `<文件名>`）。
2. 新项目：`CLAUDE.md` §2 → Discovery → **Draft Spec** → 读 decision-protocol + knowledge + decision-trees
   → 填 template 到 `specs/<id>-<name>/` → 写 `decision.json` → 写 `verification.md`。
3. **决策语义不在入口文件里**：约束优先级、决策状态、评分、复杂度预算、确认门槛的唯一权威是
   `.sdd/decision-trees/decision-protocol.md`；默认选型（候选先验）的唯一权威是 `.sdd/decision-trees/`。
   入口文件（`CLAUDE.md` / `AGENTS.md`）只给指针（`.sdd/CANONICAL.md` 硬规则 1）。
4. 存量项目改动：先跑 `.sdd/decision-trees/impact-analysis.md`，再进 new-feature / bugfix / refactor。
5. 小改动：走 `.sdd/workflows/small-change.md`，不跑全流程；但**Behavioral Risk Check 失败即升级**。
6. 更新技术栈：仅改 `knowledge/` 与 `decision-trees/`；`CLAUDE.md`/`AGENTS.md` 基本不动。
   版本变化一律改 `knowledge/versioning.md` 的**策略**，不写死版本号。版本变更记入 `CHANGELOG.md`
   并同步 `.sdd/VERSION`。

## 校验
```bash
python3 scripts/gen_traceability.py   # 重建 5 份来源 → 落点的四态索引 + traceability.json（改引用后必跑）
python3 scripts/validate_rules.py     # 引用完整性 / 真 Schema 校验 / Cost 语义 / 版本一致性 / Canonical 不变量
```
收尾标准（0 错误 0 警告 + 同步矩阵）见 `AGENTS.md` 的 **DEFINITION OF DONE**。

## 来源
- `sources/v1.0/res.md`（AGENT PROJECT ENGINEERING & SPEC-DRIVEN DEVELOPMENT RULES v1.0，120 条）
- `sources/v1.0/AI Architecture Decision Matrix.md`（约束模型 / 正式决策矩阵 / 复杂度预算 / 决策状态 / 30 条规则）
- `sources/v1.0/AI Coding SDD 项目技术架构与框架选择知识库.md`（中文知识库 / 模板 / 默认技术栈 / 与 Spec Kit 衔接）
- `sources/v1.0/mod_gpt.md`（v1.3 可执行性评审：Spec 前置 / 确认收窄 / 约束分级 / design 按需 / 真 Schema 校验 / 评分标尺 / 默认值语义 / 版本策略 / DoD）
- `sources/v1.0/modv2.md`（v1.4 复核评审 22 项：归属矩阵 / 四态追溯 / Evidence / Review Triggers / Deferred / Impact Analysis / Behavioral Risk；其中 P0 清单经核实多为旧快照误判）
