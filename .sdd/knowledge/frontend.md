# Knowledge: Frontend（前端）

> 来源：res.md §16-§21,§75,§76,§83-§85；Matrix §8,§12；知识库 §12-§19,§49-§53,§57,§58
> 决策树：`.sdd/decision-trees/frontend.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## 1. Frontend Matrix（Matrix §8，正式条件）

### Vue 3 + TypeScript（Matrix §8.1，默认）
```
IF business_app = true AND frontend_complexity = medium THEN Vue 3 + TypeScript
```
适合 Admin/Dashboard/Enterprise CRUD/Internal Tool/SaaS。默认栈：Vue 3 + TS + Vite + Pinia + Vue Router + Vitest + Playwright。

### React（Matrix §8.2）
```
IF react_ecosystem_required OR existing_react OR component_ecosystem = important THEN React
```
默认 React + TypeScript + Vite（普通 SPA：React Router + TanStack Query）。

### Next.js（Matrix §8.3 / 知识库 §16）
```
IF React = true AND (SSR OR SEO OR fullstack_web OR server_components useful) THEN Next.js
ELSE React + Vite
```
新项目优先 App Router（知识库 §16）。

### Angular（Matrix §8.4）
```
IF enterprise_frontend_standard = Angular OR existing_angular OR large_enterprise_team AND Angular_expertise = strong
THEN Angular
```
无 Angular 专长不作为默认（知识库 §17）。

## 2. 新 Web Frontend 默认语言（知识库 Rule 8）
TypeScript 是新 Web 前端的默认语言。

## 3. 前后端分离（Matrix §9 / 知识库 §12）
- 分离：SaaS / 多终端 / Mobile+Web / API 对外开放 / 多个前端共享 API。
- 合并：小型工具 / 内容站 / 简单后台 / SEO / MVP / 内部工具 → Next.js Full Stack 合理。

## 4. CSS / UI（知识库 §18-§19，新增）
- **CSS 默认 Tailwind CSS**（AI Coding / SaaS / Admin / 快速 UI）。
- UI 组件库**只选一个**，按框架：
  - Vue：Element Plus / Naive UI / Ant Design Vue
  - React：Ant Design / MUI / shadcn/ui
  - 选择原则：企业后台→Element Plus/Ant Design；高度定制→shadcn/ui/Tailwind；已有体系→保持一致。
  - 禁止多库并存。

## 5. 状态管理（res.md §75 / 知识库 §51）
- 分类：Server State → TanStack Query；UI State → Local；Global Client State → Pinia/Zustand/Redux。
- 原则：**Server State 不应复制成大量 Global State**。
- Vue 默认 Pinia；React 优先内置，需 global 用 Zustand/Redux Toolkit（不要默认 Redux）。

## 6. API Client / Contract（知识库 §52-§53，新增）
- 不要在组件里直接 `fetch()`；应 API Client → Service → Component。
- 推荐 `OpenAPI` → 生成 TypeScript Client，前后端共享 API Contract，减少 response≠expectation。

## 7. Repository Structure（知识库 §57-§58）
- Vue：`frontend/src/{components,views,layouts,router,stores,services,api,types,utils}` + tests + vite.config.ts
- React：`frontend/src/{components,features,pages,hooks,services,api,types,utils}`（Feature-based > 无限扩张的 components/utils）
