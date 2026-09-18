# Workflow: New Project（新项目）

> 来源：res.md §0, §91-§118, §116。入口：CLAUDE.md §2。

## 流程
```
User Requirement
   ↓
1. Project Discovery        → 用 templates/project-discovery.md
   ↓
2. Architecture Decision     → 读 knowledge/architecture.md + decision-trees/architecture.md
   ↓
3. Technology Selection      → 读 decision-trees/* + 用 templates/technology-selection.md
   ↓                          （每个重要决策写 ADR：templates/adr.md）
4. Specification             → 用 templates/spec.md（§117 至少 23 项）
   ↓
5. Design                    → 用 templates/design.md
   ↓
6. Plan                      → 用 templates/plan.md
   ↓
7. Tasks                     → 用 templates/tasks.md
   ↓
8. Implementation            → 实现前必须读 Rules/TS/Spec/Design/Tasks（§100）
   ↓
9. Test                      → Testing Pyramid（§50-§53）
   ↓
10. Verify                   → 对照 Acceptance Criteria（§97）
   ↓
Convergence
```

## 关键检查（§116 Architecture Review Checklist）
- [ ] Project type identified
- [ ] Scale estimated
- [ ] Architecture selected
- [ ] Backend / Frontend / Database selected
- [ ] Cache / Queue / Search / Storage decision made
- [ ] Authentication / API style selected
- [ ] Testing / Observability / Deployment / CI-CD defined
- [ ] Security / Backup considered
- [ ] Risks / Open questions documented

## 决策输出（§109）
生成 Spec 前必须输出一段技术决策摘要（见 technology-selection.md 速填区）。

## 默认技术矩阵（§110）
无特殊约束时按 `knowledge/*.md` 的 DEFAULT 选型；中小 SaaS 参考 §111，AI 应用 §112，企业 §113，高性能服务 §114。

## 原则
未解决架构决策前**不得**写实现代码（CLAUDE.md §2）。
