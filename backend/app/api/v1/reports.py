from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import ReportItem

router = APIRouter()


@router.get("", response_model=ApiResponse[list[ReportItem]])
async def list_reports(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[ReportItem]]:
    return ApiResponse(data=repo.list_reports())
