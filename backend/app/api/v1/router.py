"""v1 API 路由总入口。"""

from fastapi import APIRouter

from app.api.v1 import (
    ai_hub,
    catalog,
    lifecycle,
    lineage,
    mdm,
    metadata,
    metrics_store,
    overview,
    quality,
    reports,
    security,
    standards,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(overview.router, prefix="/overview", tags=["Overview"])
api_router.include_router(metadata.router, prefix="/metadata", tags=["Metadata"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["Catalog"])
api_router.include_router(quality.router, prefix="/quality", tags=["Quality"])
api_router.include_router(lineage.router, prefix="/lineage", tags=["Lineage"])
api_router.include_router(standards.router, prefix="/standards", tags=["Standards"])
api_router.include_router(metrics_store.router, prefix="/metrics", tags=["Metrics"])
api_router.include_router(mdm.router, prefix="/mdm", tags=["MDM"])
api_router.include_router(lifecycle.router, prefix="/lifecycle", tags=["Lifecycle"])
api_router.include_router(security.router, prefix="/security", tags=["Security"])
api_router.include_router(ai_hub.router, prefix="/ai", tags=["AI Hub"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
