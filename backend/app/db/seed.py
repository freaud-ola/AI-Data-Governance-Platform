"""首次启动时按 Sprint 01 Mock 基准灌库（可重入：仅空库触发）。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.mock import data as M
from app.models.orm import (
    AIInvocationORM,
    AIPromptORM,
    DataAssetORM,
    DataSourceORM,
    DataStandardORM,
    LifecyclePolicyORM,
    MasterEntityORM,
    MetricORM,
    QualityIncidentORM,
    QualityRuleORM,
    ReportItemORM,
    SecurityClassificationORM,
    TenantBlobORM,
)
from app.schemas.models import ReportItem

BLOB_LINEAGE = "lineage_graph"
BLOB_OVERVIEW_KPI = "overview_kpi"
BLOB_TREND_QUALITY = "trend_quality"
BLOB_TREND_LINEAGE = "trend_lineage"
BLOB_TREND_ASSET = "trend_asset"
BLOB_DOMAIN_COVERAGE = "domain_coverage"


def seed_tenant_if_empty(session: Session, tenant_id: str) -> bool:
    """若该租户尚未有任何数据源，则灌入 Mock 数据。返回是否执行了灌库。"""
    count = session.scalar(
        select(func.count()).select_from(DataSourceORM).where(DataSourceORM.tenant_id == tenant_id)
    )
    if count and count > 0:
        return False

    for s in M.DATA_SOURCES:
        session.add(
            DataSourceORM(
                tenant_id=tenant_id,
                id=s.id,
                name=s.name,
                type=s.type,
                status=s.status,
                table_count=s.table_count,
                last_sync_at=s.last_sync_at,
                description=s.description,
                endpoint_host=s.endpoint_host,
                endpoint_port=s.endpoint_port,
                default_database=s.default_database,
            )
        )

    for a in M.DATA_ASSETS:
        session.add(
            DataAssetORM(
                tenant_id=tenant_id,
                id=a.id,
                name=a.name,
                full_name=a.full_name,
                source_id=a.source_id,
                source_type=a.source_type,
                database=a.database,
                schema_name=a.schema_name,
                layer=a.layer,
                owner=a.owner,
                domain=a.domain,
                row_count=a.row_count,
                size_bytes=a.size_bytes,
                quality_score=a.quality_score,
                pii_level=a.pii_level,
                tags=list(a.tags),
                description=a.description,
                ai_description=a.ai_description,
                updated_at=a.updated_at,
            )
        )

    for r in M.QUALITY_RULES:
        session.add(
            QualityRuleORM(
                tenant_id=tenant_id,
                id=r.id,
                name=r.name,
                dimension=r.dimension,
                asset_id=r.asset_id,
                asset_name=r.asset_name,
                expression=r.expression,
                severity=r.severity,
                enabled=r.enabled,
                last_run_status=r.last_run_status,
                last_run_at=r.last_run_at,
            )
        )

    for i in M.QUALITY_INCIDENTS:
        session.add(
            QualityIncidentORM(
                tenant_id=tenant_id,
                id=i.id,
                rule_id=i.rule_id,
                rule_name=i.rule_name,
                asset_name=i.asset_name,
                severity=i.severity,
                status=i.status,
                owner=i.owner,
                created_at=i.created_at,
                resolved_at=i.resolved_at,
            )
        )

    for st in M.DATA_STANDARDS:
        session.add(
            DataStandardORM(
                tenant_id=tenant_id,
                id=st.id,
                code=st.code,
                name=st.name,
                category=st.category,
                data_type=st.data_type,
                bound_count=st.bound_count,
                owner=st.owner,
                status=st.status,
            )
        )

    for m in M.METRICS:
        session.add(
            MetricORM(
                tenant_id=tenant_id,
                id=m.id,
                code=m.code,
                name=m.name,
                domain=m.domain,
                formula=m.formula,
                owner=m.owner,
                version=m.version,
                status=m.status,
            )
        )

    for e in M.MASTER_ENTITIES:
        session.add(
            MasterEntityORM(
                tenant_id=tenant_id,
                id=e.id,
                name=e.name,
                type=e.type,
                record_count=e.record_count,
                owner=e.owner,
                last_merge_at=e.last_merge_at,
            )
        )

    for p in M.LIFECYCLE_POLICIES:
        session.add(
            LifecyclePolicyORM(
                tenant_id=tenant_id,
                id=p.id,
                name=p.name,
                asset_pattern=p.asset_pattern,
                cold_after_days=p.cold_after_days,
                archive_after_days=p.archive_after_days,
                delete_after_days=p.delete_after_days,
                enabled=p.enabled,
            )
        )

    for c in M.SECURITY_CLASSIFICATIONS:
        session.add(
            SecurityClassificationORM(
                tenant_id=tenant_id,
                asset_id=c.asset_id,
                asset_name=c.asset_name,
                classification=c.classification,
                pii_level=c.pii_level,
                masking_strategy=c.masking_strategy,
                owner=c.owner,
            )
        )

    for p in M.AI_PROMPTS:
        session.add(
            AIPromptORM(
                tenant_id=tenant_id,
                id=p.id,
                name=p.name,
                scenario=p.scenario,
                version=p.version,
                status=p.status,
                avg_tokens=p.avg_tokens,
                success_rate=p.success_rate,
            )
        )

    for inv in M.AI_INVOCATIONS:
        session.add(
            AIInvocationORM(
                tenant_id=tenant_id,
                id=inv.id,
                scenario=inv.scenario,
                model=inv.model,
                tokens=inv.tokens,
                cost=inv.cost,
                latency_ms=inv.latency_ms,
                status=inv.status,
                created_at=inv.created_at,
            )
        )

    _reports = [
        ReportItem(
            id="rp-001",
            name="2026-04 治理月报",
            type="月报",
            period="2026-04",
            status="published",
            generated_at=datetime(2026, 4, 28, 10, 0, 0),
        ),
        ReportItem(
            id="rp-002",
            name="2026-W17 数据健康周报",
            type="周报",
            period="2026-W17",
            status="published",
            generated_at=datetime(2026, 4, 27, 9, 0, 0),
        ),
        ReportItem(
            id="rp-003",
            name="2026-Q1 合规导出清单",
            type="合规",
            period="2026-Q1",
            status="archived",
            generated_at=datetime(2026, 4, 1, 18, 0, 0),
        ),
        ReportItem(
            id="rp-004",
            name="数据出境清单（2026-04）",
            type="合规",
            period="2026-04",
            status="draft",
            generated_at=datetime(2026, 4, 28, 16, 0, 0),
        ),
    ]
    for rp in _reports:
        session.add(
            ReportItemORM(
                tenant_id=tenant_id,
                id=rp.id,
                name=rp.name,
                type=rp.type,
                period=rp.period,
                status=rp.status,
                generated_at=rp.generated_at,
            )
        )

    session.add(
        TenantBlobORM(
            tenant_id=tenant_id,
            blob_key=BLOB_LINEAGE,
            payload=M.LINEAGE_GRAPH.model_dump(mode="json"),
        )
    )
    session.add(
        TenantBlobORM(
            tenant_id=tenant_id,
            blob_key=BLOB_OVERVIEW_KPI,
            payload=M.OVERVIEW_KPI.model_dump(mode="json"),
        )
    )
    session.add(
        TenantBlobORM(
            tenant_id=tenant_id,
            blob_key=BLOB_TREND_QUALITY,
            payload=[p.model_dump(mode="json") for p in M.QUALITY_TREND],
        )
    )
    session.add(
        TenantBlobORM(
            tenant_id=tenant_id,
            blob_key=BLOB_TREND_LINEAGE,
            payload=[p.model_dump(mode="json") for p in M.LINEAGE_TREND],
        )
    )
    session.add(
        TenantBlobORM(
            tenant_id=tenant_id,
            blob_key=BLOB_TREND_ASSET,
            payload=[p.model_dump(mode="json") for p in M.ASSET_GROWTH_TREND],
        )
    )
    session.add(
        TenantBlobORM(
            tenant_id=tenant_id,
            blob_key=BLOB_DOMAIN_COVERAGE,
            payload=[d.model_dump(mode="json") for d in M.DOMAIN_COVERAGE],
        )
    )

    return True
