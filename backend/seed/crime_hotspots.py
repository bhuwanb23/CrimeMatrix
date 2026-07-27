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
    ("Commercial Street Retail", "Pickpocket and phone theft density", "theft", 12.9833, 77.6089, 0.8, 22, "Theft", "high", "BLR-U", "BLR-SJ"),
    ("MG Road Nightlife", "Robbery and snatching after dark", "robbery", 12.9758, 77.6063, 1.0, 14, "Robbery", "high", "BLR-U", "BLR-CP"),
    ("Hubballi Bus Depot", "Depot-area robbery and theft", "robbery", 15.3647, 75.1240, 1.4, 10, "Robbery", "medium", "HUB", "HUB-E"),
    ("Indiranagar Pub Street", "Assault and vehicle theft weekends", "assault", 12.9784, 77.6408, 1.1, 11, "Assault", "medium", "BLR-U", "BLR-IN"),
    ("Kalaburagi Rural Belt", "Land-dispute violence cluster", "murder", 17.3297, 76.8343, 4.0, 6, "Murder", "high", "KLB", "KLB-C"),
    ("Ballari Mining Corridor", "Vehicle theft and extortion signals", "vehicle_theft", 15.1394, 76.9214, 3.5, 8, "Vehicle Theft", "medium", "BLY", "BLY-T"),
    ("Shivamogga Temple Circuit", "Temple property crime risk", "arson", 13.9299, 75.5681, 2.2, 5, "Arson", "medium", "SHV", "SHV-R"),
    ("Mandya Highway Stretch", "NDPS transit corridor", "drugs", 12.5218, 76.8951, 5.0, 9, "Drug Offense", "high", "MDY", None),
    ("Kolar Night Corridor", "Hit-and-run density after midnight", "hit_and_run", 13.1360, 78.1290, 3.0, 7, "Hit and Run", "high", "KLR", None),
    ("Ramanagara Market", "Extortion and cheating complaints", "extortion", 12.7209, 77.2813, 1.8, 8, "Extortion", "medium", "RMR", None),
]


async def seed(db) -> int:
    n = 0
    for name, desc, htype, lat, lng, radius, count, dominant, risk, dcode, scode in ROWS:
        district = await get_one(db, District, code=dcode)
        station = await get_one(db, Station, code=scode) if scode else None
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
