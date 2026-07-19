"""Phase 2: Crime Pattern Discovery — crime_patterns, pattern_occurrences, pattern_clusters

Revision ID: 014
Revises: 013
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '014'
down_revision = '013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('crime_patterns',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('pattern_type', sa.String(50), nullable=False),
        sa.Column('crime_type', sa.String(100)),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('frequency', sa.Integer(), server_default='0'),
        sa.Column('time_pattern', sa.String(100)),
        sa.Column('location_pattern', sa.String(100)),
        sa.Column('mo_summary', sa.Text()),
        sa.Column('first_seen', sa.DateTime(timezone=True)),
        sa.Column('last_seen', sa.DateTime(timezone=True)),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('pattern_occurrences',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('pattern_id', sa.Integer(), nullable=False, index=True),
        sa.Column('crime_id', sa.Integer(), nullable=False, index=True),
        sa.Column('similarity_score', sa.Float(), server_default='0'),
        sa.Column('matched_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('pattern_id', 'crime_id', name='uq_pattern_crime'),
    )

    op.create_table('pattern_clusters',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('pattern_ids', sa.Text()),
        sa.Column('cluster_type', sa.String(50)),
        sa.Column('strength', sa.Float(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('pattern_clusters')
    op.drop_table('pattern_occurrences')
    op.drop_table('crime_patterns')
