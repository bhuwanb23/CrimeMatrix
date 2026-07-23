"""ComplainantDetails + Occupation/Religion/Caste/Gender lookup tables

Revision ID: 033
Revises: 032
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '033'
down_revision = '032'
branch_labels = None
depends_on = None


def table_exists(name):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'"))
    return result.fetchone() is not None


def upgrade():
    # --- Lookup Tables ---
    if not table_exists('occupations'):
        op.create_table('occupations',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('religions'):
        op.create_table('religions',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('caste_master'):
        op.create_table('caste_master',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(100), nullable=False),
            sa.Column('code', sa.String(20), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('genders'):
        op.create_table('genders',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('code', sa.String(10), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    # --- Complainant Table ---
    if not table_exists('complainants'):
        op.create_table('complainants',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('case_id', sa.Integer, sa.ForeignKey('cases.id'), nullable=False, index=True),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('age_year', sa.Integer, nullable=True),
            sa.Column('occupation_id', sa.Integer, sa.ForeignKey('occupations.id'), nullable=True),
            sa.Column('religion_id', sa.Integer, sa.ForeignKey('religions.id'), nullable=True),
            sa.Column('caste_id', sa.Integer, sa.ForeignKey('caste_master.id'), nullable=True),
            sa.Column('gender_id', sa.Integer, sa.ForeignKey('genders.id'), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        )


def downgrade():
    if table_exists('complainants'):
        op.drop_table('complainants')
    for t in ['genders', 'caste_master', 'religions', 'occupations']:
        if table_exists(t):
            op.drop_table(t)
