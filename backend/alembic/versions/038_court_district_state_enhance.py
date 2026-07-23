"""Court/District/State/CaseStatusMaster Enhancement

Revision ID: 038
Revises: 037
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '038'
down_revision = '037'
branch_labels = None
depends_on = None


def column_exists(table, column):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in result.fetchall())


def upgrade():
    # Courts — add district_id, state_id, active
    with op.batch_alter_table('courts') as batch_op:
        if not column_exists('courts', 'district_id'):
            batch_op.add_column(sa.Column('district_id', sa.Integer, sa.ForeignKey('districts.id'), nullable=True))
        if not column_exists('courts', 'state_id'):
            batch_op.add_column(sa.Column('state_id', sa.Integer, sa.ForeignKey('states.id'), nullable=True))
        if not column_exists('courts', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))

    # Districts — add state_id, active
    with op.batch_alter_table('districts') as batch_op:
        if not column_exists('districts', 'state_id'):
            batch_op.add_column(sa.Column('state_id', sa.Integer, sa.ForeignKey('states.id'), nullable=True))
        if not column_exists('districts', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))

    # States — add nationality_id, active
    with op.batch_alter_table('states') as batch_op:
        if not column_exists('states', 'nationality_id'):
            batch_op.add_column(sa.Column('nationality_id', sa.Integer, nullable=True))
        if not column_exists('states', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))


def downgrade():
    with op.batch_alter_table('states') as batch_op:
        if column_exists('states', 'active'):
            batch_op.drop_column('active')
        if column_exists('states', 'nationality_id'):
            batch_op.drop_column('nationality_id')

    with op.batch_alter_table('districts') as batch_op:
        if column_exists('districts', 'active'):
            batch_op.drop_column('active')
        if column_exists('districts', 'state_id'):
            batch_op.drop_column('state_id')

    with op.batch_alter_table('courts') as batch_op:
        if column_exists('courts', 'active'):
            batch_op.drop_column('active')
        if column_exists('courts', 'state_id'):
            batch_op.drop_column('state_id')
        if column_exists('courts', 'district_id'):
            batch_op.drop_column('district_id')
