from seed.data import CRIMES, CRIME_TYPES, DISTRICTS, STATIONS
from seed.utils import get_one
from app.models.fir import FIR


def _station_for_district(district_idx: int) -> str:
    district_code = DISTRICTS[district_idx][1]
    for name, _code, dcode in STATIONS:
        if dcode == district_code:
            return name
    return "Cubbon Park PS"


async def seed(db) -> int:
    n = 0
    for i, row in enumerate(CRIMES, start=1):
        fir_number = f"FIR/{i:04d}/2026"
        existing = await get_one(db, FIR, fir_number=fir_number)
        if existing:
            continue
        crime_type_name = CRIME_TYPES[row["type_idx"]][0]
        district_name = DISTRICTS[row["district_idx"]][0]
        db.add(FIR(
            id=i,  # align with crime ids on fresh DB
            fir_number=fir_number,
            title=row["title"],
            description=row["desc"],
            crime_type=crime_type_name,
            district=district_name,
            station=_station_for_district(row["district_idx"]),
            status="filed",
            complainant_name=f"Complainant {i}",
            complainant_phone=f"98450{i:05d}",
        ))
        n += 1
    await db.flush()
    return n
