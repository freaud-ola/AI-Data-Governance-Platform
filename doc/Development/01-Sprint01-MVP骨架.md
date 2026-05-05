# Sprint 01 · MVP 骨架搭建

**日期**：2026-04-29  
**目标**：在 1 个工作日内完成可演示的 MVP 骨架版本——前端覆盖架构里全部核心模块的页面框架，后端用 Mock 数据驱动，关键页面前后端联调通过。

---

## 一、本次目标

> 一句话：**让用户/老板第一次打开就能看见"完整治理平台的轮廓"，每个治理域是什么、长什么样一目了然。**

具体：

- ✅ 项目脚手架：`frontend/` + `backend/` + `doc/Development/` 三个一级目录
- ✅ 前端：React 18 + TS + Vite + Ant Design v5 + Pro Components
- ✅ 后端：FastAPI + Pydantic v2 + 内存 Mock
- ✅ 19 个页面 / 12 个 API 模块全部贯通
- ✅ 至少 3 个真实联调示例（总览 / 资产目录 / AI 中台）

---

## 二、完成项

### 2.1 后端（FastAPI）

```
backend/
├── app/
│   ├── api/v1/                # 12 个治理域 API
│   │   ├── overview.py        # 看板 KPI / 趋势 / 业务域覆盖
│   │   ├── metadata.py        # 数据源
│   │   ├── catalog.py         # 资产目录（搜索/筛选/分页）
│   │   ├── quality.py         # 规则 + 工单
│   │   ├── lineage.py         # 血缘图
│   │   ├── standards.py
│   │   ├── metrics_store.py
│   │   ├── mdm.py
│   │   ├── lifecycle.py
│   │   ├── security.py
│   │   ├── ai_hub.py          # Prompt + LLM 调用
│   │   └── reports.py
│   ├── core/
│   │   ├── config.py          # pydantic-settings 全局配置
│   │   └── tenant.py          # X-Tenant-Id 租户上下文
│   ├── mock/data.py           # 全部 Mock 数据
│   ├── schemas/
│   │   ├── common.py          # ApiResponse / PageMeta / PageData
│   │   └── models.py          # 14 个核心实体
│   └── main.py                # FastAPI 入口（含 CORS / 健康检查）
├── pyproject.toml
├── requirements.txt
├── .env.example
└── README.md
```

- 总路由数：**26 条**（含健康检查、根路径）
- 统一响应包装：`{ success, code, message, data }`
- 多租户：所有 API 默认从 `X-Tenant-Id` 头读，缺省 `default`
- CORS：默认放开 `localhost:5173 / 127.0.0.1:5173`

**自检**：

```bash
curl -s http://localhost:8000/health
# {"status":"ok","service":"AI Data Governance Platform","version":"0.1.0","env":"dev"}

curl -s "http://localhost:8000/api/v1/overview/kpi"
# 返回 KPI JSON
```

### 2.2 前端（Vite + React + AntD）

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts          # axios 实例 + 拦截器
│   │   ├── query-provider.tsx # TanStack Query 全局
│   │   └── services.ts        # 12 个模块的 API 服务封装
│   ├── components/
│   │   ├── PageHeader.tsx
│   │   └── ModuleStatusBanner.tsx  # 统一标识模块成熟度
│   ├── layouts/
│   │   └── MainLayout.tsx     # ProLayout 主框架
│   ├── pages/                 # 19 个页面
│   │   ├── overview/Overview.tsx
│   │   ├── metadata/Metadata.tsx
│   │   ├── catalog/{Catalog,Glossary}.tsx
│   │   ├── profiling/Profiling.tsx
│   │   ├── quality/{Quality,Incidents}.tsx
│   │   ├── lineage/Lineage.tsx
│   │   ├── standards/Standards.tsx
│   │   ├── metrics/Metrics.tsx
│   │   ├── mdm/MDM.tsx
│   │   ├── lifecycle/Lifecycle.tsx
│   │   ├── security/{Security,Audit}.tsx
│   │   ├── ai-hub/{AIHub,PromptRegistry,NL2SQLPlayground}.tsx
│   │   ├── reports/Reports.tsx
│   │   └── settings/Settings.tsx
│   ├── routes/routes.tsx      # 路由表 + 7 个一级菜单分组
│   ├── styles/global.css
│   ├── types/api.ts           # 与后端 Pydantic 对齐
│   ├── App.tsx
│   └── main.tsx
├── vite.config.ts             # 含 /api 反代到 8000
├── tsconfig.json
├── package.json
└── README.md
```

- 状态管理：TanStack Query（服务端态）+ React 内置 useState（局部态）
- 路由：React Router v6
- 国际化：默认 zh-CN（AntD ConfigProvider + dayjs）
- 类型安全：与后端 Pydantic Schema 一对一映射在 `src/types/api.ts`
- 构建：**通过 `tsc -b && vite build` 全量类型检查 + 生产构建**（产物 ~880 kB gzipped）

### 2.3 前后端联调示例

| 页面 | 调用 | 验证方式 |
|---|---|---|
| 总览看板 | `GET /api/v1/overview/{kpi,trend/quality,trend/asset,domain-coverage}` + `GET /api/v1/quality/incidents` | 浏览器 → KPI 数字、趋势图、域覆盖表均渲染 |
| 资产目录 | `GET /api/v1/catalog/assets?keyword=&domain=&layer=&page=` | 12 张资产分页显示，搜索/筛选可用 |
| AI 中台 | `GET /api/v1/ai/{prompts,invocations}` + 复用 overview KPI | Prompt 表 + 近期 LLM 调用表均渲染 |

### 2.4 文档

```
doc/
└── Development/
    ├── README.md                  # 索引 + 写作约定
    ├── 00-开发总览.md             # 进度全景 + 模块成熟度矩阵
    └── 01-Sprint01-MVP骨架.md     # 本文
