"""Phase 7: Add last_accessed to investigations

Revision ID: 012
Revises: 011
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('investigations', sa.Column('last_accessed', sa.DateTime(timezone=True)))


def downgrade() -> None:
    op.drop_column('investigations', 'last_accessed')
