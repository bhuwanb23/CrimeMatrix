from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.crime import Crime
from app.models.district import District
from app.models.crimetype import CrimeType
import structlog

logger = structlog.get_logger()


class HeatmapEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def district_heatmap(self) -> dict:
        districts_result = await self.db.execute(select(District.id, District.name))
        districts = {row[0]: row[1] for row in districts_result.all()}

        crime_types_result = await self.db.execute(select(CrimeType.id, CrimeType.name))
        crime_types = {row[0]: row[1] for row in crime_types_result.all()}

        matrix = {}
        for ct_id, ct_name in crime_types.items():
            matrix[ct_name] = {}
            for did, dname in districts.items():
                count_result = await self.db.execute(
                    select(func.count(Crime.id)).where(
                        Crime.crime_type_id == ct_id,
                        Crime.district_id == did
                    )
                )
                count = count_result.scalar() or 0
                if count > 0:
                    matrix[ct_name][dname] = count

        if not districts:
            crimes = await self.db.execute(
                select(Crime.district_id, Crime.crime_type_id, func.count(Crime.id))
                .group_by(Crime.district_id, Crime.crime_type_id)
            )
            for did, ctid, count in crimes.all():
                dname = str(did) if did else "Unknown"
                ctname = str(ctid) if ctid else "Unknown"
                if ctname not in matrix:
                    matrix[ctname] = {}
                matrix[ctname][dname] = count

        return {
            "districts": list(districts.values()),
            "crime_types": list(crime_types.values()),
            "matrix": matrix,
        }

    async def timeline_heatmap(self) -> dict:
        crimes = await self.db.execute(
            select(Crime.district_id, Crime.created_at, func.count(Crime.id))
            .group_by(Crime.district_id, Crime.created_at)
        )

        timeline = {}
        for district_id, created_at, count in crimes.all():
            district_name = str(district_id) if district_id else "Unknown"
            date_key = str(created_at)[:7] if created_at else "unknown"
            if district_name not in timeline:
                timeline[district_name] = {}
            timeline[district_name][date_key] = count

        return {"timeline": timeline}
