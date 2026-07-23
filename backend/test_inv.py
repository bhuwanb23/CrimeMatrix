import asyncio
from app.db.session import SessionLocal
from app.services.investigation_service import InvestigationService

async def main():
    async with SessionLocal() as db:
        svc = InvestigationService(db)
        try:
            items = await svc.list_investigations()
            print("Investigations:", items)
        except Exception as e:
            print("ERROR:", e)
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
