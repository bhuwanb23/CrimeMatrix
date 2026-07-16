"""initial tables

Revision ID: 001
Revises: 
Create Date: 2026-07-16
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(200), nullable=False),
        sa.Column('full_name', sa.String(100)),
        sa.Column('role', sa.String(20), server_default='officer'),
        sa.Column('station', sa.String(100)),
        sa.Column('is_active', sa.Boolean(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('firs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('fir_number', sa.String(50), unique=True, nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('crime_type', sa.String(50), nullable=False),
        sa.Column('district', sa.String(100), nullable=False),
        sa.Column('station', sa.String(100)),
        sa.Column('status', sa.String(20), server_default='filed'),
        sa.Column('complainant_name', sa.String(100)),
        sa.Column('complainant_phone', sa.String(20)),
        sa.Column('date_filed', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('cases',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('case_number', sa.String(50), unique=True, nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('crime_type', sa.String(50), nullable=False),
        sa.Column('district', sa.String(100), nullable=False),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('priority', sa.String(20), server_default='medium'),
        sa.Column('officer_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('fir_id', sa.Integer(), sa.ForeignKey('firs.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('suspects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('age', sa.Integer()),
        sa.Column('gender', sa.String(10)),
        sa.Column('district', sa.String(100)),
        sa.Column('status', sa.String(20), server_default='at_large'),
        sa.Column('risk_score', sa.Float(), server_default='0'),
        sa.Column('description', sa.Text()),
        sa.Column('physical_description', sa.Text()),
        sa.Column('aliases', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('evidence',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('case_id', sa.Integer(), sa.ForeignKey('cases.id')),
        sa.Column('evidence_type', sa.String(50), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('file_path', sa.String(500)),
        sa.Column('recorded_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('investigations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('case_id', sa.Integer(), sa.ForeignKey('cases.id')),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('priority', sa.String(20), server_default='medium'),
        sa.Column('officer_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('progress', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('priority', sa.String(20), server_default='medium'),
        sa.Column('status', sa.String(20), server_default='new'),
        sa.Column('case_id', sa.Integer()),
        sa.Column('district', sa.String(100)),
        sa.Column('is_read', sa.Boolean(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('alerts')
    op.drop_table('investigations')
    op.drop_table('evidence')
    op.drop_table('suspects')
    op.drop_table('cases')
    op.drop_table('firs')
    op.drop_table('users')
