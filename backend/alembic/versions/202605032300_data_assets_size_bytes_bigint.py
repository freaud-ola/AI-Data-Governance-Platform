"""data_assets.size_bytes INTEGER -> BIGINT（Mock 种子含超过 int32 的字节数）."""

from alembic import op
import sqlalchemy as sa


revision = "202605032300_bigint_size_bytes"
down_revision = "202605031200_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "data_assets",
        "size_bytes",
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        postgresql_using="size_bytes::bigint",
    )


def downgrade() -> None:
    op.alter_column(
        "data_assets",
        "size_bytes",
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="size_bytes::integer",
    )
