"""Phase 7: Explainable Predictions — prediction_explanations, prediction_sources

Revision ID: 025
Revises: 024
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '025'
down_revision = '024'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('prediction_explanations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('prediction_id', sa.Integer(), nullable=False, index=True),
        sa.Column('explanation_type', sa.String(50)),
        sa.Column('contributing_factors', sa.Text()),
        sa.Column('confidence_breakdown', sa.Text()),
        sa.Column('model_explanation', sa.Text()),
        sa.Column('evidence_links', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('prediction_sources',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('prediction_id', sa.Integer(), nullable=False, index=True),
        sa.Column('source_type', sa.String(50)),
        sa.Column('source_id', sa.Integer()),
        sa.Column('source_name', sa.String(200)),
        sa.Column('relevance_score', sa.Float(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('prediction_sources')
    op.drop_table('prediction_explanations')
