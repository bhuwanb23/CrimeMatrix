"""Phase 4: Cross-District Intelligence — cross_district_matches, match_history

Revision ID: 029
Revises: 028
Create Date: 2026-07-21
"""
from alembic import op
import sqlalchemy as sa

revision = '029'
down_revision = '028'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('cross_district_matches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('match_type', sa.String(50), nullable=False),
        sa.Column('entity_id_1', sa.Integer()),
        sa.Column('entity_type_1', sa.String(50)),
        sa.Column('district_1', sa.String(100)),
        sa.Column('entity_id_2', sa.Integer()),
        sa.Column('entity_type_2', sa.String(50)),
        sa.Column('district_2', sa.String(100)),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('match_reason', sa.Text()),
        sa.Column('evidence_json', sa.Text()),
        sa.Column('status', sa.String(20), server_default='new'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('match_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('match_id', sa.Integer(), nullable=False, index=True),
        sa.Column('action', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('match_history')
    op.drop_table('cross_district_matches')
