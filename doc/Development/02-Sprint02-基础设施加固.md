# Sprint 02 · 基础设施加固包

**日期**：2026-05-02
**目标**：在 MVP 骨架（Sprint 01）之上，把"开箱可跑、可测、可发布"补齐，
为 Sprint 03 起的 PostgreSQL 持久化、OpenMetadata 接入、Hive Connector 打地基。

---

## 一、本次目标

> 一句话：**让任何人 5 分钟内能在自己机器上跑起完整全栈，并且 PR 提交前能跑 lint/test 自检。**

具体：

- ✅ 一键 `docker compose up` 起齐 PostgreSQL / Redis / 后端 / 前端
- ✅ `start.sh` 双模式：本机（venv + uvicorn + vite）+ Docker
- ✅ 后端 26 个 pytest smoke 全绿，覆盖 12 个治理域 API + 健康检查
- ✅ 前端 ESLint 9（flat config）+ Prettier 3 + 0 warning
- ✅ 前端全局错误处理：ErrorBoundary + axios/Query 错误统一 toast
- ✅ Sprint 01 技术债清理：T-02 / T-03 / T-05 / T-09 落地，T-10 部分推进
- ✅ 文档更新：根 README、backend/README、frontend/README、本 sprint 日志、开发总览

---

## 二、完成项

### 2.1 容器化与一键部署（解决 T-09）

```
.
├── docker-compose.yml           # 4 服务编排（postgres / redis / backend / frontend）
├── .env.example                 # 顶层环境变量模板
├── backend/
│   ├── Dockerfile               # python:3.11-slim + uvicorn + healthcheck
│   └── .dockerignore
├── frontend/
│   ├── Dockerfile               # 多阶段：node 22 build → nginx 1.27 runtime
│   ├── nginx.conf               # SPA fallback + /api 反代到 backend 服务
│   └── .dockerignore
└── start.sh                     # 增加 --docker 子模式
```

**服务清单**

| 服务 | 镜像 | 端口 | healthcheck | 备注 |
|---|---|---|---|---|
| `postgres` | `postgres:15-alpine` | 5432 | `pg_isready` | Sprint 03 起后端真读写 |
| `redis`    | `redis:7-alpine`     | 6379 | `redis-cli ping` | 缓存 / 任务队列基线 |
| `backend`  | 自建 | 8000 | `/health` | uvicorn，环境变量已注入 DATABASE_URL/REDIS_URL（占位） |
| `frontend` | 自建（多阶段） | 5173 | `wget /` | nginx 静态托管 + 反代 `/api` 到 `backend:8000` |

**首启命令**

```bash
cp .env.example .env
./start.sh --docker          # = docker compose up -d --build
./start.sh --docker logs     # 跟随日志
./start.sh --docker down     # 停止
```

**关键决策**：`postgres` / `redis` 在 Sprint 02 即引入并保持运行，但后端 API 当前**仍走内存 Mock**。理由是先把基础设施稳定下来，避免 Sprint 03 同时改容器编排 + ORM + 测试基础设施三件事。`backend` 已通过 `DATABASE_URL` / `REDIS_URL` 环境变量做好接线，Sprint 03 只需新增 SQLAlchemy 仓储层。

### 2.2 后端 pytest smoke 测试（解决 T-03）

```
backend/
└── tests/
    ├── __init__.py
    ├── conftest.py              # session 级 TestClient fixture
    ├── test_system.py           # health / root / openapi schema
    └── test_api_smoke.py        # 12 治理域 API 全覆盖
```

**覆盖矩阵（26 个用例）**

| 模块 | 用例 |
|---|---|
| 系统 | 3：health、root、openapi（断言 12 路由前缀都存在） |
| Overview | 4：kpi、3 条 trend（参数化）、domain-coverage |
| Metadata | 2：sources 列表、404 |
| Catalog | 4：分页、按 layer 过滤、关键字搜索、详情 + 404 |
| Quality | 2：rules（验 7 维度集合）、incidents（验 P0/P1 等级） |
| Lineage | 1：graph（验 edge.source/target 都存在于 nodes） |
| Standards / Metrics / MDM / Lifecycle | 4：参数化简单列表 |
| Security | 1：classifications（验 PII 等级集合） |
| AI Hub | 2：prompts（验 success_rate 0-1）、invocations |
| Reports | 1：list |
| 通用 | 2：响应包装 `{success,code,message,data}` 全部模块、X-Tenant-Id Header 透传 |

