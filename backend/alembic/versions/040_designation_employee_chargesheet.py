"""Designation/Employee/ChargesheetDetails + Frontend Integration

Revision ID: 040
Revises: 039
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '040'
down_revision = '039'
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
    # Designations table
    if not table_exists('designations'):
        op.create_table('designations',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('active', sa.Boolean, default=True),
            sa.Column('sort_order', sa.Integer, default=0),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    # Blood Groups table
    if not table_exists('blood_groups'):
        op.create_table('blood_groups',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(10), nullable=False),
            sa.Column('code', sa.String(5), unique=True, nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    # Chargesheet Details table
    if not table_exists('chargesheet_details'):
        op.create_table('chargesheet_details',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('case_id', sa.Integer, nullable=False, index=True),
            sa.Column('cs_date', sa.DateTime, nullable=True),
            sa.Column('cs_type', sa.String(1), nullable=True),
            sa.Column('police_person_id', sa.Integer, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    # Enhance officers with 9 new columns
    with op.batch_alter_table('officers') as batch_op:
        if not column_exists('officers', 'designation_id'):
            batch_op.add_column(sa.Column('designation_id', sa.Integer, nullable=True))
        if not column_exists('officers', 'district_id'):
            batch_op.add_column(sa.Column('district_id', sa.Integer, nullable=True))
        if not column_exists('officers', 'kgid'):
            batch_op.add_column(sa.Column('kgid', sa.String(20), nullable=True))
        if not column_exists('officers', 'first_name'):
            batch_op.add_column(sa.Column('first_name', sa.String(100), nullable=True))
        if not column_exists('officers', 'dob'):
            batch_op.add_column(sa.Column('dob', sa.Date, nullable=True))
        if not column_exists('officers', 'gender_id'):
            batch_op.add_column(sa.Column('gender_id', sa.Integer, nullable=True))
        if not column_exists('officers', 'blood_group_id'):
            batch_op.add_column(sa.Column('blood_group_id', sa.Integer, nullable=True))
        if not column_exists('officers', 'physically_challenged'):
            batch_op.add_column(sa.Column('physically_challenged', sa.Boolean, default=False))
        if not column_exists('officers', 'appointment_date'):
            batch_op.add_column(sa.Column('appointment_date', sa.Date, nullable=True))

    # Enhance case_categories and gravity_offences
    with op.batch_alter_table('case_categories') as batch_op:
        if not column_exists('case_categories', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))

    with op.batch_alter_table('gravity_offences') as batch_op:
        if not column_exists('gravity_offences', 'active'):
            batch_op.add_column(sa.Column('active', sa.Boolean, default=True))


def downgrade():
    with op.batch_alter_table('gravity_offences') as batch_op:
        if column_exists('gravity_offences', 'active'):
            batch_op.drop_column('active')

    with op.batch_alter_table('case_categories') as batch_op:
        if column_exists('case_categories', 'active'):
            batch_op.drop_column('active')

    with op.batch_alter_table('officers') as batch_op:
        for col in ['appointment_date', 'physically_challenged', 'blood_group_id',
                     'gender_id', 'dob', 'first_name', 'kgid', 'district_id', 'designation_id']:
            if column_exists('officers', col):
                batch_op.drop_column(col)

    if table_exists('chargesheet_details'):
        op.drop_table('chargesheet_details')
    if table_exists('blood_groups'):
        op.drop_table('blood_groups')
    if table_exists('designations'):
        op.drop_table('designations')
