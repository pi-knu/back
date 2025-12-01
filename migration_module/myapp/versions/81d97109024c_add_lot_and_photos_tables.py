"""add auction system tables (lot, photos, auction, bid)

Revision ID: 81d97109024c
Revises: 847037f27aee

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = '81d97109024c'  
down_revision: Union[str, Sequence[str], None] = '847037f27aee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- 1. TABLE: LOT ---
    op.create_table(
        'lot',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    )

    # --- 2. TABLE: PHOTOS ---
    op.create_table(
        'photos',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('lot_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('lot.id'), nullable=False),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.CheckConstraint('"order" >= 1 AND "order" <= 8', name='ck_photos_order_range'),
    )

    # --- 3. TABLE: AUCTION ---
    auction_status_enum = sa.Enum(
        'draft', 'scheduled', 'active', 'finished', 'cancelled', 
        name='auction_status_enum'
    )
    
    op.create_table(
        'auction',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('lot_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('lot.id'), nullable=False),
        
        sa.Column('min_price', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('min_step', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('current_price', sa.Numeric(precision=12, scale=2), nullable=True), 
        
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        
        sa.Column('user_winner_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', auction_status_enum, server_default='draft', nullable=False),
        
        sa.CheckConstraint('min_price >= 1', name='ck_auction_min_price'),
        sa.CheckConstraint('min_step > 1', name='ck_auction_min_step'),
    )

    # --- 4. TABLE: BID ---
    op.create_table(
        'bid',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('auction_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('auction.id', ondelete='CASCADE'), nullable=False),
        
        sa.Column('price', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_aborted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    )

    # function to update current_price = max bid 
    op.execute("""
        CREATE OR REPLACE FUNCTION update_auction_current_price()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE auction
            SET current_price = (
                SELECT MAX(price)
                FROM bid
                WHERE bid.auction_id = COALESCE(NEW.auction_id, OLD.auction_id)
                  AND bid.is_aborted = false
            )
            WHERE id = COALESCE(NEW.auction_id, OLD.auction_id);
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
        CREATE TRIGGER trigger_update_auction_price_on_bid
        AFTER INSERT OR UPDATE OR DELETE ON bid
        FOR EACH ROW
        EXECUTE FUNCTION update_auction_current_price();
    """)

def downgrade() -> None:
    op.drop_table('bid')
    op.drop_table('auction')
    op.drop_table('photos')
    op.drop_table('lot')
    
    op.execute("DROP TYPE IF EXISTS auction_status_enum")