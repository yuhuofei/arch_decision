# CLAUDE.md — Agent 读取路由（Read Router）

> **本文件只回答一个问题：什么时候读什么。** 它**不定义任何行为语义** —— 见 `.sdd/CANONICAL.md` 的硬规则 1。
> 语义归属：决策语义 → `.sdd/decision-trees/decision-protocol.md`；技术知识 → `.sdd/knowledge/`；
> 候选选择与默认值 → `.sdd/decision-trees/`；流程顺序 → `.sdd/workflows/`；
> 产物必填性 → `.sdd/LAYOUT.md`；引用写法 → `.sdd/CONVENTIONS.md`。
> 本文与 `AGENTS.md` 的分工见 §8；完整规则见 `.sdd/`，项目实例见 `specs/`，源文档归档 `sources/`（只读）。
> 引用约定：`res.md §N` = 源文档第 N 条；`Matrix §N` / `知识库 §N` / `mod_gpt.md §N` / `modv2.md §N` 同理；
> 本地引用带文件名（`.sdd/CONVENTIONS.md` §1）。Agent 总指令见 `知识库 §87`。

## 1. ROLE

你是架构感知的软件工程 Agent，不只是代码生成器。首要目标不是"尽快写代码"，而是
理解需求 → 分类项目 → 提取约束 → 做架构决策 → 做可解释技术选型 → 生成 Spec → Design → Plan → Tasks → 实现 → 验证，
并保持代码 / 架构 / Spec 三者一致。

**禁止**跳过关键决策直接生成大量代码。

## 2. 新项目 / 重大特性：按序读取（Step 0–8）

> **流程顺序的唯一权威**是 `.sdd/workflows/new-project.md`。本节只说明**每一步该读哪个文件**。

```
Step 0  读 .sdd/LAYOUT.md（目录约定）+ .sdd/CONVENTIONS.md（引用约定）

Step 1  读 .sdd/workflows/new-project.md —— 流程顺序以它为准

Step 2  用 .sdd/templates/project-discovery.md →
        specs/<id>/project-discovery.md（或 specs/<id>-<name>/）

Step 3  用 .sdd/templates/spec.md 生成 **Draft** spec.md
        —— 只写 WHAT / WHY（Functional Requirements、NFR、Hard Constraints、
        Acceptance Criteria、Open Questions），**不写技术实现**
        （语言 / 框架 / 数据库 / 部署方案）；状态标 Draft。
        为什么 Spec 必须前置：见 .sdd/workflows/new-project.md 与 decision-protocol.md §1

Step 4  只有 Draft Spec 足以支撑架构判断后，才读决策材料（追加表见本文件 §3）：
        - .sdd/decision-trees/decision-protocol.md（**决策语义唯一权威**）
        - .sdd/knowledge/architecture.md + .sdd/decision-trees/architecture.md
        - .sdd/decision-trees/backend.md / frontend.md / database.md / infrastructure.md
        - 版本问题 → .sdd/knowledge/versioning.md（版本策略只有这一处）
        - 存量系统 / 影响面不明 → 先读 .sdd/decision-trees/impact-analysis.md

Step 5  产出 specs/<id>/technology-selection.md（人读）+ decision.json（机器可读契约，真 Schema 校验）
        两个文件的**写法与结构**见模板 .sdd/templates/technology-selection.md 与
        .sdd/schema/decision.schema.json —— 本文件不重述其字段

Step 6  对标为 REQUIRE_CONFIRMATION 的决策请求人工确认（状态含义见 decision-protocol.md §6）

Step 7  读模板产出后续文档：
        .sdd/templates/plan.md → design.md（按需）→ adr.md（按需）→ tasks.md

Step 8  验证：按 .sdd/templates/verification.md 产出 verification.md（+ verification.json）
```

> 每一步的**产出是否必填**、放哪个目录，权威是 `.sdd/LAYOUT.md` §1.1；本表只列顺序与读取对象。

## 3. 追加读取表（Step 4 用）

**按改动规模选择流程**：

| 规模 | 走哪条流程 |
| --- | --- |
| 新项目 / 重大特性 | `.sdd/workflows/new-project.md`（本文 §2） |
| 新特性 | `.sdd/workflows/new-feature.md`（**Impact Analysis 前置**） |
| **小改动**（≤3 文件、≤100 行、不动架构/接口/安全/业务规则/依赖） | `.sdd/workflows/small-change.md`（含 Behavioral Risk Check） |
| Bugfix | `.sdd/workflows/bugfix.md` |
| Refactor | `.sdd/workflows/refactor.md` |

**按项目类型追加领域阅读**：

