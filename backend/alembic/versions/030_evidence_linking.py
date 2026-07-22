"""Phase 5: Dynamic Evidence Linking — evidence_links, evidence_relationships, link_history

Revision ID: 030
Revises: 029
Create Date: 2026-07-21
"""
from alembic import op
import sqlalchemy as sa

revision = '030'
down_revision = '029'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('evidence_links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('evidence_id_1', sa.Integer()),
        sa.Column('evidence_id_2', sa.Integer()),
        sa.Column('link_type', sa.String(50), nullable=False),
        sa.Column('confidence', sa.Float(), server_default='0'),
        sa.Column('link_reason', sa.Text()),
        sa.Column('status', sa.String(20), server_default='new'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('evidence_relationships',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('evidence_id', sa.Integer()),
        sa.Column('case_id_1', sa.Integer()),
        sa.Column('case_id_2', sa.Integer()),
        sa.Column('relationship_type', sa.String(50)),
        sa.Column('strength', sa.Float(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('link_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('link_id', sa.Integer(), nullable=False, index=True),
        sa.Column('action', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('link_history')
    op.drop_table('evidence_relationships')
    op.drop_table('evidence_links')
