# AI-Data-Governance-Platform

> 一个 **AI Native** 的通用数据治理平台。在成熟开源元数据底座（OpenMetadata）之上，叠加完整治理域 + 工业级 AI 能力层。

**当前版本**：MVP v0.1 · 骨架版 · 2026-04-29

---

## 一句话定位

**用 AI 把"数据治理"从看板和工单，升级为可观测、可自动化、可合规的工程系统。**

---

## 快速启动

### 方式 A · 本机模式（推荐用于日常开发）

在项目根目录执行：

```bash
./start.sh
```

脚本会自动完成：

- 创建 `backend/.venv` 并安装 Python 依赖（首次）
- 复制 `backend/.env.example` → `backend/.env`（首次）
- 在 `frontend/` 执行 `npm install`（首次）
- 同时启动 **FastAPI**（:8000） + **Vite**（:5173）
- 实时合并打印两边日志到当前终端，并写入 `.logs/`
- `Ctrl+C` 一次性优雅停止前后端

常用选项：

```bash
./start.sh --backend          # 只启动后端
./start.sh --frontend         # 只启动前端
./start.sh --reinstall        # 强制重装前后端依赖
BACKEND_PORT=8001 FRONTEND_PORT=5174 ./start.sh   # 自定义端口
```

### 方式 B · Docker 模式（一键拉起含 PG / Redis 的完整基线）

```bash
cp .env.example .env          # 首次：调整 POSTGRES_PASSWORD 等
./start.sh --docker           # 等价于 docker compose up -d --build
./start.sh --docker down      # 停止
./start.sh --docker logs      # 跟随日志
```

包含的服务：

| 服务 | 镜像 | 端口 | 说明 |
|---|---|---|---|
| `postgres`  | `postgres:15-alpine` | 5432 | 持久化基线（Sprint 03 起后端真正读写） |
| `redis`     | `redis:7-alpine`     | 6379 | 缓存 / 任务队列基线 |
| `backend`   | 自建（`backend/Dockerfile`） | 8000 | FastAPI + uvicorn，含 healthcheck |
| `frontend`  | 自建（多阶段 nginx） | 5173 | Vite 构建产物 + Nginx 反代 `/api` 到 backend |

> Windows 用户：本机模式建议在 WSL 中运行 `start.sh`，或直接使用 Docker 模式。

#### 国内 / 受限网络无法拉镜像？

如果 `python:3.11-slim` 等基础镜像 build 时超时（典型报错：`auth.docker.io ... i/o timeout`），原因通常是 **BuildKit 不读 daemon 的 `registry-mirrors`**。

修复：编辑根目录 `.env`，把 `IMAGE_REGISTRY` 改成可达的 docker.io 镜像源（compose 与 Dockerfile 都会自动用）：

```bash
# .env
IMAGE_REGISTRY=docker.m.daocloud.io/library     # daocloud 镜像
# 或
IMAGE_REGISTRY=docker.1panel.live/library
# 或
IMAGE_REGISTRY=dockerproxy.com/library
```

之后 `./start.sh --docker` 就会从 mirror 拉所有官方镜像（postgres / redis / python / node / nginx）。

后端镜像构建阶段的 pip 默认走清华 TUNA PyPI（根目录 `.env` / `.env.example` 里的 `PIP_INDEX_URL`）；若在境外构建可改为 `https://pypi.org/simple`。

### 方式 C · 分别启动

#### C-1 启动后端（FastAPI）

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

