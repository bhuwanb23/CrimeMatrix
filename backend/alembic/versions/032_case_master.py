"""CaseMaster ER Diagram — add lookup tables + case columns

Revision ID: 032
Revises: 031
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '032'
down_revision = '031'
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
    # --- Lookup Tables ---
    if not table_exists('case_categories'):
        op.create_table('case_categories',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('gravity_offences'):
        op.create_table('gravity_offences',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('severity_level', sa.Integer, default=1),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('crime_heads'):
        op.create_table('crime_heads',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('crime_sub_heads'):
        op.create_table('crime_sub_heads',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('crime_head_id', sa.Integer, sa.ForeignKey('crime_heads.id'), nullable=True),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('case_status_master'):
        op.create_table('case_status_master',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('courts'):
        op.create_table('courts',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=True),
            sa.Column('district', sa.String(100), nullable=True),
            sa.Column('court_type', sa.String(50), nullable=True),
            sa.Column('address', sa.Text, nullable=True),
            sa.Column('phone', sa.String(20), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    # --- Alter cases table ---
    case_cols = [
        ('crime_no', sa.String(50)),
        ('incident_from_date', sa.DateTime(timezone=True)),
        ('incident_to_date', sa.DateTime(timezone=True)),
        ('info_received_ps_date', sa.DateTime(timezone=True)),
        ('latitude', sa.Float),
        ('longitude', sa.Float),
        ('brief_facts', sa.Text),
        ('case_category_id', sa.Integer),
        ('gravity_offence_id', sa.Integer),
        ('crime_major_head_id', sa.Integer),
        ('crime_minor_head_id', sa.Integer),
        ('case_status_id', sa.Integer),
        ('court_id', sa.Integer),
        ('police_person_id', sa.Integer),
        ('police_station_id', sa.Integer),
    ]

    with op.batch_alter_table('cases') as batch_op:
        for col_name, col_type in case_cols:
            if not column_exists('cases', col_name):
                batch_op.add_column(sa.Column(col_name, col_type, nullable=True))


def downgrade():
    with op.batch_alter_table('cases') as batch_op:
        for col_name in ['crime_no', 'incident_from_date', 'incident_to_date',
                          'info_received_ps_date', 'latitude', 'longitude', 'brief_facts',
                          'case_category_id', 'gravity_offence_id', 'crime_major_head_id',
                          'crime_minor_head_id', 'case_status_id', 'court_id',
                          'police_person_id', 'police_station_id']:
            if column_exists('cases', col_name):
                batch_op.drop_column(col_name)

    for t in ['courts', 'case_status_master', 'crime_sub_heads', 'crime_heads',
              'gravity_offences', 'case_categories']:
        if table_exists(t):
            op.drop_table(t)
