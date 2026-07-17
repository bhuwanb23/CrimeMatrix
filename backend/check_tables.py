import sqlite3
db = sqlite3.connect("data/crimematrix.db")
tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
print(f"Total tables: {len(tables)}")
for t in tables:
    print(f"  - {t}")
db.close()
