"""Phase 4: High-Risk Suspect Scoring — suspect_risk_scores, risk_score_history, risk_factors

Revision ID: 022
Revises: 021
Create Date: 2026-07-20
"""
from alembic import op
import sqlalchemy as sa

revision = '022'
down_revision = '021'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('suspect_risk_scores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('suspect_id', sa.Integer(), nullable=False, index=True),
        sa.Column('overall_score', sa.Float(), server_default='0'),
        sa.Column('risk_level', sa.String(20), server_default='low'),
        sa.Column('criminal_history_score', sa.Float(), server_default='0'),
        sa.Column('offense_severity_score', sa.Float(), server_default='0'),
        sa.Column('age_factor_score', sa.Float(), server_default='0'),
        sa.Column('location_risk_score', sa.Float(), server_default='0'),
        sa.Column('associate_risk_score', sa.Float(), server_default='0'),
        sa.Column('recency_score', sa.Float(), server_default='0'),
        sa.Column('network_influence_score', sa.Float(), server_default='0'),
        sa.Column('mo_similarity_score', sa.Float(), server_default='0'),
        sa.Column('investigation_links_score', sa.Float(), server_default='0'),
        sa.Column('behavioral_score', sa.Float(), server_default='0'),
        sa.Column('explanation_json', sa.Text()),
        sa.Column('evidence_json', sa.Text()),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('risk_score_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('suspect_id', sa.Integer(), nullable=False, index=True),
        sa.Column('score', sa.Float()),
        sa.Column('risk_level', sa.String(20)),
        sa.Column('scored_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('change_from_previous', sa.Float()),
    )

    op.create_table('risk_factors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('suspect_id', sa.Integer(), nullable=False, index=True),
        sa.Column('factor_name', sa.String(100), nullable=False),
        sa.Column('factor_value', sa.Float()),
        sa.Column('weight', sa.Float(), server_default='0'),
        sa.Column('description', sa.Text()),
        sa.Column('source', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('risk_factors')
    op.drop_table('risk_score_history')
    op.drop_table('suspect_risk_scores')
