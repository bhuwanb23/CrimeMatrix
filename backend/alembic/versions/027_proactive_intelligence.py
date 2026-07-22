"""Phase 1: Proactive Intelligence — intelligence_events, event_queue, processed_events

Revision ID: 027
Revises: 026
Create Date: 2026-07-21
"""
from alembic import op
import sqlalchemy as sa

revision = '027'
down_revision = '026'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('intelligence_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.Integer()),
        sa.Column('entity_type', sa.String(50)),
        sa.Column('event_data', sa.Text()),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('processed_at', sa.DateTime(timezone=True)),
    )

    op.create_table('event_queue',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), nullable=False, index=True),
        sa.Column('priority', sa.String(20), server_default='medium'),
        sa.Column('status', sa.String(20), server_default='queued'),
        sa.Column('retry_count', sa.Integer(), server_default='0'),
        sa.Column('max_retries', sa.Integer(), server_default='3'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('processed_at', sa.DateTime(timezone=True)),
    )

    op.create_table('processed_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_id', sa.Integer(), nullable=False, index=True),
        sa.Column('processor_name', sa.String(100)),
        sa.Column('result', sa.Text()),
        sa.Column('duration_ms', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('processed_events')
    op.drop_table('event_queue')
    op.drop_table('intelligence_events')
