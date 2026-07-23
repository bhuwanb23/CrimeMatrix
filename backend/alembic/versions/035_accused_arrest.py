"""Accused + ArrestSurrender tables

Revision ID: 035
Revises: 034
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '035'
down_revision = '034'
branch_labels = None
depends_on = None


def table_exists(name):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'"))
    return result.fetchone() is not None


def upgrade():
    if not table_exists('states'):
        op.create_table('states',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(10), unique=True, nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('arrest_surrender_types'):
        op.create_table('arrest_surrender_types',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('accused'):
        op.create_table('accused',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('case_id', sa.Integer, sa.ForeignKey('cases.id'), nullable=False, index=True),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('age_year', sa.Integer, nullable=True),
            sa.Column('gender_id', sa.Integer, sa.ForeignKey('genders.id'), nullable=True),
            sa.Column('person_id', sa.String(10), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        )

    if not table_exists('arrest_surrender'):
        op.create_table('arrest_surrender',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('case_id', sa.Integer, sa.ForeignKey('cases.id'), nullable=False, index=True),
            sa.Column('type_id', sa.Integer, sa.ForeignKey('arrest_surrender_types.id'), nullable=True),
            sa.Column('date', sa.DateTime, nullable=True),
            sa.Column('state_id', sa.Integer, sa.ForeignKey('states.id'), nullable=True),
            sa.Column('district_id', sa.Integer, sa.ForeignKey('districts.id'), nullable=True),
            sa.Column('police_station_id', sa.Integer, sa.ForeignKey('stations.id'), nullable=True),
            sa.Column('io_id', sa.Integer, sa.ForeignKey('officers.id'), nullable=True),
            sa.Column('court_id', sa.Integer, sa.ForeignKey('courts.id'), nullable=True),
            sa.Column('accused_id', sa.Integer, sa.ForeignKey('accused.id'), nullable=True),
            sa.Column('is_accused', sa.Boolean, default=False),
            sa.Column('is_complainant_accused', sa.Boolean, default=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        )


def downgrade():
    for t in ['arrest_surrender', 'accused', 'arrest_surrender_types', 'states']:
        if table_exists(t):
            op.drop_table(t)
