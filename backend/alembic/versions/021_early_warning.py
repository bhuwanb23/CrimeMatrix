"""Phase 3: Early Warning Alerts — early_warning_alerts, alert_rules, alert_events

Revision ID: 021
Revises: 020
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '021'
down_revision = '020'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('early_warning_alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('severity', sa.String(20), server_default='medium'),
        sa.Column('district_id', sa.Integer()),
        sa.Column('crime_type_id', sa.Integer()),
        sa.Column('case_id', sa.Integer()),
        sa.Column('detected_value', sa.Float()),
        sa.Column('threshold', sa.Float()),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('acknowledged_by', sa.String(100)),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True)),
        sa.Column('evidence_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('resolved_at', sa.DateTime(timezone=True)),
    )

    op.create_table('alert_rules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('rule_type', sa.String(50), nullable=False),
        sa.Column('condition_json', sa.Text()),
        sa.Column('threshold', sa.Float(), server_default='0'),
        sa.Column('action', sa.String(100)),
        sa.Column('is_active', sa.Boolean(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('alert_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('alert_id', sa.Integer(), nullable=False, index=True),
        sa.Column('event_type', sa.String(50)),
        sa.Column('message', sa.Text()),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('alert_events')
    op.drop_table('alert_rules')
    op.drop_table('early_warning_alerts')
