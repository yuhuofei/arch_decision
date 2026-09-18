# TRACEABILITY.md — 源规则 → 落点反向索引

> 本文件由 `scripts/gen_traceability.py` **自动生成，请勿手工编辑**。
> 机器可读版本：`.sdd/traceability.json`。

> 用途：源文档升级时快速评估影响面——某条规则被本仓哪些文件引用、落到哪一层。

> 引用解析（`§A,§B` 压缩、`§A-§B` 区间、`§N.M` 子条目）见 `scripts/sdd_refs.py`；书写约定见 `.sdd/CONVENTIONS.md` §1。

> **四态模型**（`modv2.md §14`）：证据强度由弱到强为
> `MAPPED` → `IMPLEMENTED` → `VERIFIED`；`**（未引用）**` 表示无文件写明该条号为出处。
> `MAPPED` 只说明被描述层文件（README / CHANGELOG / REVIEW）提到；
> `IMPLEMENTED` 说明有实现层落点；`VERIFIED` 说明另有机器校验项覆盖。

> **（未直接引用；见子条目）** = 只有它的 `§N.M` 被引用，父条目本身未出现。

> 状态只衡量**证据层级**，**不衡量内容是否被正确、完整地实现**——见文末说明。


---


## res.md（条目 132 条，含子条目）

