"""SQLAlchemy ORM · 治理域 MVP 持久化模型（全部为 tenant_id + 实体键复合）。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

T_LEN = 64
ID_LEN = 128


class DataSourceORM(Base):
    __tablename__ = "data_sources"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    type: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    table_count: Mapped[int] = mapped_column(Integer)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    description: Mapped[str | None] = mapped_column(Text)
    endpoint_host: Mapped[str | None] = mapped_column(String(256))
    endpoint_port: Mapped[int | None] = mapped_column(Integer)
    default_database: Mapped[str | None] = mapped_column(String(256))


class DataAssetORM(Base):
    __tablename__ = "data_assets"
    __table_args__ = (
        Index("ix_data_assets_tenant_layer", "tenant_id", "layer"),
        Index("ix_data_assets_tenant_domain", "tenant_id", "domain"),
        Index("ix_data_assets_tenant_name", "tenant_id", "name"),
    )

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    full_name: Mapped[str] = mapped_column(String(1024))
    source_id: Mapped[str] = mapped_column(String(ID_LEN))
    source_type: Mapped[str] = mapped_column(String(64))
    database: Mapped[str] = mapped_column(String(256))
    schema_name: Mapped[str] = mapped_column(String(256))
    layer: Mapped[str] = mapped_column(String(32))
    owner: Mapped[str] = mapped_column(String(256))
    domain: Mapped[str] = mapped_column(String(256))
    row_count: Mapped[int] = mapped_column(Integer)
    size_bytes: Mapped[int] = mapped_column(BigInteger)
    quality_score: Mapped[float] = mapped_column(Float)
    pii_level: Mapped[str] = mapped_column(String(8))
    tags: Mapped[list] = mapped_column(JSON, default=list)
    description: Mapped[str | None] = mapped_column(Text)
    ai_description: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class QualityRuleORM(Base):
    __tablename__ = "quality_rules"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    dimension: Mapped[str] = mapped_column(String(64))
    asset_id: Mapped[str] = mapped_column(String(ID_LEN))
    asset_name: Mapped[str] = mapped_column(String(512))
    expression: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(8))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run_status: Mapped[str] = mapped_column(String(32))
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class QualityIncidentORM(Base):
    __tablename__ = "quality_incidents"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    rule_id: Mapped[str] = mapped_column(String(ID_LEN))
    rule_name: Mapped[str] = mapped_column(String(512))
    asset_name: Mapped[str] = mapped_column(String(512))
    severity: Mapped[str] = mapped_column(String(8))
    status: Mapped[str] = mapped_column(String(32))
    owner: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DataStandardORM(Base):
    __tablename__ = "data_standards"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    code: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(512))
    category: Mapped[str] = mapped_column(String(128))
    data_type: Mapped[str] = mapped_column(String(256))
    bound_count: Mapped[int] = mapped_column(Integer)
    owner: Mapped[str] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(String(32))


class MetricORM(Base):
    __tablename__ = "metrics"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    code: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(512))
    domain: Mapped[str] = mapped_column(String(256))
    formula: Mapped[str] = mapped_column(Text)
    owner: Mapped[str] = mapped_column(String(256))
    version: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))


class MasterEntityORM(Base):
    __tablename__ = "master_entities"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    type: Mapped[str] = mapped_column(String(64))
    record_count: Mapped[int] = mapped_column(Integer)
    owner: Mapped[str] = mapped_column(String(256))
    last_merge_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LifecyclePolicyORM(Base):
    __tablename__ = "lifecycle_policies"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    asset_pattern: Mapped[str] = mapped_column(String(512))
    cold_after_days: Mapped[int] = mapped_column(Integer)
    archive_after_days: Mapped[int] = mapped_column(Integer)
    delete_after_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class SecurityClassificationORM(Base):
    __tablename__ = "security_classifications"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    asset_name: Mapped[str] = mapped_column(String(512))
    classification: Mapped[str] = mapped_column(String(64))
    pii_level: Mapped[str] = mapped_column(String(8))
    masking_strategy: Mapped[str | None] = mapped_column(Text)
    owner: Mapped[str] = mapped_column(String(256))


class AIPromptORM(Base):
    __tablename__ = "ai_prompts"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    scenario: Mapped[str] = mapped_column(String(128))
    version: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    avg_tokens: Mapped[int] = mapped_column(Integer)
    success_rate: Mapped[float] = mapped_column(Float)


class AIInvocationORM(Base):
    __tablename__ = "ai_invocations"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    scenario: Mapped[str] = mapped_column(String(128))
    model: Mapped[str] = mapped_column(String(256))
    tokens: Mapped[int] = mapped_column(Integer)
    cost: Mapped[float] = mapped_column(Float)
    latency_ms: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ReportItemORM(Base):
    __tablename__ = "report_items"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    id: Mapped[str] = mapped_column(String(ID_LEN), primary_key=True)
    name: Mapped[str] = mapped_column(String(512))
    type: Mapped[str] = mapped_column(String(64))
    period: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TenantBlobORM(Base):
    __tablename__ = "tenant_blobs"

    tenant_id: Mapped[str] = mapped_column(String(T_LEN), primary_key=True)
    blob_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)


MODELS_READY = True
