"""Shared demo fixtures used across crime / case / people seeds."""

DISTRICTS = [
    ("Bengaluru Urban", "BLR-U"),
    ("Bengaluru Rural", "BLR-R"),
    ("Mysuru", "MYS"),
    ("Mangaluru", "MNG"),
    ("Hubballi-Dharwad", "HUB"),
    ("Kalaburagi", "KLB"),
    ("Ballari", "BLY"),
    ("Vijayapura", "VJP"),
    ("Shivamogga", "SHV"),
    ("Davangere", "DVG"),
    ("Hassan", "HSM"),
    ("Mandya", "MDY"),
    ("Tumakuru", "TMK"),
    ("Kolar", "KLR"),
    ("Chikkaballapur", "CKB"),
    ("Ramanagara", "RMR"),
]

CRIME_TYPES = [
    ("Theft", "THR", 2),
    ("Robbery", "ROB", 3),
    ("Burglary", "BRG", 3),
    ("Murder", "MUR", 5),
    ("Assault", "ASL", 3),
    ("Fraud", "FRD", 2),
    ("Cybercrime", "CYB", 2),
    ("Kidnapping", "KID", 5),
    ("Drug Offense", "DRG", 3),
    ("Domestic Violence", "DV", 3),
    ("Hit and Run", "H&R", 3),
    ("Vehicle Theft", "VT", 2),
    ("Snatching", "SNCH", 3),
    ("Extortion", "EXT", 3),
    ("Forgery", "FRG", 2),
    ("Cheating", "CHT", 2),
    ("Arson", "ARS", 4),
    ("Rape", "RPE", 5),
]

STATIONS = [
    # (name, code, district_code)
    ("Cubbon Park PS", "BLR-CP", "BLR-U"),
    ("Shivajinagar PS", "BLR-SJ", "BLR-U"),
    ("Koramangala PS", "BLR-KM", "BLR-U"),
    ("Indiranagar PS", "BLR-IN", "BLR-U"),
    ("Whitefield PS", "BLR-WF", "BLR-U"),
    ("Nazarbad PS", "MYS-NZ", "MYS"),
    ("Vani Vilas Mohalla PS", "MYS-VV", "MYS"),
    ("Mangalore South PS", "MNG-S", "MNG"),
    ("Mangalore North PS", "MNG-N", "MNG"),
    ("Hubballi East PS", "HUB-E", "HUB"),
    ("Dharwad North PS", "HUB-DN", "HUB"),
    ("Kalaburagi Central PS", "KLB-C", "KLB"),
    ("Ballari Town PS", "BLY-T", "BLY"),
    ("Shivamogga Rural PS", "SHV-R", "SHV"),
]

LOCATIONS = [
    # (name, address, lat, lng, district_code, type)
    ("MG Road", "MG Road, Bengaluru", 12.9758, 77.6063, "BLR-U", "commercial"),
    ("Majestic Bus Stand", "Kempegowda Bus Station", 12.9774, 77.5709, "BLR-U", "transit"),
    ("Commercial Street", "Commercial Street, Bengaluru", 12.9833, 77.6089, "BLR-U", "commercial"),
    ("Koramangala 5th Block", "Koramangala, Bengaluru", 12.9352, 77.6245, "BLR-U", "residential"),
    ("Whitefield ITPL", "ITPL Road, Whitefield", 12.9850, 77.7324, "BLR-U", "commercial"),
    ("Mysuru Palace Area", "Sayyaji Rao Road, Mysuru", 12.3051, 76.6551, "MYS", "tourist"),
    ("Mangaluru Port", "New Mangalore Port", 12.9285, 74.8050, "MNG", "industrial"),
    ("Hubballi Bus Depot", "CBT Hubballi", 15.3647, 75.1240, "HUB", "transit"),
]

