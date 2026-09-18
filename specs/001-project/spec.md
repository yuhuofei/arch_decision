# Spec — 001-project（示例实例）

> 按 `.sdd/templates/spec.md` 填写。Spec 是 Source of Truth（§91）。

## 1. Overview
<待填写>

## 2. Goals
<待填写>

## 3. Non-Goals
<待填写>

## 4. Users
<引用 project-discovery.md §2>

## 5. Functional Requirements
- WHEN <condition> THE SYSTEM SHALL <behavior>

## 6. Non-Functional Requirements
<引用 project-discovery.md §5>

## 7. Scale
<引用 project-discovery.md §6>

## 8. Architecture
Modular Monolith（见 technology-selection.md）

## 9. Technology Decisions
见 `technology-selection.md`

## 10. Repository Structure
<见 `.sdd/knowledge/backend.md` / `frontend.md` 的 Repository Structure>

## 11. Data Model
<待填写>

## 12. API Design
REST + OpenAPI（§33）；错误格式（§70）；分页（§71）

## 13. Authentication
OIDC / Cookie Session（§41-§44）

## 14. Authorization
RBAC 默认（§46）

## 15. Error Handling
统一错误格式（§70）

## 16. Logging
JSON structured（§48）；禁记敏感信息

## 17. Testing
Testing Pyramid（§50-§53）

## 18. CI/CD
GitHub Actions（§63）

## 19. Deployment
Docker（§60）

## 20. Security
§45 baseline

## 21. Risks
<待填写>

## 22. Open Questions
<待填写>

## 23. Acceptance Criteria
- Given <valid invitation> When <user accepts> Then <becomes member>
