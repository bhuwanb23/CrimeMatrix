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


def column_exists(table, column):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in result.fetchall())


def table_exists(table):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
    return result.fetchone() is not None


def upgrade():
    # Alter existing recommendations table — add new columns (idempotent)
    with op.batch_alter_table('recommendations') as batch_op:
        for col_name, col_type in [
            ('rec_type', sa.String(50)),
            ('title', sa.Text),
            ('description', sa.Text),
            ('score', sa.Float),
            ('reasons_json', sa.Text),
            ('status', sa.String(20)),
            ('feedback', sa.String(20)),
            ('metadata_json', sa.Text),
            ('updated_at', sa.DateTime(timezone=True)),
        ]:
            if not column_exists('recommendations', col_name):
                batch_op.add_column(sa.Column(col_name, col_type, nullable=True))
        if not column_exists('recommendations', 'ix_recommendations_rec_type'):
            batch_op.create_index('ix_recommendations_rec_type', ['rec_type'])
        if not column_exists('recommendations', 'ix_recommendations_status'):
            batch_op.create_index('ix_recommendations_status', ['status'])

    # Create recommendation_history table (idempotent)
    if not table_exists('recommendation_history'):
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
    if table_exists('recommendation_history'):
        op.drop_table('recommendation_history')

    with op.batch_alter_table('recommendations') as batch_op:
        for col in ['ix_recommendations_status', 'ix_recommendations_rec_type']:
            try:
                batch_op.drop_index(col)
            except Exception:
                pass
        for col_name in ['updated_at', 'metadata_json', 'feedback', 'status', 'reasons_json', 'score', 'description', 'title', 'rec_type']:
            if column_exists('recommendations', col_name):
                batch_op.drop_column(col_name)
