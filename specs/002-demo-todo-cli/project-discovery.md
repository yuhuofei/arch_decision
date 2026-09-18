# Project Discovery — 002-demo-todo-cli（演示实例）

> 按 `.sdd/templates/project-discovery.md` 填写。
> 这是用本仓库 SDD 工作流新建项目的「最小可演示」样例：一个单人本地命令行待办工具。
> 未知项标 `UNKNOWN`，不编造。

## 1. Business
- 项目是什么：本地命令行待办清单（todo CLI），单人使用
- 解决什么问题：记不住/随手记待办，需要轻量、离线、零部署的工具
- 谁使用：开发者本人（1 人）
- 核心业务流程：新增 → 列出 → 标记完成 → 删除
- MVP 还是 Production：MVP 即可，但要求稳定可靠
- 内部系统还是公开产品：内部/个人工具
- 是否需要商业化：否

## 2. Users
- Total Users: 1
- DAU: 1
- MAU: UNKNOWN
- Concurrent Users: 1
- Peak Concurrent Users: 1

## 3. Traffic
- Average RPS: N/A（本地进程）
- Peak RPS: N/A
- Read / Write Ratio: 约 1:1
- Batch Traffic: 无
- Background Jobs: 无

## 4. Data
- Primary data type: 结构化待办条目（标题、完成状态、创建时间）
- Data volume: 极小（百条级）
- Growth rate: 低
- Transaction requirements: 单用户，弱事务即可
- Relationship complexity: 无关联（仅单表）
- Search requirements: 仅按关键字过滤列出，不需全文检索
- File storage: 无
- Retention requirements: 本地持久化，不清空

## 5. Non-functional Requirements
- [x] Performance（本地操作 < 100ms）
- [ ] Availability（本地，无 SLA 要求）
- [ ] Scalability（不扩缩）
- [x] Security（本地文件，靠文件系统权限）
- [ ] Privacy（无第三方）
- [ ] Compliance（无）
- [x] Observability（基础日志即可）
- [ ] Disaster Recovery（单文件，定期备份即可）
- [x] Backup（复制 todo.db）
- [ ] RPO / RTO

## 6. Scale Estimate
Small（单人、单文件、无并发压力）

## 7. Existing Stack（Brownfield）
无（Greenfield）。本演示不引用任何既有栈。
