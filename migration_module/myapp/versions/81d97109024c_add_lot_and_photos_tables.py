"""add lot and photos tables

Revision ID: 81d97109024c
Revises: 847037f27aee
Create Date: 2025-11-23 17:43:43.982569

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81d97109024c'
down_revision: Union[str, Sequence[str], None] = '847037f27aee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lot",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),

        sa.Column("min_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("min_step", sa.Numeric(12, 2), nullable=False),
        sa.Column("current_price", sa.Numeric(12, 2), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("is_finished", sa.Boolean(), server_default=sa.text("false"), nullable=False),

        sa.CheckConstraint("min_price >= 1", name="ck_lot_min_price_ge_1"),
        sa.CheckConstraint("min_step > 1", name="ck_lot_min_step_gt_1"),
    )

    op.create_table(
        "lot_photos",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "lot_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("lot.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("url", sa.String(length=1024), nullable=False),
    )

    op.create_index("ix_lot_photos_lot_id", "lot_photos", ["lot_id"])


def downgrade() -> None:
    op.drop_index("ix_lot_photos_lot_id", table_name="lot_photos")
    op.drop_table("lot_photos")
    op.drop_table("lot")