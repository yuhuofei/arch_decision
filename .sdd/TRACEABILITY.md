# TRACEABILITY.md — 源规则 → 落点反向索引

> 本文件由 `scripts/gen_traceability.py` **自动生成，请勿手工编辑**。

> 用途：源文档升级时快速评估影响面——某条规则被本仓哪些文件引用。

> 引用解析（`§A,§B` 压缩、`§A-§B` 区间、`§N.M` 子条目）见 `scripts/sdd_refs.py`；书写约定见 `.sdd/CONVENTIONS.md` §1。

> 读表约定：**（未引用）** = 无文件写明该条号为出处；**（未直接引用；见子条目）** = 只有它的 `§N.M` 被引用，父条目本身未出现。


---


## res.md（条目 132 条，含子条目）

| 源规则 | 标题 | 落点文件 |
| --- | --- | --- |
| `res.md §0` | CORE MISSION | `.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`specs/001-project/verification.md` |
| `res.md §1` | GENERAL ENGINEERING PRINCIPLES | `.sdd/LAYOUT.md`<br>`AGENTS.md` |
| `res.md §1.1` | 　Simple Before Complex | `.sdd/knowledge/architecture.md` |
| `res.md §1.2` | 　Prefer Boring Technology | `.sdd/CONVENTIONS.md`<br>`AGENTS.md` |
| `res.md §1.3` | 　Minimize Technology Diversity | `.sdd/CONVENTIONS.md`<br>`AGENTS.md` |
| `res.md §1.4` | 　Existing Project Takes Priority | `.sdd/CONVENTIONS.md`<br>`AGENTS.md` |
| `res.md §1.5` | 　Explicit User Decisions Have Highest Priority | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/backend.md` |
| `res.md §2` | PROJECT DISCOVERY | `.sdd/LAYOUT.md`<br>`.sdd/templates/project-discovery.md` |
| `res.md §2.1` | 　Business | `.sdd/CONVENTIONS.md`<br>`.sdd/templates/project-discovery.md` |
| `res.md §2.2` | 　Users | `.sdd/templates/project-discovery.md` |
| `res.md §2.3` | 　Traffic | `.sdd/templates/project-discovery.md` |
| `res.md §2.4` | 　Data | `.sdd/templates/project-discovery.md` |
| `res.md §2.5` | 　Non-functional Requirements | `.sdd/templates/project-discovery.md` |
| `res.md §3` | PROJECT SCALE CLASSIFICATION | `.sdd/LAYOUT.md`<br>`.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/templates/project-discovery.md`<br>`.sdd/workflows/bugfix.md`<br>`.sdd/workflows/new-feature.md`<br>`.sdd/workflows/refactor.md` |
| `res.md §4` | ARCHITECTURE STYLE | `.sdd/LAYOUT.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/backend.md` |
| `res.md §4.1` | 　Modular Monolith | `.sdd/knowledge/architecture.md` |
| `res.md §5` | BACKEND LANGUAGE DECISION | `.sdd/LAYOUT.md`<br>`.sdd/knowledge/backend.md` |
| `res.md §6` | PYTHON | `.sdd/knowledge/backend.md` |
| `res.md §7` | FASTAPI | `.sdd/knowledge/backend.md` |
| `res.md §8` | DJANGO | `.sdd/knowledge/backend.md` |
| `res.md §9` | FLASK | `.sdd/knowledge/backend.md` |
| `res.md §10` | GO | `.sdd/CONVENTIONS.md`<br>`.sdd/LAYOUT.md`<br>`.sdd/knowledge/backend.md` |
| `res.md §11` | GO FRAMEWORK | `.sdd/knowledge/backend.md` |
| `res.md §12` | TYPESCRIPT BACKEND | `.sdd/knowledge/backend.md` |
| `res.md §13` | NESTJS | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`AGENTS.md` |
| `res.md §14` | JAVA / KOTLIN | `.sdd/knowledge/backend.md` |
| `res.md §15` | SPRING BOOT | `.sdd/knowledge/backend.md` |
| `res.md §16` | FRONTEND DECISION | `.sdd/knowledge/frontend.md` |
| `res.md §17` | VUE | `.sdd/knowledge/frontend.md` |
| `res.md §18` | REACT | `.sdd/knowledge/frontend.md` |
| `res.md §19` | NEXT.JS | `.sdd/knowledge/frontend.md` |
| `res.md §20` | ANGULAR | `.sdd/knowledge/frontend.md` |
| `res.md §21` | FRONTEND ARCHITECTURE | `.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/frontend.md` |
| `res.md §22` | DATABASE DECISION | `.sdd/knowledge/database.md` |
| `res.md §23` | POSTGRESQL | `.sdd/knowledge/database.md`<br>`specs/001-project/technology-selection.md` |
| `res.md §24` | MYSQL | `.sdd/knowledge/database.md` |
| `res.md §25` | SQLITE | `.sdd/knowledge/database.md` |
| `res.md §26` | MONGODB | `.sdd/knowledge/database.md` |
| `res.md §27` | REDIS | `.sdd/knowledge/database.md` |
| `res.md §28` | ORM | `.sdd/knowledge/backend.md` |
| `res.md §29` | API STYLE | `.sdd/knowledge/api.md` |
| `res.md §30` | REST | `.sdd/knowledge/api.md` |
| `res.md §31` | GRAPHQL | `.sdd/knowledge/api.md` |
| `res.md §32` | GRPC | `.sdd/knowledge/api.md` |
| `res.md §33` | OPENAPI | `.sdd/knowledge/api.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md` |
| `res.md §34` | MESSAGE QUEUE | `.sdd/knowledge/messaging.md` |
| `res.md §35` | RABBITMQ | `.sdd/knowledge/messaging.md` |
| `res.md §36` | KAFKA | `.sdd/knowledge/messaging.md` |
| `res.md §37` | BACKGROUND JOBS | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/messaging.md` |
| `res.md §38` | SEARCH | `.sdd/knowledge/caching.md` |
| `res.md §39` | VECTOR SEARCH | `.sdd/knowledge/database.md` |
| `res.md §40` | OBJECT STORAGE | `.sdd/knowledge/database.md` |
| `res.md §41` | AUTHENTICATION | `.sdd/knowledge/security.md`<br>`.sdd/templates/design.md` |
| `res.md §42` | SESSION | `.sdd/knowledge/security.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md` |
| `res.md §43` | JWT | `.sdd/knowledge/security.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md` |
| `res.md §44` | OIDC / OAuth | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/security.md`<br>`.sdd/templates/design.md` |
| `res.md §45` | SECURITY | `.sdd/knowledge/security.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §46` | AUTHORIZATION | `.sdd/knowledge/security.md`<br>`specs/001-project/design.md` |
| `res.md §47` | OBSERVABILITY | `.sdd/knowledge/observability.md`<br>`specs/001-project/tasks.md` |
| `res.md §48` | LOGGING | `.sdd/knowledge/observability.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §49` | DISTRIBUTED TRACING | `.sdd/knowledge/observability.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md` |
| `res.md §50` | TESTING STRATEGY | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/workflows/refactor.md` |
| `res.md §51` | UNIT TEST | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/workflows/refactor.md`<br>`specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §52` | INTEGRATION TEST | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/workflows/refactor.md`<br>`specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §53` | E2E TEST | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/workflows/refactor.md`<br>`specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §54` | PYTHON TESTING | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md` |
| `res.md §55` | FRONTEND TESTING | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/testing.md` |
| `res.md §56` | GO TESTING | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md` |
| `res.md §57` | JAVA TESTING | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md` |
| `res.md §58` | CODE QUALITY | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/testing.md` |
| `res.md §59` | PACKAGE MANAGEMENT | `.sdd/knowledge/backend.md` |
| `res.md §60` | CONTAINERIZATION | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md` |
| `res.md §61` | DOCKER COMPOSE | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md` |
| `res.md §62` | KUBERNETES | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md` |
| `res.md §63` | CI/CD | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §64` | DATABASE MIGRATION | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md` |
| `res.md §65` | BACKUP | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md` |
| `res.md §66` | DATABASE DESIGN RULES | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §67` | TRANSACTION RULES | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/templates/design.md`<br>`.sdd/workflows/bugfix.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/adr/ADR-001-postgres.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §68` | ID STRATEGY | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §69` | TIME | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/plan.md` |
| `res.md §70` | API ERROR FORMAT | `.sdd/knowledge/api.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §71` | PAGINATION | `.sdd/knowledge/api.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §72` | RATE LIMITING | `.sdd/knowledge/api.md`<br>`.sdd/knowledge/caching.md`<br>`specs/001-project/plan.md` |
| `res.md §73` | CACHING | `.sdd/knowledge/api.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §74` | ASYNC ARCHITECTURE | `.sdd/knowledge/messaging.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §75` | FRONTEND STATE MANAGEMENT | `.sdd/knowledge/frontend.md`<br>`specs/001-project/plan.md` |
| `res.md §76` | UI COMPONENT LIBRARY | `.sdd/knowledge/frontend.md` |
| `res.md §77` | MONOREPO | `.sdd/knowledge/architecture.md` |
| `res.md §78` | REPOSITORY STRUCTURE | `.sdd/knowledge/backend.md`<br>`specs/001-project/plan.md` |
| `res.md §79` | Django | `.sdd/knowledge/backend.md` |
| `res.md §80` | Go | `.sdd/knowledge/backend.md` |
| `res.md §81` | NestJS | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`AGENTS.md` |
| `res.md §82` | Spring Boot | `.sdd/knowledge/backend.md` |
| `res.md §83` | VUE | `.sdd/knowledge/frontend.md` |
| `res.md §84` | REACT | `.sdd/knowledge/frontend.md` |
| `res.md §85` | NEXT.JS | `.sdd/knowledge/frontend.md` |
| `res.md §86` | CONFIGURATION | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/tasks.md` |
| `res.md §87` | SECRET MANAGEMENT | `.sdd/knowledge/deployment.md`<br>`.sdd/knowledge/security.md`<br>`specs/001-project/plan.md` |
| `res.md §88` | VERSION STRATEGY | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md` |
| `res.md §89` | VERSION PINNING | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md` |
| `res.md §90` | DEPENDENCY DECISION | `.sdd/workflows/small-change.md` |
| `res.md §91` | SPEC-DRIVEN DEVELOPMENT | `.sdd/templates/spec.md`<br>`.sdd/workflows/new-project.md`<br>`specs/001-project/spec.md` |
| `res.md §92` | SPEC ARTIFACTS | `.sdd/workflows/new-project.md`<br>`CHANGELOG.md` |
| `res.md §93` | PROJECT-LEVEL SPEC | `.sdd/workflows/new-project.md`<br>`CHANGELOG.md` |
| `res.md §94` | TECHNOLOGY-SELECTION.MD | `.sdd/templates/technology-selection.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §95` | DECISION RECORD FORMAT | `.sdd/templates/adr.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §96` | REQUIREMENTS | `.sdd/workflows/new-project.md` |
| `res.md §97` | ACCEPTANCE CRITERIA | `.sdd/workflows/new-project.md`<br>`specs/001-project/verification.md` |
| `res.md §98` | DESIGN | `.sdd/templates/design.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §99` | TASKS | `.sdd/templates/plan.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/workflows/new-project.md`<br>`specs/001-project/plan.md` |
| `res.md §100` | IMPLEMENTATION RULE | `.sdd/templates/plan.md`<br>`.sdd/workflows/new-project.md`<br>`specs/001-project/plan.md` |
| `res.md §101` | CHANGE MANAGEMENT | `.sdd/templates/plan.md`<br>`.sdd/workflows/bugfix.md`<br>`.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §102` | BROWNFIELD PROJECT | `.sdd/templates/project-discovery.md`<br>`.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`CLAUDE.md`<br>`specs/001-project/plan.md` |
| `res.md §103` | BROWNFIELD TECHNOLOGY RULE | `.sdd/workflows/new-project.md` |
| `res.md §104` | FEATURE DEVELOPMENT FLOW | `.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §105` | BUGFIX FLOW | `.sdd/workflows/bugfix.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §106` | REFACTOR FLOW | `.sdd/workflows/new-project.md`<br>`.sdd/workflows/refactor.md`<br>`.sdd/workflows/small-change.md` |
| `res.md §107` | AGENT QUESTION POLICY | `.sdd/workflows/new-project.md` |
| `res.md §108` | QUESTIONS CLASSIFICATION | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md`<br>`CLAUDE.md` |
| `res.md §109` | TECHNOLOGY DECISION OUTPUT | `.sdd/templates/technology-selection.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §110` | DEFAULT TECHNOLOGY MATRIX | `.sdd/knowledge/backend.md`<br>`.sdd/workflows/new-project.md`<br>`AGENTS.md` |
| `res.md §111` | DEFAULT FULL STACK | `.sdd/workflows/new-project.md` |
| `res.md §112` | DEFAULT AI APPLICATION STACK | `.sdd/workflows/new-project.md` |
| `res.md §113` | DEFAULT ENTERPRISE STACK | `.sdd/workflows/new-project.md` |
| `res.md §114` | DEFAULT HIGH-PERFORMANCE SERVICE | `.sdd/workflows/new-project.md` |
| `res.md §115` | TECHNOLOGY INTRODUCTION CHECKLIST | `.sdd/workflows/new-feature.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §116` | ARCHITECTURE REVIEW CHECKLIST | `.sdd/workflows/new-project.md` |
| `res.md §117` | FINAL SPEC REQUIREMENTS | `.sdd/README.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/spec.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`specs/001-project/verification.md` |
| `res.md §118` | FINAL AGENT BEHAVIOR | `.sdd/workflows/new-project.md` |
| `res.md §119` | GOLDEN RULE | `CLAUDE.md` |
| `res.md §120` | FINAL PRINCIPLE | `.sdd/README.md`<br>`AGENTS.md`<br>`CLAUDE.md`<br>`README.md`<br>`specs/001-project/technology-selection.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）


