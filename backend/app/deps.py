"""FastAPI 依赖：治理数据仓储注入。"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.tenant import get_tenant_id
from app.db.session import db_session_dependency
from app.repositories.governance import (
    GovernanceRepository,
    MockGovernanceRepository,
    SqlGovernanceRepository,
)


def get_governance_repository(
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    session: Annotated[Session | None, Depends(db_session_dependency)],
) -> GovernanceRepository:
    settings = get_settings()
    if settings.database_enabled:
        assert session is not None
        return SqlGovernanceRepository(session, tenant_id)
    assert session is None
    return MockGovernanceRepository(tenant_id)