| 源规则 | 标题 | 状态 | 落点文件 |
| --- | --- | --- | --- |
| `res.md §0` | CORE MISSION | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §1` | GENERAL ENGINEERING PRINCIPLES | IMPLEMENTED | **（未直接引用；见子条目）** |
| `res.md §1.1` | 　Simple Before Complex | IMPLEMENTED | `.sdd/knowledge/architecture.md` |
| `res.md §1.2` | 　Prefer Boring Technology | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`AGENTS.md`<br>`CHANGELOG.md` |
| `res.md §1.3` | 　Minimize Technology Diversity | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`AGENTS.md`<br>`CHANGELOG.md` |
| `res.md §1.4` | 　Existing Project Takes Priority | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`AGENTS.md`<br>`CHANGELOG.md` |
| `res.md §1.5` | 　Explicit User Decisions Have Highest Priority | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/backend.md` |
| `res.md §2` | PROJECT DISCOVERY | IMPLEMENTED | `.sdd/templates/project-discovery.md` |
| `res.md §2.1` | 　Business | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/templates/project-discovery.md` |
| `res.md §2.2` | 　Users | IMPLEMENTED | `.sdd/templates/project-discovery.md` |
| `res.md §2.3` | 　Traffic | IMPLEMENTED | `.sdd/templates/project-discovery.md` |
| `res.md §2.4` | 　Data | IMPLEMENTED | `.sdd/knowledge/data-lifecycle.md`<br>`.sdd/templates/project-discovery.md` |
| `res.md §2.5` | 　Non-functional Requirements | IMPLEMENTED | `.sdd/knowledge/reliability.md`<br>`.sdd/templates/project-discovery.md` |
| `res.md §3` | PROJECT SCALE CLASSIFICATION | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/templates/project-discovery.md` |
| `res.md §4` | ARCHITECTURE STYLE | IMPLEMENTED | `.sdd/knowledge/architecture.md` |
| `res.md §4.1` | 　Modular Monolith | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`CHANGELOG.md` |
| `res.md §5` | BACKEND LANGUAGE DECISION | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §6` | PYTHON | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §7` | FASTAPI | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §8` | DJANGO | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §9` | FLASK | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §10` | GO | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §11` | GO FRAMEWORK | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §12` | TYPESCRIPT BACKEND | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §13` | NESTJS | IMPLEMENTED | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`AGENTS.md` |
| `res.md §14` | JAVA / KOTLIN | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §15` | SPRING BOOT | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §16` | FRONTEND DECISION | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §17` | VUE | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §18` | REACT | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §19` | NEXT.JS | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §20` | ANGULAR | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §21` | FRONTEND ARCHITECTURE | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/frontend.md` |
| `res.md §22` | DATABASE DECISION | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `res.md §23` | POSTGRESQL | IMPLEMENTED | `.sdd/knowledge/database.md`<br>`specs/001-project/technology-selection.md` |
| `res.md §24` | MYSQL | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `res.md §25` | SQLITE | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `res.md §26` | MONGODB | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `res.md §27` | REDIS | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `res.md §28` | ORM | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §29` | API STYLE | IMPLEMENTED | `.sdd/knowledge/api.md` |
| `res.md §30` | REST | IMPLEMENTED | `.sdd/knowledge/api.md` |
| `res.md §31` | GRAPHQL | IMPLEMENTED | `.sdd/knowledge/api.md` |
| `res.md §32` | GRPC | IMPLEMENTED | `.sdd/knowledge/api.md` |
| `res.md §33` | OPENAPI | IMPLEMENTED | `.sdd/knowledge/api.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md` |
| `res.md §34` | MESSAGE QUEUE | IMPLEMENTED | `.sdd/knowledge/messaging.md` |
| `res.md §35` | RABBITMQ | IMPLEMENTED | `.sdd/knowledge/messaging.md` |
| `res.md §36` | KAFKA | IMPLEMENTED | `.sdd/knowledge/messaging.md` |
| `res.md §37` | BACKGROUND JOBS | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/messaging.md` |
| `res.md §38` | SEARCH | IMPLEMENTED | `.sdd/knowledge/caching.md`<br>`CHANGELOG.md` |
| `res.md §39` | VECTOR SEARCH | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `res.md §40` | OBJECT STORAGE | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `res.md §41` | AUTHENTICATION | IMPLEMENTED | `.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/data-lifecycle.md`<br>`.sdd/knowledge/security.md` |
| `res.md §42` | SESSION | IMPLEMENTED | `.sdd/knowledge/security.md`<br>`specs/001-project/design.md` |
| `res.md §43` | JWT | IMPLEMENTED | `.sdd/knowledge/security.md`<br>`specs/001-project/design.md` |
| `res.md §44` | OIDC / OAuth | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/security.md` |
| `res.md §45` | SECURITY | IMPLEMENTED | `.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/data-lifecycle.md`<br>`.sdd/knowledge/dependency-management.md`<br>`.sdd/knowledge/security.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §46` | AUTHORIZATION | IMPLEMENTED | `.sdd/knowledge/security.md`<br>`specs/001-project/design.md` |
| `res.md §47` | OBSERVABILITY | IMPLEMENTED | `.sdd/knowledge/observability.md`<br>`specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §48` | LOGGING | IMPLEMENTED | `.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/data-lifecycle.md`<br>`.sdd/knowledge/observability.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §49` | DISTRIBUTED TRACING | IMPLEMENTED | `.sdd/knowledge/observability.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md` |
| `res.md §50` | TESTING STRATEGY | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/templates/verification.md`<br>`.sdd/workflows/refactor.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §51` | UNIT TEST | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/templates/verification.md`<br>`.sdd/workflows/refactor.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/tasks.md` |
| `res.md §52` | INTEGRATION TEST | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/templates/verification.md`<br>`.sdd/workflows/refactor.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/tasks.md` |
| `res.md §53` | E2E TEST | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/templates/verification.md`<br>`.sdd/workflows/refactor.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/tasks.md` |
| `res.md §54` | PYTHON TESTING | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §55` | FRONTEND TESTING | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §56` | GO TESTING | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §57` | JAVA TESTING | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §58` | CODE QUALITY | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §59` | PACKAGE MANAGEMENT | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `res.md §60` | CONTAINERIZATION | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/versioning.md`<br>`specs/001-project/plan.md` |
| `res.md §61` | DOCKER COMPOSE | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/versioning.md` |
| `res.md §62` | KUBERNETES | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/versioning.md` |
| `res.md §63` | CI/CD | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/versioning.md`<br>`specs/001-project/plan.md` |
| `res.md §64` | DATABASE MIGRATION | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/versioning.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md` |
| `res.md §65` | BACKUP | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/data-lifecycle.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/reliability.md`<br>`.sdd/knowledge/versioning.md` |
| `res.md §66` | DATABASE DESIGN RULES | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §67` | TRANSACTION RULES | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/knowledge/multi-tenancy.md`<br>`.sdd/workflows/bugfix.md`<br>`.sdd/workflows/small-change.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/adr/ADR-001-postgres.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §68` | ID STRATEGY | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §69` | TIME | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/plan.md` |
| `res.md §70` | API ERROR FORMAT | IMPLEMENTED | `.sdd/knowledge/api.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §71` | PAGINATION | IMPLEMENTED | `.sdd/knowledge/api.md`<br>`.sdd/knowledge/caching.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §72` | RATE LIMITING | IMPLEMENTED | `.sdd/knowledge/api.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/knowledge/integration.md`<br>`.sdd/knowledge/reliability.md`<br>`specs/001-project/plan.md` |
| `res.md §73` | CACHING | IMPLEMENTED | `.sdd/knowledge/api.md`<br>`.sdd/knowledge/caching.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §74` | ASYNC ARCHITECTURE | IMPLEMENTED | `.sdd/knowledge/messaging.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §75` | FRONTEND STATE MANAGEMENT | IMPLEMENTED | `.sdd/knowledge/frontend.md`<br>`specs/001-project/plan.md` |
| `res.md §76` | UI COMPONENT LIBRARY | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §77` | MONOREPO | IMPLEMENTED | `.sdd/knowledge/architecture.md` |
| `res.md §78` | REPOSITORY STRUCTURE | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md` |
| `res.md §79` | Django | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §80` | Go | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §81` | NestJS | IMPLEMENTED | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`AGENTS.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §82` | Spring Boot | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §83` | VUE | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §84` | REACT | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §85` | NEXT.JS | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `res.md §86` | CONFIGURATION | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/deployment.md`<br>`CHANGELOG.md`<br>`specs/001-project/tasks.md` |
| `res.md §87` | SECRET MANAGEMENT | IMPLEMENTED | `.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/security.md`<br>`CHANGELOG.md`<br>`specs/001-project/plan.md` |
| `res.md §88` | VERSION STRATEGY | **VERIFIED**<br>`check_version_consistency` | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/versioning.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §89` | VERSION PINNING | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/versioning.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §90` | DEPENDENCY DECISION | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/knowledge/dependency-management.md`<br>`.sdd/workflows/small-change.md`<br>`CHANGELOG.md`<br>`specs/002-demo-todo-cli/technology-selection.md` |
| `res.md §91` | SPEC-DRIVEN DEVELOPMENT | IMPLEMENTED | `.sdd/templates/spec.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/spec.md` |
| `res.md §92` | SPEC ARTIFACTS | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §93` | PROJECT-LEVEL SPEC | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §94` | TECHNOLOGY-SELECTION.MD | IMPLEMENTED | `.sdd/templates/technology-selection.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §95` | DECISION RECORD FORMAT | IMPLEMENTED | `.sdd/templates/adr.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §96` | REQUIREMENTS | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §97` | ACCEPTANCE CRITERIA | IMPLEMENTED | `.sdd/templates/verification.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/verification.md` |
| `res.md §98` | DESIGN | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/design.md` |
| `res.md §99` | TASKS | IMPLEMENTED | `.sdd/templates/plan.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md` |
| `res.md §100` | IMPLEMENTATION RULE | IMPLEMENTED | `.sdd/templates/plan.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md` |
| `res.md §101` | CHANGE MANAGEMENT | IMPLEMENTED | `.sdd/decision-trees/impact-analysis.md`<br>`.sdd/templates/plan.md`<br>`.sdd/workflows/bugfix.md`<br>`.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §102` | BROWNFIELD PROJECT | IMPLEMENTED | `.sdd/decision-trees/impact-analysis.md`<br>`.sdd/templates/project-discovery.md`<br>`.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`CLAUDE.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md` |
| `res.md §103` | BROWNFIELD TECHNOLOGY RULE | IMPLEMENTED | `.sdd/decision-trees/impact-analysis.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §104` | FEATURE DEVELOPMENT FLOW | IMPLEMENTED | `.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §105` | BUGFIX FLOW | IMPLEMENTED | `.sdd/workflows/bugfix.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §106` | REFACTOR FLOW | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`.sdd/workflows/refactor.md`<br>`.sdd/workflows/small-change.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §107` | AGENT QUESTION POLICY | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §108` | QUESTIONS CLASSIFICATION | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md`<br>`CLAUDE.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §109` | TECHNOLOGY DECISION OUTPUT | IMPLEMENTED | `.sdd/templates/technology-selection.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §110` | DEFAULT TECHNOLOGY MATRIX | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §111` | DEFAULT FULL STACK | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §112` | DEFAULT AI APPLICATION STACK | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §113` | DEFAULT ENTERPRISE STACK | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §114` | DEFAULT HIGH-PERFORMANCE SERVICE | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §115` | TECHNOLOGY INTRODUCTION CHECKLIST | IMPLEMENTED | `.sdd/decision-trees/impact-analysis.md`<br>`.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §116` | ARCHITECTURE REVIEW CHECKLIST | IMPLEMENTED | `.sdd/templates/verification.md`<br>`.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §117` | FINAL SPEC REQUIREMENTS | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/spec.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §118` | FINAL AGENT BEHAVIOR | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`REVIEW-2026-09-19.md` |
| `res.md §119` | GOLDEN RULE | IMPLEMENTED | `CLAUDE.md` |
| `res.md §120` | FINAL PRINCIPLE | IMPLEMENTED | `.sdd/README.md`<br>`AGENTS.md`<br>`CLAUDE.md`<br>`README.md`<br>`specs/001-project/technology-selection.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）

状态分布：IMPLEMENTED 131 ／ VERIFIED 1 ／ MAPPED 0 ／ 未引用 0


## Matrix（条目 59 条，含子条目）

| 源规则 | 标题 | 状态 | 落点文件 |
| --- | --- | --- | --- |
| `Matrix §1` | Agent 总决策协议 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/adr.md` |
| `Matrix §2` | 决策优先级 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §3` | Hard Constraint / Soft Constraint | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/architecture.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §3.1` | 　Hard Constraint | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md` |
| `Matrix §3.2` | 　Soft Constraint | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md` |
| `Matrix §4` | 项目类型矩阵 | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §5` | Architecture Decision Matrix | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/multi-tenancy.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §5.1` | 　Monolith | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §5.2` | 　Modular Monolith | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md` |
| `Matrix §5.3` | 　Microservices | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §6` | Backend Language Matrix | IMPLEMENTED | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md` |
| `Matrix §6.1` | 　Python | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §6.2` | 　Go | IMPLEMENTED | `.sdd/examples/high-concurrency.md`<br>`.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `Matrix §6.3` | 　TypeScript | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `Matrix §6.4` | 　Java / Kotlin | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `Matrix §6.5` | 　Rust | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `Matrix §7` | Backend Framework Matrix | IMPLEMENTED | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `Matrix §8` | Frontend Matrix | IMPLEMENTED | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `Matrix §8.1` | 　Vue | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `Matrix §8.2` | 　React | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `Matrix §8.3` | 　Next.js | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `Matrix §8.4` | 　Angular | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `Matrix §9` | Frontend / Backend Separation Matrix | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/frontend.md` |
| `Matrix §10` | Database Matrix | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/adr/ADR-001-postgres.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §11` | MySQL | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/adr/ADR-001-postgres.md` |
| `Matrix §12` | SQLite | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/knowledge/frontend.md`<br>`specs/001-project/adr/ADR-001-postgres.md` |
| `Matrix §13` | Redis Matrix | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §14` | ORM Matrix | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `Matrix §15` | API Protocol Matrix | IMPLEMENTED | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/api.md`<br>`.sdd/knowledge/integration.md` |
| `Matrix §16` | Message Queue Matrix | IMPLEMENTED | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/integration.md`<br>`.sdd/knowledge/messaging.md` |
| `Matrix §17` | Search Engine Matrix | IMPLEMENTED | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/caching.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §18` | Vector Database Matrix | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/templates/adr.md` |
| `Matrix §19` | Object Storage Matrix | IMPLEMENTED | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §20` | Authentication Matrix | IMPLEMENTED | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/security.md`<br>`specs/001-project/adr/ADR-003-session-auth.md`<br>`specs/001-project/plan.md` |
| `Matrix §21` | Authorization Matrix | IMPLEMENTED | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/security.md` |
| `Matrix §22` | Multi-Tenant Matrix | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/database.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/knowledge/multi-tenancy.md`<br>`CHANGELOG.md` |
| `Matrix §23` | Caching Matrix | IMPLEMENTED | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/caching.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §24` | Deployment Matrix | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/deployment.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md` |
| `Matrix §25` | Kubernetes Decision Rule | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/deployment.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/plan.md` |
| `Matrix §26` | Observability Matrix | IMPLEMENTED | `.sdd/knowledge/observability.md`<br>`.sdd/knowledge/reliability.md`<br>`specs/001-project/plan.md` |
| `Matrix §27` | Testing Matrix | IMPLEMENTED | `.sdd/knowledge/testing.md`<br>`.sdd/templates/verification.md` |
| `Matrix §28` | Test Strategy Matrix | IMPLEMENTED | `.sdd/knowledge/data.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/verification.md`<br>`specs/001-project/plan.md` |
| `Matrix §29` | AI Application Matrix | IMPLEMENTED | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §30` | LLM Provider Architecture | IMPLEMENTED | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/examples/ai-saas.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §31` | RAG Matrix | IMPLEMENTED | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §32` | Architecture Complexity Budget | **VERIFIED**<br>`check_complexity_json` | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/templates/technology-selection.md`<br>`REVIEW-2026-09-19.md` |
| `Matrix §33` | Infrastructure Introduction Rule | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/messaging.md` |
| `Matrix §34` | Existing Project Decision Matrix | IMPLEMENTED | `.sdd/decision-trees/impact-analysis.md`<br>`.sdd/examples/brownfield.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`specs/001-project/plan.md` |
| `Matrix §35` | Existing Stack Conflict | IMPLEMENTED | `.sdd/decision-trees/impact-analysis.md`<br>`.sdd/examples/brownfield.md`<br>`specs/001-project/plan.md` |
| `Matrix §36` | Technology Selection Scoring | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md`<br>`AGENTS.md` |
| `Matrix §37` | Example | IMPLEMENTED | `.sdd/examples/saas.md` |
| `Matrix §38` | Example: AI SaaS | IMPLEMENTED | `.sdd/examples/ai-saas.md` |
| `Matrix §39` | Example: High-Concurrency Service | IMPLEMENTED | `.sdd/examples/high-concurrency.md` |
| `Matrix §40` | Decision Output Schema | **VERIFIED**<br>`check_decision_json` | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §41` | Decision Status | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §42` | 哪些决策必须人工确认 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/security.md` |
| `Matrix §43` | Agent Decision Loop | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-project.md` |
| `Matrix §44` | 最终 Agent Rule | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md` |
| `Matrix §45` | 推荐最终目录 | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/LAYOUT.md`<br>`.sdd/knowledge/deployment.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）