```bash
$ pytest -q
..........................                                               [100%]
26 passed in 0.16s
```

**配置**：`pyproject.toml` 加了 `[tool.pytest.ini_options]`，`testpaths = ["tests"]`、`-ra --strict-markers`。

### 2.3 前端 ESLint + Prettier（解决 T-02）

| 工具 | 版本 | 选型理由 |
|---|---|---|
| ESLint | 9.x | flat config（`eslint.config.js`），是 2025+ 推荐 |
| typescript-eslint | 8.x | 与 ESLint 9 + flat 兼容 |
| eslint-plugin-react | 7.x | + jsx-runtime preset，免去手写 React import |
| eslint-plugin-react-hooks | 5.x | recommended 规则 |
| eslint-plugin-react-refresh | 0.4 | Vite 热更约束 |
| eslint-config-prettier | 9.x | 关闭与 Prettier 冲突的格式规则 |
| Prettier | 3.x | `singleQuote / trailingComma=all / printWidth=100` |

**npm scripts**

```jsonc
{
  "lint":         "eslint .",                  // 仅 fail on errors
  "lint:strict":  "eslint . --max-warnings 0", // CI 严格模式
  "lint:fix":     "eslint . --fix",
  "format":       "prettier --write .",
  "format:check": "prettier --check .",
  "typecheck":    "tsc --noEmit"
}
```

**结果**：全量 `prettier --write` + 修一处 `MainLayout.tsx` 中未使用的 `Avatar` 导入后，`lint:strict` / `typecheck` / `build` 三件套全绿。

### 2.4 前端全局错误处理（解决 T-05）

```
frontend/src/
├── components/
│   ├── AppShell.tsx          # AntD <App> + FeedbackBridge（注入 message/notification）
│   └── ErrorBoundary.tsx     # 渲染期异常兜底，路由切换自动重置
├── api/
│   ├── client.ts             # axios 拦截器：success===false 也抛 reject
│   └── query-provider.tsx    # QueryCache + MutationCache 全局 onError
├── utils/
│   ├── error.ts              # getErrorMessage(err) 友好文案抽取
│   └── feedback.ts           # toast / notify 全局桥（懒注入）
├── layouts/
│   └── MainLayout.tsx        # 用 ErrorBoundary 包裹 <Outlet>
└── main.tsx                  # ConfigProvider > AppShell > QueryProvider > Router
```

**三层防御**

| 异常类型 | 触发位置 | 处理 |
|---|---|---|
| 渲染期异常（throw in render）| 组件树 | `ErrorBoundary` 渲染降级 UI；左侧菜单仍可导航 |
| 请求异常（HTTP 4xx/5xx / 超时 / 断网） | axios | 拦截器 reject → `QueryCache.onError` → `toast.error` |
| 业务异常（HTTP 200 但 `success === false`）| axios 拦截器 | 转成 reject，与请求异常同路径 |
| 静默场景（轮询 / 后台刷新） | useQuery | 用 `meta: { silent: true }` 跳过自动 toast |

**文案抽取优先级**：
`ApiResponse.message → HTTP statusText → axios code（超时 / 断网） → error.message → "未知错误"`

### 2.5 配置与文档更新

- `backend/app/core/config.py`：新增 `database_url` / `redis_url` 字段（Optional），与 docker-compose 注入对齐
- `backend/.env.example`：注释形式给出 `DATABASE_URL` / `REDIS_URL` 模板
- `start.sh`：新增 `--docker [up|down|logs|ps|restart]` 子模式
- 根 `README.md`：把"快速启动"重排为 A·本机 / B·Docker / C·分别启动 三段
- `backend/README.md`：补 Docker 启动 + 测试章节
- `frontend/README.md`：补 lint / format / typecheck 命令 + 错误处理小节
- `doc/Development/00-开发总览.md`：状态表 / 模块成熟度 / 里程碑同步更新

---

## 三、关键决策

