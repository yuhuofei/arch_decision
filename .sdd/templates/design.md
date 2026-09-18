# Template: Design（设计，**按需**）

> 用途：`design.md` **只写对 `plan.md` 来说太细的内容**（`mod_gpt.md §4`）。
> **它不是第二份 Plan。** 任何 `plan.md` 已写的架构、技术栈、模块划分、缓存 TTL、错误格式等，
> **不得**在本文件重述 —— 两边都写时 Agent 无法判断哪份是 Source of Truth
> （例：`plan.md: Redis TTL=10min` 与 `design.md: Redis TTL=30min`，谁对？）。
> 目录约定与判据见 `.sdd/LAYOUT.md` §1.2；实例见 `specs/001-project/design.md`。

---

## 何时创建（SHOULD be created when one or more apply）

```
- complex domain model                （复杂领域模型）
- non-trivial state machine           （状态机）
- concurrency                         （并发）
- async workflow                      （异步流程）
- multiple external integrations      （多外部集成）
- distributed consistency             （分布式一致性）
- complex API contract                （复杂接口契约）
- security-sensitive flow             （安全敏感流程）
- algorithm requires explicit design  （算法需要显式设计）
```

**否则不创建** —— `plan.md` 足够。

## 文档职责边界

| 文件 | 回答 | 不应包含 |
| --- | --- | --- |
| `spec.md` | WHAT / WHY | 技术方案 |
| `technology-selection.md` + `decision.json` | WHICH / WHY NOT | 实现细节 |
| `plan.md` | HOW（架构级） | 算法级伪代码、完整状态转移表 |
| `design.md`（本文件） | 只有 plan 装不下的细节 | **任何 plan 已写的内容** |
| `tasks.md` | 可执行工作 | 设计论证 |

> 冲突时以 `plan.md` 为准（`decision-protocol §10` 的仲裁顺序不含本文档，因为本文档不应与它冲突）。
> 若确实需要修改 `plan.md` 的内容，**改 `plan.md` 本身**，不要在 `design.md` 里"另立一份"。

---

# Design: <feature-name>

## 1. 状态机 / 流程
<!-- 完整状态转移表；plan.md 只写"有状态机"，这里写转移条件与非法转移 -->

## 2. 领域模型细节
<!-- 聚合边界、不变量、领域事件；plan.md 只写模块名 -->

## 3. 并发与一致性
<!-- 锁粒度、隔离级别、幂等键、重试与竞态处理 -->

## 4. 算法 / 计算过程
<!-- 需要显式设计的算法（伪代码、复杂度、边界条件） -->

## 5. 复杂接口契约细节
<!-- 只有复杂契约才写；简单 CRUD 的端点定义放 plan.md 即可 -->

## 6. 安全敏感流程
<!-- 信任边界、鉴权判定点、敏感数据流转；只写 plan 未覆盖的判定细节 -->

## 7. 外部集成细节
<!-- 多外部系统时的适配、超时、失败语义映射 -->

---

## 写法要求
1. 每条内容都能回答"为什么 plan.md 装不下它"；答不出就删掉。
2. 不复制 `plan.md` 的段落，需要时用引用：`见 plan.md §6`。
3. 出现与 `plan.md` 不一致的内容时，**必须**先修正 `plan.md`，再回来改本文件。
