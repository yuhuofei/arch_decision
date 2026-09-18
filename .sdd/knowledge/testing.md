# Knowledge: Testing（测试）

> 来源：res.md §50-§58；Matrix §27,§28；知识库 §39-§43
> 测试金字塔（res.md §50）：Unit > Integration > E2E，不要全写 E2E。

## 1. Testing Pyramid & Matrix（Matrix §27）
- Unit：`business_logic = true → unit tests`
- Integration：`database OR external_api OR queue = true → integration tests`（优先真实 infra / Testcontainers）
- E2E：`web_ui AND critical_user_flow = true → E2E`，至少覆盖 login / 关键 CRUD / payment / core workflow

## 2. Test Strategy Matrix by Project（Matrix §28，新增）
| Project | Unit | Integration | E2E |
| --- | ---: | ---: | ---: |
| Library | High | Medium | Low |
| CRUD API | High | High | Medium |
| SaaS | High | High | High |
| AI SaaS | High | High | High |
| CLI | High | Medium | Low |
| Data Pipeline | High | High | Low |
| Infrastructure | High | High | Medium |
| Frontend-heavy | Medium | Medium | High |

## 3. 语言测试栈（res.md §54-§57 / 知识库 §40-§43）
- **Python**：pytest + pytest-asyncio + httpx + factory-boy；必要时 Hypothesis。Django → pytest-django。
- **Frontend**：Vitest + Testing Library + Playwright（E2E）。
- **Go**：`testing` + testify + gomock；E2E/API 用 `httptest`。
- **Java**：JUnit 5 + Mockito + Testcontainers；Integration 用 Spring Boot Test。

## 4. 代码质量（res.md §58）
- Python：Ruff + Mypy + Pytest
- TypeScript：ESLint + Prettier + Vitest
- Go：gofmt + go vet + golangci-lint + go test
- Java：Checkstyle / Spotless + JUnit

## 5. AI Coding 要求（知识库 §39）
**每一个 Requirement 至少对应一个验证方式。** 每个重要需求至少一个自动化验证策略。
