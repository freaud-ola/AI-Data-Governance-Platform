"""FastAPI 入口。"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.migrate import alembic_upgrade_head
from app.db.seed import seed_tenant_if_empty
from app.db.session import dispose_engine, init_engine, session_factory

settings_at_import = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.database_enabled:
        assert settings.database_url is not None
        init_engine(settings.database_url)
        alembic_upgrade_head()
        SessionLocal = session_factory()
        sess = SessionLocal()
        try:
            if seed_tenant_if_empty(sess, settings.default_tenant_id):
                pass
            sess.commit()
        finally:
            sess.close()
    yield
    if settings.database_enabled:
        dispose_engine()


app = FastAPI(
    title=settings_at_import.app_name,
    version=__version__,
    description="AI Data Governance Platform - MVP backend (Mock 或 PostgreSQL)",
    debug=settings_at_import.app_debug,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings_at_import.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health() -> dict:
    s = get_settings()
    payload = {
        "status": "ok",
        "service": s.app_name,
        "version": __version__,
        "env": s.app_env,
    }
    if s.database_enabled:
        payload["persistence"] = "postgres"
    else:
        payload["persistence"] = "mock"
    return payload


@app.get("/", tags=["System"])
async def root() -> dict:
    return {
        "service": settings_at_import.app_name,
        "version": __version__,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


app.include_router(api_router)
