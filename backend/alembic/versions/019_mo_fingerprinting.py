"""Phase 10: MO Fingerprinting — mo_profiles, mo_embeddings, mo_similarity

Revision ID: 019
Revises: 018
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '019'
down_revision = '018'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('mo_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('crime_id', sa.Integer(), index=True),
        sa.Column('case_id', sa.Integer()),
        sa.Column('entry_method', sa.String(100)),
        sa.Column('exit_method', sa.String(100)),
        sa.Column('timing_pattern', sa.String(100)),
        sa.Column('weapon_type', sa.String(100)),
        sa.Column('target_type', sa.String(100)),
        sa.Column('location_pattern', sa.String(100)),
        sa.Column('victim_profile', sa.String(100)),
        sa.Column('escape_method', sa.String(100)),
        sa.Column('mo_text', sa.Text()),
        sa.Column('fingerprint_json', sa.Text()),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('mo_embeddings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profile_id', sa.Integer(), nullable=False, index=True),
        sa.Column('dimension', sa.String(50)),
        sa.Column('vector_json', sa.Text()),
        sa.Column('content', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('mo_similarity',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profile_id_1', sa.Integer(), nullable=False, index=True),
        sa.Column('profile_id_2', sa.Integer(), nullable=False, index=True),
        sa.Column('similarity_score', sa.Float(), server_default='0'),
        sa.Column('match_level', sa.String(20)),
        sa.Column('shared_features', sa.Text()),
        sa.Column('compared_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('mo_similarity')
    op.drop_table('mo_embeddings')
    op.drop_table('mo_profiles')
