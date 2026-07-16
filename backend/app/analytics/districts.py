from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.district import District
from app.models.crime import Crime
from app.models.officer import Officer
from app.models.station import Station
import structlog

logger = structlog.get_logger()


class DistrictAnalytics:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_districts(self) -> list:
        districts = await self.db.execute(select(District))
        result = []

        for district in districts.scalars().all():
            crime_count = (await self.db.execute(
                select(func.count(Crime.id)).where(Crime.district_id == district.id)
            )).scalar() or 0

            station_ids_q = await self.db.execute(
                select(Station.id).where(Station.district_id == district.id)
            )
            station_ids = [r[0] for r in station_ids_q.all()]

            officer_count = 0
            if station_ids:
                officer_count = (await self.db.execute(
                    select(func.count(Officer.id)).where(Officer.station_id.in_(station_ids))
                )).scalar() or 0

            station_count = len(station_ids)

            result.append({
                "id": district.id,
                "name": district.name,
                "crime_count": crime_count,
                "officer_count": officer_count,
                "station_count": station_count,
            })

        return result

    async def get_district_detail(self, district_id: int) -> dict:
        district = (await self.db.execute(
            select(District).where(District.id == district_id)
        )).scalar_one_or_none()

        if not district:
            return {"error": "District not found"}

        crime_count = (await self.db.execute(
            select(func.count(Crime.id)).where(Crime.district_id == district_id)
        )).scalar() or 0

        station_ids_q = await self.db.execute(
            select(Station.id).where(Station.district_id == district_id)
        )
        station_ids = [r[0] for r in station_ids_q.all()]
        station_count = len(station_ids)

        officer_count = 0
        if station_ids:
            officer_count = (await self.db.execute(
                select(func.count(Officer.id)).where(Officer.station_id.in_(station_ids))
            )).scalar() or 0

        open_count = (await self.db.execute(
            select(func.count(Crime.id)).where(
                Crime.district_id == district_id, Crime.status == "open"
            )
        )).scalar() or 0

        closed_count = (await self.db.execute(
            select(func.count(Crime.id)).where(
                Crime.district_id == district_id, Crime.status == "closed"
            )
        )).scalar() or 0

        return {
            "id": district.id,
            "name": district.name,
            "crime_count": crime_count,
            "officer_count": officer_count,
            "station_count": station_count,
            "open_crimes": open_count,
            "closed_crimes": closed_count,
            "resolution_rate": round((closed_count / crime_count * 100), 1) if crime_count else 0,
        }
