
from fastapi import APIRouter, Depends, Query

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse, PageData
from app.schemas.models import DataAsset

router = APIRouter()


@router.get("/assets", response_model=ApiResponse[PageData[DataAsset]])
async def list_assets(
    repo: GovernanceRepository = Depends(get_governance_repository),
    keyword: str | None = Query(default=None, description="模糊搜索：表名 / 描述 / Owner"),
    domain: str | None = Query(default=None),
    layer: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=200),
) -> ApiResponse[PageData[DataAsset]]:
    items, meta = repo.list_assets_page(
        keyword=keyword, domain=domain, layer=layer, page=page, page_size=page_size
    )
    return ApiResponse(data=PageData(items=items, meta=meta))


@router.get("/assets/{asset_id}", response_model=ApiResponse[DataAsset])
async def get_asset(
    asset_id: str,
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[DataAsset]:
    hit = repo.get_asset(asset_id)
    if hit is None:
        return ApiResponse(success=False, code=404, message="asset not found", data=None)
    return ApiResponse(data=hit)
