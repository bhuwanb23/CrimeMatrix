"""Phase 3: Crime Trend Analysis — crime_statistics, trend_snapshots

Revision ID: 015
Revises: 014
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '015'
down_revision = '014'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('crime_statistics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('period_type', sa.String(20), nullable=False),
        sa.Column('period_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('period_end', sa.DateTime(timezone=True)),
        sa.Column('total_crimes', sa.Integer(), server_default='0'),
        sa.Column('open_crimes', sa.Integer(), server_default='0'),
        sa.Column('closed_crimes', sa.Integer(), server_default='0'),
        sa.Column('resolution_rate', sa.Float(), server_default='0'),
        sa.Column('district_id', sa.Integer()),
        sa.Column('crime_type_id', sa.Integer()),
        sa.Column('station_id', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_crime_stats_period', 'crime_statistics', ['period_type', 'period_start'])
    op.create_index('idx_crime_stats_district', 'crime_statistics', ['district_id'])

    op.create_table('trend_snapshots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('snapshot_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('metric_name', sa.String(100), nullable=False),
        sa.Column('metric_value', sa.Float(), nullable=False),
        sa.Column('comparison_value', sa.Float()),
        sa.Column('change_pct', sa.Float()),
        sa.Column('direction', sa.String(20)),
        sa.Column('metadata_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_trend_snapshots_metric', 'trend_snapshots', ['metric_name', 'snapshot_date'])


def downgrade() -> None:
    op.drop_table('trend_snapshots')
    op.drop_table('crime_statistics')
