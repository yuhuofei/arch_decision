# arch_decision 与 Spec Kit / OpenSpec 集成使用指南
## 1. 定位：三个框架分别解决什么问题

arch_decision、Spec Kit、OpenSpec 都属于 AI Agent 驱动开发体系的一部分，但职责不同。

不要让三个框架同时解决同一个问题。

推荐职责划分：

| 工具 | 核心职责 | 解决的问题 |
| --- | --- | --- |
| arch_decision | Architecture Decision Governance | 为什么这么设计？为什么选择这些技术？ |
| Spec Kit | Specification Driven Development | 需求是什么？如何拆解成 Spec/Plan/Task？ |
| OpenSpec | Change/Spec Proposal Workflow | 如何管理需求变化、变更提案和实现过程？ |
| Claude Code / Cursor / Codex | Agent Runtime | 执行代码、修改文件、运行测试 |


整体关系：

```text
                 User Requirement
                         |
                         v

              +--------------------+
              |   arch_decision    |
              |                    |
              | Architecture Gate  |
              | Technology Choice  |
              | Constraint Control |
              +--------------------+

                         |
                         |
              Architecture Accepted

                         |
                         v

       +--------------------------------+
       |                                |
       |          Spec Framework        |
       |                                |
       |   Spec Kit        OpenSpec     |
       |                                |
       +--------------------------------+

                         |
                         v

              Implementation Agent

       Claude Code / Cursor / Codex
```

## 2. arch_decision 在整个流程中的位置
推荐流程
```text
Discovery
    |
    v
Requirement Understanding
    |
    v
arch_decision
    |
    +-- Architecture Decision
    |
    +-- Technology Selection
    |
    +-- Complexity Budget
    |
    +-- ADR
    |
    +-- Human Confirmation
    |
    v

Spec Kit / OpenSpec

    |
    +-- Requirement Spec
    |
    +-- Change Proposal
    |
    +-- Implementation Plan
    |
    +-- Tasks

    |
    v

Coding Agent

    |
    v

Verification
```

## 3. 新项目初始化方式

假设创建项目：

enterprise-ai-kb

目标：

企业内部 AI 知识库系统

需求：

用户上传 PDF / Markdown
自动解析
文档向量化
RAG 查询
Web UI
20~100 用户
企业内部部署
### 3.1 初始化项目

创建目录：

```bash
mkdir enterprise-ai-kb
cd enterprise-ai-kb
git init
```

### 3.2 引入 arch_decision

推荐作为项目级治理规则：

enterprise-ai-kb/

```text
├── .sdd/
├── scripts/
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

来源：

```text
arch_decision
        |
        |
        v

new project
```

例如：

```bash
cp -r ../arch_decision/.sdd .
cp -r ../arch_decision/scripts .
cp ../arch_decision/AGENTS.md .
cp ../arch_decision/CLAUDE.md .
```

## 4. 引入 Spec Kit

Spec Kit 负责：

```text
Requirement
      |
      v
Specification
      |
      v
Plan
      |
      v
Tasks
      |
      v
Implementation
```

目录：

enterprise-ai-kb/

```text
├── .sdd/
├── .specify/
├── specs/
├── src/
└── tests/
```

## 5. 引入 OpenSpec

OpenSpec 更适合处理：

已有项目
需求变化
Feature Proposal
Change Management

例如：

已有：

AI Knowledge Base v1

新增：

增加企业微信登录

不要直接改代码。

先创建 Change Proposal：

openspec/

```text
└── changes/

    └── add-wechat-login/

        ├── proposal.md

        ├── spec.md

        ├── design.md

        └── tasks.md
```

流程：

Change Request

```text
      |
      v

OpenSpec Proposal

      |
      v

Review

      |
      v

Implementation
```

## 6. 三者组合推荐模式
新项目

推荐：

```text
arch_decision
        |
        |
        v

Spec Kit

        |
        |
        v

Implementation
已存在项目增加功能
```

推荐：

```text
arch_decision
        |
        |
        v

OpenSpec

        |
        |
        v

Implementation
大型长期项目
```

推荐：

                 Requirement

```text
                      |
                      v

              arch_decision

                      |
        +-------------+-------------+

        |                           |

   Spec Kit                   OpenSpec

 新功能开发                 变化管理

        |                           |

        +-------------+-------------+

                      |

              Coding Agent

                      |

              Verification
