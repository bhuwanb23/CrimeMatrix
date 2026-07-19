from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime import Crime
from app.models.district import District
from app.models.crimetype import CrimeType
from app.models.station import Station
from app.models.location import Location
from app.models.crime_hotspot import CrimeHotspot
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()

# Karnataka district approximate centers (lat, lng)
DISTRICT_COORDS = {
    "Bengaluru Urban": {"lat": 12.9716, "lng": 77.5946},
    "Bengaluru Rural": {"lat": 13.2500, "lng": 77.7000},
    "Mysuru": {"lat": 12.2958, "lng": 76.6394},
    "Mangaluru": {"lat": 12.9141, "lng": 74.8560},
    "Hubballi-Dharwad": {"lat": 15.3647, "lng": 75.1240},
    "Belagavi": {"lat": 15.8497, "lng": 74.4977},
    "Kalaburagi": {"lat": 17.3297, "lng": 76.8343},
    "Ballari": {"lat": 15.1394, "lng": 76.9214},
    "Vijayapura": {"lat": 16.8302, "lng": 75.7100},
    "Davangere": {"lat": 14.4644, "lng": 75.9218},
    "Shivamogga": {"lat": 13.9299, "lng": 75.5681},
    "Tumakuru": {"lat": 13.3409, "lng": 77.0932},
    "Hassan": {"lat": 12.7878, "lng": 76.0910},
    "Mandya": {"lat": 12.5218, "lng": 76.8953},
    "Chamarajanagar": {"lat": 11.9237, "lng": 76.9391},
    "Kodagu": {"lat": 12.3375, "lng": 75.8069},
    "Uttara Kannada": {"lat": 14.7938, "lng": 74.5315},
    "Dakshina Kannada": {"lat": 12.8590, "lng": 74.8901},
    "Gadag": {"lat": 15.4313, "lng": 75.6265},
    "Koppal": {"lat": 15.3500, "lng": 76.1000},
    "Raichur": {"lat": 16.2120, "lng": 77.3439},
    "Bidar": {"lat": 17.9153, "lng": 77.5260},
    "Chitradurga": {"lat": 14.2262, "lng": 76.3956},
    "Kolar": {"lat": 13.1366, "lng": 78.1292},
    "Chikkaballapur": {"lat": 13.4355, "lng": 77.7273},
    "Ramanagara": {"lat": 12.7224, "lng": 77.2814},
    "Yadgir": {"lat": 16.7703, "lng": 77.1370},
    "Vijayanagara": {"lat": 15.2100, "lng": 76.4600},
}


