"""Phase 8: Extend bookmarks with entity_type, entity_id, bookmark_note

Revision ID: 013
Revises: 012
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '013'
down_revision = '012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('bookmarks', sa.Column('entity_type', sa.String(50), server_default='investigation'))
    op.add_column('bookmarks', sa.Column('entity_id', sa.Integer(), index=True))
    op.add_column('bookmarks', sa.Column('bookmark_note', sa.Text()))


def downgrade() -> None:
    op.drop_column('bookmarks', 'bookmark_note')
    op.drop_column('bookmarks', 'entity_id')
    op.drop_column('bookmarks', 'entity_type')
