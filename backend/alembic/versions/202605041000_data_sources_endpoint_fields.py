"""data_sources：接入地址 / 端口 / 默认库（展示 Hive / MySQL Docker 环境）."""

from alembic import op
import sqlalchemy as sa


revision = "202605041000_ds_endpoint"
down_revision = "202605032300_bigint_size_bytes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "data_sources",
        sa.Column("endpoint_host", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "data_sources",
        sa.Column("endpoint_port", sa.Integer(), nullable=True),
    )
    op.add_column(
        "data_sources",
        sa.Column("default_database", sa.String(length=256), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("data_sources", "default_database")
    op.drop_column("data_sources", "endpoint_port")
    op.drop_column("data_sources", "endpoint_host")
