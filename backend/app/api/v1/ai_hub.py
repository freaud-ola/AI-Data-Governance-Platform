from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import AIInvocation, AIPrompt

router = APIRouter()


@router.get("/prompts", response_model=ApiResponse[list[AIPrompt]])
async def list_prompts(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[AIPrompt]]:
    return ApiResponse(data=repo.list_ai_prompts())


@router.get("/invocations", response_model=ApiResponse[list[AIInvocation]])
async def list_invocations(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[AIInvocation]]:
    return ApiResponse(data=repo.list_ai_invocations())
