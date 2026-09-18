# .sdd — Spec-Driven Development Rule Library

本目录是 Agent 在 SDD 模式下进行项目框架选择与技术选型的**可解释决策系统**。
它不是"把 Python+FastAPI+PostgreSQL 当最佳实践硬塞给 Agent"，而是一套让 Agent 依据项目上下文选择技术、并把选择固化进 `technology-selection.md` 与 `spec.md` 的规则库。

## 设计原则（对应 FINAL PRINCIPLE §120）

- 技术、架构、Framework、SDD 都不是目的；目标是 Correctness / Maintainability / Simplicity / Testability / Observability / Security / Evolvability。
- 无明确需求 → 最简单、成熟、可维护、易验证的方案。
- 复杂需求 → 满足需求并**记录必要性**。

## 目录结构

```
.sdd/
├── README.md                 # 本文件
├── knowledge/                 # 技术知识库（"选什么、何时选"的参考）
│   ├── architecture.md
│   ├── backend.md
│   ├── frontend.md
│   ├── database.md
│   ├── messaging.md
│   ├── api.md
│   ├── security.md
│   ├── testing.md
│   ├── deployment.md
│   └── observability.md
├── decision-trees/            # 决策树（"什么情况选什么"的判断逻辑）
│   ├── architecture.md
│   ├── backend.md
│   ├── frontend.md
│   ├── database.md
│   └── infrastructure.md
├── templates/                 # 文档模板
│   ├── project-discovery.md
│   ├── technology-selection.md
│   ├── spec.md
│   ├── design.md
│   ├── plan.md
│   ├── tasks.md
│   └── adr.md
└── workflows/                 # 流程
    ├── new-project.md
    ├── new-feature.md
    ├── bugfix.md
    └── refactor.md
```

## 上层文件

- `CLAUDE.md`：Agent 总入口，只负责"什么时候读取什么"。
- `AGENTS.md`：通用 Agent 工程规则摘要。
- `specs/`：项目实例目录（如 `specs/001-project/`）。

## 使用方式

1. 新项目：`CLAUDE.md` §2 流程 → 读 workflow + knowledge + decision-trees → 生成 template 实例到 `specs/<id>-<name>/`。
2. 更新技术栈：仅改 `knowledge/` 与 `decision-trees/`，`CLAUDE.md` / `AGENTS.md` 基本不动。
3. 每个重要决策用 `templates/adr.md` 固化为 ADR。

## 来源

全部规则整理自 `res.md`（AGENT PROJECT ENGINEERING & SPEC-DRIVEN DEVELOPMENT RULES v1.0，120 条）。
