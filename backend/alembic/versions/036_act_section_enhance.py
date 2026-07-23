"""Act/Section Enhancement + CrimeHeadActSection

Revision ID: 036
Revises: 035
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '036'
down_revision = '035'
branch_labels = None
depends_on = None


def column_exists(table, column):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in result.fetchall())


def table_exists(name):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'"))
    return result.fetchone() is not None


def upgrade():
    # Add short_name and active to acts
    with op.batch_alter_table('acts') as batch_op:
        if not column_exists('acts', 'short_name'):
            batch_op.add_column(sa.Column('short_name', sa.String(50), nullable=True))
        if not column_exists('acts', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))

    # Add active to sections
    with op.batch_alter_table('sections') as batch_op:
        if not column_exists('sections', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))

    # Create crime_head_act_sections
    if not table_exists('crime_head_act_sections'):
        op.create_table('crime_head_act_sections',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('crime_head_id', sa.Integer, sa.ForeignKey('crime_heads.id'), nullable=False, index=True),
            sa.Column('act_code', sa.String(50), sa.ForeignKey('acts.act_code'), nullable=False),
            sa.Column('section_code', sa.String(50), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )


def downgrade():
    if table_exists('crime_head_act_sections'):
        op.drop_table('crime_head_act_sections')

    with op.batch_alter_table('sections') as batch_op:
        if column_exists('sections', 'active'):
            batch_op.drop_column('active')

    with op.batch_alter_table('acts') as batch_op:
        if column_exists('acts', 'active'):
            batch_op.drop_column('active')
        if column_exists('acts', 'short_name'):
            batch_op.drop_column('short_name')
