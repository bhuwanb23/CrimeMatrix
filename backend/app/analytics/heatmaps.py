from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from app.models.crime import Crime
from app.models.district import District
import structlog

logger = structlog.get_logger()


class HeatmapEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def district_heatmap(self) -> dict:
        districts_result = await self.db.execute(
            select(District.id, District.name)
        )
        districts = {row[0]: row[1] for row in districts_result.all()}

        crime_types_result = await self.db.execute(
            select(Crime.crime_type).distinct()
        )
        crime_types = [row[0] for row in crime_types_result.all() if row[0]]

        matrix = {}
        for ct in crime_types:
            matrix[ct] = {}
            for did, dname in districts.items():
                count_result = await self.db.execute(
                    select(func.count(Crime.id)).where(
                        Crime.district == did
                    )
                )
                matrix[ct][dname] = count_result.scalar() or 0

        if not districts:
            crimes = await self.db.execute(
                select(Crime.district, Crime.crime_type, func.count(Crime.id))
                .group_by(Crime.district, Crime.crime_type)
            )
            for district, crime_type, count in crimes.all():
                district_name = district or "Unknown"
                ct = crime_type or "Unknown"
                if ct not in matrix:
                    matrix[ct] = {}
                matrix[ct][district_name] = count

        return {
            "districts": list(districts.values()) if districts else [],
            "crime_types": crime_types if crime_types else list(matrix.keys()),
            "matrix": matrix,
        }

    async def timeline_heatmap(self) -> dict:
        crimes = await self.db.execute(
            select(Crime.district, Crime.created_at, func.count(Crime.id))
            .group_by(Crime.district, Crime.created_at)
        )

        timeline = {}
        for district, created_at, count in crimes.all():
            district_name = district or "Unknown"
            date_key = str(created_at)[:7] if created_at else "unknown"
            if district_name not in timeline:
                timeline[district_name] = {}
            timeline[district_name][date_key] = count

        return {"timeline": timeline}
