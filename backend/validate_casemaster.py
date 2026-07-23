import sys
sys.path.insert(0, r'D:\projects\website\crimematrix\backend')

# 1. Import validation
print("1. Import validation...")
try:
    from app.models.case import Case
    from app.models.case_category import CaseCategory
    from app.models.gravity_offence import GravityOffence
    from app.models.crime_head import CrimeHead
    from app.models.crime_sub_head import CrimeSubHead
    from app.models.case_status_master import CaseStatusMaster
    from app.models.court import Court
    print("  All models import OK")
except Exception as e:
    print(f"  FAIL: {e}")
    sys.exit(1)

try:
    from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse
    print("  All schemas import OK")
except Exception as e:
    print(f"  FAIL: {e}")
    sys.exit(1)

try:
    from app.api.v1.cases_api import router
    print("  Cases API import OK")
except Exception as e:
    print(f"  FAIL: {e}")
    sys.exit(1)

try:
    from app.api.v1.lookup_api import router
    print("  Lookup API import OK")
except Exception as e:
    print(f"  FAIL: {e}")
    sys.exit(1)

# 2. Route validation
print("\n2. Route validation...")
from app.api.v1.router import router
paths = [r.path for r in router.routes if hasattr(r, 'path')]

needed_cases = ['/api/v1/cases/', '/api/v1/cases/{case_id}', '/api/v1/cases/by-number/{case_number}',
                '/api/v1/cases/by-crime-no/{crime_no}', '/api/v1/cases/search/{query}']
for p in needed_cases:
    found = any(p in path for path in paths)
    print(f"  [{'OK' if found else 'MISSING'}] {p}")

needed_lookups = ['/api/v1/lookups/categories', '/api/v1/lookups/gravity-offences',
                  '/api/v1/lookups/crime-heads', '/api/v1/lookups/crime-sub-heads',
                  '/api/v1/lookups/case-statuses', '/api/v1/lookups/courts',
                  '/api/v1/lookups/seed']
for p in needed_lookups:
    found = p in paths
    print(f"  [{'OK' if found else 'MISSING'}] {p}")

# 3. Schema field validation
print("\n3. Schema field validation...")
new_fields = ['crime_no', 'incident_from_date', 'incident_to_date', 'info_received_ps_date',
              'latitude', 'longitude', 'brief_facts', 'case_category_id', 'gravity_offence_id',
              'crime_major_head_id', 'crime_minor_head_id', 'case_status_id', 'court_id',
              'police_person_id', 'police_station_id']

for schema_name, schema in [('CaseCreate', CaseCreate), ('CaseUpdate', CaseUpdate), ('CaseResponse', CaseResponse)]:
    fields = set(schema.model_fields.keys())
    missing = [f for f in new_fields if f not in fields]
    if missing:
        print(f"  FAIL {schema_name}: missing {missing}")
    else:
        print(f"  OK {schema_name}: all {len(new_fields)} CaseMaster fields present")

# 4. Database validation
print("\n4. Database validation...")
import sqlite3
conn = sqlite3.connect(r'D:\projects\website\crimematrix\backend\data\crimematrix.db')
c = conn.cursor()

for t in ['case_categories', 'gravity_offences', 'crime_heads', 'crime_sub_heads', 'case_status_master', 'courts']:
    c.execute(f"SELECT count(*) FROM {t}")
    count = c.fetchone()[0]
    print(f"  {t}: {count} records")

c.execute("PRAGMA table_info(cases)")
case_cols = {r[1] for r in c.fetchall()}
for col in new_fields:
    print(f"  [{'OK' if col in case_cols else 'MISSING'}] cases.{col}")

c.execute("SELECT count(name) FROM sqlite_master WHERE type='table'")
print(f"\n  Total tables: {c.fetchone()[0]}")
print(f"  Case columns: {len(case_cols)}")
print(f"  Total routes: {len(paths)}")

conn.close()
print("\n=== Validation Complete ===")
