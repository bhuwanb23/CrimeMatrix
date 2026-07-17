"""Phase 8: AI Monitoring Database

Revision ID: 008
Revises: 007
Create Date: 2026-07-17
"""
from alembic import op
import sqlalchemy as sa

revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('model_usage',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('provider', sa.String(50), nullable=False, index=True),
        sa.Column('model', sa.String(50), nullable=False),
        sa.Column('prompt_tokens', sa.Integer(), server_default='0'),
        sa.Column('completion_tokens', sa.Integer(), server_default='0'),
        sa.Column('duration_ms', sa.Float(), server_default='0'),
        sa.Column('session_id', sa.String(50)),
        sa.Column('status', sa.String(20), server_default='success'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('latency_records',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('endpoint', sa.String(200), nullable=False, index=True),
        sa.Column('provider', sa.String(50)),
        sa.Column('duration_ms', sa.Float(), nullable=False),
        sa.Column('status', sa.String(20), server_default='ok'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('token_usage_records',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('provider', sa.String(50), nullable=False, index=True),
        sa.Column('model', sa.String(50)),
        sa.Column('prompt_tokens', sa.Integer(), server_default='0'),
        sa.Column('completion_tokens', sa.Integer(), server_default='0'),
        sa.Column('total_tokens', sa.Integer(), server_default='0'),
        sa.Column('session_id', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('tool_calls',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tool_name', sa.String(50), nullable=False, index=True),
        sa.Column('success', sa.Boolean(), server_default='1'),
        sa.Column('duration_ms', sa.Float(), server_default='0'),
        sa.Column('error', sa.Text()),
        sa.Column('request_id', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('tool_calls')
    op.drop_table('token_usage_records')
    op.drop_table('latency_records')
    op.drop_table('model_usage')