| # | 决策 | 理由 |
|---|------|------|
| D-09 | 持久化层（SQLAlchemy + Alembic）**留到 Sprint 03 单独做** | 改造涉及 12 个 API 模块的仓储层 + 13 个 ORM 模型 + 数据迁移脚本，与 OpenMetadata 接入设计强耦合，分开做风险更低 |
| D-10 | docker-compose 中的 `postgres` / `redis` 现在就引入并 `restart: unless-stopped` | 让所有人本地都有"持久化基线"，Sprint 03 切换时不需要再装服务 |
| D-11 | 选 ESLint 9 flat config，而非保留 `.eslintrc` 经典模式 | 2025+ 推荐方向，且 typescript-eslint v8 + react 系列 plugin 已全部支持 |
| D-12 | 错误处理用 AntD v5 `<App>` + 自建 feedback 桥，而非直接 `import { message } from 'antd'` | v5 后者是 legacy 用法，无法继承 ConfigProvider 的主题 / locale；桥能让非 React 模块也可调用 |
| D-13 | Frontend Dockerfile 用 nginx 静态托管 + 反代 `/api`，而非保留 Vite dev server | 生产环境需要静态产物 + CDN 友好；dev 模式仍走 `start.sh` 本机 vite |
| D-14 | `backend/.env.example` 的 DB/Redis 用注释形式给出 | 本机 `start.sh` 模式默认不依赖外部服务，避免新人误以为必须装 PG 才能跑 |
| D-15 | pytest 用 FastAPI `TestClient`（基于 httpx），不真启端口 | 测试快、可并行、与 CI 环境解耦 |

---

## 四、技术债清理 / 新增

### Sprint 01 技术债状态

| ID | 问题 | 状态 |
|---|---|---|
| T-01 | 前端构建产物 2.8 MB 未拆分 chunk | 🟡 暂留（功能页面后会拆，Sprint 04 优化） |
| T-02 | 没有 ESLint / Prettier 配置 | ✅ **已解决** |
| T-03 | 后端没有任何单元测试 | ✅ **已解决**（26 用例） |
| T-04 | Mock 数据写死 | 🟡 Sprint 03 切 PG 时自然消失 |
| T-05 | 前端没有错误边界 / Toast | ✅ **已解决** |
| T-06 | menuItemRender 用 `<a>` | 🟡 暂留 |
| T-07 | OpenAPI `schema` alias 手动对齐 | 🟡 暂留（引入 codegen 后自然消失） |
| T-08 | @ant-design/plots v2 与 v1 文档冲突 | 🟡 已规避 |
| T-09 | 没有 docker-compose 一键起 | ✅ **已解决** |
| T-10 | 多租户 Header 没真生效 | 🟡 部分推进（pytest 已覆盖 Header 透传断言） |

### Sprint 02 新增技术债

| ID | 问题 | 严重 | 处理时机 |
|---|---|---|---|
| T-11 | 前端构建警告 chunk > 500kB | 低 | Sprint 04 路由懒加载 + manualChunks |
| T-12 | 后端测试覆盖率未量化（缺 coverage 报告） | 低 | Sprint 03 引入 `pytest-cov` |
| T-13 | 没有 GitHub Actions / GitLab CI | 中 | Sprint 03 引入：lint + test + build 流水线 |
| T-14 | docker-compose 没有挂卷热更新（开发体验差） | 低 | 本机模式 `start.sh` 已经覆盖此场景，暂不需要 |
| T-15 | 错误日志未上报（前端没接 Sentry / 后端没接日志聚合） | 中 | Phase 2 接入 |

---

## 五、验证记录

### 5.1 后端

```bash
$ cd backend && .venv/bin/python -m pytest -q
..........................                                               [100%]
26 passed in 0.16s

$ docker compose config --services
postgres
redis
backend
frontend
```

### 5.2 前端

```bash
$ npm run lint:strict
✓ 0 errors, 0 warnings

$ npm run typecheck
✓ no errors

$ npm run build
✓ built in 6.92s
dist/index.html                   0.44 kB │ gzip:   0.32 kB
dist/assets/index-*.css           0.58 kB │ gzip:   0.38 kB
dist/assets/index-*.js        2,928.53 kB │ gzip: 903.09 kB
```

