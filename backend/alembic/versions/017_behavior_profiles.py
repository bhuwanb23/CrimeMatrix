"""Phase 8: Behavioral Profiling — behavior_profiles, behavior_features

Revision ID: 017
Revises: 016
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '017'
down_revision = '016'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('behavior_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('criminal_id', sa.Integer(), index=True),
        sa.Column('profile_type', sa.String(50), nullable=False),
        sa.Column('pattern_description', sa.Text()),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('frequency', sa.Integer(), server_default='0'),
        sa.Column('features_json', sa.Text()),
        sa.Column('risk_level', sa.String(20), server_default='low'),
        sa.Column('risk_score', sa.Float(), server_default='0'),
        sa.Column('last_analyzed', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('behavior_features',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profile_id', sa.Integer(), nullable=False, index=True),
        sa.Column('feature_name', sa.String(100), nullable=False),
        sa.Column('feature_value', sa.String(200)),
        sa.Column('weight', sa.Float(), server_default='0'),
        sa.Column('source_crime_ids', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('behavior_features')
    op.drop_table('behavior_profiles')