# type_idx / district_idx index into CRIME_TYPES / DISTRICTS
CRIMES = [
    {"title": "Armed robbery at jewelry store on MG Road", "desc": "Two suspects entered the store at 2:30 AM, threatened staff with knives, and stole gold jewelry worth Rs 15 lakhs. CCTV captured the incident.", "type_idx": 1, "district_idx": 0, "status": "open", "priority": "high", "location_idx": 0},
    {"title": "Chain snatching near Majestic Bus Stand", "desc": "Victim's gold chain snatched by two persons on a motorcycle. Incident occurred at 6:30 PM during rush hour.", "type_idx": 12, "district_idx": 0, "status": "open", "priority": "high", "location_idx": 1},
    {"title": "Mobile theft at Commercial Street", "desc": "iPhone 15 Pro stolen from victim's pocket while shopping. Suspect caught on nearby CCTV.", "type_idx": 0, "district_idx": 0, "status": "active", "priority": "medium", "location_idx": 2},
    {"title": "Burglary at Koramangala apartment", "desc": "House broken into through rear window. Laptop and gold chain stolen. No fingerprints found.", "type_idx": 2, "district_idx": 0, "status": "open", "priority": "medium", "location_idx": 3},
    {"title": "Murder case in Whitefield", "desc": "Body found in abandoned building. Victim identified as daily wage worker. Multiple stab wounds.", "type_idx": 3, "district_idx": 0, "status": "active", "priority": "high", "location_idx": 4},
    {"title": "Cyber fraud targeting senior citizens", "desc": "Multiple complaints of online banking fraud. Scammers posing as bank officials. Loss of Rs 8 lakhs.", "type_idx": 6, "district_idx": 0, "status": "active", "priority": "high", "location_idx": 0},
    {"title": "Drug seizure at bus stand", "desc": "1.5 kg of ganja seized from a passenger. Suspect arrested and remanded.", "type_idx": 8, "district_idx": 0, "status": "closed", "priority": "medium", "location_idx": 1},
    {"title": "Assault on traffic police", "desc": "Auto driver assaulted traffic constable during checking. Multiple witnesses.", "type_idx": 4, "district_idx": 0, "status": "closed", "priority": "medium", "location_idx": 1},
    {"title": "Vehicle theft from parking lot", "desc": "Honda City stolen from mall parking. GPS tracked vehicle toward Tamil Nadu border.", "type_idx": 11, "district_idx": 0, "status": "active", "priority": "high", "location_idx": 3},
    {"title": "Domestic violence complaint", "desc": "Wife filed complaint against husband for repeated assault. Medical report confirms injuries.", "type_idx": 9, "district_idx": 0, "status": "active", "priority": "medium", "location_idx": 3},
    {"title": "Hit and run near Hebbal flyover", "desc": "Pedestrian hit by speeding car. Driver fled. CCTV shows white sedan.", "type_idx": 10, "district_idx": 0, "status": "open", "priority": "high", "location_idx": 0},
    {"title": "Snatching at Forum Mall", "desc": "Woman's purse snatched by two persons on bike. Cash and cards stolen.", "type_idx": 12, "district_idx": 0, "status": "open", "priority": "medium", "location_idx": 3},
    {"title": "Extortion call to businessman", "desc": "Threatening call demanding Rs 10 lakhs. Caller claimed to be from organized crime group.", "type_idx": 13, "district_idx": 0, "status": "active", "priority": "high", "location_idx": 0},
    {"title": "Forgery of property documents", "desc": "Fake sale deed created for ancestral property. Multiple families affected.", "type_idx": 14, "district_idx": 0, "status": "open", "priority": "medium", "location_idx": 2},
    {"title": "Cheating in online job portal", "desc": "Multiple victims cheated of registration fees. Fake company operating from rented office.", "type_idx": 15, "district_idx": 0, "status": "active", "priority": "medium", "location_idx": 2},
    {"title": "Burglary at electronics shop", "desc": "Shop broken into at night. Laptops and phones worth Rs 5 lakhs stolen.", "type_idx": 2, "district_idx": 0, "status": "open", "priority": "medium", "location_idx": 2},
    {"title": "Robbery at ATM booth", "desc": "Armed robbery at ATM. Customer threatened and cash stolen.", "type_idx": 1, "district_idx": 0, "status": "open", "priority": "high", "location_idx": 1},
    {"title": "Vehicle theft from hospital", "desc": "Two-wheeler stolen from hospital parking. Lock broken.", "type_idx": 11, "district_idx": 0, "status": "open", "priority": "medium", "location_idx": 4},
    {"title": "Kidnapping attempt near school", "desc": "Attempt to kidnap school girl. Locals intervened and suspect fled.", "type_idx": 7, "district_idx": 0, "status": "active", "priority": "high", "location_idx": 3},
    {"title": "Arson at warehouse", "desc": "Fire set at abandoned warehouse. Suspect known rival owner.", "type_idx": 16, "district_idx": 0, "status": "open", "priority": "high", "location_idx": 4},
    {"title": "Robbery at silk warehouse in Mysuru", "desc": "Cash and silk worth Rs 50 lakhs stolen. Inside job suspected.", "type_idx": 1, "district_idx": 2, "status": "active", "priority": "high", "location_idx": 5},
    {"title": "Theft at Mysuru Palace tourist area", "desc": "Tourist's bag snatched. CCTV shows two suspects on bike.", "type_idx": 0, "district_idx": 2, "status": "open", "priority": "medium", "location_idx": 5},
    {"title": "Cyber fraud via fake OLX listing", "desc": "Victim paid advance for fake OLX listing. Rs 2 lakhs lost.", "type_idx": 6, "district_idx": 2, "status": "active", "priority": "medium", "location_idx": 5},
    {"title": "Assault at Mysuru railway station", "desc": "Altercation between two groups. One person injured.", "type_idx": 4, "district_idx": 2, "status": "closed", "priority": "low", "location_idx": 5},
    {"title": "Drug peddling near Mangaluru port", "desc": "Contraband seized from shipping container. Two arrested.", "type_idx": 8, "district_idx": 3, "status": "closed", "priority": "high", "location_idx": 6},
    {"title": "Burglary at Mangaluru jewelry shop", "desc": "Shop broken into at night. Gold ornaments stolen.", "type_idx": 2, "district_idx": 3, "status": "open", "priority": "medium", "location_idx": 6},
    {"title": "Robbery at Hubballi bus depot", "desc": "Cash stolen from ticket counter. Employee involved.", "type_idx": 1, "district_idx": 4, "status": "active", "priority": "medium", "location_idx": 7},
    {"title": "Theft of cattle in Dharwad", "desc": "Three cattle stolen from farm. Suspects traced to neighboring district.", "type_idx": 0, "district_idx": 4, "status": "open", "priority": "medium", "location_idx": 7},
    {"title": "Fraud in cooperative bank", "desc": "Manager embezzled Rs 2 crores. Multiple accounts manipulated.", "type_idx": 5, "district_idx": 4, "status": "active", "priority": "high", "location_idx": 7},
    {"title": "Murder in Kalaburagi village", "desc": "Farmers' dispute turned violent. One dead, two injured.", "type_idx": 3, "district_idx": 5, "status": "active", "priority": "high", "location_idx": 0},
    {"title": "Vehicle theft ring busted", "desc": "Gang operating across Bellari and Ballari districts. 12 vehicles recovered.", "type_idx": 11, "district_idx": 6, "status": "closed", "priority": "high", "location_idx": 0},
    {"title": "Kidnapping for ransom in Vijayapura", "desc": "Businessman kidnapped. Rs 50 lakhs ransom demanded. Rescue operation launched.", "type_idx": 7, "district_idx": 7, "status": "active", "priority": "high", "location_idx": 0},
    {"title": "Arson at Shivamogga temple", "desc": "Temple set on fire. Sacred idols damaged. Community outrage.", "type_idx": 16, "district_idx": 8, "status": "active", "priority": "high", "location_idx": 0},
    {"title": "Cheating in real estate deal", "desc": "Multiple families cheated of advance payments. Fake property documents.", "type_idx": 15, "district_idx": 9, "status": "open", "priority": "medium", "location_idx": 0},
    {"title": "Domestic violence in Hassan", "desc": "Repeated assault reported by victim. Medical evidence collected.", "type_idx": 9, "district_idx": 10, "status": "active", "priority": "medium", "location_idx": 0},
    {"title": "Drug racket in Mandya", "desc": "Illegal drug manufacturing unit busted. Three arrested.", "type_idx": 8, "district_idx": 11, "status": "closed", "priority": "high", "location_idx": 0},
    {"title": "Theft of temple donations in Tumakuru", "desc": "Cash box stolen from temple. Temple priest suspected.", "type_idx": 0, "district_idx": 12, "status": "open", "priority": "medium", "location_idx": 0},
    {"title": "Hit and run in Kolar", "desc": "Two-wheeler rider hit by car. Driver fled scene.", "type_idx": 10, "district_idx": 13, "status": "open", "priority": "high", "location_idx": 0},
    {"title": "Forgery of educational certificates", "desc": "Fake SSLC certificates being sold. Multiple victims.", "type_idx": 14, "district_idx": 14, "status": "active", "priority": "medium", "location_idx": 0},
    {"title": "Extortion by fake police officer", "desc": "Person impersonating police demanding money from shopkeepers.", "type_idx": 13, "district_idx": 15, "status": "active", "priority": "high", "location_idx": 0},
]

