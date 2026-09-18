# Decision Tree: Frontend（前端框架选型）

> 配套知识：`.sdd/knowledge/frontend.md`　治理：`.sdd/decision-trees/decision-protocol.md`

## 1. 语言（知识库 Rule 8）
新 Web Frontend 默认 **TypeScript**。

## 2. 框架（Matrix §8，正式条件）

```
IF business_app = true AND frontend_complexity = medium
→ Vue 3 + TypeScript + Vite        # 默认 AUTO（Admin/Dashboard/Enterprise/CRUD/Internal/SaaS）

IF react_ecosystem_required OR existing_react OR component_ecosystem = important
→ React + TypeScript              # AUTO

IF React = true AND (SSR OR SEO OR fullstack_web OR server_components)
→ Next.js + TypeScript           # RECOMMEND（新项目优先 App Router）
ELSE React + Vite

IF enterprise_frontend_standard = Angular OR existing_angular
   OR large_enterprise_team AND Angular_expertise = strong
→ Angular                         # 无 Angular 专长不作为默认
```

## 3. 前后端分离（Matrix §9）
```
SaaS / 多终端 / Mobile+Web / 多 client / 大型前端 / AI API+Web → 分离
简单 CRUD / SEO / MVP / 内部工具 → 可合并（Next.js Full Stack）
```

## 4. CSS / UI（知识库 §18-§19）
```
CSS 默认 Tailwind CSS
UI 库只选一个：Vue→Element Plus/Naive UI/Ant Design Vue；React→Ant Design/MUI/shadcn/ui
已有体系 → 保持一致；禁止多库并存
```

## 5. 状态管理（知识库 §51）
```
Server State  → TanStack Query
UI State      → Local
Global Client → Pinia (Vue) / Zustand·Redux (React)
原则：Server State 不复制成大量 Global State
```

## 6. API Client / Contract（知识库 §52-§53）
```
OpenAPI → 生成 TypeScript Client → 前后端共享 Contract
禁止组件内直接 fetch()
```

## 输出
写入 `technology-selection.md` 的 Frontend 段。
