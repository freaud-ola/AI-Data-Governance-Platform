"""治理域统一数据访问：Mock（内存）与 PostgreSQL 双实现。"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db import seed as seed_const
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
from app.schemas.common import PageMeta
from app.schemas.models import (
    AIInvocation,
    AIPrompt,
    DataAsset,
    DataSource,
    DataStandard,
    DomainCoverage,
    LifecyclePolicy,
    LineageGraph,
    MasterEntity,
    Metric,
    OverviewKPI,
    QualityIncident,
    QualityRule,
    ReportItem,
    SecurityClassification,
    TimePoint,
)


class GovernanceRepository(ABC):
    tenant_id: str

    @abstractmethod
    def list_data_sources(self) -> list[DataSource]:
        raise NotImplementedError

    @abstractmethod
    def get_data_source(self, source_id: str) -> DataSource | None:
        raise NotImplementedError

    @abstractmethod
    def list_assets_page(
        self,
        *,
        keyword: str | None,
        domain: str | None,
        layer: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[DataAsset], PageMeta]:
        raise NotImplementedError

    @abstractmethod
    def get_asset(self, asset_id: str) -> DataAsset | None:
        raise NotImplementedError

    @abstractmethod
    def list_quality_rules(self) -> list[QualityRule]:
        raise NotImplementedError

    @abstractmethod
    def list_quality_incidents(self) -> list[QualityIncident]:
        raise NotImplementedError

    @abstractmethod
    def get_lineage_graph(self) -> LineageGraph:
        raise NotImplementedError

    @abstractmethod
    def list_data_standards(self) -> list[DataStandard]:
        raise NotImplementedError

    @abstractmethod
    def list_metrics(self) -> list[Metric]:
        raise NotImplementedError

    @abstractmethod
    def list_master_entities(self) -> list[MasterEntity]:
        raise NotImplementedError

    @abstractmethod
    def list_lifecycle_policies(self) -> list[LifecyclePolicy]:
        raise NotImplementedError

    @abstractmethod
    def list_security_classifications(self) -> list[SecurityClassification]:
        raise NotImplementedError

    @abstractmethod
    def list_ai_prompts(self) -> list[AIPrompt]:
        raise NotImplementedError

    @abstractmethod
    def list_ai_invocations(self) -> list[AIInvocation]:
        raise NotImplementedError

    @abstractmethod
    def list_reports(self) -> list[ReportItem]:
        raise NotImplementedError

    @abstractmethod
    def get_overview_kpi(self) -> OverviewKPI:
        raise NotImplementedError

    @abstractmethod
    def get_quality_trend(self) -> list[TimePoint]:
        raise NotImplementedError

    @abstractmethod
    def get_lineage_trend(self) -> list[TimePoint]:
        raise NotImplementedError

    @abstractmethod
    def get_asset_trend(self) -> list[TimePoint]:
        raise NotImplementedError

    @abstractmethod
    def get_domain_coverage(self) -> list[DomainCoverage]:
        raise NotImplementedError


class MockGovernanceRepository(GovernanceRepository):
    """Sprint 01 原版内存数据集（忽略 tenant_id —— 与原 Mock 一致）。"""

    def __init__(self, tenant_id: str, **_kwargs):  # noqa: ARG002
        self.tenant_id = tenant_id

    def list_data_sources(self) -> list[DataSource]:
        return list(M.DATA_SOURCES)

    def get_data_source(self, source_id: str) -> DataSource | None:
        for s in M.DATA_SOURCES:
            if s.id == source_id:
                return s
        return None

    def list_assets_page(
        self,
        *,
        keyword: str | None,
        domain: str | None,
        layer: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[DataAsset], PageMeta]:
        items = list(M.DATA_ASSETS)
        if keyword:
            kw = keyword.lower()
            items = [
                a
                for a in items
                if kw in a.name.lower()
                or kw in (a.description or "").lower()
                or kw in (a.ai_description or "").lower()
                or kw in a.owner.lower()
            ]
        if domain:
            items = [a for a in items if a.domain == domain]
        if layer:
            items = [a for a in items if a.layer == layer]
        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        return items[start:end], PageMeta(page=page, page_size=page_size, total=total)

    def get_asset(self, asset_id: str) -> DataAsset | None:
        for a in M.DATA_ASSETS:
            if a.id == asset_id:
                return a
        return None

    def list_quality_rules(self) -> list[QualityRule]:
        return list(M.QUALITY_RULES)

    def list_quality_incidents(self) -> list[QualityIncident]:
        return list(M.QUALITY_INCIDENTS)

    def get_lineage_graph(self) -> LineageGraph:
        return M.LINEAGE_GRAPH

    def list_data_standards(self) -> list[DataStandard]:
        return list(M.DATA_STANDARDS)

    def list_metrics(self) -> list[Metric]:
        return list(M.METRICS)

    def list_master_entities(self) -> list[MasterEntity]:
        return list(M.MASTER_ENTITIES)

    def list_lifecycle_policies(self) -> list[LifecyclePolicy]:
        return list(M.LIFECYCLE_POLICIES)

    def list_security_classifications(self) -> list[SecurityClassification]:
        return list(M.SECURITY_CLASSIFICATIONS)

    def list_ai_prompts(self) -> list[AIPrompt]:
        return list(M.AI_PROMPTS)

    def list_ai_invocations(self) -> list[AIInvocation]:
        return list(M.AI_INVOCATIONS)

    def list_reports(self) -> list[ReportItem]:
        return list(_mock_reports_seed())

    def get_overview_kpi(self) -> OverviewKPI:
        return M.OVERVIEW_KPI

    def get_quality_trend(self) -> list[TimePoint]:
        return list(M.QUALITY_TREND)

    def get_lineage_trend(self) -> list[TimePoint]:
        return list(M.LINEAGE_TREND)

    def get_asset_trend(self) -> list[TimePoint]:
        return list(M.ASSET_GROWTH_TREND)

    def get_domain_coverage(self) -> list[DomainCoverage]:
        return list(M.DOMAIN_COVERAGE)


def _mock_reports_seed() -> list[ReportItem]:
    from datetime import datetime

    return [
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


class SqlGovernanceRepository(GovernanceRepository):
    def __init__(self, session: Session, tenant_id: str):
        self.session = session
        self.tenant_id = tenant_id

    def _blob(self, key: str):
        row = self.session.scalar(
            select(TenantBlobORM).where(
                TenantBlobORM.tenant_id == self.tenant_id,
                TenantBlobORM.blob_key == key,
            )
        )
        if row is None or row.payload is None:
            return None
        return row.payload

    def list_data_sources(self) -> list[DataSource]:
        rows = self.session.scalars(
            select(DataSourceORM).where(DataSourceORM.tenant_id == self.tenant_id)
        ).all()
        out: list[DataSource] = []
        for r in rows:
            out.append(
                DataSource(
                    id=r.id,
                    name=r.name,
                    type=r.type,
                    status=r.status,
                    table_count=r.table_count,
                    last_sync_at=r.last_sync_at,
                    description=r.description,
                    endpoint_host=r.endpoint_host,
                    endpoint_port=r.endpoint_port,
                    default_database=r.default_database,
                )
            )
        return out

    def get_data_source(self, source_id: str) -> DataSource | None:
        r = self.session.scalar(
            select(DataSourceORM).where(
                DataSourceORM.tenant_id == self.tenant_id,
                DataSourceORM.id == source_id,
            )
        )
        if r is None:
            return None
        return DataSource(
            id=r.id,
            name=r.name,
            type=r.type,
            status=r.status,
            table_count=r.table_count,
            last_sync_at=r.last_sync_at,
            description=r.description,
            endpoint_host=r.endpoint_host,
            endpoint_port=r.endpoint_port,
            default_database=r.default_database,
        )

    def _row_to_asset(self, r: DataAssetORM) -> DataAsset:
        return DataAsset(
            id=r.id,
            name=r.name,
            full_name=r.full_name,
            source_id=r.source_id,
            source_type=r.source_type,
            database=r.database,
            schema=r.schema_name,
            layer=r.layer,
            owner=r.owner,
            domain=r.domain,
            row_count=r.row_count,
            size_bytes=r.size_bytes,
            quality_score=r.quality_score,
            pii_level=r.pii_level,
            tags=list(r.tags or []),
            description=r.description,
            ai_description=r.ai_description,
            updated_at=r.updated_at,
        )

    def list_assets_page(
        self,
        *,
        keyword: str | None,
        domain: str | None,
        layer: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[DataAsset], PageMeta]:
        predicates = [DataAssetORM.tenant_id == self.tenant_id]
        if keyword:
            kw = f"%{keyword.lower()}%"
            predicates.append(
                or_(
                    DataAssetORM.name.ilike(kw),
                    DataAssetORM.description.ilike(kw),
                    DataAssetORM.ai_description.ilike(kw),
                    DataAssetORM.owner.ilike(kw),
                )
            )
        if domain:
            predicates.append(DataAssetORM.domain == domain)
        if layer:
            predicates.append(DataAssetORM.layer == layer)

        base = select(DataAssetORM).where(*predicates)
        total = int(
            self.session.scalar(
                select(func.count()).select_from(DataAssetORM).where(*predicates)
            )
            or 0
        )
        stmt = base.order_by(DataAssetORM.updated_at.desc()).offset((page - 1) * page_size).limit(
            page_size
        )
        rows = self.session.scalars(stmt).all()
        return [self._row_to_asset(r) for r in rows], PageMeta(
            page=page,
            page_size=page_size,
            total=total,
        )

    def get_asset(self, asset_id: str) -> DataAsset | None:
        r = self.session.scalar(
            select(DataAssetORM).where(
                DataAssetORM.tenant_id == self.tenant_id,
                DataAssetORM.id == asset_id,
            )
        )
        return self._row_to_asset(r) if r else None

    def list_quality_rules(self) -> list[QualityRule]:
        rows = self.session.scalars(
            select(QualityRuleORM).where(QualityRuleORM.tenant_id == self.tenant_id)
        ).all()
        return [
            QualityRule(
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
            for r in rows
        ]

    def list_quality_incidents(self) -> list[QualityIncident]:
        rows = self.session.scalars(
            select(QualityIncidentORM).where(QualityIncidentORM.tenant_id == self.tenant_id)
        ).all()
        return [
            QualityIncident(
                id=r.id,
                rule_id=r.rule_id,
                rule_name=r.rule_name,
                asset_name=r.asset_name,
                severity=r.severity,
                status=r.status,
                owner=r.owner,
                created_at=r.created_at,
                resolved_at=r.resolved_at,
            )
            for r in rows
        ]

    def get_lineage_graph(self) -> LineageGraph:
        payload = self._blob(seed_const.BLOB_LINEAGE)
        if not payload:
            return LineageGraph(nodes=[], edges=[])
        return LineageGraph.model_validate(payload)

    def list_data_standards(self) -> list[DataStandard]:
        rows = self.session.scalars(
            select(DataStandardORM).where(DataStandardORM.tenant_id == self.tenant_id)
        ).all()
        return [
            DataStandard(
                id=r.id,
                code=r.code,
                name=r.name,
                category=r.category,
                data_type=r.data_type,
                bound_count=r.bound_count,
                owner=r.owner,
                status=r.status,
            )
            for r in rows
        ]

    def list_metrics(self) -> list[Metric]:
        rows = self.session.scalars(
            select(MetricORM).where(MetricORM.tenant_id == self.tenant_id)
        ).all()
        return [
            Metric(
                id=r.id,
                code=r.code,
                name=r.name,
                domain=r.domain,
                formula=r.formula,
                owner=r.owner,
                version=r.version,
                status=r.status,
            )
            for r in rows
        ]

    def list_master_entities(self) -> list[MasterEntity]:
        rows = self.session.scalars(
            select(MasterEntityORM).where(MasterEntityORM.tenant_id == self.tenant_id)
        ).all()
        return [
            MasterEntity(
                id=r.id,
                name=r.name,
                type=r.type,
                record_count=r.record_count,
                owner=r.owner,
                last_merge_at=r.last_merge_at,
            )
            for r in rows
        ]

    def list_lifecycle_policies(self) -> list[LifecyclePolicy]:
        rows = self.session.scalars(
            select(LifecyclePolicyORM).where(LifecyclePolicyORM.tenant_id == self.tenant_id)
        ).all()
        return [
            LifecyclePolicy(
                id=r.id,
                name=r.name,
                asset_pattern=r.asset_pattern,
                cold_after_days=r.cold_after_days,
                archive_after_days=r.archive_after_days,
                delete_after_days=r.delete_after_days,
                enabled=r.enabled,
            )
            for r in rows
        ]

    def list_security_classifications(self) -> list[SecurityClassification]:
        rows = self.session.scalars(
            select(SecurityClassificationORM).where(
                SecurityClassificationORM.tenant_id == self.tenant_id
            )
        ).all()
        return [
            SecurityClassification(
                asset_id=r.asset_id,
                asset_name=r.asset_name,
                classification=r.classification,
                pii_level=r.pii_level,
                masking_strategy=r.masking_strategy,
                owner=r.owner,
            )
            for r in rows
        ]

    def list_ai_prompts(self) -> list[AIPrompt]:
        rows = self.session.scalars(
            select(AIPromptORM).where(AIPromptORM.tenant_id == self.tenant_id)
        ).all()
        return [
            AIPrompt(
                id=r.id,
                name=r.name,
                scenario=r.scenario,
                version=r.version,
                status=r.status,
                avg_tokens=r.avg_tokens,
                success_rate=r.success_rate,
            )
            for r in rows
        ]

    def list_ai_invocations(self) -> list[AIInvocation]:
        rows = self.session.scalars(
            select(AIInvocationORM).where(AIInvocationORM.tenant_id == self.tenant_id)
        ).all()
        return [
            AIInvocation(
                id=r.id,
                scenario=r.scenario,
                model=r.model,
                tokens=r.tokens,
                cost=r.cost,
                latency_ms=r.latency_ms,
                status=r.status,
                created_at=r.created_at,
            )
            for r in rows
        ]

    def list_reports(self) -> list[ReportItem]:
        rows = self.session.scalars(
            select(ReportItemORM).where(ReportItemORM.tenant_id == self.tenant_id)
        ).all()
        return [
            ReportItem(
                id=r.id,
                name=r.name,
                type=r.type,
                period=r.period,
                status=r.status,
                generated_at=r.generated_at,
            )
            for r in rows
        ]

    def get_overview_kpi(self) -> OverviewKPI:
        payload = self._blob(seed_const.BLOB_OVERVIEW_KPI)
        if not payload:
            raise ValueError("overview_kpi blob missing — run migrations + seed")
        return OverviewKPI.model_validate(payload)

    def get_quality_trend(self) -> list[TimePoint]:
        payload = self._blob(seed_const.BLOB_TREND_QUALITY)
        if not isinstance(payload, list):
            return []
        return [TimePoint.model_validate(p) for p in payload]

    def get_lineage_trend(self) -> list[TimePoint]:
        payload = self._blob(seed_const.BLOB_TREND_LINEAGE)
        if not isinstance(payload, list):
            return []
        return [TimePoint.model_validate(p) for p in payload]

    def get_asset_trend(self) -> list[TimePoint]:
        payload = self._blob(seed_const.BLOB_TREND_ASSET)
        if not isinstance(payload, list):
            return []
        return [TimePoint.model_validate(p) for p in payload]

    def get_domain_coverage(self) -> list[DomainCoverage]:
        payload = self._blob(seed_const.BLOB_DOMAIN_COVERAGE)
        if not isinstance(payload, list):
            return []
        return [DomainCoverage.model_validate(p) for p in payload]
