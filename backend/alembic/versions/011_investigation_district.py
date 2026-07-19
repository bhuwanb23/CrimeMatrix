"""Phase 6: Add district to investigations

Revision ID: 011
Revises: 010
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('investigations', sa.Column('district', sa.String(100)))


def downgrade() -> None:
    op.drop_column('investigations', 'district')
