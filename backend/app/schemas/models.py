"""平台核心实体的 Pydantic 模型（MVP 简化版）。"""

from datetime import datetime

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# 元数据中心
# ---------------------------------------------------------------------------
class DataSource(BaseModel):
    id: str
    name: str
    type: str  # hive / mysql / iceberg / dbt / scheduler
    status: str  # online / offline / error
    table_count: int
    last_sync_at: datetime | None = None
    description: str | None = None
    # 接入信息（宿主机 / Compose 网络内可在 description 中补充说明）
    endpoint_host: str | None = None
    endpoint_port: int | None = None
    default_database: str | None = None


class DataAsset(BaseModel):
    id: str
    name: str
    full_name: str
    source_id: str
    source_type: str
    database: str
    schema_name: str = Field(alias="schema")
    layer: str  # ODS / DWD / DWS / ADS
    owner: str
    domain: str
    row_count: int
    size_bytes: int
    quality_score: float
    pii_level: str  # L1/L2/L3/L4
    tags: list[str] = []
    description: str | None = None
    ai_description: str | None = None
    updated_at: datetime

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# 数据质量
# ---------------------------------------------------------------------------
class QualityRule(BaseModel):
    id: str
    name: str
    dimension: str
    asset_id: str
    asset_name: str
    expression: str
    severity: str  # P0/P1/P2/P3
    enabled: bool = True
    last_run_status: str  # passed / failed / pending
    last_run_at: datetime | None = None


class QualityIncident(BaseModel):
    id: str
    rule_id: str
    rule_name: str
    asset_name: str
    severity: str
    status: str
    owner: str
    created_at: datetime
    resolved_at: datetime | None = None


# ---------------------------------------------------------------------------
# 血缘
# ---------------------------------------------------------------------------
class LineageNode(BaseModel):
    id: str
    name: str
    type: str  # table / job / column
    layer: str | None = None


class LineageEdge(BaseModel):
    source: str
    target: str
    relation: str = "derives_from"


class LineageGraph(BaseModel):
    nodes: list[LineageNode]
    edges: list[LineageEdge]


# ---------------------------------------------------------------------------
# 数据标准 / 指标 / 主数据
# ---------------------------------------------------------------------------
class DataStandard(BaseModel):
    id: str
    code: str
    name: str
    category: str
    data_type: str
    bound_count: int
    owner: str
    status: str


class Metric(BaseModel):
    id: str
    code: str
    name: str
    domain: str
    formula: str
    owner: str
    version: str
    status: str


class MasterEntity(BaseModel):
    id: str
    name: str
    type: str
    record_count: int
    owner: str
    last_merge_at: datetime | None = None


# ---------------------------------------------------------------------------
# 生命周期 / 安全 / AI
# ---------------------------------------------------------------------------
class LifecyclePolicy(BaseModel):
    id: str
    name: str
    asset_pattern: str
    cold_after_days: int
    archive_after_days: int
    delete_after_days: int | None = None
    enabled: bool = True


class SecurityClassification(BaseModel):
    asset_id: str
    asset_name: str
    classification: str
    pii_level: str
    masking_strategy: str | None = None
    owner: str


class AIPrompt(BaseModel):
    id: str
    name: str
    scenario: str
    version: str
    status: str
    avg_tokens: int
    success_rate: float


class AIInvocation(BaseModel):
    id: str
    scenario: str
    model: str
    tokens: int
    cost: float
    latency_ms: int
    status: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
class OverviewKPI(BaseModel):
    asset_total: int
    asset_today_new: int
    quality_score: float
    quality_incidents_open: int
    pii_assets: int
    coverage_lineage: float
    coverage_comment: float
    ai_invocations_today: int
    ai_cost_today: float


class TimePoint(BaseModel):
    ts: str
    value: float


class DomainCoverage(BaseModel):
    domain: str
    asset_count: int
    quality_score: float
    governance_score: float


# ---------------------------------------------------------------------------
# 报告中心
# ---------------------------------------------------------------------------
class ReportItem(BaseModel):
    id: str
    name: str
    type: str
    period: str
    status: str
    generated_at: datetime