class MapService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_crime_markers(self, district_id: int = None, crime_type_id: int = None,
                                days: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        query = select(Crime).where(Crime.created_at >= date_from)
        if district_id:
            query = query.where(Crime.district_id == district_id)
        if crime_type_id:
            query = query.where(Crime.crime_type_id == crime_type_id)

        result = await self.db.execute(query)
        crimes = result.scalars().all()

        features = []
        for crime in crimes:
            district_name = await self._get_district_name(crime.district_id)
            coords = DISTRICT_COORDS.get(district_name, {"lat": 12.9716, "lng": 77.5946})
            # Add slight randomness for visualization
            import random
            lat = coords["lat"] + random.uniform(-0.05, 0.05)
            lng = coords["lng"] + random.uniform(-0.05, 0.05)

            crime_type_name = await self._get_crime_type_name(crime.crime_type_id)
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lng, lat]},
                "properties": {
                    "id": crime.id,
                    "title": crime.title,
                    "crime_type": crime_type_name,
                    "district": district_name,
                    "status": crime.status,
                    "priority": crime.priority,
                    "date": str(crime.created_at)[:10] if crime.created_at else None,
                },
            })

        return {
            "type": "FeatureCollection",
            "features": features,
            "count": len(features),
        }

    async def get_district_geojson(self) -> dict:
        stmt = select(District)
        result = await self.db.execute(stmt)
        districts = result.scalars().all()

        features = []
        for d in districts:
            coords = DISTRICT_COORDS.get(d.name, {"lat": 12.9716, "lng": 77.5946})
            crime_count = await self._get_district_crime_count(d.id)

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [coords["lng"], coords["lat"]],
                },
                "properties": {
                    "id": d.id,
                    "name": d.name,
                    "code": d.code,
                    "population": d.population,
                    "area_sq_km": d.area_sq_km,
                    "crime_count": crime_count,
                    "risk_level": "high" if crime_count > 20 else "medium" if crime_count > 10 else "low",
                },
            })

        return {"type": "FeatureCollection", "features": features}

    async def get_heatmap_data(self, days: int = 30) -> dict:
        date_from = datetime.utcnow() - timedelta(days=days)
        stmt = select(Crime.district_id, sql_func.count(Crime.id)).where(Crime.created_at >= date_from)
        stmt = stmt.group_by(Crime.district_id)
        result = await self.db.execute(stmt)
        rows = result.all()

        points = []
        for district_id, count in rows:
            district_name = await self._get_district_name(district_id)
            coords = DISTRICT_COORDS.get(district_name, {"lat": 12.9716, "lng": 77.5946})
            points.append({
                "lat": coords["lat"],
                "lng": coords["lng"],
                "intensity": count,
                "district": district_name,
                "count": count,
            })

        return {"points": points, "total": sum(p["count"] for p in points)}

    async def get_hotspot_markers(self) -> dict:
        stmt = select(CrimeHotspot).where(CrimeHotspot.status == "active")
        result = await self.db.execute(stmt)
        hotspots = result.scalars().all()

        features = []
        for h in hotspots:
            district_name = await self._get_district_name(h.district_id)
            coords = DISTRICT_COORDS.get(district_name, {"lat": 12.9716, "lng": 77.5946})

            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [coords["lng"], coords["lat"]]},
                "properties": {
                    "id": h.id,
                    "name": h.name,
                    "risk_level": h.risk_level,
                    "crime_count": h.crime_count,
                    "dominant_type": h.dominant_crime_type,
                    "district": district_name,
                },
            })

        return {"type": "FeatureCollection", "features": features}

    async def get_station_markers(self) -> dict:
        stmt = select(Station)
        result = await self.db.execute(stmt)
        stations = result.scalars().all()

        features = []
        for s in stations:
            district_name = await self._get_district_name(s.district_id)
            coords = DISTRICT_COORDS.get(district_name, {"lat": 12.9716, "lng": 77.5946})
            import random
            lat = coords["lat"] + random.uniform(-0.03, 0.03)
            lng = coords["lng"] + random.uniform(-0.03, 0.03)

            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lng, lat]},
                "properties": {
                    "id": s.id,
                    "name": s.name,
                    "code": s.code,
                    "district": district_name,
                    "type": s.type,
                },
            })

        return {"type": "FeatureCollection", "features": features}

    async def get_route_data(self) -> dict:
        stmt = select(CrimeHotspot).where(CrimeHotspot.status == "active").limit(10)
        result = await self.db.execute(stmt)
        hotspots = result.scalars().all()

        routes = []
        hotspot_list = list(hotspots)
        for i in range(len(hotspot_list) - 1):
            h1 = hotspot_list[i]
            h2 = hotspot_list[i + 1]
            d1 = await self._get_district_name(h1.district_id)
            d2 = await self._get_district_name(h2.district_id)
            c1 = DISTRICT_COORDS.get(d1, {"lat": 12.9716, "lng": 77.5946})
            c2 = DISTRICT_COORDS.get(d2, {"lat": 12.9716, "lng": 77.5946})

            routes.append({
                "from": {"name": h1.name, "lat": c1["lat"], "lng": c1["lng"]},
                "to": {"name": h2.name, "lat": c2["lat"], "lng": c2["lng"]},
                "type": "suspect-movement" if i % 2 == 0 else "evidence-link",
                "label": f"{h1.name} → {h2.name}",
            })

        return {"routes": routes}

    async def get_spatial_stats(self) -> dict:
        total_crimes = (await self.db.execute(select(sql_func.count(Crime.id)))).scalar() or 0
        total_districts = (await self.db.execute(select(sql_func.count(District.id)))).scalar() or 0
        total_stations = (await self.db.execute(select(sql_func.count(Station.id)))).scalar() or 0
        total_hotspots = (await self.db.execute(
            select(sql_func.count(CrimeHotspot.id)).where(CrimeHotspot.status == "active")
        )).scalar() or 0

        return {
            "total_crimes": total_crimes,
            "total_districts": total_districts,
            "total_stations": total_stations,
            "total_hotspots": total_hotspots,
        }

    async def _get_district_name(self, district_id: int) -> Optional[str]:
        if not district_id:
            return None
        stmt = select(District.name).where(District.id == district_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _get_crime_type_name(self, crime_type_id: int) -> Optional[str]:
        if not crime_type_id:
            return None
        stmt = select(CrimeType.name).where(CrimeType.id == crime_type_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _get_district_crime_count(self, district_id: int) -> int:
        stmt = select(sql_func.count(Crime.id)).where(Crime.district_id == district_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0
