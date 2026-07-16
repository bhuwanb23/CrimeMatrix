from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.crime import Crime
from app.models.person import Person
from app.models.criminal import Criminal
from app.models.victim import Victim
from app.models.witness import Witness
from app.models.officer import Officer
from app.models.station import Station
from app.models.district import District
from app.models.vehicle import Vehicle
from app.models.phone import Phone
from app.models.location import Location
from app.models.crimetype import CrimeType
import structlog

logger = structlog.get_logger()

ENTITY_MAP = {
    "crimes": Crime,
    "persons": Person,
    "criminals": Criminal,
    "victims": Victim,
    "witnesses": Witness,
    "officers": Officer,
    "stations": Station,
    "districts": District,
    "vehicles": Vehicle,
    "phones": Phone,
    "locations": Location,
    "crime_types": CrimeType,
}


class AggregationEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def aggregate(self, entity: str, group_by: str, metric: str = "count") -> dict:
        model = ENTITY_MAP.get(entity)
        if not model:
            return {"error": f"Unknown entity: {entity}"}

        if not hasattr(model, group_by):
            return {"error": f"Field '{group_by}' not found on {entity}"}

        column = getattr(model, group_by)

        if metric == "count":
            query = select(column, func.count(model.id)).group_by(column)
        elif metric == "sum" and hasattr(model, group_by):
            query = select(column, func.count(model.id)).group_by(column)
        else:
            query = select(column, func.count(model.id)).group_by(column)

        result = await self.db.execute(query)
        rows = result.all()

        return {
            "entity": entity,
            "group_by": group_by,
            "metric": metric,
            "data": [{"key": str(row[0]) if row[0] else "unknown", "value": row[1]} for row in rows],
        }