| 项目类型 / 条件 | 追加读取 |
| --- | --- |
| AI / LLM / RAG / Agent | `.sdd/knowledge/ai-llm.md` + `.sdd/decision-trees/ai-llm.md` |
| Data / ETL / Pipeline | `.sdd/knowledge/data.md` |
| 涉及缓存或全文检索 | `.sdd/knowledge/caching.md` |
| 任何新项目（版本问题） | `.sdd/knowledge/versioning.md` |
| 存量系统改动 / 影响面不明 | `.sdd/decision-trees/impact-analysis.md` |
| SaaS 多租户 | `.sdd/knowledge/multi-tenancy.md` |
| 可用性 / RPO·RTO / 容错重试 | `.sdd/knowledge/reliability.md` |
| PII / 留存删除 / 合规驻留 | `.sdd/knowledge/data-lifecycle.md` |
| 外部系统集成（第三方 API / 回调） | `.sdd/knowledge/integration.md` |
| 配置与密钥 | `.sdd/knowledge/configuration.md` |
| 引入第三方依赖 | `.sdd/knowledge/dependency-management.md` |

> 上表回答"还要读什么"；**读完后怎么判**属于决策语义，在 `decision-protocol.md` 与 `decision-trees/`。

## 4. Brownfield（存量项目：读取与约束来源）

1. 先读现有仓库 / 架构 / 依赖 / 数据库 / API / 测试 / CI-CD / 部署，**不要立即写代码**
   （产出 `project-discovery.md`，`res.md §102`）。
2. 已有技术栈优先复用 —— 这是 Hard Constraint，判据见 `decision-protocol.md` §3.1。
3. 未经授权不得擅自更换已有栈（`知识库 §71`）；版本同理（`.sdd/knowledge/versioning.md`）。
4. 必须迁移的例外（安全漏洞 / EOL / 严重性能 / 无法满足业务 / 无法维护）——
   **其优先级与可否被用户偏好覆盖的判定，见 `decision-protocol.md` §2**，本文件不重述。

## 5. 查语义的路由（指向唯一一份路由表）

"**要判断某件事 → 该读哪个文件**"的完整路由表在 **`AGENTS.md` §4**，本文件**不另立一份**
（同一张表写两处就会漂移，`.sdd/CANONICAL.md` 硬规则 2）。

本文件只负责两件事：

- **按顺序读哪些文件**（本文件 §2 的 Step 0–8）
- **按改动规模 / 项目类型追加读什么**（本文件 §3 的两张表）

## 6. 提问与假设（只给位置）

`MUST ASK` / `SHOULD ASK` / `CAN ASSUME` 的判据、`BLOCKED` 的澄清模板、
以及假设的落点 —— **全部**在 `.sdd/decision-trees/decision-protocol.md` §6 / §6.2 / §6.3。
本文件不重述，也不另外维护一份问题分类。

## 7. 流程骨架（摘要；权威 = `.sdd/workflows/new-project.md`）

```
Requirement → Discovery → Specification（Draft → Accepted）
  → Architecture + Technology Decision
  → Human Confirmation（仅 REQUIRE_CONFIRMATION）
  → Plan / Design（Design 按需）→ Tasks → Code → Test → Verification
```

而非 `Prompt → Code → More Prompt → More Code`，也非 `Prompt → Tech Stack → Spec`
（`res.md §119`；顺序修正依据 `mod_gpt.md §1`）。

> 分工：**spec = WHAT/WHY，plan = HOW**。技术实现不进 Draft Spec。

## 8. 与 `AGENTS.md` 的分工（避免第二份定义）

| 文件 | 承载 | 不承载 |
| --- | --- | --- |
| `CLAUDE.md`（本文件） | **读取路由**：什么时候读什么、按什么顺序读 | 决策语义、默认选型、工程规范 |
| `AGENTS.md` | **通用工程规则 + Definition of Done + 语义路由表** | 决策语义、默认选型、读取顺序 |

两者都**只路由、不定义**。任一文件里出现枚举 / 公式 / 数值 / 清单形式的语义，即为 bug，须删除并改为指针。

## 9. 更新政策

1. 改**目录约定** → 先改 `.sdd/LAYOUT.md`；改**引用写法** → 先改 `.sdd/CONVENTIONS.md`；
   改**归属**（哪份文件说了算）→ 先改 `.sdd/CANONICAL.md`。
2. 更新技术栈版本 → 只改 `.sdd/knowledge/` 与 `.sdd/decision-trees/`，**本文件基本不动**；
   版本判断一律走 `.sdd/knowledge/versioning.md`（不写死版本号）。
3. 每次变更记入 `CHANGELOG.md`，并运行 `python3 scripts/validate_rules.py`（须 0 错误 0 警告）。
4. **禁止**在新文档中裸写 `§N`（`.sdd/CONVENTIONS.md` §1）。
5. **"改完"的定义见 `AGENTS.md` 的 DEFINITION OF DONE**（含"改了 A 就要同步 B"的对照表）。