### 5.3 容器

```bash
$ docker compose config --quiet
(no output → ok)
```

> 完整 `docker compose up` 端到端拉起需要本地拉镜像（postgres / redis / node / nginx），首次约 3-5 分钟，建议在用户机器上手动执行验收。

---

## 六、下次接续点（Sprint 03 候选）

> **如果下次开发从这里开始**，按以下顺序：

### 6.1 必做（Sprint 03 核心）

1. **后端持久化层**（按 ADR-009 多租户 + RLS 设计）
   - SQLAlchemy 2.x async engine + 13 个 ORM 模型（全部带 `tenant_id` 列）
   - Alembic 初始化 + `0001_init.py` 建表
   - `app/repositories/` 仓储层 + `app/services/` 业务封装（替换路由直接吃 mock）
   - 启动时 seed mock 数据（可重入：基于 `tenant_id + id` upsert）
   - **保留 `USE_MOCK=true` 开关**：本机不装 PG 也能跑（向后兼容）
   - pytest 加上 SQLite in-memory fixture，CI 跑真 DB
2. **CI 流水线**（GitHub Actions）：lint + typecheck + pytest + docker build
3. **后端 coverage 报告**：`pytest-cov`，目标 ≥ 70%（架构 §六.2 验收门槛）

### 6.2 可并行（独立小切片）

- **资产详情页** `/catalog/assets/:id`（前端，纯前端工作量约 0.5d）
- **AI 注释生成 MVP**：调用 OpenAI 兼容接口，输入字段名 → 注释返回 → 写回资产详情
- **血缘图换 AntV G6**：替换当前 JSON 占位（前端约 1d）

### 6.3 必须先回写架构的事

- ADR-009 多租户 RLS 落地细则（Postgres RLS / 应用层 filter / 还是混合）— Sprint 03 启动前必须定
- ADR-006 工作流引擎（Temporal vs Airflow）— Sprint 03 不阻塞，但 Phase 2 之前必须定

---

## 七、本次代码量（估算）

| 部分 | 文件数 | 代码行数（约） |
|---|---|---|
| Docker（compose / 2 Dockerfile / nginx / dockerignore） | 6 | ~180 |
| 后端 tests | 4 | ~190 |
| 后端 config / pyproject 调整 | 2 | +20 |
| 前端 ESLint / Prettier 配置 | 4 | ~95 |
| 前端 ErrorBoundary / AppShell / utils | 4 | ~150 |
| 前端 query-provider / client / main / MainLayout 改造 | 4 | +60 / -20 |
| start.sh 增量 | 1 | +60 |
| 文档（本 sprint + 总览 + 各 README） | 5 | ~550 |
| **合计** | **30** | **~1,300** |

---

## 八、附：与架构文档对应关系

| 本次实现 | 架构出处 | 状态 |
|---|---|---|
| docker-compose 基础设施 | [`Architecture/05 §部署与运维`](../Architecture/05-部署与运维.md) | ✅ 起步版（K8s/Helm 留待 Phase 1 末期） |
| pytest 单元测试 | [`Architecture/06 §六.2 非功能验收`](../Architecture/06-开发路线图与风险.md#62-非功能验收) | 🟡 用例数达标，覆盖率指标待量化 |
| 全局错误处理 + Toast | 内部约定（建议加入架构 UX 章节）| ✅ 已落地 |
| ESLint / Prettier | 内部约定 | ✅ 已落地 |
| 多租户 Header 透传断言 | [`Architecture/00 ADR-009`](../Architecture/00-总体规划-v2.md#32-关键架构决策adr-摘要) | 🟡 测试覆盖，业务隔离待 Sprint 03 RLS |
| PostgreSQL/Redis 编排 | [`Architecture/05`](../Architecture/05-部署与运维.md) | ✅ Compose 下联调路径见 Sprint 03 |

---

> 上一篇：[`01-Sprint01-MVP骨架.md`](./01-Sprint01-MVP骨架.md)
> 下一篇：[`03-Sprint03-持久化层.md`](./03-Sprint03-持久化层.md)
> 回到：[`README`](./README.md) ｜ [`00-开发总览`](./00-开发总览.md)