# Procedural expansions keep charts/maps dense while preserving handcrafted quality above.
_STATUSES = ("open", "active", "closed", "open", "active")
_PRIORITIES = ("high", "medium", "low", "medium", "high")
_TITLE_TEMPLATES = [
    "{ctype} reported near {district} market",
    "Night-time {ctype} in {district} residential block",
    "{ctype} complaint from {district} bus stand",
    "Weekend {ctype} cluster - {district}",
    "Suspected {ctype} ring operating in {district}",
    "Late-night {ctype} near {district} highway",
    "Repeat {ctype} pattern in {district}",
    "{ctype} during festival crowd - {district}",
]
_DESC_TEMPLATES = [
    "Complaint registered for {ctype} in {district}. Preliminary enquiry underway; local CCTV being collected.",
    "Victim reported {ctype} incident in {district}. Witnesses identified; IO assigned for follow-up.",
    "Patrol team flagged {ctype} activity in {district}. Scene inspected and evidence logged.",
    "Multiple calls regarding {ctype} around {district}. Pattern analysis recommended for hotspot mapping.",
]


def _build_expanded_crimes(base: list[dict], target: int = 100) -> list[dict]:
    out = list(base)
    seen = {row["title"] for row in out}
    i = 0
    while len(out) < target:
        type_idx = i % len(CRIME_TYPES)
        district_idx = i % len(DISTRICTS)
        ctype = CRIME_TYPES[type_idx][0]
        district = DISTRICTS[district_idx][0]
        title = _TITLE_TEMPLATES[i % len(_TITLE_TEMPLATES)].format(ctype=ctype, district=district)
        # Ensure uniqueness when templates wrap
        if title in seen:
            title = f"{title} #{len(out) + 1}"
        seen.add(title)
        loc_idx = i % len(LOCATIONS)
        out.append({
            "title": title,
            "desc": _DESC_TEMPLATES[i % len(_DESC_TEMPLATES)].format(ctype=ctype, district=district),
            "type_idx": type_idx,
            "district_idx": district_idx,
            "status": _STATUSES[i % len(_STATUSES)],
            "priority": _PRIORITIES[i % len(_PRIORITIES)],
            "location_idx": loc_idx,
        })
        i += 1
    return out


