# Knowledge: Frontend（前端）

> 来源：res.md §16-§21, §75, §76, §83-§85
> 决策树：`.sdd/decision-trees/frontend.md`

## 1. Frontend Decision（§16）

| 候选 | 默认原则 |
| --- | --- |
| Vue | Enterprise / Admin |
| React | Complex Web App |
| Next.js | SEO / SSR |
| Svelte | 轻量/现代 |
| Angular | 大型 Enterprise Angular 生态 |

## 2. Vue（§17, DEFAULT）

默认 `Vue 3 + TypeScript + Vite`。
选：Admin / Dashboard / Enterprise Web / CRUD / Internal tool / 团队 Vue 专长。
默认 Stack：Vue 3 + TS + Vite + Pinia + Vue Router + Vitest + Playwright。

## 3. React（§18）

选：Complex interaction / Consumer Web App / 大生态 / 已有 React 团队 / Component-heavy。
默认 `React + TypeScript`。

## 4. Next.js（§19）

选：SEO / SSR / SSG / Full-stack React / Content-heavy / Public-facing。
不选：如果只是 Admin SPA + REST API → 直接 React+Vite 或 Vue+Vite。

## 5. Angular（§20）

选：Large enterprise / 已有 Angular 组织 / 强框架约定 / Enterprise-scale 前端团队。新项目若无 Angular 专长，优先 Vue/React/Next.js。

## 6. Frontend/Backend 分离（§21）

见 `architecture.md` §5。Web+Mobile / 多 API consumer / 复杂度 medium+ 才分离。

## 7. State Management（§75）

- Vue：默认 Pinia。
- React：优先内置 state；需 global state 时用 Zustand / Redux Toolkit。**不要默认 Redux**。

## 8. UI Component Library（§76）

Agent 不应自动引入多个 UI library。默认选一个：Ant Design / MUI / shadcn/ui / Element Plus / Naive UI（按前端框架与项目类型）。

## 9. Repository Structure

- **Vue（§83）**：`web/src/{components,views,layouts,stores,router,services,types,utils}` + tests + public + package.json + vite.config.ts。
- **React（§84）**：`web/src/{components,features,pages,hooks,services,stores,types,utils}` + tests（Feature-oriented）。
- **Next.js（§85）**：`web/app/{(marketing),dashboard,api,layout.tsx}` + components + features + lib + services + types + tests。

## 10. Frontend Testing（§55）

- Vue：Vitest + Playwright。
- React：Vitest/Jest + Playwright。
- E2E：Playwright。
