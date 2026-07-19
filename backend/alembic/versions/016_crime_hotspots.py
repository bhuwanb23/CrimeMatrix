"""Phase 4: Crime Hotspot Detection — crime_hotspots, location_clusters

Revision ID: 016
Revises: 015
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa

revision = '016'
down_revision = '015'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('crime_hotspots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('hotspot_type', sa.String(50), nullable=False),
        sa.Column('latitude', sa.Float()),
        sa.Column('longitude', sa.Float()),
        sa.Column('radius_km', sa.Float()),
        sa.Column('crime_count', sa.Integer(), server_default='0'),
        sa.Column('dominant_crime_type', sa.String(100)),
        sa.Column('risk_level', sa.String(20), server_default='low'),
        sa.Column('density_score', sa.Float(), server_default='0'),
        sa.Column('trend_direction', sa.String(20)),
        sa.Column('trend_change_pct', sa.Float()),
        sa.Column('district_id', sa.Integer()),
        sa.Column('station_id', sa.Integer()),
        sa.Column('first_detected', sa.DateTime(timezone=True)),
        sa.Column('last_updated', sa.DateTime(timezone=True)),
        sa.Column('status', sa.String(20), server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_hotspots_risk', 'crime_hotspots', ['risk_level'])
    op.create_index('idx_hotspots_district', 'crime_hotspots', ['district_id'])

    op.create_table('location_clusters',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('cluster_type', sa.String(50)),
        sa.Column('center_lat', sa.Float()),
        sa.Column('center_lng', sa.Float()),
        sa.Column('radius_km', sa.Float()),
        sa.Column('member_count', sa.Integer(), server_default='0'),
        sa.Column('avg_crime_count', sa.Float(), server_default='0'),
        sa.Column('cohesion_score', sa.Float(), server_default='0'),
        sa.Column('hotspot_ids', sa.Text()),
        sa.Column('crime_type_ids', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('location_clusters')
    op.drop_table('crime_hotspots')