CRIMES = _build_expanded_crimes(CRIMES, target=100)

SUSPECTS = [
    {"name": "Ravi Kumar", "age": 32, "gender": "Male", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 78.5, "description": "Known for chain snatching on motorcycle. Linked to multiple open cases.", "aliases": '["Ravi", "RK"]'},
    {"name": "Mohammed Ali", "age": 28, "gender": "Male", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 65.0, "description": "Repeat offender for vehicle theft. Post-release surveillance active.", "aliases": '["Ali", "MA"]'},
    {"name": "Deepak Reddy", "age": 35, "gender": "Male", "district": "Mysuru", "status": "custody", "risk_score": 82.0, "description": "Suspected network organizer for silk warehouse robbery.", "aliases": '["Deepak", "Reddy"]'},
    {"name": "Suresh Gowda", "age": 41, "gender": "Male", "district": "Mandya", "status": "at_large", "risk_score": 55.0, "description": "Linked to NDPS manufacturing unit in Mandya.", "aliases": '["Suresh"]'},
    {"name": "Priya Sharma", "age": 26, "gender": "Female", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 42.0, "description": "Suspected accomplice in cyber fraud targeting seniors.", "aliases": '["Priya"]'},
    {"name": "Imran Khan", "age": 30, "gender": "Male", "district": "Mangaluru", "status": "custody", "risk_score": 70.0, "description": "Arrested in port drug seizure; further links under probe.", "aliases": '["Imran"]'},
    {"name": "Naveen Patil", "age": 38, "gender": "Male", "district": "Hubballi-Dharwad", "status": "at_large", "risk_score": 60.0, "description": "Suspected in cooperative bank fraud.", "aliases": '["Naveen"]'},
    {"name": "Anil Shetty", "age": 45, "gender": "Male", "district": "Kalaburagi", "status": "at_large", "risk_score": 88.0, "description": "Prime suspect in village murder over land dispute.", "aliases": '["Anil"]'},
    {"name": "Karthik Rao", "age": 29, "gender": "Male", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 50.0, "description": "CCTV match for ATM robbery.", "aliases": '["Karthik"]'},
    {"name": "Faisal Ahmed", "age": 33, "gender": "Male", "district": "Vijayapura", "status": "at_large", "risk_score": 91.0, "description": "Suspected in kidnapping for ransom case.", "aliases": '["Faisal"]'},
    {"name": "Vikram Singh", "age": 36, "gender": "Male", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 72.0, "description": "Linked to night burglaries in Koramangala.", "aliases": '["Vikram"]'},
    {"name": "Ramesh Hegde", "age": 44, "gender": "Male", "district": "Shivamogga", "status": "at_large", "risk_score": 58.0, "description": "Suspected in temple arson and related threats.", "aliases": '["Hegde"]'},
    {"name": "Salman Pasha", "age": 27, "gender": "Male", "district": "Ballari", "status": "custody", "risk_score": 64.0, "description": "Part of vehicle theft recovery operation.", "aliases": '["Salman"]'},
    {"name": "Geetha Nair", "age": 31, "gender": "Female", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 47.0, "description": "Suspected mule in cyber fraud transfers.", "aliases": '["Geetha"]'},
    {"name": "Manjunath K", "age": 39, "gender": "Male", "district": "Tumakuru", "status": "at_large", "risk_score": 53.0, "description": "Linked to temple donation theft.", "aliases": '["Manju"]'},
    {"name": "Yogesh Pawar", "age": 34, "gender": "Male", "district": "Davangere", "status": "at_large", "risk_score": 61.0, "description": "Repeat offender for cheating/real-estate fraud.", "aliases": '["Yogesh"]'},
    {"name": "Arjun Das", "age": 25, "gender": "Male", "district": "Bengaluru Rural", "status": "at_large", "risk_score": 49.0, "description": "CCTV match for highway hit-and-run.", "aliases": '["Arjun"]'},
    {"name": "Sheela Bai", "age": 42, "gender": "Female", "district": "Hassan", "status": "at_large", "risk_score": 38.0, "description": "Witness-turned-suspect in domestic violence probe.", "aliases": '["Sheela"]'},
    {"name": "Prakash Naik", "age": 48, "gender": "Male", "district": "Kolar", "status": "custody", "risk_score": 76.0, "description": "Forgery of educational certificates racket.", "aliases": '["Prakash"]'},
    {"name": "Javed Hussain", "age": 29, "gender": "Male", "district": "Kalaburagi", "status": "at_large", "risk_score": 69.0, "description": "Suspected associate in village murder case.", "aliases": '["Javed"]'},
    {"name": "Harish Bhat", "age": 37, "gender": "Male", "district": "Shivamogga", "status": "at_large", "risk_score": 44.0, "description": "Coastal belt snatching pattern suspect.", "aliases": '["Harish"]'},
    {"name": "Sunil Kumar", "age": 40, "gender": "Male", "district": "Chikkaballapur", "status": "at_large", "risk_score": 57.0, "description": "Linked to fake certificate sales.", "aliases": '["Sunil"]'},
    {"name": "Mehboob Shariff", "age": 35, "gender": "Male", "district": "Ramanagara", "status": "at_large", "risk_score": 66.0, "description": "Extortion calls to shopkeepers under probe.", "aliases": '["Mehboob"]'},
    {"name": "Kiran Shetty", "age": 28, "gender": "Male", "district": "Mangaluru", "status": "custody", "risk_score": 71.0, "description": "Jewelry shop burglary MO match.", "aliases": '["Kiran"]'},
    {"name": "Bhavana Rao", "age": 24, "gender": "Female", "district": "Mysuru", "status": "at_large", "risk_score": 41.0, "description": "Suspected in tourist-area theft fence network.", "aliases": '["Bhavana"]'},
    {"name": "Gopal Krishna", "age": 52, "gender": "Male", "district": "Hubballi-Dharwad", "status": "at_large", "risk_score": 63.0, "description": "Bus depot cash theft insider angle.", "aliases": '["Gopal"]'},
    {"name": "Roshan Ali", "age": 31, "gender": "Male", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 80.0, "description": "ATM robbery CCTV match; high mobility.", "aliases": '["Roshan"]'},
    {"name": "Dinesh Yadav", "age": 33, "gender": "Male", "district": "Mandya", "status": "at_large", "risk_score": 59.0, "description": "NDPS unit logistics suspect.", "aliases": '["Dinesh"]'},
    {"name": "Sangeetha M", "age": 27, "gender": "Female", "district": "Bengaluru Urban", "status": "at_large", "risk_score": 45.0, "description": "Fake job portal cheating accomplice.", "aliases": '["Sangeetha"]'},
]

