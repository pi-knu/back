"""add is_finished and is_deleted fields

Revision ID: d3850d810e2e
Revises: 6e00d86a8c1b
Create Date: 2025-11-28 22:58:09.756708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3850d810e2e'
down_revision: Union[str, Sequence[str], None] = '81d97109024c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('lot', sa.Column('is_deleted', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('lot', sa.Column('is_finished', sa.Boolean(), server_default='false', nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('lot', 'is_finished')
    op.drop_column('lot', 'is_deleted')
    pass