状态分布：IMPLEMENTED 57 ／ VERIFIED 2 ／ MAPPED 0 ／ 未引用 0


## 知识库（条目 103 条，含子条目）

| 源规则 | 标题 | 状态 | 落点文件 |
| --- | --- | --- | --- |
| `知识库 §1` | 文档目标 | MAPPED | `.sdd/README.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §2` | 总体原则 | MAPPED | `.sdd/README.md`<br>`CHANGELOG.md` |
| `知识库 §2.1` | 　默认原则 | MAPPED | `.sdd/README.md`<br>`CHANGELOG.md` |
| `知识库 §3` | 架构选择总决策树 | IMPLEMENTED | `.sdd/knowledge/architecture.md` |
| `知识库 §4` | 项目类型分类 | IMPLEMENTED | `.sdd/knowledge/architecture.md` |
| `知识库 §4.1` | 　Web Application | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`CHANGELOG.md` |
| `知识库 §4.2` | 　API / Backend Service | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`CHANGELOG.md` |
| `知识库 §4.3` | 　Data / AI Application | IMPLEMENTED | `.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/data.md` |
| `知识库 §4.4` | 　CLI / Automation | IMPLEMENTED | `.sdd/knowledge/data.md` |
| `知识库 §4.5` | 　Worker / Background Job | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/data.md`<br>`.sdd/knowledge/messaging.md` |
| `知识库 §5` | 编程语言选择 | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `知识库 §5.1` | 　Python | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md` |
| `知识库 §6` | Python Web Framework | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §6.1` | 　FastAPI —— 默认 API 首选 | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §6.2` | 　Flask | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md` |
| `知识库 §6.3` | 　Django | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md` |
| `知识库 §7` | Go | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `知识库 §8` | Go Web Framework | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/integration.md`<br>`.sdd/knowledge/reliability.md` |
| `知识库 §8.1` | 　Gin | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md` |
| `知识库 §8.2` | 　Echo | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md` |
| `知识库 §8.3` | 　net/http | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`CHANGELOG.md` |
| `知识库 §9` | TypeScript / Node.js | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `知识库 §10` | Java / Kotlin | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `知识库 §11` | Rust | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`.sdd/templates/verification.md` |
| `知识库 §12` | 前后端架构 | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §12.1` | 　前后端分离 | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`CHANGELOG.md` |
| `知识库 §13` | 前后端合并 | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §14` | Vue | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §15` | React | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §16` | Next.js | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §17` | Angular | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §18` | CSS/UI 技术 | IMPLEMENTED | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §19` | UI Component Library | IMPLEMENTED | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §20` | Database 选择 | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `知识库 §21` | PostgreSQL | IMPLEMENTED | `.sdd/knowledge/database.md`<br>`.sdd/knowledge/multi-tenancy.md` |
| `知识库 §22` | MySQL | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `知识库 §23` | SQLite | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `知识库 §24` | Redis | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `知识库 §25` | ORM | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `知识库 §26` | API 风格 | IMPLEMENTED | `.sdd/knowledge/api.md` |
| `知识库 §27` | GraphQL | IMPLEMENTED | `.sdd/knowledge/api.md` |
| `知识库 §28` | gRPC | IMPLEMENTED | `.sdd/knowledge/api.md` |
| `知识库 §29` | Message Queue | IMPLEMENTED | `.sdd/knowledge/messaging.md` |
| `知识库 §30` | 搜索 | IMPLEMENTED | `.sdd/knowledge/caching.md`<br>`CHANGELOG.md` |
| `知识库 §31` | Vector Database | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `知识库 §32` | Object Storage | IMPLEMENTED | `.sdd/knowledge/database.md` |
| `知识库 §33` | Authentication | IMPLEMENTED | `.sdd/knowledge/security.md`<br>`specs/001-project/adr/ADR-003-session-auth.md`<br>`specs/001-project/plan.md` |
| `知识库 §34` | Authorization | IMPLEMENTED | `.sdd/knowledge/messaging.md`<br>`.sdd/knowledge/security.md`<br>`specs/001-project/plan.md` |
| `知识库 §35` | API Security | IMPLEMENTED | `.sdd/knowledge/data-lifecycle.md`<br>`.sdd/knowledge/integration.md`<br>`.sdd/knowledge/security.md` |
| `知识库 §36` | Configuration | IMPLEMENTED | `.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/security.md`<br>`CHANGELOG.md` |
| `知识库 §37` | Logging | IMPLEMENTED | `.sdd/knowledge/observability.md` |
| `知识库 §38` | Observability | IMPLEMENTED | `.sdd/knowledge/observability.md` |
| `知识库 §39` | Testing | IMPLEMENTED | `.sdd/knowledge/testing.md`<br>`specs/001-project/plan.md` |
| `知识库 §40` | Python Testing | IMPLEMENTED | `.sdd/knowledge/testing.md` |
| `知识库 §41` | Frontend Testing | IMPLEMENTED | `.sdd/knowledge/testing.md` |
| `知识库 §42` | Go Testing | IMPLEMENTED | `.sdd/knowledge/testing.md` |
| `知识库 §43` | Java Testing | IMPLEMENTED | `.sdd/knowledge/testing.md` |
| `知识库 §44` | Container | IMPLEMENTED | `.sdd/knowledge/deployment.md` |
| `知识库 §45` | Kubernetes | IMPLEMENTED | `.sdd/knowledge/deployment.md` |
| `知识库 §46` | CI/CD | IMPLEMENTED | `.sdd/knowledge/deployment.md` |
| `知识库 §47` | Python 项目工具链 | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `知识库 §48` | Go 项目工具链 | IMPLEMENTED | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md` |
| `知识库 §49` | Frontend Vue 工具链 | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §50` | Frontend React 工具链 | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §51` | 前端状态管理 | IMPLEMENTED | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §52` | API Client | IMPLEMENTED | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/api.md`<br>`.sdd/knowledge/frontend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md` |
| `知识库 §53` | API Contract | IMPLEMENTED | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/api.md`<br>`.sdd/knowledge/frontend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md` |
| `知识库 §54` | Monorepo | IMPLEMENTED | `.sdd/knowledge/architecture.md` |
| `知识库 §55` | Repository Structure | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `知识库 §56` | Go Backend | IMPLEMENTED | `.sdd/knowledge/backend.md` |
| `知识库 §57` | Vue Frontend | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §58` | React Frontend | IMPLEMENTED | `.sdd/knowledge/frontend.md` |
| `知识库 §59` | 推荐的默认技术栈 | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`CHANGELOG.md` |
| `知识库 §60` | AI / RAG SaaS | IMPLEMENTED | `.sdd/examples/ai-saas.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §61` | 高并发 API | IMPLEMENTED | `.sdd/examples/high-concurrency.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md` |
| `知识库 §62` | 企业 Java 系统 | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`CHANGELOG.md` |
| `知识库 §63` | 小型内部工具 | IMPLEMENTED | `.sdd/examples/internal-tool.md` |
| `知识库 §64` | MVP | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md` |
| `知识库 §65` | 微服务决策 | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §66` | Event-Driven Architecture | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/messaging.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §67` | CQRS | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §68` | Event Sourcing | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §69` | DDD | IMPLEMENTED | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §70` | AI Coding 特殊要求 | IMPLEMENTED | `.sdd/knowledge/architecture.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §71` | Agent 不得自行做的决定 | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/examples/brownfield.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/security.md`<br>`CLAUDE.md` |
| `知识库 §72` | 技术选型评分模型 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md` |
| `知识库 §73` | 技术选择必须记录理由 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/adr.md` |
| `知识库 §74` | Agent 技术选型规则 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md` |
| `知识库 §75` | Existing Project 特殊规则 | IMPLEMENTED | `.sdd/examples/brownfield.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §76` | Agent 生成 spec.md 时必须包含的架构上下文 | IMPLEMENTED | `.sdd/templates/spec.md` |
| `知识库 §77` | plan.md 必须包含 | IMPLEMENTED | `.sdd/templates/plan.md`<br>`.sdd/templates/spec.md` |
| `知识库 §78` | 推荐的 SDD Artifact | IMPLEMENTED | `.sdd/LAYOUT.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §79` | 推荐的 spec.md 模板 | IMPLEMENTED | `.sdd/templates/spec.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §80` | 推荐的 plan.md 技术架构模板 | IMPLEMENTED | `.sdd/templates/plan.md`<br>`REVIEW-2026-09-19.md`<br>`specs/001-project/design.md` |
| `知识库 §81` | Agent 生成项目 Spec 的最终规则 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §82` | 技术栈选择的默认优先级 | IMPLEMENTED | `.sdd/workflows/new-project.md`<br>`AGENTS.md` |
| `知识库 §83` | 默认不要使用的复杂技术 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §84` | AI Agent 的最终输出格式 | IMPLEMENTED | `.sdd/templates/technology-selection.md` |
| `知识库 §85` | 最重要的规则 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`AGENTS.md`<br>`REVIEW-2026-09-19.md` |
| `知识库 §86` | 最终 SDD Traceability | MAPPED | `CHANGELOG.md` |
| `知识库 §87` | 给 AI Agent 的总指令 | IMPLEMENTED | `AGENTS.md`<br>`CHANGELOG.md`<br>`CLAUDE.md` |
| `知识库 §88` | 与 Spec Kit / OpenSpec 的结合方式 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/spec.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §89` | 推荐最终目录 | IMPLEMENTED | `.sdd/LAYOUT.md`<br>`CHANGELOG.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）

