"""Phase 6: Knowledge Graph Persistence — Add confidence and weight

Revision ID: 006
Revises: 005
Create Date: 2026-07-17
"""
from alembic import op
import sqlalchemy as sa

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('graph_nodes', sa.Column('confidence', sa.Float(), server_default='1.0'))
    op.add_column('graph_edges', sa.Column('weight', sa.Float(), server_default='1.0'))


def downgrade() -> None:
    op.drop_column('graph_edges', 'weight')
    op.drop_column('graph_nodes', 'confidence')