PERSONS = [
    {"first_name": "Ravi", "last_name": "Kumar", "gender": "Male", "district": "Bengaluru Urban", "phone": "9876500001"},
    {"first_name": "Mohammed", "last_name": "Ali", "gender": "Male", "district": "Bengaluru Urban", "phone": "9876500002"},
    {"first_name": "Deepak", "last_name": "Reddy", "gender": "Male", "district": "Mysuru", "phone": "9876500003"},
    {"first_name": "Lakshmi", "last_name": "Devi", "gender": "Female", "district": "Bengaluru Urban", "phone": "9876500010"},
    {"first_name": "Suresh", "last_name": "Gowda", "gender": "Male", "district": "Mandya", "phone": "9876500004"},
    {"first_name": "Anita", "last_name": "Rao", "gender": "Female", "district": "Mysuru", "phone": "9876500011"},
    {"first_name": "Imran", "last_name": "Khan", "gender": "Male", "district": "Mangaluru", "phone": "9876500005"},
    {"first_name": "Naveen", "last_name": "Patil", "gender": "Male", "district": "Hubballi-Dharwad", "phone": "9876500006"},
    {"first_name": "Vikram", "last_name": "Singh", "gender": "Male", "district": "Bengaluru Urban", "phone": "9876500007"},
    {"first_name": "Geetha", "last_name": "Nair", "gender": "Female", "district": "Bengaluru Urban", "phone": "9876500008"},
    {"first_name": "Prakash", "last_name": "Naik", "gender": "Male", "district": "Kolar", "phone": "9876500009"},
    {"first_name": "Bhavana", "last_name": "Rao", "gender": "Female", "district": "Mysuru", "phone": "9876500012"},
    {"first_name": "Roshan", "last_name": "Ali", "gender": "Male", "district": "Bengaluru Urban", "phone": "9876500013"},
    {"first_name": "Kiran", "last_name": "Shetty", "gender": "Male", "district": "Mangaluru", "phone": "9876500014"},
    {"first_name": "Harish", "last_name": "Bhat", "gender": "Male", "district": "Shivamogga", "phone": "9876500015"},
    {"first_name": "Sangeetha", "last_name": "M", "gender": "Female", "district": "Bengaluru Urban", "phone": "9876500016"},
]

