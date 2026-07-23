"""Unit/UnitType/Rank Tables

Revision ID: 039
Revises: 038
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '039'
down_revision = '038'
branch_labels = None
depends_on = None


def table_exists(name):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'"))
    return result.fetchone() is not None


def column_exists(table, column):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in result.fetchall())


def upgrade():
    # Unit Types table
    if not table_exists('unit_types'):
        op.create_table('unit_types',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('city_dist_state', sa.String(50), nullable=True),
            sa.Column('hierarchy', sa.Integer, nullable=True),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('active', sa.Boolean, default=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    # Ranks table
    if not table_exists('ranks'):
        op.create_table('ranks',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('hierarchy', sa.Integer, nullable=True),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('active', sa.Boolean, default=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    # Enhance stations
    with op.batch_alter_table('stations') as batch_op:
        if not column_exists('stations', 'type_id'):
            batch_op.add_column(sa.Column('type_id', sa.Integer, nullable=True))
        if not column_exists('stations', 'parent_unit'):
            batch_op.add_column(sa.Column('parent_unit', sa.Integer, nullable=True))
        if not column_exists('stations', 'nationality_id'):
            batch_op.add_column(sa.Column('nationality_id', sa.Integer, nullable=True))
        if not column_exists('stations', 'state_id'):
            batch_op.add_column(sa.Column('state_id', sa.Integer, nullable=True))
        if not column_exists('stations', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))

    # Enhance officers
    with op.batch_alter_table('officers') as batch_op:
        if not column_exists('officers', 'rank_id'):
            batch_op.add_column(sa.Column('rank_id', sa.Integer, nullable=True))
        if not column_exists('officers', 'unit_id'):
            batch_op.add_column(sa.Column('unit_id', sa.Integer, nullable=True))


def downgrade():
    with op.batch_alter_table('officers') as batch_op:
        if column_exists('officers', 'unit_id'):
            batch_op.drop_column('unit_id')
        if column_exists('officers', 'rank_id'):
            batch_op.drop_column('rank_id')

    with op.batch_alter_table('stations') as batch_op:
        if column_exists('stations', 'active'):
            batch_op.drop_column('active')
        if column_exists('stations', 'state_id'):
            batch_op.drop_column('state_id')
        if column_exists('stations', 'nationality_id'):
            batch_op.drop_column('nationality_id')
        if column_exists('stations', 'parent_unit'):
            batch_op.drop_column('parent_unit')
        if column_exists('stations', 'type_id'):
            batch_op.drop_column('type_id')

    if table_exists('ranks'):
        op.drop_table('ranks')
    if table_exists('unit_types'):
        op.drop_table('unit_types')