状态分布：IMPLEMENTED 99 ／ VERIFIED 0 ／ MAPPED 4 ／ 未引用 0


## mod_gpt.md（条目 9 条，含子条目）

| 源规则 | 标题 | 状态 | 落点文件 |
| --- | --- | --- | --- |
| `mod_gpt.md §1` | P0：SDD 主流程顺序仍然自相矛盾 | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/README.md`<br>`.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`CHANGELOG.md`<br>`CLAUDE.md` |
| `mod_gpt.md §2` | SDD REQUIRED（新项目 / 重大特性） | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`CHANGELOG.md`<br>`CLAUDE.md` |
| `mod_gpt.md §3` | P0：用户明确要求 = 最高 Hard Constraint 太绝对 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md`<br>`CLAUDE.md`<br>`REVIEW-2026-09-19.md` |
| `mod_gpt.md §4` | P1：plan.md 和 design.md 职责高度重复 | IMPLEMENTED | `.sdd/CONVENTIONS.md`<br>`.sdd/LAYOUT.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/design.md`<br>`CHANGELOG.md` |
| `mod_gpt.md §5` | P1：现在所谓的 JSON Schema 校验实际上没有真正执行 Schema | MAPPED | `CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `mod_gpt.md §6` | P1：评分公式有权重，但没有评分标尺，Agent 会产生“伪精确评分” | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md` |
| `mod_gpt.md §7` | P1：默认技术矩阵仍然偏“答案库”，而不是“决策系统” | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`CLAUDE.md` |
| `mod_gpt.md §8` | P1：你最初要求的“默认版本策略”目前还没有真正形成规则 | IMPLEMENTED | `.sdd/knowledge/versioning.md`<br>`CHANGELOG.md` |
| `mod_gpt.md §9` | 我建议顺手调整 AGENTS.md | IMPLEMENTED | `AGENTS.md`<br>`CHANGELOG.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）

