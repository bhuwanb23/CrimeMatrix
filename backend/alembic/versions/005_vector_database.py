"""Phase 4: Local Vector Database

Revision ID: 005
Revises: 004
Create Date: 2026-07-17
"""
from alembic import op
import sqlalchemy as sa

revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('embedding_documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('domain', sa.String(50), nullable=False, index=True),
        sa.Column('title', sa.String(200)),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('embedding_chunks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('document_id', sa.Integer(), nullable=False, index=True),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('vector_json', sa.Text(), nullable=False),
        sa.Column('metadata_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('embedding_chunks')
    op.drop_table('embedding_documents')
