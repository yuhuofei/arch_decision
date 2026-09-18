# AGENTS.md — General Agent Engineering Rules

> 通用 Agent 软件工程与 Spec-Driven Development 规则。详细知识库见 `.sdd/`。
> 来源：res.md（AGENT PROJECT ENGINEERING & SPEC-DRIVEN DEVELOPMENT RULES v1.0）

## CORE MISSION（§0）

1. 正确理解需求
2. 识别项目类型和规模
3. 做出合理的架构决策
4. 做出可解释的技术选型
5. 生成结构化 Specification
6. 将 Spec 转换为 Design / Plan / Tasks
7. 按 Tasks 实现代码
8. 验证实现是否符合 Spec
9. 避免无必要的技术复杂度
10. 保持代码、架构、Spec 三者一致

默认流程：User Requirement → Project Discovery → Architecture Decision → Technology Selection → Specification → Design → Implementation Plan → Tasks → Implementation → Verification → Convergence。

## GENERAL PRINCIPLES

### Simple Before Complex（§1.1）
优先级：Modular Monolith > Monolith > Microservices。
复杂组件（K8s / Kafka / ES / Redis / GraphQL / gRPC / Event Sourcing / CQRS / Service Mesh / Distributed Tx）仅在存在**明确需求**时引入。
禁止因"以后可能需要 / 方便扩展 / 大厂架构 / 性能更好 / 比较现代 / 业界流行"而增加组件。

### Prefer Boring Technology（§1.2）
优先：成熟、稳定、社区活跃、文档完整、招聘易、Agent 易理解、运维成本低、迁移路径清晰。
而非单纯：最新、最热门、Benchmark 最高、Star 最高。

### Minimize Technology Diversity（§1.3）
普通项目默认：1 后端语言 + 1 后端框架 + 1 主数据库 + 0/1 缓存 + 0/1 消息队列 + 1 前端框架 + 1 API 风格 + 1 部署策略。
禁止无理由并存：PG+MySQL / Redis+Memcached / Kafka+RabbitMQ / REST+GraphQL+gRPC / Vue+React。

### Existing Project Takes Priority（§1.4）
Brownfield：已有语言/框架/数据库/部署/认证/CI-CD 优先复用，不主动为"升级"重写。

### Explicit User Decisions Highest Priority（§1.5）
用户明确指定即最高优先级，不得擅自改；可记录风险、必要时请求确认。

## PROJECT DISCOVERY（§2）
生成 spec 前必须回答：Business / Users（标记 UNKNOWN 不编造）/ Traffic（LOW/MEDIUM/HIGH）/ Data / Non-functional Requirements。

## SCALE（§3）
- Small：1-3 人 / <10k 用户 / <100 RPS / <10GB → Modular Monolith + PostgreSQL + Docker（Redis 可选）。
- Medium：3-10 人 / 10k-1M / 100-2000 RPS / 10GB-1TB → Modular Monolith + PG + Redis(按需) + 对象存储 + 后台 Worker。
- Large：>10 人 / >1M / >2000 RPS / >1TB / 多域 → 考虑服务拆分、读副本、分布式缓存、MQ、搜索集群、K8s，但逐项证明必要性。

## ARCHITECTURE（§4）
默认 Modular Monolith（§4.1）。Microservices 非默认（§4.2），仅在满足强条件（独立部署/扩缩容/团队 ownership/故障隔离/bounded context/极高吞吐/不同技术栈）时选用。

## DEFAULT TECHNOLOGY MATRIX（§110）
| Category | Default | Alternatives |
| --- | --- | --- |
| Architecture | Modular Monolith | Microservices |
| Backend | Python | Go / TS / Java |
| Python API | FastAPI | Django / Flask |
| DB | PostgreSQL | MySQL / MongoDB |
| Cache | None | Redis |
| Queue | None | RabbitMQ |
| Search | PostgreSQL FTS | OpenSearch / Elasticsearch |
| API | REST | GraphQL / gRPC |
| Auth | OIDC / Session | JWT |
| Container | Docker | — |
| CI/CD | GitHub Actions | GitLab CI |
| Observability | OpenTelemetry | Vendor SDK |

## SPEC-DRIVEN（§91-100）
- Spec 是 Source of Truth，不是 README 附属。
- 实现前必须读：Project Rules / Technology Selection / Relevant Spec / Design / Tasks（§100）。
- 发现 Spec 错误：更新 Spec → Design → Tasks → 继续实现，不直接绕过（§101）。

## FINAL PRINCIPLE（§120）
技术/架构/Framework/SDD 都不是目的。目标：Correctness + Maintainability + Simplicity + Testability + Observability + Security + Evolvability。无明确需求选最简单成熟方案；复杂需求必须记录必要性。不要为架构而架构。