```

---

## 三、关键决策

| # | 决策 | 理由 |
|---|------|------|
| D-01 | 一次性把 19 个页面 + 12 个 API 占位完整搭出来，而不是只做"几个核心页" | 用户原话"先搭一个整体可看见骨架的 MVP"——优先**完整轮廓**而非"几个深入页" |
| D-02 | 后端 MVP 用内存 Mock，不引入数据库 | 缩短从 0 到能 demo 的时间；后续替换为 OpenMetadata / PostgreSQL 时只改 service 层 |
| D-03 | 前端按 7 大一级菜单分组：总览 / 元数据与目录 / 质量血缘 / 建模治理 / 安全合规 / AI 中台 / 报告系统 | 与架构 §五 模块全景对齐，且自然分散到不同 Sprint |
| D-04 | 引入 `<ModuleStatusBanner stage="mvp-skeleton">` 组件，每个页面顶部显眼标识 | "骨架"和"真实功能"必须对用户可见，避免误以为已上线 |
| D-05 | 后端 Schema 用 `Optional[X]` 替代 `X \| None`，兼容 Python 3.9 | 本机只有 3.9.6，无 Homebrew；不影响 3.11+ 生产环境 |
| D-06 | TS 类型与 Pydantic Schema 手工同步（不引入 OpenAPI codegen） | 当前规模下手工成本低；Phase 2 模块复杂时再引入 `openapi-typescript` 自动生成 |
| D-07 | NL2SQL Playground 加交互骨架（输入框 + 示例提问 + 假返回） | 让最重要的差异化能力"可点击"，演示效果好 |
| D-08 | 血缘图先放 JSON 占位，不引入 AntV G6 | G6 调试成本高，留到 Phase 3 一起做（与运行时 Hook 联动） |

---

## 四、已知问题 / 技术债

| ID | 问题 | 严重 | 处理时机 |
|---|---|---|---|
| T-01 | 前端构建产物 2.8 MB，未拆分 chunk | 中 | Phase 1 末期做 manual chunks 优化 |
| T-02 | 没有 ESLint / Prettier 配置 | 中 | Sprint 02 加 |
| T-03 | 后端没有任何单元测试（pyproject 已声明 pytest） | 中 | Sprint 02 至少加 API smoke test |
| T-04 | Mock 数据写死在 Python 文件，没法热更新 | 低 | 切真实存储后自然消失 |
| T-05 | 前端没有错误边界 / 全局 Toast 提示 | 中 | Sprint 02 加 |
| T-06 | `MainLayout` 中 menuItemRender 用了 `<a>`，可访问性可优化 | 低 | 后续重构 |
| T-07 | 后端 OpenAPI Schema 中 `schema` 字段用了 alias，TS 端要手动对齐 | 低 | 已用 populate_by_name 保留 |
| T-08 | 前端用的 `@ant-design/plots` v2 API 与社区文档大量 v1 示例不一致 | 低 | 已规避（用 `shapeField` / `style.fill`） |
| T-09 | 没有 docker-compose 一键起 | 中 | Sprint 02 加（PostgreSQL + Redis + 后端） |
| T-10 | 多租户只在 Header 占位，没有真正生效 | 中 | Sprint 02 接 SSO 后真做 |

---

## 五、验证记录

### 5.1 后端

```bash
$ python -c "from app.main import app; print(app.title)"
AI Data Governance Platform

