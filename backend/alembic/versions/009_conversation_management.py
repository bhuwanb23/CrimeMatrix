"""Phase 10: Conversation Management — Pin, Bookmark, Export

Revision ID: 009
Revises: 008
Create Date: 2026-07-18
"""
from alembic import op
import sqlalchemy as sa

revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('chat_sessions', sa.Column('is_pinned', sa.Boolean(), server_default='0'))
    op.add_column('chat_sessions', sa.Column('is_archived', sa.Boolean(), server_default='0'))

    op.create_table('bookmarked_messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(50), nullable=False, index=True),
        sa.Column('message_content', sa.Text(), nullable=False),
        sa.Column('message_role', sa.String(20)),
        sa.Column('note', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('conversation_exports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(50), nullable=False, index=True),
        sa.Column('format', sa.String(20), server_default='json'),
        sa.Column('file_path', sa.String(500)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('conversation_exports')
    op.drop_table('bookmarked_messages')
    op.drop_column('chat_sessions', 'is_archived')
    op.drop_column('chat_sessions', 'is_pinned')
