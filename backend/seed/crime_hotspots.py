from seed.utils import ensure, get_one
from app.models.crime_hotspot import CrimeHotspot
from app.models.district import District
from app.models.station import Station

ROWS = [
    ("Majestic Transit Hub", "Snatching and theft cluster", "snatching", 12.9774, 77.5709, 1.2, 28, "Snatching", "critical", "BLR-U", "BLR-CP"),
    ("Koramangala Nightlife", "Burglary and assault weekend spike", "burglary", 12.9352, 77.6245, 1.5, 16, "Burglary", "high", "BLR-U", "BLR-KM"),
    ("Whitefield Industrial", "Vehicle theft near IT campuses", "vehicle_theft", 12.9850, 77.7324, 2.0, 12, "Vehicle Theft", "medium", "BLR-U", "BLR-WF"),
    ("Mysuru Palace Tourist Belt", "Tourist-targeted theft", "theft", 12.3051, 76.6551, 1.0, 9, "Theft", "medium", "MYS", "MYS-NZ"),
    ("Mangaluru Port Zone", "NDPS and smuggling signals", "drugs", 12.9285, 74.8050, 3.0, 7, "Drug Offense", "high", "MNG", "MNG-S"),
]


async def seed(db) -> int:
    n = 0
    for name, desc, htype, lat, lng, radius, count, dominant, risk, dcode, scode in ROWS:
        district = await get_one(db, District, code=dcode)
        station = await get_one(db, Station, code=scode)
        _, created = await ensure(
            db, CrimeHotspot,
            unique={"name": name},
            defaults={
                "description": desc,
                "hotspot_type": htype,
                "latitude": lat,
                "longitude": lng,
                "radius_km": radius,
                "crime_count": count,
                "dominant_crime_type": dominant,
                "risk_level": risk,
                "density_score": float(count) / radius,
                "trend_direction": "up",
                "trend_change_pct": 12.5,
                "district_id": district.id if district else None,
                "station_id": station.id if station else None,
                "status": "active",
            },
        )
        n += int(created)
    return n