## Matrix（条目 59 条，含子条目）

| 源规则 | 标题 | 落点文件 |
| --- | --- | --- |
| `Matrix §1` | Agent 总决策协议 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/data.md`<br>`.sdd/templates/adr.md` |
| `Matrix §2` | 决策优先级 | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §3` | Hard Constraint / Soft Constraint | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/architecture.md` |
| `Matrix §3.1` | 　Hard Constraint | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §3.2` | 　Soft Constraint | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §4` | 项目类型矩阵 | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/architecture.md` |
| `Matrix §5` | Architecture Decision Matrix | `.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §5.1` | 　Monolith | `.sdd/templates/technology-selection.md` |
| `Matrix §5.2` | 　Modular Monolith | `specs/001-project/plan.md` |
| `Matrix §5.3` | 　Microservices | `specs/001-project/plan.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §6` | Backend Language Matrix | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md` |
| `Matrix §6.1` | 　Python | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §6.2` | 　Go | `.sdd/examples/high-concurrency.md`<br>`.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `Matrix §6.3` | 　TypeScript | `.sdd/knowledge/backend.md` |
| `Matrix §6.4` | 　Java / Kotlin | `.sdd/knowledge/backend.md` |
| `Matrix §6.5` | 　Rust | `.sdd/knowledge/backend.md` |
| `Matrix §7` | Backend Framework Matrix | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `Matrix §8` | Frontend Matrix | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `Matrix §8.1` | 　Vue | `.sdd/knowledge/frontend.md` |
| `Matrix §8.2` | 　React | `.sdd/knowledge/frontend.md` |
| `Matrix §8.3` | 　Next.js | `.sdd/knowledge/frontend.md` |
| `Matrix §8.4` | 　Angular | `.sdd/knowledge/frontend.md` |
| `Matrix §9` | Frontend / Backend Separation Matrix | `.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/frontend.md` |
| `Matrix §10` | Database Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/adr/ADR-001-postgres.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §11` | MySQL | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/adr/ADR-001-postgres.md` |
| `Matrix §12` | SQLite | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/knowledge/frontend.md`<br>`specs/001-project/adr/ADR-001-postgres.md` |
| `Matrix §13` | Redis Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §14` | ORM Matrix | `.sdd/knowledge/backend.md` |
| `Matrix §15` | API Protocol Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/api.md` |
| `Matrix §16` | Message Queue Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/messaging.md` |
| `Matrix §17` | Search Engine Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/caching.md`<br>`CHANGELOG.md` |
| `Matrix §18` | Vector Database Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/templates/adr.md` |
| `Matrix §19` | Object Storage Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §20` | Authentication Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/security.md`<br>`specs/001-project/adr/ADR-003-session-auth.md`<br>`specs/001-project/plan.md` |
| `Matrix §21` | Authorization Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/security.md` |
| `Matrix §22` | Multi-Tenant Matrix | `.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/database.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §23` | Caching Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/caching.md`<br>`CHANGELOG.md` |
| `Matrix §24` | Deployment Matrix | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md` |
| `Matrix §25` | Kubernetes Decision Rule | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md` |
| `Matrix §26` | Observability Matrix | `.sdd/knowledge/observability.md`<br>`specs/001-project/plan.md` |
| `Matrix §27` | Testing Matrix | `.sdd/knowledge/testing.md` |
| `Matrix §28` | Test Strategy Matrix | `.sdd/knowledge/data.md`<br>`.sdd/knowledge/testing.md`<br>`specs/001-project/plan.md` |
| `Matrix §29` | AI Application Matrix | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md` |
| `Matrix §30` | LLM Provider Architecture | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/examples/ai-saas.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md` |
| `Matrix §31` | RAG Matrix | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md` |
| `Matrix §32` | Architecture Complexity Budget | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/templates/technology-selection.md` |
| `Matrix §33` | Infrastructure Introduction Rule | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/messaging.md` |
| `Matrix §34` | Existing Project Decision Matrix | `.sdd/examples/brownfield.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md`<br>`specs/001-project/plan.md` |
| `Matrix §35` | Existing Stack Conflict | `.sdd/examples/brownfield.md`<br>`specs/001-project/plan.md` |
| `Matrix §36` | Technology Selection Scoring | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md`<br>`AGENTS.md` |
| `Matrix §37` | Example | `.sdd/examples/saas.md` |
| `Matrix §38` | Example: AI SaaS | `.sdd/examples/ai-saas.md` |
| `Matrix §39` | Example: High-Concurrency Service | `.sdd/examples/high-concurrency.md` |
| `Matrix §40` | Decision Output Schema | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §41` | Decision Status | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §42` | 哪些决策必须人工确认 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/security.md` |
| `Matrix §43` | Agent Decision Loop | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-project.md` |
| `Matrix §44` | 最终 Agent Rule | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/ai-llm.md`<br>`CHANGELOG.md` |
| `Matrix §45` | 推荐最终目录 | `.sdd/CONVENTIONS.md`<br>`.sdd/LAYOUT.md`<br>`.sdd/knowledge/deployment.md`<br>`CHANGELOG.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）


## 知识库（条目 103 条，含子条目）

| 源规则 | 标题 | 落点文件 |
| --- | --- | --- |
| `知识库 §1` | 文档目标 | `.sdd/LAYOUT.md` |
| `知识库 §2` | 总体原则 | `.sdd/README.md` |
| `知识库 §2.1` | 　默认原则 | `.sdd/README.md` |
| `知识库 §3` | 架构选择总决策树 | `.sdd/knowledge/architecture.md` |
| `知识库 §4` | 项目类型分类 | `.sdd/knowledge/architecture.md` |
| `知识库 §4.1` | 　Web Application | `.sdd/knowledge/architecture.md` |
| `知识库 §4.2` | 　API / Backend Service | `.sdd/knowledge/architecture.md` |
| `知识库 §4.3` | 　Data / AI Application | `.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/data.md` |
| `知识库 §4.4` | 　CLI / Automation | `.sdd/knowledge/data.md` |
| `知识库 §4.5` | 　Worker / Background Job | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/data.md`<br>`.sdd/knowledge/messaging.md` |
| `知识库 §5` | 编程语言选择 | `.sdd/knowledge/backend.md` |
| `知识库 §5.1` | 　Python | `.sdd/knowledge/backend.md` |
| `知识库 §6` | Python Web Framework | `.sdd/knowledge/backend.md` |
| `知识库 §6.1` | 　FastAPI —— 默认 API 首选 | `.sdd/knowledge/backend.md` |
| `知识库 §6.2` | 　Flask | `.sdd/knowledge/backend.md` |
| `知识库 §6.3` | 　Django | `.sdd/knowledge/backend.md` |
| `知识库 §7` | Go | `.sdd/knowledge/backend.md` |
| `知识库 §8` | Go Web Framework | `.sdd/knowledge/backend.md` |
| `知识库 §8.1` | 　Gin | `.sdd/knowledge/backend.md` |
| `知识库 §8.2` | 　Echo | `.sdd/knowledge/backend.md` |
| `知识库 §8.3` | 　net/http | `.sdd/knowledge/backend.md` |
| `知识库 §9` | TypeScript / Node.js | `.sdd/knowledge/backend.md` |
| `知识库 §10` | Java / Kotlin | `.sdd/knowledge/backend.md` |
| `知识库 §11` | Rust | `.sdd/knowledge/backend.md` |
| `知识库 §12` | 前后端架构 | `.sdd/knowledge/frontend.md` |
| `知识库 §12.1` | 　前后端分离 | `.sdd/knowledge/architecture.md` |
| `知识库 §13` | 前后端合并 | `.sdd/knowledge/frontend.md` |
| `知识库 §14` | Vue | `.sdd/knowledge/frontend.md` |
| `知识库 §15` | React | `.sdd/knowledge/frontend.md` |
| `知识库 §16` | Next.js | `.sdd/knowledge/frontend.md` |
| `知识库 §17` | Angular | `.sdd/knowledge/frontend.md` |
| `知识库 §18` | CSS/UI 技术 | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §19` | UI Component Library | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §20` | Database 选择 | `.sdd/knowledge/database.md` |
| `知识库 §21` | PostgreSQL | `.sdd/knowledge/database.md` |
| `知识库 §22` | MySQL | `.sdd/knowledge/database.md` |
| `知识库 §23` | SQLite | `.sdd/knowledge/database.md` |
| `知识库 §24` | Redis | `.sdd/knowledge/database.md` |
| `知识库 §25` | ORM | `.sdd/knowledge/backend.md` |
| `知识库 §26` | API 风格 | `.sdd/knowledge/api.md` |
| `知识库 §27` | GraphQL | `.sdd/knowledge/api.md` |
| `知识库 §28` | gRPC | `.sdd/knowledge/api.md` |
| `知识库 §29` | Message Queue | `.sdd/knowledge/messaging.md` |
| `知识库 §30` | 搜索 | `.sdd/knowledge/caching.md` |
| `知识库 §31` | Vector Database | `.sdd/knowledge/database.md` |
| `知识库 §32` | Object Storage | `.sdd/knowledge/database.md` |
| `知识库 §33` | Authentication | `.sdd/knowledge/security.md`<br>`specs/001-project/adr/ADR-003-session-auth.md`<br>`specs/001-project/plan.md` |
| `知识库 §34` | Authorization | `.sdd/knowledge/messaging.md`<br>`.sdd/knowledge/security.md`<br>`specs/001-project/plan.md` |
| `知识库 §35` | API Security | `.sdd/knowledge/security.md` |
| `知识库 §36` | Configuration | `.sdd/knowledge/security.md` |
| `知识库 §37` | Logging | `.sdd/knowledge/observability.md` |
| `知识库 §38` | Observability | `.sdd/knowledge/observability.md` |
| `知识库 §39` | Testing | `.sdd/knowledge/testing.md`<br>`specs/001-project/plan.md` |
| `知识库 §40` | Python Testing | `.sdd/knowledge/testing.md` |
| `知识库 §41` | Frontend Testing | `.sdd/knowledge/testing.md` |
| `知识库 §42` | Go Testing | `.sdd/knowledge/testing.md` |
| `知识库 §43` | Java Testing | `.sdd/knowledge/testing.md` |
| `知识库 §44` | Container | `.sdd/knowledge/deployment.md` |
| `知识库 §45` | Kubernetes | `.sdd/knowledge/deployment.md` |
| `知识库 §46` | CI/CD | `.sdd/knowledge/deployment.md` |
| `知识库 §47` | Python 项目工具链 | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `知识库 §48` | Go 项目工具链 | `.sdd/knowledge/backend.md`<br>`.sdd/knowledge/deployment.md` |
| `知识库 §49` | Frontend Vue 工具链 | `.sdd/knowledge/frontend.md` |
| `知识库 §50` | Frontend React 工具链 | `.sdd/knowledge/frontend.md` |
| `知识库 §51` | 前端状态管理 | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §52` | API Client | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/api.md`<br>`.sdd/knowledge/frontend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md` |
| `知识库 §53` | API Contract | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/api.md`<br>`.sdd/knowledge/frontend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md` |
| `知识库 §54` | Monorepo | `.sdd/knowledge/architecture.md` |
| `知识库 §55` | Repository Structure | `.sdd/knowledge/backend.md` |
| `知识库 §56` | Go Backend | `.sdd/knowledge/backend.md` |
| `知识库 §57` | Vue Frontend | `.sdd/knowledge/frontend.md` |
| `知识库 §58` | React Frontend | `.sdd/knowledge/frontend.md` |
| `知识库 §59` | 推荐的默认技术栈 | `.sdd/workflows/new-project.md`<br>`AGENTS.md`<br>`CHANGELOG.md` |
| `知识库 §60` | AI / RAG SaaS | `.sdd/examples/ai-saas.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md` |
| `知识库 §61` | 高并发 API | `.sdd/examples/high-concurrency.md`<br>`.sdd/workflows/new-project.md`<br>`CHANGELOG.md` |
| `知识库 §62` | 企业 Java 系统 | `.sdd/workflows/new-project.md`<br>`CHANGELOG.md` |
| `知识库 §63` | 小型内部工具 | `.sdd/examples/internal-tool.md` |
| `知识库 §64` | MVP | `.sdd/decision-trees/decision-protocol.md` |
| `知识库 §65` | 微服务决策 | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §66` | Event-Driven Architecture | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/messaging.md` |
| `知识库 §67` | CQRS | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §68` | Event Sourcing | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §69` | DDD | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §70` | AI Coding 特殊要求 | `.sdd/knowledge/architecture.md` |
| `知识库 §71` | Agent 不得自行做的决定 | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/examples/brownfield.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/security.md`<br>`CLAUDE.md` |
| `知识库 §72` | 技术选型评分模型 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md` |
| `知识库 §73` | 技术选择必须记录理由 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/adr.md` |
| `知识库 §74` | Agent 技术选型规则 | `.sdd/decision-trees/decision-protocol.md` |
| `知识库 §75` | Existing Project 特殊规则 | `.sdd/examples/brownfield.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §76` | Agent 生成 spec.md 时必须包含的架构上下文 | `.sdd/templates/spec.md` |
| `知识库 §77` | plan.md 必须包含 | `.sdd/templates/plan.md`<br>`.sdd/templates/spec.md` |
| `知识库 §78` | 推荐的 SDD Artifact | `.sdd/LAYOUT.md`<br>`CHANGELOG.md` |
| `知识库 §79` | 推荐的 spec.md 模板 | `.sdd/templates/spec.md`<br>`CHANGELOG.md` |
| `知识库 §80` | 推荐的 plan.md 技术架构模板 | `.sdd/templates/plan.md`<br>`specs/001-project/design.md` |
| `知识库 §81` | Agent 生成项目 Spec 的最终规则 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §82` | 技术栈选择的默认优先级 | `.sdd/workflows/new-project.md`<br>`AGENTS.md` |
| `知识库 §83` | 默认不要使用的复杂技术 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §84` | AI Agent 的最终输出格式 | `.sdd/templates/technology-selection.md` |
| `知识库 §85` | 最重要的规则 | `.sdd/decision-trees/decision-protocol.md`<br>`AGENTS.md` |
| `知识库 §86` | 最终 SDD Traceability | `.sdd/README.md` |
| `知识库 §87` | 给 AI Agent 的总指令 | `AGENTS.md`<br>`CLAUDE.md` |
| `知识库 §88` | 与 Spec Kit / OpenSpec 的结合方式 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/spec.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §89` | 推荐最终目录 | `.sdd/LAYOUT.md` |

**未被引用（顶层 自身及子条目均未出现 / 子条目 未出现）：0 条**

（无）


---

## 关于「未被引用」

机器只能判断「有无写明出处」，不能判断「内容是否已被覆盖」。清单需人工分诊：

- **已覆盖未标注**：内容已在知识/决策文件中表达，只是没写来源条号 —— 补标注即可。
- **真实落点缺失**：该规则在本仓确无对应内容 —— 需新增落点，或在此显式登记为不适用。

> **引用率 ≠ 内容覆盖率。** 下表全空只说明「每条源规则都至少被一处声明为来源」，不说明该条已被完整、正确地落地。内容质量仍需人工评审。

**已确认的真实缺口**：（无）

---

## 校验：引用了不存在的条号（应为空）

（无）
