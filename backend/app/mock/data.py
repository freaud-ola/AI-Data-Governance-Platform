"""MVP 阶段使用的内存 Mock 数据。

后续阶段会替换为：
- 元数据：OpenMetadata + Hive HMS Connector
- 质量：Great Expectations / Soda Core
- 血缘：sqlglot 静态 + 运行时 Hook
- AI：自研 LLM Router + Langfuse
"""

from datetime import datetime, timedelta

from app.schemas.models import (
    AIInvocation,
    AIPrompt,
    DataAsset,
    DataSource,
    DataStandard,
    DomainCoverage,
    LifecyclePolicy,
    LineageEdge,
    LineageGraph,
    LineageNode,
    MasterEntity,
    Metric,
    OverviewKPI,
    QualityIncident,
    QualityRule,
    SecurityClassification,
    TimePoint,
)

_NOW = datetime(2026, 4, 29, 22, 0, 0)


# ---------------------------------------------------------------------------
# 元数据
# ---------------------------------------------------------------------------
DATA_SOURCES: list[DataSource] = [
    DataSource(
        id="ds-hive-cluster",
        name="Hive 集群",
        type="hive",
        status="online",
        table_count=0,
        last_sync_at=None,
        endpoint_host="127.0.0.1",
        endpoint_port=10000,
        default_database="default",
        description=(
            "与生产同名对接对象：主数仓 Hive。"
            "本地 Docker（profile datasources）：独立 Metastore `hive-metastore:9083` + "
            "HiveServer2 `hive-dev:10000`；宿主机 JDBC jdbc:hive2://127.0.0.1:10000/default。"
            "表数量待 HMS / 采集同步后回填。"
        ),
    ),
    DataSource(
        id="ds-mysql-platform",
        name="数据平台 MySQL",
        type="mysql",
        status="online",
        table_count=0,
        last_sync_at=None,
        endpoint_host="127.0.0.1",
        endpoint_port=3307,
        default_database="adg_platform",
        description=(
            "数据平台 MySQL（生产结构可导入本库）。"
            "本地 Docker：`mysql-platform`，默认映射宿主机 3307→3306，库 adg_platform。"
            "将导出 SQL 放入 docker/mysql-platform/init/（按文件名顺序执行），"
            "或使用 mysql 客户端导入。"
            "Compose 网络内主机名：mysql-platform。"
        ),
    ),
]


_OWNERS = ["data_team", "growth_team", "risk_team", "finance_team", "supply_team"]


def _gen_assets() -> list[DataAsset]:
    seed_tables = [
        ("dwd_order_detail", "交易", "DWD", "L2"),
        ("dws_user_active_daily", "用户", "DWS", "L2"),
        ("ads_marketing_funnel", "营销", "ADS", "L1"),
        ("dwd_payment_log", "交易", "DWD", "L3"),
        ("ods_user_register", "用户", "ODS", "L4"),
        ("dws_risk_score_hourly", "风控", "DWS", "L3"),
        ("ads_finance_pnl", "财务", "ADS", "L3"),
        ("dwd_supply_inbound", "供应链", "DWD", "L2"),
        ("dws_gmv_summary", "交易", "DWS", "L1"),
        ("ods_user_address", "用户", "ODS", "L4"),
        ("ads_user_lifecycle", "用户", "ADS", "L2"),
        ("dwd_coupon_use", "营销", "DWD", "L2"),
    ]
    items: list[DataAsset] = []
    for i, (name, domain, layer, pii) in enumerate(seed_tables):
        use_mysql = i >= 8
        db = "adg_platform" if use_mysql else "prod"
        sch = "app" if use_mysql else "dw"
        sid = "ds-mysql-platform" if use_mysql else "ds-hive-cluster"
        stype = "mysql" if use_mysql else "hive"
        full_name = f"{db}.{sch}.{name}" if use_mysql else f"prod.dw.{name}"
        items.append(
            DataAsset(
                id=f"asset-{i:04d}",
                name=name,
                full_name=full_name,
                source_id=sid,
                source_type=stype,
                database=db,
                schema=sch,
                layer=layer,
                owner=_OWNERS[i % len(_OWNERS)],
                domain=domain,
                row_count=1_000_000 * (i + 3),
                size_bytes=1_073_741_824 * (i % 5 + 1),
                quality_score=round(70 + (i * 3) % 30, 1),
                pii_level=pii,
                tags=[layer, domain, "P0" if i < 4 else "P1"],
                description=f"{domain}域 {layer} 层核心宽表" if i < 6 else None,
                ai_description=(
                    f"AI 自动注释：{domain}域 {layer} 层，记录"
                    f"{name.split('_', 1)[-1]}相关业务事实。"
                ),
                updated_at=_NOW - timedelta(hours=i),
            )
        )
    return items


