from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import Metric

router = APIRouter()


@router.get("", response_model=ApiResponse[list[Metric]])
async def list_metrics(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[Metric]]:
    return ApiResponse(data=repo.list_metrics())
