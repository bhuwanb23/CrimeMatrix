import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime import Crime
from app.models.district import District
from app.models.crimetype import CrimeType
from app.models.crime_hotspot import CrimeHotspot
from app.models.location_cluster import LocationCluster
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()

RISK_THRESHOLDS = {"critical": 20, "high": 10, "medium": 5, "low": 0}


class HotspotService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_hotspots(self) -> dict:
        stmt = select(Crime)
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()

        if not crimes:
            return {"hotspots_found": 0, "message": "No crimes to analyze"}

        crime_dicts = []
        for c in crimes:
            crime_dicts.append({
                "id": c.id,
                "district_id": c.district_id,
                "crime_type_id": c.crime_type_id,
                "created_at": c.created_at,
            })

        district_groups = defaultdict(list)
        for c in crime_dicts:
            did = c.get("district_id")
            if did:
                district_groups[did].append(c)

        saved_count = 0
        for district_id, group_crimes in district_groups.items():
            if len(group_crimes) < 3:
                continue

            district = await self._load_district(district_id)
            crime_types = defaultdict(int)
            for c in group_crimes:
                crime_types[c.get("crime_type_id")] += 1
            dominant_type = max(crime_types, key=crime_types.get) if crime_types else None

            count = len(group_crimes)
            risk_level = "critical" if count > 20 else "high" if count > 10 else "medium" if count > 5 else "low"
            density = count / max(1, 1)

            existing = await self._hotspot_exists(district_id)
            if existing:
                existing.crime_count = count
                existing.risk_level = risk_level
                existing.density_score = density
                existing.last_updated = datetime.utcnow()
            else:
                hotspot = CrimeHotspot(
                    name=f"Hotspot: {district.get('name', f'District #{district_id}')}" if district else f"Hotspot: District #{district_id}",
                    description=f"{count} crimes detected in {district.get('name', f'District #{district_id}')}" if district else f"{count} crimes",
                    hotspot_type="district",
                    crime_count=count,
                    dominant_crime_type=str(dominant_type) if dominant_type else None,
                    risk_level=risk_level,
                    density_score=density,
                    district_id=district_id,
                    first_detected=datetime.utcnow(),
                    last_updated=datetime.utcnow(),
                )
                self.db.add(hotspot)
                saved_count += 1

        await self.db.commit()

        return {
            "hotspots_found": len(district_groups),
            "hotspots_saved": saved_count,
            "total_crimes_analyzed": len(crime_dicts),
        }

    async def get_hotspots(self, risk_level: str = None, hotspot_type: str = None) -> List[dict]:
        stmt = select(CrimeHotspot).where(CrimeHotspot.status == "active")
        if risk_level:
            stmt = stmt.where(CrimeHotspot.risk_level == risk_level)
        if hotspot_type:
            stmt = stmt.where(CrimeHotspot.hotspot_type == hotspot_type)
        stmt = stmt.order_by(CrimeHotspot.crime_count.desc())
        result = await self.db.execute(stmt)
        return [self._hotspot_to_dict(h) for h in result.scalars().all()]

    async def get_hotspot(self, hotspot_id: int) -> Optional[dict]:
        stmt = select(CrimeHotspot).where(CrimeHotspot.id == hotspot_id)
        result = await self.db.execute(stmt)
        h = result.scalar()
        return self._hotspot_to_dict(h) if h else None

    async def get_rankings(self, limit: int = 10) -> List[dict]:
        stmt = (
            select(CrimeHotspot)
            .where(CrimeHotspot.status == "active")
            .order_by(CrimeHotspot.crime_count.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return [self._hotspot_to_dict(h) for h in result.scalars().all()]

    async def get_risk_map(self) -> dict:
        hotspots = await self.get_hotspots()
        risk_zones = {"critical": [], "high": [], "medium": [], "low": []}
        for h in hotspots:
            level = h.get("risk_level", "low")
            if level in risk_zones:
                risk_zones[level].append(h)
        return {"risk_zones": risk_zones, "total": len(hotspots)}

    async def get_density(self, district_id: int) -> dict:
        stmt = select(Crime).where(Crime.district_id == district_id)
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()

        type_counts = defaultdict(int)
        for c in crimes:
            type_counts[c.crime_type_id] += 1

        types = []
        for ct_id, count in type_counts.items():
            ct_name = f"Type #{ct_id}"
            if ct_id:
                ct_result = await self.db.execute(select(CrimeType.name).where(CrimeType.id == ct_id))
                name = ct_result.scalar()
                if name:
                    ct_name = name
            types.append({"crime_type": ct_name, "count": count})

        types.sort(key=lambda x: x["count"], reverse=True)
        district = await self._load_district(district_id)

        return {
            "district": district,
            "total_crimes": len(crimes),
            "crime_types": types,
            "density_score": len(crimes),
        }

    async def get_clusters(self) -> List[dict]:
        stmt = select(LocationCluster).order_by(LocationCluster.cohesion_score.desc())
        result = await self.db.execute(stmt)
        return [self._cluster_to_dict(c) for c in result.scalars().all()]

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(CrimeHotspot.id)))).scalar() or 0
        critical = (await self.db.execute(
            select(sql_func.count(CrimeHotspot.id)).where(CrimeHotspot.risk_level == "critical")
        )).scalar() or 0
        high = (await self.db.execute(
            select(sql_func.count(CrimeHotspot.id)).where(CrimeHotspot.risk_level == "high")
        )).scalar() or 0
        clusters = (await self.db.execute(select(sql_func.count(LocationCluster.id)))).scalar() or 0
        return {"total_hotspots": total, "critical": critical, "high": high, "total_clusters": clusters}

    async def _hotspot_exists(self, district_id: int) -> Optional[CrimeHotspot]:
        stmt = select(CrimeHotspot).where(
            CrimeHotspot.district_id == district_id,
            CrimeHotspot.status == "active",
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _load_district(self, district_id: int) -> Optional[dict]:
        stmt = select(District).where(District.id == district_id)
        result = await self.db.execute(stmt)
        d = result.scalar()
        return {"id": d.id, "name": d.name} if d else None

    def _hotspot_to_dict(self, h: CrimeHotspot) -> dict:
        return {
            "id": h.id, "name": h.name, "description": h.description,
            "hotspot_type": h.hotspot_type, "latitude": h.latitude, "longitude": h.longitude,
            "radius_km": h.radius_km, "crime_count": h.crime_count,
            "dominant_crime_type": h.dominant_crime_type, "risk_level": h.risk_level,
            "density_score": h.density_score, "trend_direction": h.trend_direction,
            "trend_change_pct": h.trend_change_pct, "district_id": h.district_id,
            "status": h.status,
            "created_at": str(h.created_at) if h.created_at else None,
            "last_updated": str(h.last_updated) if h.last_updated else None,
        }

    def _cluster_to_dict(self, c: LocationCluster) -> dict:
        return {
            "id": c.id, "name": c.name, "description": c.description,
            "cluster_type": c.cluster_type, "center_lat": c.center_lat,
            "center_lng": c.center_lng, "radius_km": c.radius_km,
            "member_count": c.member_count, "avg_crime_count": c.avg_crime_count,
            "cohesion_score": c.cohesion_score,
            "hotspot_ids": json.loads(c.hotspot_ids) if c.hotspot_ids else [],
        }
