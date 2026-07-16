from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.crime import Crime
from app.models.person import Person
from app.models.officer import Officer
from app.models.station import Station
from app.models.district import District
from app.models.criminal import Criminal
from app.models.victim import Victim
from app.models.witness import Witness
import structlog

logger = structlog.get_logger()


class StatisticsEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_overview(self) -> dict:
        crime_count = (await self.db.execute(select(func.count(Crime.id)))).scalar() or 0
        person_count = (await self.db.execute(select(func.count(Person.id)))).scalar() or 0
        officer_count = (await self.db.execute(select(func.count(Officer.id)))).scalar() or 0
        station_count = (await self.db.execute(select(func.count(Station.id)))).scalar() or 0
        district_count = (await self.db.execute(select(func.count(District.id)))).scalar() or 0
        criminal_count = (await self.db.execute(select(func.count(Criminal.id)))).scalar() or 0
        victim_count = (await self.db.execute(select(func.count(Victim.id)))).scalar() or 0
        witness_count = (await self.db.execute(select(func.count(Witness.id)))).scalar() or 0

        open_count = (await self.db.execute(
            select(func.count(Crime.id)).where(Crime.status == "open")
        )).scalar() or 0
        closed_count = (await self.db.execute(
            select(func.count(Crime.id)).where(Crime.status == "closed")
        )).scalar() or 0

        return {
            "total_crimes": crime_count,
            "total_persons": person_count,
            "total_officers": officer_count,
            "total_stations": station_count,
            "total_districts": district_count,
            "total_criminals": criminal_count,
            "total_victims": victim_count,
            "total_witnesses": witness_count,
            "open_crimes": open_count,
            "closed_crimes": closed_count,
            "resolution_rate": round((closed_count / crime_count * 100), 1) if crime_count else 0,
        }

    async def get_summary(self) -> dict:
        return await self.get_overview()