DATA_ASSETS: list[DataAsset] = _gen_assets()


# ---------------------------------------------------------------------------
# 质量
# ---------------------------------------------------------------------------
QUALITY_RULES: list[QualityRule] = [
    QualityRule(
        id="qr-001",
        name="订单主键非空",
        dimension="completeness",
        asset_id="asset-0000",
        asset_name="dwd_order_detail",
        expression="order_id IS NOT NULL",
        severity="P0",
        enabled=True,
        last_run_status="passed",
        last_run_at=_NOW - timedelta(hours=1),
    ),
    QualityRule(
        id="qr-002",
        name="支付金额范围",
        dimension="validity",
        asset_id="asset-0003",
        asset_name="dwd_payment_log",
        expression="amount BETWEEN 0 AND 1000000",
        severity="P0",
        enabled=True,
        last_run_status="failed",
        last_run_at=_NOW - timedelta(hours=1),
    ),
    QualityRule(
        id="qr-003",
        name="GMV 日环比漂移",
        dimension="timeliness",
        asset_id="asset-0008",
        asset_name="dws_gmv_summary",
        expression="psi(today, yesterday) < 0.2",
        severity="P1",
        enabled=True,
        last_run_status="passed",
        last_run_at=_NOW - timedelta(hours=2),
    ),
    QualityRule(
        id="qr-004",
        name="用户ID唯一",
        dimension="uniqueness",
        asset_id="asset-0001",
        asset_name="dws_user_active_daily",
        expression="UNIQUE(user_id, dt)",
        severity="P1",
        enabled=True,
        last_run_status="passed",
        last_run_at=_NOW - timedelta(hours=3),
    ),
    QualityRule(
        id="qr-005",
        name="风控分数一致性",
        dimension="consistency",
        asset_id="asset-0005",
        asset_name="dws_risk_score_hourly",
        expression="score = sum(component_scores)",
        severity="P2",
        enabled=False,
        last_run_status="pending",
        last_run_at=None,
    ),
]


QUALITY_INCIDENTS: list[QualityIncident] = [
    QualityIncident(
        id="qi-2026042901",
        rule_id="qr-002",
        rule_name="支付金额范围",
        asset_name="dwd_payment_log",
        severity="P0",
        status="processing",
        owner="risk_team",
        created_at=_NOW - timedelta(hours=1),
    ),
    QualityIncident(
        id="qi-2026042802",
        rule_id="qr-003",
        rule_name="GMV 日环比漂移",
        asset_name="dws_gmv_summary",
        severity="P1",
        status="open",
        owner="data_team",
        created_at=_NOW - timedelta(hours=12),
    ),
    QualityIncident(
        id="qi-2026042702",
        rule_id="qr-001",
        rule_name="订单主键非空",
        asset_name="dwd_order_detail",
        severity="P0",
        status="resolved",
        owner="data_team",
        created_at=_NOW - timedelta(days=2),
        resolved_at=_NOW - timedelta(days=1, hours=21),
    ),
]


