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
                select(func.count(Crime.id)).where(Crime.district == district.id)
            )).scalar() or 0

            officer_count = (await self.db.execute(
                select(func.count(Officer.id)).where(Officer.district == district.id)
            )).scalar() or 0

            station_count = (await self.db.execute(
                select(func.count(Station.id)).where(Station.district == district.id)
            )).scalar() or 0

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
            select(func.count(Crime.id)).where(Crime.district == district_id)
        )).scalar() or 0

        officer_count = (await self.db.execute(
            select(func.count(Officer.id)).where(Officer.district == district_id)
        )).scalar() or 0

        crimes_by_type = await self.db.execute(
            select(Crime.crime_type, func.count(Crime.id))
            .where(Crime.district == district_id)
            .group_by(Crime.crime_type)
        )

        return {
            "id": district.id,
            "name": district.name,
            "crime_count": crime_count,
            "officer_count": officer_count,
            "crimes_by_type": [
                {"type": row[0] or "unknown", "count": row[1]}
                for row in crimes_by_type.all()
            ],
        }
