"""crime data tables

Revision ID: 002
Revises: 001
Create Date: 2026-07-16
"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('persons',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('date_of_birth', sa.String(10)),
        sa.Column('gender', sa.String(10)),
        sa.Column('phone', sa.String(20)),
        sa.Column('email', sa.String(100)),
        sa.Column('address', sa.Text()),
        sa.Column('district', sa.String(100)),
        sa.Column('aadhar_number', sa.String(20)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('criminals',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('person_id', sa.Integer()),
        sa.Column('alias', sa.String(100)),
        sa.Column('risk_score', sa.Float(), server_default='0'),
        sa.Column('status', sa.String(20), server_default='at_large'),
        sa.Column('mo_description', sa.Text()),
        sa.Column('behavioral_profile', sa.Text()),
        sa.Column('first_offense_date', sa.String(10)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('victims',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('person_id', sa.Integer()),
        sa.Column('case_id', sa.Integer()),
        sa.Column('statement', sa.Text()),
        sa.Column('injury_type', sa.String(50)),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('witnesses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('person_id', sa.Integer()),
        sa.Column('case_id', sa.Integer()),
        sa.Column('statement', sa.Text()),
        sa.Column('reliability', sa.String(20), server_default='unknown'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('officers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('badge_number', sa.String(20), unique=True, nullable=False),
        sa.Column('rank', sa.String(50)),
        sa.Column('station_id', sa.Integer()),
        sa.Column('specialization', sa.String(100)),
        sa.Column('phone', sa.String(20)),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('stations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(20), unique=True, nullable=False),
        sa.Column('district_id', sa.Integer()),
        sa.Column('address', sa.String(200)),
        sa.Column('phone', sa.String(20)),
        sa.Column('type', sa.String(50), server_default='police_station'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('districts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(20), unique=True, nullable=False),
        sa.Column('state', sa.String(50), server_default='Karnataka'),
        sa.Column('population', sa.Integer()),
        sa.Column('area_sq_km', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('vehicles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('registration_number', sa.String(20), unique=True, nullable=False),
        sa.Column('make', sa.String(50)),
        sa.Column('model', sa.String(50)),
        sa.Column('color', sa.String(30)),
        sa.Column('type', sa.String(30)),
        sa.Column('owner_id', sa.Integer()),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('phones',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('number', sa.String(20), nullable=False),
        sa.Column('owner_id', sa.Integer()),
        sa.Column('carrier', sa.String(50)),
        sa.Column('type', sa.String(20), server_default='mobile'),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('locations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('address', sa.String(300)),
        sa.Column('latitude', sa.Float()),
        sa.Column('longitude', sa.Float()),
        sa.Column('district_id', sa.Integer()),
        sa.Column('type', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('crime_types',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(20), unique=True, nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('severity_level', sa.Integer(), server_default='1'),
        sa.Column('is_active', sa.Integer(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('crimes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('crime_type_id', sa.Integer()),
        sa.Column('district_id', sa.Integer()),
        sa.Column('location_id', sa.Integer()),
        sa.Column('status', sa.String(20), server_default='open'),
        sa.Column('priority', sa.String(20), server_default='medium'),
        sa.Column('reported_by', sa.Integer()),
        sa.Column('occurred_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table('crimes')
    op.drop_table('crime_types')
    op.drop_table('locations')
    op.drop_table('phones')
    op.drop_table('vehicles')
    op.drop_table('districts')
    op.drop_table('stations')
    op.drop_table('officers')
    op.drop_table('witnesses')
    op.drop_table('victims')
    op.drop_table('criminals')
    op.drop_table('persons')
