"""Phase 7: Embedding Persistence — Add source and updated_at

Revision ID: 007
Revises: 006
Create Date: 2026-07-17
"""
from alembic import op
import sqlalchemy as sa

revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('embedding_documents', sa.Column('source', sa.String(100), server_default='unknown'))
    op.add_column('embedding_documents', sa.Column('updated_at', sa.DateTime(timezone=True)))
    op.add_column('embedding_chunks', sa.Column('updated_at', sa.DateTime(timezone=True)))


def downgrade() -> None:
    op.drop_column('embedding_chunks', 'updated_at')
    op.drop_column('embedding_documents', 'updated_at')
    op.drop_column('embedding_documents', 'source')
