"""ActSectionAssociation + Victim tables

Revision ID: 034
Revises: 033
Create Date: 2026-07-22
"""
from alembic import op
import sqlalchemy as sa

revision = '034'
down_revision = '033'
branch_labels = None
depends_on = None


def table_exists(name):
    bind = op.get_bind()
    result = bind.execute(sa.text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'"))
    return result.fetchone() is not None


def upgrade():
    if not table_exists('acts'):
        op.create_table('acts',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('code', sa.String(50), nullable=True),
            sa.Column('act_code', sa.String(50), unique=True, nullable=False),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('sections'):
        op.create_table('sections',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('code', sa.String(50), nullable=True),
            sa.Column('section_code', sa.String(50), nullable=False),
            sa.Column('act_id', sa.Integer, sa.ForeignKey('acts.id'), nullable=True),
            sa.Column('description', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('act_section_associations'):
        op.create_table('act_section_associations',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('case_id', sa.Integer, sa.ForeignKey('cases.id'), nullable=False, index=True),
            sa.Column('act_id', sa.Integer, sa.ForeignKey('acts.id'), nullable=False),
            sa.Column('section_id', sa.Integer, sa.ForeignKey('sections.id'), nullable=False),
            sa.Column('act_order', sa.Integer, default=1),
            sa.Column('section_order', sa.Integer, default=1),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        )

    if not table_exists('victims'):
        op.create_table('victims',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('case_id', sa.Integer, sa.ForeignKey('cases.id'), nullable=False, index=True),
            sa.Column('name', sa.String(200), nullable=False),
            sa.Column('age_year', sa.Integer, nullable=True),
            sa.Column('gender_id', sa.Integer, sa.ForeignKey('genders.id'), nullable=True),
            sa.Column('is_police', sa.Boolean, default=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        )


def downgrade():
    for t in ['victims', 'act_section_associations', 'sections', 'acts']:
        if table_exists(t):
            op.drop_table(t)
