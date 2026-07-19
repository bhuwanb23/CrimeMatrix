"""Phase 5: Similar Case Discovery — case_embeddings + case_similarity

Revision ID: 010
Revises: 009
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('case_embeddings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('case_id', sa.Integer(), nullable=False, index=True),
        sa.Column('dimension', sa.String(20), nullable=False),
        sa.Column('vector_json', sa.Text(), nullable=False),
        sa.Column('content', sa.Text()),
        sa.Column('model_version', sa.String(50), server_default='tfidf_v1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('case_id', 'dimension', name='uq_case_embedding_dim'),
    )
    op.create_index('idx_case_embeddings_dimension', 'case_embeddings', ['dimension'])

    op.create_table('case_similarity',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('case_id_1', sa.Integer(), nullable=False, index=True),
        sa.Column('case_id_2', sa.Integer(), nullable=False, index=True),
        sa.Column('overall_score', sa.Float(), nullable=False),
        sa.Column('mo_score', sa.Float(), server_default='0'),
        sa.Column('location_score', sa.Float(), server_default='0'),
        sa.Column('time_score', sa.Float(), server_default='0'),
        sa.Column('suspects_score', sa.Float(), server_default='0'),
        sa.Column('evidence_score', sa.Float(), server_default='0'),
        sa.Column('vehicles_score', sa.Float(), server_default='0'),
        sa.Column('reasons_json', sa.Text()),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('computed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('case_id_1', 'case_id_2', name='uq_case_similarity_pair'),
    )
    op.create_index('idx_case_similarity_score', 'case_similarity', ['overall_score'])


def downgrade() -> None:
    op.drop_table('case_similarity')
    op.drop_table('case_embeddings')
