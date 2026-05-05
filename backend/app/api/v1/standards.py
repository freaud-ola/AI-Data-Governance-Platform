from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import DataStandard

router = APIRouter()


@router.get("", response_model=ApiResponse[list[DataStandard]])
async def list_standards(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[DataStandard]]:
    return ApiResponse(data=repo.list_data_standards())
