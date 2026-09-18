# TRACEABILITY.md — 源规则 → 落点反向索引

> 本文件由 `scripts/gen_traceability.py` **自动生成，请勿手工编辑**。

> 用途：源文档升级时快速评估影响面——某条规则被本仓哪些文件引用。

> 引用约定见 `.sdd/CONVENTIONS.md` §1。


---


## res.md（共 120 条）

| 源规则 | 标题 | 落点文件 |
| --- | --- | --- |
| `res.md §0` | CORE MISSION | `.sdd/workflows/new-project.md`<br>`specs/001-project/verification.md` |
| `res.md §1` | GENERAL ENGINEERING PRINCIPLES | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/backend.md` |
| `res.md §2` | PROJECT DISCOVERY | `.sdd/CONVENTIONS.md`<br>`.sdd/templates/project-discovery.md` |
| `res.md §3` | PROJECT SCALE CLASSIFICATION | `.sdd/templates/project-discovery.md` |
| `res.md §4` | ARCHITECTURE STYLE | **（未引用）** |
| `res.md §5` | BACKEND LANGUAGE DECISION | `.sdd/knowledge/backend.md` |
| `res.md §6` | PYTHON | **（未引用）** |
| `res.md §7` | FASTAPI | **（未引用）** |
| `res.md §8` | DJANGO | **（未引用）** |
| `res.md §9` | FLASK | **（未引用）** |
| `res.md §10` | GO | **（未引用）** |
| `res.md §11` | GO FRAMEWORK | **（未引用）** |
| `res.md §12` | TYPESCRIPT BACKEND | **（未引用）** |
| `res.md §13` | NESTJS | **（未引用）** |
| `res.md §14` | JAVA / KOTLIN | **（未引用）** |
| `res.md §15` | SPRING BOOT | **（未引用）** |
| `res.md §16` | FRONTEND DECISION | `.sdd/knowledge/frontend.md` |
| `res.md §17` | VUE | **（未引用）** |
| `res.md §18` | REACT | **（未引用）** |
| `res.md §19` | NEXT.JS | **（未引用）** |
| `res.md §20` | ANGULAR | **（未引用）** |
| `res.md §21` | FRONTEND ARCHITECTURE | `.sdd/knowledge/architecture.md` |
| `res.md §22` | DATABASE DECISION | `.sdd/knowledge/database.md` |
| `res.md §23` | POSTGRESQL | `.sdd/knowledge/database.md`<br>`specs/001-project/technology-selection.md` |
| `res.md §24` | MYSQL | `.sdd/knowledge/database.md` |
| `res.md §25` | SQLITE | `.sdd/knowledge/database.md` |
| `res.md §26` | MONGODB | **（未引用）** |
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
| `res.md §38` | SEARCH | **（未引用）** |
| `res.md §39` | VECTOR SEARCH | `.sdd/knowledge/database.md` |
| `res.md §40` | OBJECT STORAGE | `.sdd/knowledge/database.md` |
| `res.md §41` | AUTHENTICATION | `.sdd/knowledge/security.md`<br>`.sdd/templates/design.md` |
| `res.md §42` | SESSION | `.sdd/knowledge/security.md`<br>`specs/001-project/design.md` |
| `res.md §43` | JWT | `.sdd/knowledge/security.md`<br>`specs/001-project/design.md` |
| `res.md §44` | OIDC / OAuth | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/security.md` |
| `res.md §45` | SECURITY | `.sdd/knowledge/security.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §46` | AUTHORIZATION | `.sdd/knowledge/security.md`<br>`specs/001-project/design.md` |
| `res.md §47` | OBSERVABILITY | `.sdd/knowledge/observability.md`<br>`specs/001-project/tasks.md` |
| `res.md §48` | LOGGING | `.sdd/knowledge/observability.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §49` | DISTRIBUTED TRACING | `.sdd/knowledge/observability.md`<br>`specs/001-project/plan.md` |
| `res.md §50` | TESTING STRATEGY | `.sdd/knowledge/testing.md`<br>`.sdd/templates/tasks.md`<br>`.sdd/workflows/refactor.md` |
| `res.md §51` | UNIT TEST | `specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §52` | INTEGRATION TEST | `specs/001-project/verification.md` |
| `res.md §53` | E2E TEST | `specs/001-project/tasks.md`<br>`specs/001-project/verification.md` |
| `res.md §54` | PYTHON TESTING | `.sdd/knowledge/testing.md` |
| `res.md §55` | FRONTEND TESTING | **（未引用）** |
| `res.md §56` | GO TESTING | **（未引用）** |
| `res.md §57` | JAVA TESTING | **（未引用）** |
| `res.md §58` | CODE QUALITY | `.sdd/knowledge/testing.md` |
| `res.md §59` | PACKAGE MANAGEMENT | `.sdd/knowledge/backend.md` |
| `res.md §60` | CONTAINERIZATION | `.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md` |
| `res.md §61` | DOCKER COMPOSE | **（未引用）** |
| `res.md §62` | KUBERNETES | **（未引用）** |
| `res.md §63` | CI/CD | `.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §64` | DATABASE MIGRATION | `.sdd/knowledge/deployment.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/tasks.md` |
| `res.md §65` | BACKUP | `.sdd/knowledge/deployment.md` |
| `res.md §66` | DATABASE DESIGN RULES | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §67` | TRANSACTION RULES | `.sdd/CONVENTIONS.md`<br>`.sdd/knowledge/database.md`<br>`.sdd/templates/design.md`<br>`.sdd/workflows/bugfix.md`<br>`.sdd/workflows/small-change.md`<br>`specs/001-project/adr/ADR-001-postgres.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §68` | ID STRATEGY | `.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §69` | TIME | `specs/001-project/plan.md` |
| `res.md §70` | API ERROR FORMAT | `.sdd/knowledge/api.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §71` | PAGINATION | `.sdd/knowledge/api.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §72` | RATE LIMITING | `specs/001-project/plan.md` |
| `res.md §73` | CACHING | `.sdd/knowledge/caching.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §74` | ASYNC ARCHITECTURE | `.sdd/knowledge/messaging.md`<br>`.sdd/templates/design.md`<br>`specs/001-project/design.md`<br>`specs/001-project/plan.md` |
| `res.md §75` | FRONTEND STATE MANAGEMENT | `.sdd/knowledge/frontend.md`<br>`specs/001-project/plan.md` |
| `res.md §76` | UI COMPONENT LIBRARY | **（未引用）** |
| `res.md §77` | MONOREPO | `.sdd/knowledge/architecture.md` |
| `res.md §78` | REPOSITORY STRUCTURE | `specs/001-project/plan.md` |
| `res.md §79` | Django | **（未引用）** |
| `res.md §80` | Go | **（未引用）** |
| `res.md §81` | NestJS | **（未引用）** |
| `res.md §82` | Spring Boot | **（未引用）** |
| `res.md §83` | VUE | **（未引用）** |
| `res.md §84` | REACT | **（未引用）** |
| `res.md §85` | NEXT.JS | **（未引用）** |
| `res.md §86` | CONFIGURATION | `.sdd/knowledge/deployment.md`<br>`specs/001-project/tasks.md` |
| `res.md §87` | SECRET MANAGEMENT | `.sdd/knowledge/security.md`<br>`specs/001-project/plan.md` |
| `res.md §88` | VERSION STRATEGY | **（未引用）** |
| `res.md §89` | VERSION PINNING | **（未引用）** |
| `res.md §90` | DEPENDENCY DECISION | `.sdd/workflows/small-change.md` |
| `res.md §91` | SPEC-DRIVEN DEVELOPMENT | `.sdd/templates/spec.md`<br>`specs/001-project/spec.md` |
| `res.md §92` | SPEC ARTIFACTS | **（未引用）** |
| `res.md §93` | PROJECT-LEVEL SPEC | **（未引用）** |
| `res.md §94` | TECHNOLOGY-SELECTION.MD | `.sdd/templates/technology-selection.md` |
| `res.md §95` | DECISION RECORD FORMAT | `.sdd/templates/adr.md` |
| `res.md §96` | REQUIREMENTS | **（未引用）** |
| `res.md §97` | ACCEPTANCE CRITERIA | `specs/001-project/verification.md` |
| `res.md §98` | DESIGN | `.sdd/templates/design.md` |
| `res.md §99` | TASKS | `.sdd/templates/plan.md`<br>`.sdd/templates/tasks.md`<br>`specs/001-project/plan.md` |
| `res.md §100` | IMPLEMENTATION RULE | `.sdd/templates/plan.md`<br>`.sdd/workflows/new-project.md` |
| `res.md §101` | CHANGE MANAGEMENT | `.sdd/templates/plan.md`<br>`.sdd/workflows/bugfix.md`<br>`.sdd/workflows/new-feature.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/verification.md` |
| `res.md §102` | BROWNFIELD PROJECT | `.sdd/templates/project-discovery.md`<br>`specs/001-project/plan.md` |
| `res.md §103` | BROWNFIELD TECHNOLOGY RULE | **（未引用）** |
| `res.md §104` | FEATURE DEVELOPMENT FLOW | `.sdd/workflows/new-feature.md` |
| `res.md §105` | BUGFIX FLOW | `.sdd/workflows/bugfix.md` |
| `res.md §106` | REFACTOR FLOW | `.sdd/workflows/refactor.md`<br>`.sdd/workflows/small-change.md` |
| `res.md §107` | AGENT QUESTION POLICY | **（未引用）** |
| `res.md §108` | QUESTIONS CLASSIFICATION | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-feature.md` |
| `res.md §109` | TECHNOLOGY DECISION OUTPUT | **（未引用）** |
| `res.md §110` | DEFAULT TECHNOLOGY MATRIX | `.sdd/workflows/new-project.md` |
| `res.md §111` | DEFAULT FULL STACK | **（未引用）** |
| `res.md §112` | DEFAULT AI APPLICATION STACK | **（未引用）** |
| `res.md §113` | DEFAULT ENTERPRISE STACK | **（未引用）** |
| `res.md §114` | DEFAULT HIGH-PERFORMANCE SERVICE | **（未引用）** |
| `res.md §115` | TECHNOLOGY INTRODUCTION CHECKLIST | `.sdd/workflows/new-feature.md` |
| `res.md §116` | ARCHITECTURE REVIEW CHECKLIST | `.sdd/workflows/new-project.md` |
| `res.md §117` | FINAL SPEC REQUIREMENTS | `.sdd/README.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/spec.md`<br>`specs/001-project/verification.md` |
| `res.md §118` | FINAL AGENT BEHAVIOR | **（未引用）** |
| `res.md §119` | GOLDEN RULE | **（未引用）** |
| `res.md §120` | FINAL PRINCIPLE | `.sdd/README.md`<br>`specs/001-project/technology-selection.md` |

