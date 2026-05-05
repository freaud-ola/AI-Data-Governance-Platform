from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import LifecyclePolicy

router = APIRouter()


@router.get("/policies", response_model=ApiResponse[list[LifecyclePolicy]])
async def list_policies(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[LifecyclePolicy]]:
    return ApiResponse(data=repo.list_lifecycle_policies())
