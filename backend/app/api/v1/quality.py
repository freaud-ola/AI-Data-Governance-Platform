from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import QualityIncident, QualityRule

router = APIRouter()


@router.get("/rules", response_model=ApiResponse[list[QualityRule]])
async def list_rules(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[QualityRule]]:
    return ApiResponse(data=repo.list_quality_rules())


@router.get("/incidents", response_model=ApiResponse[list[QualityIncident]])
async def list_incidents(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[QualityIncident]]:
    return ApiResponse(data=repo.list_quality_incidents())