**未被显式引用的条号（44 条，非缺陷，仅供覆盖率参考）**：
res.md §4、res.md §6、res.md §7、res.md §8、res.md §9、res.md §10、res.md §11、res.md §12、res.md §13、res.md §14、res.md §15、res.md §17、res.md §18、res.md §19、res.md §20、res.md §26、res.md §38、res.md §55、res.md §56、res.md §57、res.md §61、res.md §62、res.md §76、res.md §79、res.md §80、res.md §81、res.md §82、res.md §83、res.md §84、res.md §85、res.md §88、res.md §89、res.md §92、res.md §93、res.md §96、res.md §103、res.md §107、res.md §109、res.md §111、res.md §112、res.md §113、res.md §114、res.md §118、res.md §119


## Matrix（共 45 条）

| 源规则 | 标题 | 落点文件 |
| --- | --- | --- |
| `Matrix §1` | Agent 总决策协议 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/adr.md` |
| `Matrix §2` | 决策优先级 | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §3` | Hard Constraint / Soft Constraint | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/architecture.md` |
| `Matrix §4` | 项目类型矩阵 | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md` |
| `Matrix §5` | Architecture Decision Matrix | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §6` | Backend Language Matrix | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/backend.md`<br>`.sdd/examples/high-concurrency.md`<br>`.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §7` | Backend Framework Matrix | `.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `Matrix §8` | Frontend Matrix | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `Matrix §9` | Frontend / Backend Separation Matrix | `.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/frontend.md` |
| `Matrix §10` | Database Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md`<br>`specs/001-project/adr/ADR-001-postgres.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §11` | MySQL | `.sdd/knowledge/database.md`<br>`specs/001-project/adr/ADR-001-postgres.md` |
| `Matrix §12` | SQLite | `.sdd/knowledge/database.md`<br>`specs/001-project/adr/ADR-001-postgres.md` |
| `Matrix §13` | Redis Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/caching.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §14` | ORM Matrix | **（未引用）** |
| `Matrix §15` | API Protocol Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/api.md` |
| `Matrix §16` | Message Queue Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/messaging.md` |
| `Matrix §17` | Search Engine Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/caching.md` |
| `Matrix §18` | Vector Database Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §19` | Object Storage Matrix | `.sdd/decision-trees/database.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §20` | Authentication Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/security.md`<br>`specs/001-project/adr/ADR-003-session-auth.md`<br>`specs/001-project/plan.md` |
| `Matrix §21` | Authorization Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/security.md` |
| `Matrix §22` | Multi-Tenant Matrix | `.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/database.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/database.md` |
| `Matrix §23` | Caching Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/caching.md` |
| `Matrix §24` | Deployment Matrix | `.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md` |
| `Matrix §25` | Kubernetes Decision Rule | `.sdd/knowledge/deployment.md`<br>`specs/001-project/plan.md` |
| `Matrix §26` | Observability Matrix | `.sdd/knowledge/observability.md`<br>`specs/001-project/plan.md` |
| `Matrix §27` | Testing Matrix | `.sdd/knowledge/testing.md` |
| `Matrix §28` | Test Strategy Matrix | `.sdd/knowledge/data.md`<br>`.sdd/knowledge/testing.md`<br>`specs/001-project/plan.md` |
| `Matrix §29` | AI Application Matrix | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/knowledge/ai-llm.md` |
| `Matrix §30` | LLM Provider Architecture | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/examples/ai-saas.md`<br>`.sdd/knowledge/ai-llm.md` |
| `Matrix §31` | RAG Matrix | `.sdd/decision-trees/ai-llm.md`<br>`.sdd/knowledge/ai-llm.md` |
| `Matrix §32` | Architecture Complexity Budget | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/architecture.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/decision-trees/infrastructure.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/templates/technology-selection.md` |
| `Matrix §33` | Infrastructure Introduction Rule | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §34` | Existing Project Decision Matrix | `.sdd/examples/brownfield.md`<br>`.sdd/workflows/new-project.md`<br>`specs/001-project/plan.md` |
| `Matrix §35` | Existing Stack Conflict | **（未引用）** |
| `Matrix §36` | Technology Selection Scoring | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md` |
| `Matrix §37` | Example | `.sdd/examples/saas.md` |
| `Matrix §38` | Example: AI SaaS | `.sdd/examples/ai-saas.md` |
| `Matrix §39` | Example: High-Concurrency Service | `.sdd/examples/high-concurrency.md` |
| `Matrix §40` | Decision Output Schema | `.sdd/templates/technology-selection.md`<br>`specs/001-project/technology-selection.md` |
| `Matrix §41` | Decision Status | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §42` | 哪些决策必须人工确认 | `.sdd/decision-trees/decision-protocol.md` |
| `Matrix §43` | Agent Decision Loop | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/workflows/new-project.md` |
| `Matrix §44` | 最终 Agent Rule | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/ai-llm.md` |
| `Matrix §45` | 推荐最终目录 | **（未引用）** |

