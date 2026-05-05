from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import LineageGraph

router = APIRouter()


@router.get("/graph", response_model=ApiResponse[LineageGraph])
async def get_graph(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[LineageGraph]:
    return ApiResponse(data=repo.get_lineage_graph())
