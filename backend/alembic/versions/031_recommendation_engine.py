"""Phase 7: Recommendation Engine — enhance recommendations table, add recommendation_history

Revision ID: 031
Revises: 030
Create Date: 2026-07-21
"""
from alembic import op
import sqlalchemy as sa

revision = '031'
down_revision = '030'
branch_labels = None
depends_on = None


def upgrade():
    # Alter existing recommendations table — add new columns
    with op.batch_alter_table('recommendations') as batch_op:
        batch_op.add_column(sa.Column('rec_type', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('title', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('description', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('score', sa.Float, default=0))
        batch_op.add_column(sa.Column('reasons_json', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(20), default='active'))
        batch_op.add_column(sa.Column('feedback', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('metadata_json', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()))
        batch_op.create_index('ix_recommendations_rec_type', ['rec_type'])
        batch_op.create_index('ix_recommendations_status', ['status'])

    # Create recommendation_history table
    op.create_table(
        'recommendation_history',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('recommendation_id', sa.Integer, nullable=False, index=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('old_status', sa.String(20), nullable=True),
        sa.Column('new_status', sa.String(20), nullable=True),
        sa.Column('metadata_json', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('recommendation_history')

    with op.batch_alter_table('recommendations') as batch_op:
        batch_op.drop_index('ix_recommendations_status')
        batch_op.drop_index('ix_recommendations_rec_type')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('metadata_json')
        batch_op.drop_column('feedback')
        batch_op.drop_column('status')
        batch_op.drop_column('reasons_json')
        batch_op.drop_column('score')
        batch_op.drop_column('description')
        batch_op.drop_column('title')
        batch_op.drop_column('rec_type')