# ---------------------------------------------------------------------------
# 血缘
# ---------------------------------------------------------------------------
LINEAGE_GRAPH: LineageGraph = LineageGraph(
    nodes=[
        LineageNode(id="ods_user_register", name="ods_user_register", type="table", layer="ODS"),
        LineageNode(id="ods_user_address", name="ods_user_address", type="table", layer="ODS"),
        LineageNode(id="dwd_user", name="dwd_user", type="table", layer="DWD"),
        LineageNode(id="dwd_order_detail", name="dwd_order_detail", type="table", layer="DWD"),
        LineageNode(id="job_dwd_user", name="dwd_user_etl", type="job"),
        LineageNode(id="dws_user_active_daily", name="dws_user_active_daily", type="table", layer="DWS"),
        LineageNode(id="dws_gmv_summary", name="dws_gmv_summary", type="table", layer="DWS"),
        LineageNode(id="ads_marketing_funnel", name="ads_marketing_funnel", type="table", layer="ADS"),
    ],
    edges=[
        LineageEdge(source="ods_user_register", target="job_dwd_user"),
        LineageEdge(source="ods_user_address", target="job_dwd_user"),
        LineageEdge(source="job_dwd_user", target="dwd_user"),
        LineageEdge(source="dwd_user", target="dws_user_active_daily"),
        LineageEdge(source="dwd_order_detail", target="dws_gmv_summary"),
        LineageEdge(source="dws_user_active_daily", target="ads_marketing_funnel"),
        LineageEdge(source="dws_gmv_summary", target="ads_marketing_funnel"),
    ],
)


# ---------------------------------------------------------------------------
# 标准 / 指标 / 主数据
# ---------------------------------------------------------------------------
DATA_STANDARDS: list[DataStandard] = [
    DataStandard(id="std-001", code="STD.USER_ID", name="用户ID", category="标识符", data_type="bigint", bound_count=128, owner="data_team", status="published"),
    DataStandard(id="std-002", code="STD.ORDER_ID", name="订单ID", category="标识符", data_type="varchar(32)", bound_count=87, owner="data_team", status="published"),
    DataStandard(id="std-003", code="STD.AMOUNT", name="金额", category="数值", data_type="decimal(18,2)", bound_count=204, owner="finance_team", status="published"),
    DataStandard(id="std-004", code="STD.PHONE", name="手机号", category="敏感信息", data_type="varchar(11)", bound_count=46, owner="security_team", status="published"),
    DataStandard(id="std-005", code="STD.DT", name="数据日期", category="分区", data_type="string(8)", bound_count=1872, owner="data_team", status="published"),
]


METRICS: list[Metric] = [
    Metric(id="m-001", code="GMV", name="商品交易总额", domain="交易", formula="SUM(order_amount)", owner="data_team", version="1.3", status="online"),
    Metric(id="m-002", code="DAU", name="日活跃用户", domain="用户", formula="COUNT(DISTINCT active_user_id)", owner="growth_team", version="2.1", status="online"),
    Metric(id="m-003", code="ARPU", name="人均收入", domain="财务", formula="GMV / DAU", owner="finance_team", version="1.0", status="approved"),
    Metric(id="m-004", code="CAC", name="获客成本", domain="营销", formula="marketing_cost / new_user", owner="growth_team", version="0.5", status="draft"),
]


MASTER_ENTITIES: list[MasterEntity] = [
    MasterEntity(id="me-user", name="用户主数据", type="party", record_count=12_842_103, owner="data_team", last_merge_at=_NOW - timedelta(hours=8)),
    MasterEntity(id="me-product", name="商品主数据", type="product", record_count=482_193, owner="supply_team", last_merge_at=_NOW - timedelta(hours=10)),
    MasterEntity(id="me-supplier", name="供应商主数据", type="party", record_count=1842, owner="supply_team", last_merge_at=_NOW - timedelta(days=1)),
]


# ---------------------------------------------------------------------------
# 生命周期 / 安全 / AI
# ---------------------------------------------------------------------------
LIFECYCLE_POLICIES: list[LifecyclePolicy] = [
    LifecyclePolicy(id="lp-001", name="ODS 默认生命周期", asset_pattern="prod.ods.*", cold_after_days=30, archive_after_days=180, delete_after_days=730, enabled=True),
    LifecyclePolicy(id="lp-002", name="DWS 高频访问层", asset_pattern="prod.dw.dws_*", cold_after_days=90, archive_after_days=365, delete_after_days=None, enabled=True),
    LifecyclePolicy(id="lp-003", name="临时表清理", asset_pattern="*.tmp_*", cold_after_days=3, archive_after_days=7, delete_after_days=14, enabled=True),
]


