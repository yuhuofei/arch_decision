# Template: Spec（规格说明）

> 用途：Spec 是 Source of Truth（res.md §91, §92, §93, §117）。
> 项目级见 `docs/architecture.md` + `docs/technology-selection.md` + `docs/engineering-rules.md` + `specs/`。

# Spec: <feature-name>

## 1. Overview
## 2. Goals
## 3. Non-Goals
## 4. Users
## 5. Functional Requirements
<!-- 明确 / 可测试 / 可验证 / 不含不必要实现细节（§96） -->
<!-- 推荐：WHEN <condition> THE SYSTEM SHALL <behavior> -->

## 6. Non-Functional Requirements
## 7. Scale
## 8. Architecture
## 9. Technology Decisions
<!-- 引用 technology-selection.md -->
## 10. Repository Structure
## 11. Data Model
## 12. API Design
## 13. Authentication
## 14. Authorization
## 15. Error Handling
## 16. Logging
## 17. Testing
## 18. CI/CD
## 19. Deployment
## 20. Security
## 21. Risks
## 22. Open Questions
## 23. Acceptance Criteria
<!-- 每个核心需求必须有（§97）：Given ... When ... Then ... -->

---

## Spec Artifacts 结构（§92）
```
docs/specs/001-feature-name/
├── context.md
├── requirements.md
├── technology-selection.md
├── design.md
├── decisions.md
├── tasks.md
└── verification.md
```
