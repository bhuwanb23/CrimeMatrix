"""Phase 8: Continuous Model Evaluation — model_metrics, prediction_feedback, evaluation_results

Revision ID: 026
Revises: 025
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '026'
down_revision = '025'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('model_metrics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('model_name', sa.String(100), nullable=False),
        sa.Column('metric_name', sa.String(100), nullable=False),
        sa.Column('metric_value', sa.Float()),
        sa.Column('measurement_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('period_type', sa.String(20)),
        sa.Column('metadata_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('prediction_feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('prediction_id', sa.Integer(), index=True),
        sa.Column('user_id', sa.Integer()),
        sa.Column('feedback_type', sa.String(20)),
        sa.Column('rating', sa.Integer()),
        sa.Column('comment', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('evaluation_results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('evaluation_type', sa.String(50)),
        sa.Column('model_name', sa.String(100)),
        sa.Column('accuracy', sa.Float()),
        sa.Column('precision_score', sa.Float()),
        sa.Column('recall_score', sa.Float()),
        sa.Column('f1_score', sa.Float()),
        sa.Column('drift_indicator', sa.Float()),
        sa.Column('sample_size', sa.Integer()),
        sa.Column('evaluation_date', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('metadata_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('evaluation_results')
    op.drop_table('prediction_feedback')
    op.drop_table('model_metrics')