$ curl -s http://127.0.0.1:8000/api/v1/overview/kpi
{"success":true,"code":0,"message":"ok","data":{"asset_total":2880,...}}
```

### 5.2 前端

```bash
$ npm run build
✓ 5943 modules transformed.
✓ built in 7.08s
```

### 5.3 浏览器实测（截图见 sprint 附件）

- ✅ http://localhost:5173/overview — KPI 卡片 8 张、趋势图 2 张、业务域表、最新工单
- ✅ http://localhost:5173/catalog — 12 条资产分页、关键字 + 域 + 分层筛选可用
- ✅ http://localhost:5173/ai-hub — Prompt 列表 + 近期 LLM 调用日志
- ✅ http://localhost:5173/metadata — 6 个数据源（含 1 个 error 状态）
- ✅ 全部 19 个路由可正常导航

---

## 六、下次接续点（重要）

> **如果下次开发从这里开始**，按以下顺序：

### 6.1 立刻可以做的（建议 Sprint 02 优先级）

1. **加 Docker Compose 一键起**（前端 + 后端 + PostgreSQL + Redis） — `T-09`
2. **后端切真实 PostgreSQL**：建库 + alembic 迁移 + 把 Mock 数据写进去 — 准备 OpenMetadata 接入前的基线
3. **前端加错误处理 + Toast**（`T-05`）+ ESLint/Prettier（`T-02`）
4. **OpenMetadata 部署 + 二次开发开始**：跑通"OpenMetadata Schema → 我们的 DataSource/DataAsset"映射
5. **Hive HMS Thrift Connector 雏形**：先用一个本地 Hive Docker 镜像跑通 1 张表的元数据采集

### 6.2 选做但价值高

- **AI 注释生成 MVP**：调用任意一个 OpenAI 兼容接口，输入字段名 → 返回注释 → 写回资产详情页
- **资产详情页**：当前只有列表，缺详情（建议 Sprint 02 加 `/catalog/assets/:id`）
- **血缘图换 AntV G6**：现在是 JSON 占位，做一个简单的有向图

### 6.3 必须先回写架构的事

> 如果以下假设有变，**先改 `doc/Architecture/`** 再写代码：

- 选 Keycloak 还是 Casdoor？— `Architecture/00 §六` 里写了"Keycloak / Casdoor 二选一"，落地时必须定一个
- 选 Temporal 还是 Airflow？— `Architecture/00 ADR-006` 留了备选，落地时定下来
- 多租户的 RLS 策略具体怎么实现？— `Architecture/00 ADR-009` 只到方向，没到实现细节

---

## 七、本次代码量（估算）

| 部分 | 文件数 | 代码行数（约） |
|---|---|---|
| 后端 Python | 19 | ~1,100 |
| 前端 TS / TSX | 28 | ~2,300 |
| 文档 | 3 | ~700 |
| 配置（package.json、pyproject、tsconfig、vite等） | 9 | ~250 |
| **合计** | **59** | **~4,350** |

---

## 八、附：与架构文档对应关系

| 本次实现 | 架构出处 | 状态 |
|---|---|---|
| 19 个模块页面 | [`Architecture/00 §五 核心模块全景`](../Architecture/00-总体规划-v2.md#五核心模块全景) | ✅ 全部对齐 |
| 后端 12 API 域 | [`Architecture/01 §治理域全景`](../Architecture/01-元数据接入与建模.md) | ✅ |
| 多租户 Header | [`Architecture/00 ADR-009`](../Architecture/00-总体规划-v2.md#32-关键架构决策adr-摘要) | 雏形 |
| 统一 ApiResponse | 内部约定（未明文写架构）| 已落地 |
| ModuleStatusBanner | 内部约定（建议加入架构）| 已落地 |
| 7 大菜单分组 | [`Architecture/00 §四 治理域 mindmap`](../Architecture/00-总体规划-v2.md#四核心治理域) | 收敛对齐 |

---

> 上一篇：—  
> 下一篇：（Sprint 02 待写）  
> 回到：[`README`](./README.md) ｜ [`00-开发总览`](./00-开发总览.md)
