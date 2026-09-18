# Spec — 002-demo-todo-cli（演示实例）

> 按 `.sdd/templates/spec.md` 填写。Spec 是 Source of Truth，描述 WHAT/WHY。
> **Status: `Accepted`**（真实流程从 `Draft` 起步，技术决策确认后升级为 `Accepted`；本演示直接给出终态）。
> Draft 阶段禁止写语言/框架/数据库/部署——技术决策发生在本 Spec 之后。

## 1. Overview
### Problem
单人使用场景下没有轻量、离线、零部署的待办工具，纸笔/笔记软件都过重或不同步。

### Goal
提供一个本地命令行工具，支持待办的增、删、改、查与完成标记，数据持久化在本地文件。

### Non-Goals
- 不做多用户 / 账号体系
- 不做云同步 / 网络服务
- 不做 GUI / Web 前端

### Users
单人本地用户（见 `project-discovery.md` §2）。

## 2. Context
### Existing System
Greenfield，无既有系统。

### Business Context
个人效率工具，价值在于「打开终端即可用」。

### Constraints
- 必须离线可用
- 不得引入需要常驻的服务进程（如数据库服务、Web 服务）

## 3. User Stories
### US-001
As a 用户 / I want 新增一条待办 / So that 不遗忘。

### US-002
As a 用户 / I want 列出所有待办 / So that 掌握全貌。

### US-003
As a 用户 / I want 标记某条为已完成 / So that 区分进度。

### US-004
As a 用户 / I want 删除一条待办 / So that 清理已完成/误填项。

## 4. Functional Requirements
### FR-001
The system SHALL 支持 `add <标题>` 新增待办并持久化。
#### Scenario
- GIVEN 终端 WHEN 执行 `todo add 买菜` THEN 新增一条未完成待办并返回其 ID

### FR-002
The system SHALL 支持 `list` 列出全部待办（含完成状态与 ID）。
#### Scenario
- GIVEN 存在 3 条待办 WHEN 执行 `todo list` THEN 按 ID 顺序输出 3 条及完成标记

### FR-003
The system SHALL 支持 `done <ID>` 将指定待办标记为完成。
#### Scenario
- GIVEN ID=2 未完成 WHEN 执行 `todo done 2` THEN ID=2 状态变为已完成

### FR-004
The system SHALL 支持 `rm <ID>` 删除指定待办。
#### Scenario
- GIVEN ID=2 存在 WHEN 执行 `todo rm 2` THEN 该条不再出现在 `list` 中

## 5. Non-Functional Requirements
### Performance
本地操作 p95 < 100ms。

### Security
数据存于用户目录下的本地文件，依赖文件系统权限，不对外暴露。

### Observability
关键操作记录 INFO 级日志。

## 6. Data Requirements
### Entities
tasks(id INTEGER PK, title TEXT, done INTEGER 0/1, created_at TEXT)

### Relationships / Constraints
无关联；`title` 非空；`done` 仅取 0/1。

## 7. API Requirements
### Endpoint
CLI 子命令（非 REST）：`add` / `list` / `done` / `rm`。
### Request / Response / Error
错误以非 0 退出码 + stderr 提示；未知 ID 报错 `task not found`。

## 8. Integration Requirements
### External Services / Authentication / Retry / Timeout
无。

## 9. Architecture Constraints
- Must remain a single local process（不引入网络框架）
- Must not require a separately deployed database server

## 10. Acceptance Criteria
- [x] AC-001 Given 执行 `todo add` When 提交 Then 待办被持久化
- [x] AC-002 Given 执行 `todo list` When 查询 Then 正确展示全部条目与状态
- [x] AC-003 Given 执行 `todo done <ID>` When 标记 Then 状态变更并持久化
- [x] AC-004 Given 执行 `todo rm <ID>` When 删除 Then 条目被移除

## 11. Assumptions
- 单用户，本地运行，无并发写入冲突（或仅单实例运行）

## 12. Open Questions
- 是否需要按关键字过滤 `list --grep`？（v2 可选）

## 13. Out of Scope
- 云同步、多设备、GUI、协作

## 14. Traceability
| Requirement | Design | Task | Test |
| --- | --- | --- | --- |
| FR-001 | D-001 | T-003 | TEST-001 |
| FR-002 | D-001 | T-003 | TEST-002 |
| FR-003 | D-001 | T-003 | TEST-003 |
| FR-004 | D-001 | T-003 | TEST-004 |
