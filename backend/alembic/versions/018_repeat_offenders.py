"""Phase 9: Repeat Offender Tracking — repeat_offenders, offender_scores

Revision ID: 018
Revises: 017
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '018'
down_revision = '017'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('repeat_offenders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('criminal_id', sa.Integer(), index=True),
        sa.Column('suspect_id', sa.Integer(), index=True),
        sa.Column('offender_name', sa.String(200), nullable=False),
        sa.Column('total_offenses', sa.Integer(), server_default='0'),
        sa.Column('frequency_score', sa.Float(), server_default='0'),
        sa.Column('recency_score', sa.Float(), server_default='0'),
        sa.Column('severity_score', sa.Float(), server_default='0'),
        sa.Column('geographic_score', sa.Float(), server_default='0'),
        sa.Column('overall_score', sa.Float(), server_default='0'),
        sa.Column('risk_level', sa.String(20), server_default='low'),
        sa.Column('risk_factors', sa.Text()),
        sa.Column('first_offense_date', sa.String(10)),
        sa.Column('last_offense_date', sa.String(10)),
        sa.Column('districts_active', sa.Text()),
        sa.Column('crime_types', sa.Text()),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('offender_scores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('offender_id', sa.Integer(), nullable=False, index=True),
        sa.Column('dimension', sa.String(50), nullable=False),
        sa.Column('score', sa.Float(), server_default='0'),
        sa.Column('details', sa.Text()),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('offender_scores')
    op.drop_table('repeat_offenders')