uvicorn app.main:app --reload --port 8000
```

- Swagger UI: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

#### C-2 启动前端（Vite + React + AntD）

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

> 前端通过 Vite proxy 把 `/api` 转发到后端 `:8000`，**无需配置跨域**。

---

## 项目结构

```
AI-Data-Governance-Platform/
├── frontend/                # React 18 + TS + Vite + AntD v5 + Pro Components
├── backend/                 # FastAPI + Pydantic v2（MVP 用内存 Mock）
├── doc/
│   ├── Architecture/        # 架构设计文档（v2）
│   └── Development/         # 开发日志 + 进度记录
├── docker-compose.yml       # 一键编排：postgres + redis + backend + frontend
├── .env.example             # docker-compose 顶层环境变量模板
├── start.sh                 # 一键启动前后端（本机 / Docker 双模式）
├── 数据治理平台技术选型规划书-v1.md   # v1 历史归档
├── LICENSE
└── README.md
```

---

## 文档地图

### 架构设计 — 长期稳定，回答 WHAT / WHY

| 入口 | 内容 |
|---|---|
| [`doc/Architecture/README.md`](./doc/Architecture/README.md) | 架构文档总索引 |
| [`doc/Architecture/00-总体规划-v2.md`](./doc/Architecture/00-总体规划-v2.md) | **从这里开始**：背景、设计原则、整体架构、技术栈 |
| [`doc/Architecture/01-元数据接入与建模.md`](./doc/Architecture/01-元数据接入与建模.md) | 治理域全景、Connector、Hive/MySQL/Iceberg/dbt/调度接入 |
| [`doc/Architecture/02-数据质量与血缘.md`](./doc/Architecture/02-数据质量与血缘.md) | DQ 7 维度、SLA、漂移、双轨血缘、OpenLineage |
| [`doc/Architecture/03-AI能力层设计.md`](./doc/Architecture/03-AI能力层设计.md) | LLM 路由、Prompt 治理、NL2SQL、RAG、Agent + MCP、LLMOps |
| [`doc/Architecture/04-安全与合规.md`](./doc/Architecture/04-安全与合规.md) | 分级分类、脱敏、RBAC/ABAC、审计、个保法/GDPR |
| [`doc/Architecture/05-部署与运维.md`](./doc/Architecture/05-部署与运维.md) | K8s/Helm、多租户、监控、告警、CI/CD |
| [`doc/Architecture/06-开发路线图与风险.md`](./doc/Architecture/06-开发路线图与风险.md) | Phase 1-5 计划、MVP 验收、风险清单 |

### 开发日志 — 高频更新，回答 HOW FAR / NEXT

| 入口 | 内容 |
|---|---|
| [`doc/Development/README.md`](./doc/Development/README.md) | 索引 + 写作约定 |
| [`doc/Development/00-开发总览.md`](./doc/Development/00-开发总览.md) | **当前进度** + 模块成熟度矩阵 + 快速上手 |
| [`doc/Development/01-Sprint01-MVP骨架.md`](./doc/Development/01-Sprint01-MVP骨架.md) | Sprint 01 完成项 / 决策 / 已知问题 / 下次接续点 |

> v1 历史归档：[`数据治理平台技术选型规划书-v1.md`](./数据治理平台技术选型规划书-v1.md)（已不再维护）

---

## 当前模块状态

| 模块 | 状态 | 说明 |
|------|------|------|
| 总览看板 | ✅ MVP UI + Mock | KPI / 趋势 / 域覆盖 / 工单 |
| 元数据中心 | ✅ MVP UI + Mock | 6 类数据源 |
| 资产目录 | ✅ MVP UI + Mock | 搜索 + 分层 + 域筛选 |
| 业务术语 | 🟡 占位 | Phase 2 |
| 数据探查 | 🟡 占位 | Phase 2 |
| 数据质量 | ✅ MVP UI + Mock | 7 维度规则 + 工单 |
| 数据血缘 | ✅ MVP UI + Mock | JSON 占位（待接 G6） |
| 数据标准 | ✅ MVP UI + Mock | – |
| 指标管理 | ✅ MVP UI + Mock | GMV / DAU / ARPU |
| 主数据 (MDM) | ✅ MVP UI + Mock | – |
| 生命周期 / 成本 | ✅ MVP UI + Mock | – |
| 数据安全 | ✅ MVP UI + Mock | 分级分类 + 脱敏 |
| 审计日志 | 🟡 占位 | Phase 1 末期 |
| AI 能力中台 | ✅ MVP UI + Mock | Prompt + LLM 调用 |
| NL2SQL Playground | ✅ 交互演示 | 静态返回（Phase 4 工业化） |
| 报告中心 | ✅ MVP UI + Mock | – |
| 系统设置 | ✅ MVP UI + Mock | 租户 / SSO / LLM Provider |

详细矩阵与下次接续点见 [`doc/Development/00-开发总览.md`](./doc/Development/00-开发总览.md)。

---

## License

[Apache License 2.0](./LICENSE)
