# PROMPT-LOG — 002-demo-todo-cli 演示的「可复现提示词记录」

> 本文件记录：用本仓库 SDD 工作流从零落地 `002-demo-todo-cli` 时，**每个阶段喂给 Agent 的提示词**，
> 以及**人工执行的校验命令**。复制这些 prompt 即可在同仓复现演示。
> 流程编排见 `.sdd/workflows/new-project.md` 与 `AGENTS.md` 的 READ ORDER。

---

## 阶段 0 — 启动（建立上下文）

```
你是一个遵循本仓库 .sdd/ 规则库的 Agent。
请按 new-project 工作流，为我新建一个项目：本地命令行待办工具（单人、离线、零部署）。
先读 .sdd/LAYOUT.md 与 .sdd/CONVENTIONS.md 了解目录与引用约定，再开始。
```

## 阶段 1 — Project Discovery

```
基于我对项目的描述（单人本地待办 CLI，离线，无后端无账号），
用 .sdd/templates/project-discovery.md 生成 specs/002-demo-todo-cli/project-discovery.md。
未知项标 UNKNOWN，不要编造数字。
```

## 阶段 2 — Draft Spec（先 WHAT/WHY，不写技术）

```
用 .sdd/templates/spec.md 生成 Draft 版 specs/002-demo-todo-cli/spec.md。
只写 WHAT/WHY（问题、目标、用户故事、功能需求、NFR、架构约束、验收标准），
禁止在 Draft 阶段写语言/框架/数据库/部署。Status 先写 Draft。
```

## 阶段 3 — 技术决策（Draft 之后）

```
Draft Spec 已足以支撑架构判断。请读：
  .sdd/decision-trees/decision-protocol.md
  .sdd/knowledge/architecture.md、backend.md、database.md、versioning.md
按「Hard Constraint 消除 → 候选 → 必要时评分 → 最简满足」做选型，
生成 technology-selection.md 与 machine-readable 的 decision.json（通过 .sdd/schema/decision.schema.json 校验）。
本例无 REQUIRE_CONFIRMATION 项，全部标 AUTO。
```

## 阶段 4 — Finalize（升级 + 产出计划与任务）

```
把 spec.md 的 Status 从 Draft 升级为 Accepted，并将确认后的约束回填到 Constraints/Acceptance。
生成 plan.md、tasks.md、verification.md（design.md 与 adr/ 按需，本例不需要）。
```

## 阶段 5 — 实现与验证

```
实现前先读 Rules / technology-selection / spec / plan / tasks。
实现代码后跑测试，并填写 verification.md 的结论。
```

---

## 人工校验命令（DEFINITION OF DONE）

```bash
# 1) 重建来源 → 落点索引（仅当你修改了 .sdd 内的引用时才需重跑；新建 specs 不影响）
python3 scripts/gen_traceability.py

# 2) 规则库自检：必须 0 errors 0 warnings
python3 scripts/validate_rules.py

# 3) 单独校验本 demo 的 decision.json 是否被 Schema 接受
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "scripts")
import mini_schema
schema = json.loads(Path(".sdd/schema/decision.schema.json").read_text())
data = json.loads(Path("specs/002-demo-todo-cli/decision.json").read_text())
errs = mini_schema.validate(data, schema)
print("ERRORS:", errs if errs else "none")
PY
```

## 关键提示（给使用者）

- **顺序不可交换**：先写 Spec（哪怕只是 Draft），再谈技术（见 new-project.md）。
- **AUTO 不阻塞**：语言/框架/库这类普通决策，Agent 自行选并记录，不要逐个问人。
- **只有 REQUIRE_CONFIRMATION 才需人确认**（如 Microservices / K8s / 数据库迁移 / 鉴权架构变更等）。
- **复杂度预算管"多不多"**：本例 score=0 ≤ Internal Tool 预算 6，无需重评。
- **版本不编造**：Python 版本实现前须核对上游，未知写 UNKNOWN。