状态分布：IMPLEMENTED 8 ／ VERIFIED 0 ／ MAPPED 1 ／ 未引用 0


## modv2.md（条目 22 条，含子条目）

| 源规则 | 标题 | 状态 | 落点文件 |
| --- | --- | --- | --- |
| `modv2.md §1` | P0：decision-protocol.md 仍然存在旧规则 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §2` | P0：new-project.md 还是旧流程 | MAPPED | `CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §3` | P0：LAYOUT.md 又和 v1.3 冲突了 | IMPLEMENTED | `.sdd/LAYOUT.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §4` | P0：实际上缺少 templates/verification.md | **VERIFIED**<br>`check_verification_artifact` | `.sdd/LAYOUT.md`<br>`.sdd/README.md`<br>`.sdd/templates/verification.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §5` | P0：你说“真 Schema 校验”，但 validate_rules.py 目前实际上没有调用 mini_schema.py | MAPPED | `CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §6` | P1：Schema 本身还没有完全覆盖 Decision Protocol | **VERIFIED**<br>`check_decision_json` | `.sdd/README.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §7` | P1：decision.json 的成本状态存在逻辑矛盾 | **VERIFIED**<br>`check_cost_consistency` | `.sdd/CONVENTIONS.md`<br>`.sdd/templates/technology-selection.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §8` | P1：RECOMMEND 的语义在 technology-selection.md 仍然是旧版 | IMPLEMENTED | `.sdd/templates/technology-selection.md`<br>`CHANGELOG.md` |
| `modv2.md §9` | P1：plan.md 仍然保留了旧的 Human Confirmation 语义 | MAPPED | `CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §10` | P1：decision-protocol 的决策循环仍然没有真正升级到 v1.3 | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §11` | P1：CAN_ASSUME 不应该要求 ADR | IMPLEMENTED | `.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md` |
| `modv2.md §12` | P1：README / .sdd/README / CHANGELOG 版本号不一致 | **VERIFIED**<br>`check_version_consistency` | `.sdd/CONVENTIONS.md`<br>`CHANGELOG.md` |
| `modv2.md §13` | P1：.sdd/README.md 仍然是旧流程 | MAPPED | `CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §14` | 一个更隐蔽的问题：TRACEABILITY 目前仍然不是“内容覆盖率” | IMPLEMENTED | `.sdd/CANONICAL.md`<br>`.sdd/CONVENTIONS.md`<br>`.sdd/README.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §15` | 目前还有一个重要的“内容遗漏”：没有把“证据”提升到一等公民 | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/templates/adr.md`<br>`.sdd/templates/technology-selection.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §16` | 另一个遗漏：缺少“Decision Re-evaluation Trigger” | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/templates/adr.md`<br>`.sdd/templates/technology-selection.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §17` | 还建议补一类“架构负债 / Deferred Decision” | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/templates/technology-selection.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §18` | 建议补一个 decision-log.md 或直接增强 decision.json | IMPLEMENTED | `.sdd/README.md`<br>`.sdd/templates/technology-selection.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §19` | 内容方面，我建议下一版补齐 6 个领域 | IMPLEMENTED | `.sdd/knowledge/configuration.md`<br>`.sdd/knowledge/data-lifecycle.md`<br>`.sdd/knowledge/dependency-management.md`<br>`.sdd/knowledge/integration.md`<br>`.sdd/knowledge/multi-tenancy.md`<br>`.sdd/knowledge/reliability.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §20` | 我认为还缺一个真正重要的 Agent 能力：Impact Analysis | IMPLEMENTED | `.sdd/decision-trees/impact-analysis.md`<br>`.sdd/workflows/new-feature.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §21` | small-change 还需要一个“行为变化”检测，而不仅是行数 | IMPLEMENTED | `.sdd/workflows/small-change.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |
| `modv2.md §22` | 最终我建议你把 v1.3.1 的修改分成三个层次 | IMPLEMENTED | `.sdd/CANONICAL.md`<br>`.sdd/CONVENTIONS.md`<br>`.sdd/README.md`<br>`CHANGELOG.md`<br>`REVIEW-2026-09-19.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）

状态分布：IMPLEMENTED 14 ／ VERIFIED 4 ／ MAPPED 4 ／ 未引用 0


---

## 关于「未被引用」与四态

机器只能判断「有无写明出处」与「落点在不在实现层」，**不能判断内容是否正确**。
清单需人工分诊：

- **已覆盖未标注**：内容已在知识/决策文件中表达，只是没写来源条号 —— 补标注即可。
- **真实落点缺失**：该规则在本仓确无对应内容 —— 需新增落点，或在此显式登记为不适用。

> **引用率 ≠ 内容覆盖率，`VERIFIED` ≠ 内容正确。** 本表只回答三个问题：有没有落点 / 落点在不在实现层 / 有没有检查项。规则是否被正确完整地实现，仍需人工评审。

**已确认的真实缺口**：（无）

---

## 校验：引用了不存在的条号（应为空）

> 只统计**非审计文件**的越界引用。审计报告（`REVIEW-*.md`）为说明「这里原本写错了什么」会把缺陷原文照抄下来，故其越界写法单独列出、不计为违规。

（无）

**审计报告中引用的历史越界写法（豁免）：**

- `Matrix §3.4` → `REVIEW-2026-09-19.md`
- `Matrix §65` → `REVIEW-2026-09-19.md`
- `Matrix §66` → `REVIEW-2026-09-19.md`
- `Matrix §67` → `REVIEW-2026-09-19.md`
- `Matrix §68` → `REVIEW-2026-09-19.md`
- `Matrix §69` → `REVIEW-2026-09-19.md`
- `知识库 §98` → `REVIEW-2026-09-19.md`