USERS = [
    {"username": "si.karthik", "email": "si.karthik@ksp.gov.in", "full_name": "SI Karthik Rao", "role": "officer", "station": "Cubbon Park PS"},
    {"username": "insp.meena", "email": "insp.meena@ksp.gov.in", "full_name": "Inspector Meena Joshi", "role": "officer", "station": "Koramangala PS"},
    {"username": "dsp.ramesh", "email": "dsp.ramesh@ksp.gov.in", "full_name": "DSP Ramesh Naik", "role": "admin", "station": "Bengaluru Urban HQ"},
]

OFFICERS = [
    {"badge_number": "KSP-1001", "kgid": "KGID1001", "first_name": "Karthik", "rank_code": "SI", "station_code": "BLR-CP", "district_code": "BLR-U", "phone": "9988776601"},
    {"badge_number": "KSP-1002", "kgid": "KGID1002", "first_name": "Meena", "rank_code": "INS", "station_code": "BLR-KM", "district_code": "BLR-U", "phone": "9988776602"},
    {"badge_number": "KSP-1003", "kgid": "KGID1003", "first_name": "Ramesh", "rank_code": "DSP", "station_code": "BLR-CP", "district_code": "BLR-U", "phone": "9988776603"},
    {"badge_number": "KSP-2001", "kgid": "KGID2001", "first_name": "Sanjay", "rank_code": "SI", "station_code": "MYS-NZ", "district_code": "MYS", "phone": "9988776604"},
    {"badge_number": "KSP-3001", "kgid": "KGID3001", "first_name": "Fatima", "rank_code": "INS", "station_code": "MNG-S", "district_code": "MNG", "phone": "9988776605"},
]
