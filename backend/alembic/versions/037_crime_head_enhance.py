"""CrimeHead/CrimeSubHead Enhancement + Caste/Religion/Occupation Verification

Revision ID: 037
Revises: 036
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '037'
down_revision = '036'
branch_labels = None
depends_on = None


def column_exists(table, column):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in result.fetchall())


def upgrade():
    # Add active to crime_heads
    with op.batch_alter_table('crime_heads') as batch_op:
        if not column_exists('crime_heads', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))

    # Add seq_id to crime_sub_heads
    with op.batch_alter_table('crime_sub_heads') as batch_op:
        if not column_exists('crime_sub_heads', 'seq_id'):
            batch_op.add_column(sa.Column('seq_id', sa.Integer, nullable=True))


def downgrade():
    with op.batch_alter_table('crime_sub_heads') as batch_op:
        if column_exists('crime_sub_heads', 'seq_id'):
            batch_op.drop_column('seq_id')

    with op.batch_alter_table('crime_heads') as batch_op:
        if column_exists('crime_heads', 'active'):
            batch_op.drop_column('active')
