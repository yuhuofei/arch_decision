# Decision Tree: Frontend（前端框架选型）

> 配套知识：`.sdd/knowledge/frontend.md`

## 起点：选哪个前端框架？

```
是否需要 SEO / SSR / SSG / Content-heavy / Public-facing？
├─ 是 ──→ Next.js（Full-stack React）
└─ 否 ──→ 主要面向谁？
          ├─ Enterprise / Admin / Dashboard / CRUD / Internal tool / 团队 Vue 专长
          │     └─→ Vue 3 + TypeScript + Vite（默认）
          ├─ Complex interaction / Consumer Web App / 大生态 / 已有 React 团队 / Component-heavy
          │     └─→ React + TypeScript
          └─ Large enterprise / 已有 Angular 组织 / 强框架约定
                └─→ Angular（无 Angular 专长则优先 Vue/React/Next.js）

是否需要前后端分离？（§21）
├─ Web + Mobile / API consumers > 1 / 前端复杂度 medium+ → 分离（Frontend + Backend API）
└─ 小型内部工具 / 简单 CRUD / 简单 CMS / MVP / server-rendered → 可不分离
```

## 关键判定

### Vue（§17）
- 默认 `Vue 3 + TS + Vite`
- 选：Admin / Dashboard / Enterprise / CRUD / Internal tool
- Stack：Pinia + Vue Router + Vitest + Playwright

### React（§18）
- 默认 `React + TypeScript`
- 选：Complex interaction / Consumer Web App / Component-heavy

### Next.js（§19）
- 选：SEO / SSR / SSG / Full-stack React / Public-facing
- 不选：仅 Admin SPA + REST API（用 React+Vite 或 Vue+Vite）

### Angular（§20）
- 选：Large enterprise / 已有 Angular 组织
- 新项目无 Angular 专长 → 优先 Vue/React/Next.js

## 配套决策
- State：Vue→Pinia；React→内置优先，需 global 用 Zustand/Redux Toolkit（**不要默认 Redux**）（§75）
- UI 库：选一个（Ant Design / MUI / shadcn/ui / Element Plus / Naive UI），禁止多库并存（§76）

## 输出
写入 `technology-selection.md` 的 Frontend 段。
