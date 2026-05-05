from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import SecurityClassification

router = APIRouter()


@router.get("/classifications", response_model=ApiResponse[list[SecurityClassification]])
async def list_classifications(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[SecurityClassification]]:
    return ApiResponse(data=repo.list_security_classifications())
