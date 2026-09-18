# .sdd — Spec-Driven Development Rule Library

本目录是 Agent 在 SDD 模式下进行项目框架选择与技术选型的**可解释决策系统**。
它不是"把 Python+FastAPI+PostgreSQL 当最佳实践硬塞给 Agent"，而是一套让 Agent 依据项目上下文选择技术、并把选择固化进 `technology-selection.md` 与 `spec.md` 的规则库。

## 设计原则（对应 FINAL PRINCIPLE，res.md §120）
技术、架构、Framework、SDD 都不是目的；目标是 Correctness / Maintainability / Simplicity / Testability / Observability / Security / Evolvability。
无明确需求 → 最简单、成熟、可维护、易验证的方案；复杂需求 → 满足需求并**记录必要性**。

## 目录结构

```
.sdd/
├── README.md                 # 本文件
├── LAYOUT.md                  # ⭐ 目录约定唯一权威（4 套来源约定的取舍与映射表）
├── CONVENTIONS.md             # ⭐ 引用编号与命名约定（避免 §N 歧义）
├── TRACEABILITY.md            # ⭐ res.md 120 条 → 落点文件的反向索引
├── schema/                    # 机器可校验的 JSON Schema
│   └── decision.schema.json
├── knowledge/                 # 技术知识库（"选什么、何时选"的参考）
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
│   └── data.md                # 数据工程：调度 / dbt / 批流 / 特征存储 / 数据质量 / 回填
├── decision-trees/            # 决策树（"什么情况选什么"的判断逻辑）
│   ├── decision-protocol.md   # ⭐ 元治理：约束模型(P0-P3)/评分/复杂度预算/决策状态/确认门槛/决策循环/30条规则
│   ├── architecture.md
│   ├── backend.md
│   ├── frontend.md
│   ├── database.md
│   ├── ai-llm.md              # AI/LLM/RAG 决策线
│   └── infrastructure.md      # Auth/MQ/Search/API/Deploy/Observability
├── templates/                 # 文档模板
│   ├── project-discovery.md
│   ├── technology-selection.md  # 含 Decision Output Schema(YAML) + 决策状态 + 复杂度预算
│   ├── spec.md                  # 14 节（含 Traceability 与 res.md §117 映射表）
│   ├── design.md
│   ├── plan.md                  # 16 节技术架构模板
│   ├── tasks.md
│   └── adr.md                   # 含 Status / Confidence / Decision Status
├── workflows/                 # 流程
│   ├── new-project.md          # 含 15 步决策循环 + 人工确认门槛
│   ├── new-feature.md
│   ├── small-change.md         # 轻量改动档（跳过全流程的显式阈值）
│   ├── bugfix.md
│   └── refactor.md
└── examples/                 # 已决策示例（来自 Matrix / 知识库）
    ├── saas.md
    ├── ai-saas.md
    ├── internal-tool.md
    ├── high-concurrency.md
    └── brownfield.md
```

## 上层文件
- `README.md`：仓库总览（人 + 非 Claude 的 Agent 入口）。
- `CLAUDE.md`：Agent 总入口，只负责"什么时候读取什么"。
- `AGENTS.md`：通用 Agent 工程规则摘要（含默认矩阵、最重要规则与读取顺序）。
- `sources/v1.0/`：源文档归档，**只读，Agent 决策时不读取**。
- `specs/`：项目实例目录（如 `specs/001-project/`）。

## 使用方式
1. **先看约定**：目录约定见 `.sdd/LAYOUT.md`，引用编号与命名见 `.sdd/CONVENTIONS.md`（引用的 `§` 必须带来源前缀：`res.md` / `Matrix` / `知识库` / `<文件名>`）。
2. 新项目：`CLAUDE.md` §2 → 读 decision-protocol → workflow + knowledge + decision-trees → 填 template 到 `specs/<id>-<name>/`。
3. **人工确认门槛**：技术栈类决定（Microservices/K8s/DB migration/Auth architecture 等）先 `Architecture Proposal → Human Confirmation`，再固化进 plan.md 与 ADR。
4. 小改动：走 `.sdd/workflows/small-change.md`，不跑全流程。
5. 更新技术栈：仅改 `knowledge/` 与 `decision-trees/`；`CLAUDE.md`/`AGENTS.md` 基本不动。版本变更记入 `CHANGELOG.md`。

## 校验
```
python3 scripts/validate_rules.py     # 校验引用完整性 + Decision Schema 必填项 + 复杂度预算
```

## 来源
- `sources/v1.0/res.md`（AGENT PROJECT ENGINEERING & SPEC-DRIVEN DEVELOPMENT RULES v1.0，120 条）
- `sources/v1.0/AI Architecture Decision Matrix.md`（约束模型 / 正式决策矩阵 / 复杂度预算 / 决策状态 / 30 条规则）
- `sources/v1.0/AI Coding SDD 项目技术架构与框架选择知识库.md`（中文知识库 / 模板 / 默认技术栈 / 与 Spec Kit 衔接）

