"""Phase 5: Crime Forecasting — crime_forecasts, forecast_snapshots

Revision ID: 023
Revises: 022
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '023'
down_revision = '022'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('crime_forecasts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('forecast_type', sa.String(50), nullable=False),
        sa.Column('district_id', sa.Integer()),
        sa.Column('crime_type_id', sa.Integer()),
        sa.Column('forecast_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('target_period', sa.String(20)),
        sa.Column('predicted_value', sa.Float(), server_default='0'),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('actual_value', sa.Float()),
        sa.Column('model_name', sa.String(100)),
        sa.Column('parameters_json', sa.Text()),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('forecast_snapshots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('snapshot_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('metric_name', sa.String(100), nullable=False),
        sa.Column('metric_value', sa.Float()),
        sa.Column('forecast_value', sa.Float()),
        sa.Column('confidence', sa.Float()),
        sa.Column('metadata_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('forecast_snapshots')
    op.drop_table('crime_forecasts')
