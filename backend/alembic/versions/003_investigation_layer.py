"""investigation layer tables

Revision ID: 003
Revises: 002
Create Date: 2026-07-16
"""
from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('notes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), sa.ForeignKey('investigations.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('bookmarks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('investigation_id', sa.Integer(), sa.ForeignKey('investigations.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('timeline_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), sa.ForeignKey('investigations.id'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('event_date', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('attachments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), sa.ForeignKey('investigations.id'), nullable=False),
        sa.Column('filename', sa.String(200), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('file_size', sa.Integer()),
        sa.Column('file_type', sa.String(50)),
        sa.Column('uploaded_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('case_links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), sa.ForeignKey('investigations.id'), nullable=False),
        sa.Column('linked_case_id', sa.Integer(), sa.ForeignKey('cases.id'), nullable=False),
        sa.Column('link_type', sa.String(50), nullable=False),
        sa.Column('description', sa.String(200)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('case_status_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('investigation_id', sa.Integer(), sa.ForeignKey('investigations.id'), nullable=False),
        sa.Column('old_status', sa.String(20)),
        sa.Column('new_status', sa.String(20), nullable=False),
        sa.Column('changed_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('notes', sa.Text()),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('case_status_logs')
    op.drop_table('case_links')
    op.drop_table('attachments')
    op.drop_table('timeline_events')
    op.drop_table('bookmarks')
    op.drop_table('notes')