**未被显式引用的条号（3 条，非缺陷，仅供覆盖率参考）**：
Matrix §14、Matrix §35、Matrix §45


## 知识库（共 89 条）

| 源规则 | 标题 | 落点文件 |
| --- | --- | --- |
| `知识库 §1` | 文档目标 | **（未引用）** |
| `知识库 §2` | 总体原则 | **（未引用）** |
| `知识库 §3` | 架构选择总决策树 | `.sdd/knowledge/architecture.md` |
| `知识库 §4` | 项目类型分类 | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/backend.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/backend.md`<br>`.sdd/knowledge/data.md`<br>`.sdd/knowledge/messaging.md` |
| `知识库 §5` | 编程语言选择 | `.sdd/knowledge/backend.md` |
| `知识库 §6` | Python Web Framework | **（未引用）** |
| `知识库 §7` | Go | **（未引用）** |
| `知识库 §8` | Go Web Framework | **（未引用）** |
| `知识库 §9` | TypeScript / Node.js | **（未引用）** |
| `知识库 §10` | Java / Kotlin | **（未引用）** |
| `知识库 §11` | Rust | **（未引用）** |
| `知识库 §12` | 前后端架构 | `.sdd/knowledge/frontend.md` |
| `知识库 §13` | 前后端合并 | **（未引用）** |
| `知识库 §14` | Vue | **（未引用）** |
| `知识库 §15` | React | **（未引用）** |
| `知识库 §16` | Next.js | `.sdd/knowledge/frontend.md` |
| `知识库 §17` | Angular | `.sdd/knowledge/frontend.md` |
| `知识库 §18` | CSS/UI 技术 | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §19` | UI Component Library | **（未引用）** |
| `知识库 §20` | Database 选择 | `.sdd/knowledge/database.md` |
| `知识库 §21` | PostgreSQL | **（未引用）** |
| `知识库 §22` | MySQL | **（未引用）** |
| `知识库 §23` | SQLite | **（未引用）** |
| `知识库 §24` | Redis | **（未引用）** |
| `知识库 §25` | ORM | `.sdd/knowledge/backend.md` |
| `知识库 §26` | API 风格 | `.sdd/knowledge/api.md` |
| `知识库 §27` | GraphQL | **（未引用）** |
| `知识库 §28` | gRPC | **（未引用）** |
| `知识库 §29` | Message Queue | **（未引用）** |
| `知识库 §30` | 搜索 | **（未引用）** |
| `知识库 §31` | Vector Database | `.sdd/knowledge/database.md` |
| `知识库 §32` | Object Storage | `.sdd/knowledge/database.md` |
| `知识库 §33` | Authentication | `.sdd/knowledge/security.md`<br>`specs/001-project/adr/ADR-003-session-auth.md`<br>`specs/001-project/plan.md` |
| `知识库 §34` | Authorization | `.sdd/knowledge/security.md`<br>`specs/001-project/plan.md` |
| `知识库 §35` | API Security | `.sdd/knowledge/security.md` |
| `知识库 §36` | Configuration | **（未引用）** |
| `知识库 §37` | Logging | `.sdd/knowledge/observability.md` |
| `知识库 §38` | Observability | `.sdd/knowledge/observability.md` |
| `知识库 §39` | Testing | `.sdd/knowledge/testing.md`<br>`specs/001-project/plan.md` |
| `知识库 §40` | Python Testing | `.sdd/knowledge/testing.md` |
| `知识库 §41` | Frontend Testing | **（未引用）** |
| `知识库 §42` | Go Testing | **（未引用）** |
| `知识库 §43` | Java Testing | **（未引用）** |
| `知识库 §44` | Container | `.sdd/knowledge/deployment.md` |
| `知识库 §45` | Kubernetes | `.sdd/knowledge/deployment.md` |
| `知识库 §46` | CI/CD | `.sdd/knowledge/deployment.md` |
| `知识库 §47` | Python 项目工具链 | `.sdd/knowledge/backend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md` |
| `知识库 §48` | Go 项目工具链 | **（未引用）** |
| `知识库 §49` | Frontend Vue 工具链 | **（未引用）** |
| `知识库 §50` | Frontend React 工具链 | **（未引用）** |
| `知识库 §51` | 前端状态管理 | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/frontend.md` |
| `知识库 §52` | API Client | `.sdd/decision-trees/frontend.md`<br>`.sdd/knowledge/api.md`<br>`.sdd/knowledge/frontend.md`<br>`specs/001-project/adr/ADR-002-fastapi.md`<br>`specs/001-project/plan.md` |
| `知识库 §53` | API Contract | **（未引用）** |
| `知识库 §54` | Monorepo | `.sdd/knowledge/architecture.md` |
| `知识库 §55` | Repository Structure | `.sdd/knowledge/backend.md` |
| `知识库 §56` | Go Backend | **（未引用）** |
| `知识库 §57` | Vue Frontend | `.sdd/knowledge/frontend.md` |
| `知识库 §58` | React Frontend | **（未引用）** |
| `知识库 §59` | 推荐的默认技术栈 | `.sdd/workflows/new-project.md` |
| `知识库 §60` | AI / RAG SaaS | `.sdd/examples/ai-saas.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §61` | 高并发 API | `.sdd/examples/high-concurrency.md`<br>`.sdd/workflows/new-project.md` |
| `知识库 §62` | 企业 Java 系统 | `.sdd/workflows/new-project.md` |
| `知识库 §63` | 小型内部工具 | `.sdd/examples/internal-tool.md` |
| `知识库 §64` | MVP | **（未引用）** |
| `知识库 §65` | 微服务决策 | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §66` | Event-Driven Architecture | `.sdd/decision-trees/architecture.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/messaging.md` |
| `知识库 §67` | CQRS | **（未引用）** |
| `知识库 §68` | Event Sourcing | **（未引用）** |
| `知识库 §69` | DDD | **（未引用）** |
| `知识库 §70` | AI Coding 特殊要求 | **（未引用）** |
| `知识库 §71` | Agent 不得自行做的决定 | `.sdd/CONVENTIONS.md`<br>`.sdd/decision-trees/decision-protocol.md`<br>`.sdd/examples/brownfield.md`<br>`.sdd/knowledge/ai-llm.md`<br>`.sdd/knowledge/architecture.md`<br>`.sdd/knowledge/security.md` |
| `知识库 §72` | 技术选型评分模型 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/templates/technology-selection.md` |
| `知识库 §73` | 技术选择必须记录理由 | `.sdd/templates/adr.md` |
| `知识库 §74` | Agent 技术选型规则 | **（未引用）** |
| `知识库 §75` | Existing Project 特殊规则 | `.sdd/workflows/new-project.md` |
| `知识库 §76` | Agent 生成 spec.md 时必须包含的架构上下文 | `.sdd/templates/spec.md` |
| `知识库 §77` | plan.md 必须包含 | `.sdd/templates/plan.md`<br>`.sdd/templates/spec.md` |
| `知识库 §78` | 推荐的 SDD Artifact | **（未引用）** |
| `知识库 §79` | 推荐的 spec.md 模板 | **（未引用）** |
| `知识库 §80` | 推荐的 plan.md 技术架构模板 | `specs/001-project/design.md` |
| `知识库 §81` | Agent 生成项目 Spec 的最终规则 | `.sdd/workflows/new-project.md` |
| `知识库 §82` | 技术栈选择的默认优先级 | `.sdd/workflows/new-project.md` |
| `知识库 §83` | 默认不要使用的复杂技术 | `.sdd/decision-trees/decision-protocol.md`<br>`.sdd/knowledge/architecture.md` |
| `知识库 §84` | AI Agent 的最终输出格式 | `.sdd/templates/technology-selection.md` |
| `知识库 §85` | 最重要的规则 | **（未引用）** |
| `知识库 §86` | 最终 SDD Traceability | **（未引用）** |
| `知识库 §87` | 给 AI Agent 的总指令 | **（未引用）** |
| `知识库 §88` | 与 Spec Kit / OpenSpec 的结合方式 | `.sdd/decision-trees/decision-protocol.md` |
| `知识库 §89` | 推荐最终目录 | **（未引用）** |

**未被显式引用的条号（42 条，非缺陷，仅供覆盖率参考）**：
知识库 §1、知识库 §2、知识库 §6、知识库 §7、知识库 §8、知识库 §9、知识库 §10、知识库 §11、知识库 §13、知识库 §14、知识库 §15、知识库 §19、知识库 §21、知识库 §22、知识库 §23、知识库 §24、知识库 §27、知识库 §28、知识库 §29、知识库 §30、知识库 §36、知识库 §41、知识库 §42、知识库 §43、知识库 §48、知识库 §49、知识库 §50、知识库 §53、知识库 §56、知识库 §58、知识库 §64、知识库 §67、知识库 §68、知识库 §69、知识库 §70、知识库 §74、知识库 §78、知识库 §79、知识库 §85、知识库 §86、知识库 §87、知识库 §89


---

## 校验：引用了不存在的条号（应为空）

（无）
