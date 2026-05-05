# Backend (FastAPI) · AI Data Governance Platform

MVP 阶段后端支持两种数据源：

1. **默认**：`USE_MOCK=true`，**FastAPI + Pydantic v2 + 内存 Mock**（与本机/pytest 默认一致）。
2. **PostgreSQL**：`USE_MOCK=false` 且配置 `DATABASE_URL`（Compose 已为 `backend` 注入），启动时 Alembic 迁移并 seed。

后续会接入 OpenMetadata / Hive HMS / GE / Soda / Langfuse 等真实底座。

---

## 快速启动

### 本机

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker（推荐，含 PG/Redis）

```bash
# 在项目根目录
./start.sh --docker
```

访问：

- Swagger UI: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json
- 健康检查: http://localhost:8000/health

---

## 测试

```bash
# 装上 dev 依赖（首次）
pip install -r requirements-dev.txt
# 或者：pip install -e ".[dev]"

pytest -q
```

当前覆盖：

- 系统级（health / root / openapi 路由完整性）
- 12 个治理域 API 的 smoke：响应包装、分页、筛选、404、租户 Header
- 共 26 个用例

---

## 目录结构

```
backend/
├── app/
│   ├── api/v1/          # 各模块 API（按治理域拆分）
│   ├── core/            # 配置 / 多租户上下文
│   ├── db/              # 引擎、迁移触发、seed
│   ├── models/          # ORM
│   ├── repositories/    # Governance 仓储抽象与实现
│   ├── mock/            # Mock 数据（MVP）
│   ├── schemas/         # Pydantic Schema
│   └── main.py
├── alembic/             # Alembic 版本脚本
├── tests/
├── alembic.ini
├── pyproject.toml
├── requirements-dev.txt
└── requirements.txt
```

## API 模块全景

| Prefix | 模块 | 状态 |
|---|---|---|
| `/api/v1/overview` | 总览看板 | Mock |
| `/api/v1/metadata` | 元数据中心 | Mock |
| `/api/v1/catalog` | 资产目录 / 搜索 | Mock |
| `/api/v1/quality` | 数据质量 | Mock |
| `/api/v1/lineage` | 数据血缘 | Mock |
| `/api/v1/standards` | 数据标准 | Mock |
| `/api/v1/metrics` | 指标管理 | Mock |
| `/api/v1/mdm` | 主数据 | Mock |
| `/api/v1/lifecycle` | 生命周期 | Mock |
| `/api/v1/security` | 数据安全 | Mock |
| `/api/v1/ai` | AI 能力中台 | Mock |
| `/api/v1/reports` | 报告中心 | Mock |
