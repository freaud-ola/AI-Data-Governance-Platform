from fastapi import APIRouter, Depends

from app.deps import get_governance_repository
from app.repositories.governance import GovernanceRepository
from app.schemas.common import ApiResponse
from app.schemas.models import DomainCoverage, OverviewKPI, TimePoint

router = APIRouter()


@router.get("/kpi", response_model=ApiResponse[OverviewKPI])
async def get_kpi(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[OverviewKPI]:
    return ApiResponse(data=repo.get_overview_kpi())


@router.get("/trend/quality", response_model=ApiResponse[list[TimePoint]])
async def get_quality_trend(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[TimePoint]]:
    return ApiResponse(data=repo.get_quality_trend())


@router.get("/trend/lineage", response_model=ApiResponse[list[TimePoint]])
async def get_lineage_trend(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[TimePoint]]:
    return ApiResponse(data=repo.get_lineage_trend())


@router.get("/trend/asset", response_model=ApiResponse[list[TimePoint]])
async def get_asset_trend(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[TimePoint]]:
    return ApiResponse(data=repo.get_asset_trend())


@router.get("/domain-coverage", response_model=ApiResponse[list[DomainCoverage]])
async def get_domain_coverage(
    repo: GovernanceRepository = Depends(get_governance_repository),
) -> ApiResponse[list[DomainCoverage]]:
    return ApiResponse(data=repo.get_domain_coverage())
