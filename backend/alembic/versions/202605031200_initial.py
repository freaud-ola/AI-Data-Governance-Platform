"""Initial governance persistence schema."""

from alembic import op
import sqlalchemy as sa


revision = "202605031200_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "data_sources",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("table_count", sa.Integer(), nullable=False),
        sa.Column("last_sync_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "data_assets",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("full_name", sa.String(length=1024), nullable=False),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("database", sa.String(length=256), nullable=False),
        sa.Column("schema_name", sa.String(length=256), nullable=False),
        sa.Column("layer", sa.String(length=32), nullable=False),
        sa.Column("owner", sa.String(length=256), nullable=False),
        sa.Column("domain", sa.String(length=256), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("quality_score", sa.Float(), nullable=False),
        sa.Column("pii_level", sa.String(length=8), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ai_description", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )
    op.create_index(
        "ix_data_assets_tenant_layer", "data_assets", ["tenant_id", "layer"], unique=False
    )
    op.create_index(
        "ix_data_assets_tenant_domain", "data_assets", ["tenant_id", "domain"], unique=False
    )
    op.create_index("ix_data_assets_tenant_name", "data_assets", ["tenant_id", "name"], unique=False)

    op.create_table(
        "quality_rules",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("dimension", sa.String(length=64), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=False),
        sa.Column("asset_name", sa.String(length=512), nullable=False),
        sa.Column("expression", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=8), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("last_run_status", sa.String(length=32), nullable=False),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "quality_incidents",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("rule_id", sa.String(length=128), nullable=False),
        sa.Column("rule_name", sa.String(length=512), nullable=False),
        sa.Column("asset_name", sa.String(length=512), nullable=False),
        sa.Column("severity", sa.String(length=8), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "data_standards",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("code", sa.String(length=256), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("category", sa.String(length=128), nullable=False),
        sa.Column("data_type", sa.String(length=256), nullable=False),
        sa.Column("bound_count", sa.Integer(), nullable=False),
        sa.Column("owner", sa.String(length=256), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "metrics",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("code", sa.String(length=256), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("domain", sa.String(length=256), nullable=False),
        sa.Column("formula", sa.Text(), nullable=False),
        sa.Column("owner", sa.String(length=256), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "master_entities",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("record_count", sa.Integer(), nullable=False),
        sa.Column("owner", sa.String(length=256), nullable=False),
        sa.Column("last_merge_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "lifecycle_policies",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("asset_pattern", sa.String(length=512), nullable=False),
        sa.Column("cold_after_days", sa.Integer(), nullable=False),
        sa.Column("archive_after_days", sa.Integer(), nullable=False),
        sa.Column("delete_after_days", sa.Integer(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "security_classifications",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=False),
        sa.Column("asset_name", sa.String(length=512), nullable=False),
        sa.Column("classification", sa.String(length=64), nullable=False),
        sa.Column("pii_level", sa.String(length=8), nullable=False),
        sa.Column("masking_strategy", sa.Text(), nullable=True),
        sa.Column("owner", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "asset_id"),
    )

    op.create_table(
        "ai_prompts",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("scenario", sa.String(length=128), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("avg_tokens", sa.Integer(), nullable=False),
        sa.Column("success_rate", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "ai_invocations",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("scenario", sa.String(length=128), nullable=False),
        sa.Column("model", sa.String(length=256), nullable=False),
        sa.Column("tokens", sa.Integer(), nullable=False),
        sa.Column("cost", sa.Float(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "report_items",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("period", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "id"),
    )

    op.create_table(
        "tenant_blobs",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("blob_key", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("tenant_id", "blob_key"),
    )


def downgrade() -> None:
    op.drop_table("tenant_blobs")
    op.drop_table("report_items")
    op.drop_table("ai_invocations")
    op.drop_table("ai_prompts")
    op.drop_table("security_classifications")
    op.drop_table("lifecycle_policies")
    op.drop_table("master_entities")
    op.drop_table("metrics")
    op.drop_table("data_standards")
    op.drop_table("quality_incidents")
    op.drop_table("quality_rules")
    op.drop_index("ix_data_assets_tenant_name", table_name="data_assets")
    op.drop_index("ix_data_assets_tenant_domain", table_name="data_assets")
    op.drop_index("ix_data_assets_tenant_layer", table_name="data_assets")
    op.drop_table("data_assets")
    op.drop_table("data_sources")