SECURITY_CLASSIFICATIONS: list[SecurityClassification] = [
    SecurityClassification(asset_id="asset-0004", asset_name="ods_user_register", classification="strict", pii_level="L4", masking_strategy="hash+部分脱敏", owner="security_team"),
    SecurityClassification(asset_id="asset-0009", asset_name="ods_user_address", classification="strict", pii_level="L4", masking_strategy="动态脱敏", owner="security_team"),
    SecurityClassification(asset_id="asset-0003", asset_name="dwd_payment_log", classification="confidential", pii_level="L3", masking_strategy="字段级脱敏", owner="security_team"),
    SecurityClassification(asset_id="asset-0006", asset_name="ads_finance_pnl", classification="confidential", pii_level="L3", masking_strategy="角色行级隔离", owner="finance_team"),
    SecurityClassification(asset_id="asset-0000", asset_name="dwd_order_detail", classification="internal", pii_level="L2", masking_strategy=None, owner="data_team"),
]


AI_PROMPTS: list[AIPrompt] = [
    AIPrompt(id="p-comment-v3", name="字段注释生成", scenario="comment", version="v3.1", status="online", avg_tokens=420, success_rate=0.93),
    AIPrompt(id="p-nl2sql-v2", name="NL2SQL 语义解析", scenario="nl2sql", version="v2.0", status="staging", avg_tokens=1200, success_rate=0.81),
    AIPrompt(id="p-cls-v1", name="数据分级分类", scenario="classification", version="v1.4", status="online", avg_tokens=380, success_rate=0.89),
    AIPrompt(id="p-agent-daily", name="每日健康巡检 Agent", scenario="agent", version="v0.9", status="staging", avg_tokens=2400, success_rate=0.74),
]


AI_INVOCATIONS: list[AIInvocation] = [
    AIInvocation(id="inv-001", scenario="comment", model="qwen2.5-32b", tokens=512, cost=0.012, latency_ms=2300, status="success", created_at=_NOW - timedelta(minutes=5)),
    AIInvocation(id="inv-002", scenario="nl2sql", model="deepseek-coder-v2", tokens=1842, cost=0.045, latency_ms=4800, status="success", created_at=_NOW - timedelta(minutes=8)),
    AIInvocation(id="inv-003", scenario="classification", model="qwen2.5-7b", tokens=312, cost=0.005, latency_ms=1100, status="success", created_at=_NOW - timedelta(minutes=11)),
    AIInvocation(id="inv-004", scenario="nl2sql", model="deepseek-coder-v2", tokens=2104, cost=0.058, latency_ms=8200, status="timeout", created_at=_NOW - timedelta(minutes=15)),
    AIInvocation(id="inv-005", scenario="comment", model="qwen2.5-32b", tokens=486, cost=0.011, latency_ms=2150, status="success", created_at=_NOW - timedelta(minutes=20)),
]


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
OVERVIEW_KPI: OverviewKPI = OverviewKPI(
    asset_total=2880,
    asset_today_new=23,
    quality_score=87.5,
    quality_incidents_open=14,
    pii_assets=312,
    coverage_lineage=0.81,
    coverage_comment=0.76,
    ai_invocations_today=4823,
    ai_cost_today=18.46,
)


def _gen_trend(base: float, days: int = 14) -> list[TimePoint]:
    points: list[TimePoint] = []
    for i in range(days):
        ts = (_NOW - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d")
        delta = ((i * 7) % 13) - 6
        points.append(TimePoint(ts=ts, value=round(base + delta, 2)))
    return points


QUALITY_TREND: list[TimePoint] = _gen_trend(85.0)
LINEAGE_TREND: list[TimePoint] = _gen_trend(78.0)
ASSET_GROWTH_TREND: list[TimePoint] = [
    TimePoint(ts=p.ts, value=2700 + i * 12) for i, p in enumerate(_gen_trend(2700.0))
]


DOMAIN_COVERAGE: list[DomainCoverage] = [
    DomainCoverage(domain="交易", asset_count=584, quality_score=89.2, governance_score=82.4),
    DomainCoverage(domain="用户", asset_count=412, quality_score=86.5, governance_score=78.1),
    DomainCoverage(domain="营销", asset_count=287, quality_score=84.8, governance_score=75.3),
    DomainCoverage(domain="风控", asset_count=198, quality_score=91.7, governance_score=88.9),
    DomainCoverage(domain="财务", asset_count=156, quality_score=92.3, governance_score=90.2),
    DomainCoverage(domain="供应链", asset_count=243, quality_score=83.1, governance_score=72.6),
]
