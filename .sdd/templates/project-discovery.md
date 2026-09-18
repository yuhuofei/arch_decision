# Template: Project Discovery（项目发现）

> 用途：生成 spec.md 前完成 Discovery（res.md §2）。实例见 `specs/001-project/project-discovery.md`。

## 1. Business（res.md §2.1）
- 项目是什么？
- 解决什么问题？
- 谁使用？
- 核心业务流程是什么？
- MVP 还是 Production？
- 内部系统还是公开产品？
- 是否需要商业化？

## 2. Users（res.md §2.2）
- Total Users:
- DAU:
- MAU:
- Concurrent Users:
- Peak Concurrent Users:
> 未知标 `UNKNOWN`，不要编造精确数字。

## 3. Traffic（res.md §2.3）
- Average RPS:
- Peak RPS:
- Read / Write Ratio:
- Batch Traffic:
- Background Jobs:
> 未知用 `LOW / MEDIUM / HIGH`，不虚构具体数据。

## 4. Data（res.md §2.4）
- Primary data type:
- Data volume:
- Growth rate:
- Transaction requirements:
- Relationship complexity:
- Search requirements:
- File storage:
- Retention requirements:

## 5. Non-functional Requirements（res.md §2.5）
- [ ] Performance
- [ ] Availability
- [ ] Scalability
- [ ] Security
- [ ] Privacy
- [ ] Compliance
- [ ] Observability
- [ ] Disaster Recovery
- [ ] Backup
- [ ] RPO
- [ ] RTO

## 6. Scale Estimate（res.md §3）
Small / Medium / Large（根据 res.md §3 特征判定）。

## 7. Existing Stack（Brownfield, res.md §102）
- Repository / Architecture / Dependencies / Database / API / Tests / CI-CD / Deployment
