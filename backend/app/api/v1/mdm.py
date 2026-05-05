from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import MasterEntity

router = APIRouter()


@router.get("/entities", response_model=ApiResponse[list[MasterEntity]])
async def list_entities(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[MasterEntity]]:
    return ApiResponse(data=repo.list_master_entities())
