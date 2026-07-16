import asyncio
from app.db.session import engine
from sqlalchemy import text


async def test():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables ({len(tables)}):")
        for t in tables:
            print(f"  - {t}")


asyncio.run(test())
