"""Phase 2: Predictive Crime Analytics — crime_predictions, prediction_models, prediction_results

Revision ID: 020
Revises: 019
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '020'
down_revision = '019'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('crime_predictions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('prediction_type', sa.String(50), nullable=False),
        sa.Column('district_id', sa.Integer()),
        sa.Column('crime_type_id', sa.Integer()),
        sa.Column('predicted_value', sa.Float(), server_default='0'),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('actual_value', sa.Float()),
        sa.Column('prediction_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('target_date', sa.String(20)),
        sa.Column('model_name', sa.String(100)),
        sa.Column('model_version', sa.String(20)),
        sa.Column('features_json', sa.Text()),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('prediction_models',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('version', sa.String(20)),
        sa.Column('description', sa.Text()),
        sa.Column('accuracy', sa.Float(), server_default='0'),
        sa.Column('last_trained', sa.DateTime(timezone=True)),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('parameters_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('prediction_results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('prediction_id', sa.Integer(), nullable=False, index=True),
        sa.Column('metric_name', sa.String(100)),
        sa.Column('expected_value', sa.Float()),
        sa.Column('actual_value', sa.Float()),
        sa.Column('error', sa.Float()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('prediction_results')
    op.drop_table('prediction_models')
    op.drop_table('crime_predictions')
