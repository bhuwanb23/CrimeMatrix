"""Phase 3: Live FIR Intelligence — fir_suggestions, fir_analysis_history

Revision ID: 028
Revises: 027
Create Date: 2026-07-21
"""
from alembic import op
import sqlalchemy as sa

revision = '028'
down_revision = '027'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('fir_suggestions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('fir_id', sa.Integer(), nullable=False, index=True),
        sa.Column('suggestion_type', sa.String(50), nullable=False),
        sa.Column('suggestion_text', sa.Text()),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('entity_id', sa.Integer()),
        sa.Column('entity_type', sa.String(50)),
        sa.Column('status', sa.String(20), server_default='new'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('fir_analysis_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('fir_id', sa.Integer(), nullable=False, index=True),
        sa.Column('analysis_type', sa.String(50)),
        sa.Column('analysis_result', sa.Text()),
        sa.Column('model_used', sa.String(100)),
        sa.Column('processing_time_ms', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('fir_analysis_history')
    op.drop_table('fir_suggestions')
