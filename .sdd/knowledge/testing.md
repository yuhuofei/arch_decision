# Knowledge: Testing（测试）

> 来源：res.md §50-§58

## 1. Testing Strategy（§50, DEFAULT Testing Pyramid）

```
        E2E
       /   \
 Integration
    /       \
 Unit Tests
```

不要所有测试都写成 E2E。

## 2. Unit Test（§51）

覆盖：Domain logic / Business rules / Validation / Pure functions。避免测试 framework 实现细节。

## 3. Integration Test（§52）

覆盖：Database / API / Authentication / External integration / Message queue。优先真实 infrastructure（推荐 Testcontainers）。

## 4. E2E Test（§53）

只覆盖关键业务流程（如 Login → Create Order → Pay → Receive Confirmation）。不要为每个按钮写 E2E。

## 5. Python Testing（§54）

默认 pytest；API 用 pytest + httpx；Django 用 pytest-django。

## 6. Frontend Testing（§55）

Vue：Vitest + Playwright。React：Vitest/Jest + Playwright。E2E：Playwright。

## 7. Go Testing（§56）

默认 `go test` + table-driven + integration + Testcontainers。

## 8. Java Testing（§57）

默认 JUnit + Mockito + Testcontainers；Integration 用 Spring Boot Test。

## 9. Code Quality（§58）

- Python：Ruff + Mypy + Pytest
- TypeScript：ESLint + Prettier + Vitest
- Go：gofmt + go vet + golangci-lint + go test
- Java：Checkstyle / Spotless + JUnit（按团队标准）
