"""Phase 6: Intelligent Case Prioritization — case_priorities, priority_history, priority_explanations

Revision ID: 024
Revises: 023
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '024'
down_revision = '023'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('case_priorities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), nullable=False, index=True),
        sa.Column('overall_priority_score', sa.Float(), server_default='0'),
        sa.Column('severity_score', sa.Float(), server_default='0'),
        sa.Column('victim_vulnerability_score', sa.Float(), server_default='0'),
        sa.Column('evidence_availability_score', sa.Float(), server_default='0'),
        sa.Column('repeat_offender_score', sa.Float(), server_default='0'),
        sa.Column('active_threats_score', sa.Float(), server_default='0'),
        sa.Column('investigation_age_score', sa.Float(), server_default='0'),
        sa.Column('cross_district_score', sa.Float(), server_default='0'),
        sa.Column('officer_workload_score', sa.Float(), server_default='0'),
        sa.Column('priority_level', sa.String(20), server_default='low'),
        sa.Column('explanation_json', sa.Text()),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('priority_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), nullable=False, index=True),
        sa.Column('priority_score', sa.Float()),
        sa.Column('priority_level', sa.String(20)),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('change_from_previous', sa.Float()),
    )

    op.create_table('priority_explanations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), nullable=False, index=True),
        sa.Column('factor_name', sa.String(100), nullable=False),
        sa.Column('factor_score', sa.Float()),
        sa.Column('weight', sa.Float()),
        sa.Column('explanation', sa.Text()),
        sa.Column('evidence_json', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('priority_explanations')
    op.drop_table('priority_history')
    op.drop_table('case_priorities')
