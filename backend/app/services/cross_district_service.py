import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.cross_district_match import CrossDistrictMatch
from app.models.match_history_record import MatchHistoryRecord
from app.models.suspect import Suspect
from app.models.vehicle import Vehicle
from app.models.phone import Phone
from app.models.crime import Crime
import structlog
from datetime import datetime

logger = structlog.get_logger()


class CrossDistrictService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_matches(self) -> dict:
        matches_found = 0

        # 1. Match suspects across districts
        suspect_matches = await self._match_suspects()
        matches_found += len(suspect_matches)

        # 2. Match vehicles across districts
        vehicle_matches = await self._match_vehicles()
        matches_found += len(vehicle_matches)

        # 3. Match phones across districts
        phone_matches = await self._match_phones()
        matches_found += len(phone_matches)

        return {"matches_found": matches_found, "suspect_matches": len(suspect_matches),
                "vehicle_matches": len(vehicle_matches), "phone_matches": len(phone_matches)}

    async def get_matches(self, match_type: str = None) -> List[dict]:
        stmt = select(CrossDistrictMatch)
        if match_type:
            stmt = stmt.where(CrossDistrictMatch.match_type == match_type)
        stmt = stmt.order_by(CrossDistrictMatch.confidence.desc())
        result = await self.db.execute(stmt)
        return [self._match_to_dict(m) for m in result.scalars().all()]

    async def get_match(self, match_id: int) -> Optional[dict]:
        stmt = select(CrossDistrictMatch).where(CrossDistrictMatch.id == match_id)
        result = await self.db.execute(stmt)
        m = result.scalar()
        return self._match_to_dict(m) if m else None

    async def compare_districts(self, district1: str, district2: str) -> dict:
        stmt = select(CrossDistrictMatch).where(
            CrossDistrictMatch.district_1 == district1,
            CrossDistrictMatch.district_2 == district2,
        )
        result = await self.db.execute(stmt)
        matches = [self._match_to_dict(m) for m in result.scalars().all()]

        return {"district_1": district1, "district_2": district2,
                "matches": matches, "total": len(matches)}

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(CrossDistrictMatch.id)))).scalar() or 0
        by_type = {}
        stmt = select(CrossDistrictMatch.match_type, sql_func.count(CrossDistrictMatch.id)).group_by(CrossDistrictMatch.match_type)
        result = await self.db.execute(stmt)
        for row in result.all():
            by_type[row[0]] = row[1]
        return {"total_matches": total, "by_type": by_type}

    async def _match_suspects(self) -> List[dict]:
        stmt = select(Suspect)
        result = await self.db.execute(stmt)
        suspects = result.scalars().all()

        matches = []
        by_name = defaultdict(list)
        for s in suspects:
            if s.name:
                by_name[s.name.lower()].append(s)

        for name, group in by_name.items():
            if len(group) > 1:
                districts = set(s.district for s in group if s.district)
                if len(districts) > 1:
                    for i in range(len(group)):
                        for j in range(i + 1, len(group)):
                            match = CrossDistrictMatch(
                                match_type="suspect",
                                entity_id_1=group[i].id, entity_type_1="suspect",
                                district_1=group[i].district or "",
                                entity_id_2=group[j].id, entity_type_2="suspect",
                                district_2=group[j].district or "",
                                confidence=80,
                                match_reason=f"Same suspect name '{name}' across districts",
                            )
                            self.db.add(match)
                            matches.append(match)

        await self.db.commit()
        return matches

    async def _match_vehicles(self) -> List[dict]:
        stmt = select(Vehicle)
        result = await self.db.execute(stmt)
        vehicles = result.scalars().all()

        matches = []
        by_reg = defaultdict(list)
        for v in vehicles:
            if v.registration_number:
                by_reg[v.registration_number.upper()].append(v)

        for reg, group in by_reg.items():
            if len(group) > 1:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        match = CrossDistrictMatch(
                            match_type="vehicle",
                            entity_id_1=group[i].id, entity_type_1="vehicle",
                            district_1="",
                            entity_id_2=group[j].id, entity_type_2="vehicle",
                            district_2="",
                            confidence=90,
                            match_reason=f"Same vehicle registration: {reg}",
                        )
                        self.db.add(match)
                        matches.append(match)

        await self.db.commit()
        return matches

    async def _match_phones(self) -> List[dict]:
        stmt = select(Phone)
        result = await self.db.execute(stmt)
        phones = result.scalars().all()

        matches = []
        by_number = defaultdict(list)
        for p in phones:
            if p.number:
                by_number[p.number.strip()].append(p)

        for number, group in by_number.items():
            if len(group) > 1:
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        match = CrossDistrictMatch(
                            match_type="phone",
                            entity_id_1=group[i].id, entity_type_1="phone",
                            district_1="",
                            entity_id_2=group[j].id, entity_type_2="phone",
                            district_2="",
                            confidence=95,
                            match_reason=f"Same phone number: {number}",
                        )
                        self.db.add(match)
                        matches.append(match)

        await self.db.commit()
        return matches

    def _match_to_dict(self, m: CrossDistrictMatch) -> dict:
        return {
            "id": m.id, "match_type": m.match_type,
            "entity_id_1": m.entity_id_1, "entity_type_1": m.entity_type_1, "district_1": m.district_1,
            "entity_id_2": m.entity_id_2, "entity_type_2": m.entity_type_2, "district_2": m.district_2,
            "confidence": m.confidence, "match_reason": m.match_reason, "status": m.status,
            "created_at": str(m.created_at) if m.created_at else None,
        }
