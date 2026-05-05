from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import DataSource

router = APIRouter()


@router.get("/sources", response_model=ApiResponse[list[DataSource]])
async def list_sources(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[DataSource]]:
    return ApiResponse(data=repo.list_data_sources())


@router.get("/sources/{source_id}", response_model=ApiResponse[DataSource])
async def get_source(
    source_id: str,
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[DataSource]:
    hit = repo.get_data_source(source_id)
    if hit is None:
        return ApiResponse(success=False, code=404, message="data source not found", data=None)
    return ApiResponse(data=hit)