```

## 7. 实际完整案例
项目：

企业 AI 知识库

Phase 0：启动 Agent

Prompt:

这是一个全新项目。

请不要编写代码。

首先执行架构决策流程。

必须遵守：

- AGENTS.md
- .sdd/CANONICAL.md
- .sdd/workflows/new-project.md


目标：

创建企业内部 AI Knowledge Base。


执行：

1. Discovery
2. Requirement Analysis
3. Constraint Extraction
4. Architecture Decision
5. Technology Selection
6. Complexity Budget
7. Generate Decision Artifact


输出：

- project-discovery.md
- technology-selection.md
- decision.json


不要进入 Implementation。
Phase 1：需求探索

Agent：

请回答以下问题：

1. 用户数量？
2. 数据规模？
3. 是否公网？
4. 部署环境？
5. 是否需要高可用？
6. 是否多租户？
7. 团队技术栈？
8. 预算限制？
9. 安全要求？

用户：

1. 50人以内

2. 10万文档

3. 内网

4. Ubuntu Server

5. 不需要HA

6. 单租户

7. Python团队

8. 低成本

9. 企业账号体系
Phase 2：arch_decision 架构决策

Agent：

开始 Architecture Decision。

## Architecture

候选：

A. Microservices
B. Modular Monolith


分析：

Microservices:

优势：
- 独立扩展

问题：
- 运维复杂度增加
- 当前用户规模不足


Modular Monolith:

优势：
- 简单部署
- 满足当前规模


Decision:

Modular Monolith

Status:

AUTO
Backend

Agent：

Backend Decision:


Candidates:

Python FastAPI
Go Gin
Java Spring


Constraint:

- AI ecosystem
- RAG
- Small team


Decision:

Python FastAPI


Reason:

Python AI ecosystem strongest.

Status:

AUTO
Database

Agent：

Database Decision:


Candidates:

PostgreSQL
MySQL
MongoDB


Requirement:

- Metadata
- Transaction
- Vector Search


Decision:

PostgreSQL + pgvector


Rejected:

MongoDB:
vector capability unnecessary

MySQL:
less suitable for pgvector ecosystem


Status:

AUTO

最终生成：

specs/

```text
└── 001-project/

    ├── decision.json

    ├── technology-selection.md

    ├── adr/

    └── verification.md
Phase 3：进入 Spec Kit
```

此时：

架构已经冻结。

Prompt：

架构决策已经完成。

现在进入 Spec Kit。

不要重新选择技术。


Architecture Source:

specs/001-project/decision.json


执行：

```bash
/speckit-specify
```

目标：

生成 AI Knowledge Base 产品规格。

包含：

- User Stories
- Functional Requirements
- Non Functional Requirements
- Acceptance Criteria


如果发现架构问题：

创建 ARCHITECTURE_CHANGE_REQUEST

不要自行修改架构。

生成：

specs/

```text
├── feature-auth.md

├── feature-document.md

├── feature-rag.md

└── feature-search.md
Phase 4：Spec Kit Plan
```

Prompt：

执行：

```bash
/speckit-plan
```

必须遵守：

architecture decision 已冻结。


禁止：

- 更换数据库
- 更换框架
- 增加基础设施


如果发现：

需要 Redis

但是 architecture decision 没有批准


必须：

STOP

提出 Architecture Change Request。
Phase 5：进入 Tasks

Prompt：

执行：

```bash
/speckit-tasks
```

要求：

每个任务必须关联：

Requirement

```text
↓

Spec

↓

Architecture Decision

↓

Task
```

输出：

tasks.md

例如：

TASK-001

Implement document upload API


Trace:

REQ-DOC-001

Spec:

document-upload


Architecture:

FastAPI


Acceptance:

POST /documents

returns 201
Phase 6：编码

Prompt：

开始 Implementation。


执行前检查：

Architecture:

ACCEPTED


Decision:

NO BLOCKED


Requirements:

TRACEABLE


开始实现 tasks.md。
Phase 7：已有项目变更（OpenSpec）

半年后：

需求：

增加企业微信登录

不要直接修改。

Prompt：

创建一个新的 OpenSpec Change。


需求：

增加企业微信 OAuth 登录。


请：

1. 分析现有 Architecture Decision
2. 创建 Change Proposal
3. 判断是否影响架构
4. 如果影响：
   创建 Architecture Change Request


不要直接实现。

OpenSpec 输出：

openspec/

changes/

add-wechat-login/


proposal.md

design.md

tasks.md
Phase 8：架构影响检查

Agent：

分析：

新增微信登录是否影响：

Authentication Architecture

Security Boundary

Deployment

Database


结果：

Authentication Architecture:

Changed


需要重新进入 arch_decision。

重新调用：

arch_decision

Authentication Decision Update
## 8. Agent 使用规则（建议加入 AGENTS.md）

可以加入：

# Architecture Governance Rules


## Rule 1

任何新项目必须先执行 arch_decision。


禁止：

直接生成代码。


```text
---
```

## Rule 2

Architecture Decision 是唯一技术选择来源。


Spec Kit / OpenSpec:

不得重新选择：

- Language
- Framework
- Database
- Infrastructure


```text
---
```

## Rule 3

如果发现：

Spec Requirement

与

Architecture Decision


冲突：


必须创建：

ARCHITECTURE_CHANGE_REQUEST


不得自行修改。


```text
---
```

## Rule 4

所有 Implementation 必须能够追溯：

Requirement

```text
↓

Spec

↓

Architecture Decision

↓

Task

↓

Code

↓

Test
```

## 9. 最终推荐组合
小项目
```text
arch_decision
        |
        v
Spec Kit
        |
        v
Claude Code / Cursor / Codex
中大型项目
arch_decision

       |

Spec Kit
       |
       |
OpenSpec

       |

Coding Agent

       |

CI/CD Verification
```

## 10. 对 arch_decision 下一步演进建议

如果继续发展，我认为最有价值的是增加：

Architecture Gate API

例如：

arch decision check

返回：

```json
{
 "status":"ACCEPTED",
 "architecture":"fastapi-postgresql",
 "allow_implementation":true
}
```


然后：

Spec Kit / OpenSpec 在执行：

plan
implement

之前调用：

arch_decision gate

形成：

No Architecture Decision

```text
        ↓

No Plan

        ↓

No Code
```

这样 arch_decision 就从一个规则仓库升级为：

AI Agent 软件工程流程中的 Architecture Governance Layer

这也是它与 Spec Kit / OpenSpec 最自然的结合方式。

