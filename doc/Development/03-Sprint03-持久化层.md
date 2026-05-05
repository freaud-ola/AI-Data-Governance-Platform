# Sprint 03 · 后端持久化层（接续 Sprint 02）

**本次目标**：在保留 `USE_MOCK=true` 默认路径的前提下，为 Docker / 集成环境接上 **PostgreSQL 持久化**：ORM、迁移、Seed、仓储抽象，与各 v1 路由解耦。

**状态**：主干已落地（2026-05-03）。**GitHub Actions**（后端 ruff + pytest 覆盖率 ≥70%、前端 lint/typecheck/build、Postgres 服务矩阵冒烟）已于 2026-05-05 接入；**SQLite 单测矩阵、RLS 细则**仍为后续项（见文末）。

---

## 一、完成项

| 项 | 说明 |
|---|---|
| 配置 | `backend/app/core/config.py`：`use_mock`（默认 `True`）、`database_enabled`（`not use_mock` 且配置 `database_url`） |
| 依赖 | `sqlalchemy`、`alembic`、`psycopg[binary]`（`requirements.txt` / `pyproject.toml`） |
| ORM | `backend/app/models/orm.py`：数据源、资产、质量、标准/指标/MDM/生命周期/安全/AI/报告 + `tenant_blobs` |
| 会话 | `backend/app/db/session.py`：引擎初始化、`db_session_dependency`（Mock 下不建连） |
| 迁移 | `backend/alembic/` + `alembic.ini`；`app/db/migrate.py` 在启动时 `upgrade head` |
| Seed | `backend/app/db/seed.py`：默认租户可重入 upsert，与 Sprint 01 Mock 对齐 |
| 仓储 | `backend/app/repositories/governance.py`：`MockGovernanceRepository` / `SqlGovernanceRepository` |
| 依赖注入 | `backend/app/deps.py`：`get_governance_repository`；各 `api/v1/*.py` 统一 `Depends` |
| 生命周期 | `backend/app/main.py`：启用 DB 时 `init_engine` → migrate → seed → shutdown `dispose` |
| 健康检查 | `/health` 增加 `persistence`: `"mock"` \| `"postgres"` |
| Compose | 根目录 `docker-compose.yml`：`backend` 服务 `USE_MOCK=false` + `DATABASE_URL` 指向 `postgres` |

---

## 二、关键决策

1. **默认 Mock**：本机无 PG 时零配置；pytest 默认环境仍为 Mock，与既有 26 条 smoke 兼容。
2. **Docker 真库**：Compose 内后端固定走 PG（与 Sprint 02「容器已就位」衔接），启动时自动迁移 + seed。
3. **Tenant**：当前仅对 `default`（及配置中的默认租户）做完整 seed；其他 `X-Tenant-Id` 在 PG 模式下返回空集，除非扩展 seed。

---

## 三、已知问题 / 技术债

- **RLS**：多租户行级策略（ADR-009）未在 DB 层启用，仅靠应用层 `tenant_id` 过滤。
- **异步 Engine**：当前为同步 SQLAlchemy；若后续高并发再评估 async session。
- **测试矩阵**：尚未加「内存 SQLite fixture」或「CI 起 PG」的集成测试。

---

## 四、下次接续点（Sprint 03 收尾 / Sprint 04）

1. ~~**GitHub Actions**：ruff / pytest /（可选）docker build~~ → 已实现：`.github/workflows/ci.yml`；镜像构建可作为后续独立 job 追加。
2. ~~**`pytest-cov`**：接入 `requirements-dev.txt`，逐步把覆盖率拉到架构文档门槛~~ → 已在 `pyproject.toml` 启用 `--cov-fail-under=70`（当前约 76% 含分支覆盖）。
3. ~~**可选**：Postgres 集成测试 job~~ → CI 中 `backend-postgres` job 已对 `USE_MOCK=false` + 迁移 + seed 跑全套 pytest。
4. **SQLite in-memory**：仅验证迁移/仓储逻辑（减轻 CI 对 Docker service 的依赖，可选）。
5. **产品向**：OpenMetadata 接入、资产详情页等按 `02-Sprint02` 文档 6.2 并行。

---

> 上一篇：[`02-Sprint02-基础设施加固.md`](./02-Sprint02-基础设施加固.md)  
> 回到：[`README`](./README.md) ｜ [`00-开发总览`](./00-开发总览.md)
