"""Phase 2: Intelligence-oriented entities

Revision ID: 004
Revises: 003
Create Date: 2026-07-17
"""
from alembic import op
import sqlalchemy as sa

revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # AI Conversations
    op.create_table('chat_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('user_id', sa.Integer()),
        sa.Column('title', sa.String(200)),
        sa.Column('model_used', sa.String(50)),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('chat_messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(50), nullable=False, index=True),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tokens_used', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('conversation_memory',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(50), nullable=False, index=True),
        sa.Column('key', sa.String(100), nullable=False),
        sa.Column('value', sa.Text()),
        sa.Column('summary', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Reports
    op.create_table('reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('content', sa.Text()),
        sa.Column('format', sa.String(20), server_default='pdf'),
        sa.Column('generated_by', sa.Integer()),
        sa.Column('status', sa.String(20), server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('report_templates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('template_content', sa.Text()),
        sa.Column('is_active', sa.Boolean(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('report_exports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('report_id', sa.Integer(), nullable=False, index=True),
        sa.Column('file_path', sa.String(500)),
        sa.Column('file_size', sa.Integer()),
        sa.Column('format', sa.String(20)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Notifications
    op.create_table('notifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('message', sa.Text()),
        sa.Column('type', sa.String(50)),
        sa.Column('is_read', sa.Boolean(), server_default='0'),
        sa.Column('data', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('notification_preferences',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), unique=True, nullable=False),
        sa.Column('email_enabled', sa.Boolean(), server_default='1'),
        sa.Column('sms_enabled', sa.Boolean(), server_default='0'),
        sa.Column('push_enabled', sa.Boolean(), server_default='1'),
        sa.Column('categories', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('notification_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('notification_id', sa.Integer(), nullable=False, index=True),
        sa.Column('channel', sa.String(20)),
        sa.Column('status', sa.String(20)),
        sa.Column('sent_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Predictions
    op.create_table('predictions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('prediction_type', sa.String(50), nullable=False),
        sa.Column('entity_type', sa.String(50)),
        sa.Column('entity_id', sa.Integer()),
        sa.Column('result', sa.Text()),
        sa.Column('confidence', sa.Float()),
        sa.Column('model_used', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('risk_scores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('factors', sa.Text()),
        sa.Column('calculated_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('crime_forecasts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('district_id', sa.Integer()),
        sa.Column('period', sa.String(20)),
        sa.Column('predicted_count', sa.Integer()),
        sa.Column('actual_count', sa.Integer()),
        sa.Column('confidence', sa.Float()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Audit
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer()),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('entity_type', sa.String(50)),
        sa.Column('entity_id', sa.Integer()),
        sa.Column('details', sa.Text()),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('ai_decisions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('decision', sa.Text(), nullable=False),
        sa.Column('reasoning', sa.Text()),
        sa.Column('confidence', sa.Float()),
        sa.Column('model_used', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('api_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('method', sa.String(10), nullable=False),
        sa.Column('path', sa.String(500), nullable=False),
        sa.Column('status_code', sa.Integer()),
        sa.Column('duration_ms', sa.Float()),
        sa.Column('user_id', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Search
    op.create_table('saved_searches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('query', sa.Text()),
        sa.Column('filters', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('search_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), index=True),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('results_count', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Identity Resolution
    op.create_table('identity_groups',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('group_type', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('identity_matches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('group_id', sa.Integer(), nullable=False, index=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float()),
        sa.Column('match_type', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('entity_aliases',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('alias', sa.String(100), nullable=False),
        sa.Column('alias_type', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Knowledge Graph Metadata
    op.create_table('graph_nodes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('node_id', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('node_type', sa.String(50), nullable=False),
        sa.Column('properties', sa.Text()),
        sa.Column('version', sa.Integer(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('graph_edges',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('source_id', sa.String(50), nullable=False, index=True),
        sa.Column('target_id', sa.String(50), nullable=False, index=True),
        sa.Column('relation', sa.String(50), nullable=False),
        sa.Column('properties', sa.Text()),
        sa.Column('version', sa.Integer(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('graph_versions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('node_count', sa.Integer(), server_default='0'),
        sa.Column('edge_count', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # AI Feedback
    op.create_table('feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), index=True),
        sa.Column('query', sa.Text()),
        sa.Column('response', sa.Text()),
        sa.Column('rating', sa.Integer()),
        sa.Column('comment', sa.Text()),
        sa.Column('tags', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('response_ratings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('query', sa.Text()),
        sa.Column('response', sa.Text()),
        sa.Column('rating', sa.Integer()),
        sa.Column('domain', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('hallucination_reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('response', sa.Text()),
        sa.Column('claim', sa.Text()),
        sa.Column('supported', sa.Boolean()),
        sa.Column('evidence', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Alert Rules
    op.create_table('alert_rules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('rule_type', sa.String(50), nullable=False),
        sa.Column('conditions', sa.Text()),
        sa.Column('actions', sa.Text()),
        sa.Column('is_active', sa.Boolean(), server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('alert_matches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('rule_id', sa.Integer(), nullable=False, index=True),
        sa.Column('entity_type', sa.String(50)),
        sa.Column('entity_id', sa.Integer()),
        sa.Column('match_data', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Officer Intelligence
    op.create_table('case_assignments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('case_id', sa.Integer(), nullable=False, index=True),
        sa.Column('officer_id', sa.Integer(), nullable=False, index=True),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table('recommendations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('recommendation', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Float()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('recommendations')
    op.drop_table('case_assignments')
    op.drop_table('alert_matches')
    op.drop_table('alert_rules')
    op.drop_table('hallucination_reports')
    op.drop_table('response_ratings')
    op.drop_table('feedback')
    op.drop_table('graph_versions')
    op.drop_table('graph_edges')
    op.drop_table('graph_nodes')
    op.drop_table('entity_aliases')
    op.drop_table('identity_matches')
    op.drop_table('identity_groups')
    op.drop_table('search_history')
    op.drop_table('saved_searches')
    op.drop_table('api_logs')
    op.drop_table('ai_decisions')
    op.drop_table('audit_logs')
    op.drop_table('crime_forecasts')
    op.drop_table('risk_scores')
    op.drop_table('predictions')
    op.drop_table('notification_history')
    op.drop_table('notification_preferences')
    op.drop_table('notifications')
    op.drop_table('report_exports')
    op.drop_table('report_templates')
    op.drop_table('reports')
    op.drop_table('conversation_memory')
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
