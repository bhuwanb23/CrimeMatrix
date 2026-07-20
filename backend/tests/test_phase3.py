import asyncio
from app.db.session import async_session
from app.repositories.user_repo import UserRepository
from app.repositories.case_repo import CaseRepository
from app.repositories.suspect_repo import SuspectRepository
from app.services.user_service import UserService
from app.services.case_service import CaseService
from app.services.suspect_service import SuspectService
from app.schemas.common import PaginationParams, FilterParams, SortParams


async def test():
    print("=== Phase 3: Core Backend Infrastructure ===\n")

    async with async_session() as session:
        # Repositories
        user_repo = UserRepository(session)
        case_repo = CaseRepository(session)
        suspect_repo = SuspectRepository(session)

        # Services
        user_svc = UserService(user_repo)
        case_svc = CaseService(case_repo)
        suspect_svc = SuspectService(suspect_repo)

        # Test User Service
        print("--- User Service ---")
        user = await user_svc.create_user({
            'username': 'test_officer',
            'email': 'test@ksp.gov.in',
            'hashed_password': 'hashed_123',
            'full_name': 'Test Officer',
            'role': 'officer',
        })
        print(f"✅ Created: {user.username}")

        fetched = await user_svc.get_by_username('test_officer')
        print(f"✅ Fetched: {fetched.username}")

        # Test Case Service
        print("\n--- Case Service ---")
        case = await case_svc.create({
            'case_number': 'TEST-001',
            'title': 'Test Case',
            'crime_type': 'Theft',
            'district': 'Bengaluru',
        })
        print(f"✅ Created: {case.case_number}")

        results = await case_svc.search_cases('test')
        print(f"✅ Search: {len(results)} results")

        # Test Suspect Service
        print("\n--- Suspect Service ---")
        suspect = await suspect_svc.create({
            'name': 'Test Suspect',
            'age': 30,
            'district': 'Bengaluru',
            'risk_score': 75.0,
        })
        print(f"✅ Created: {suspect.name}")

        high_risk = await suspect_svc.get_high_risk(70.0)
        print(f"✅ High risk: {len(high_risk)} suspects")

        # Test Pagination
        print("\n--- Pagination ---")
        params = PaginationParams(page=1, page_size=5)
        paginated = await case_svc.get_paginated(params)
        print(f"✅ Paginated: {paginated.total} total, page {paginated.page}")

        # Test Filtering
        print("\n--- Filtering ---")
        filters = [FilterParams(field='district', operator='eq', value='Bengaluru')]
        all_cases = await case_svc.repo.get_all()
        filtered = case_svc.apply_filters(all_cases, filters)
        print(f"✅ Filtered: {len(filtered)} cases in Bengaluru")

        # Test Sorting
        print("\n--- Sorting ---")
        sort = SortParams(field='crime_type', direction='asc')
        sorted_cases = case_svc.apply_sort(all_cases, sort)
        print(f"✅ Sorted: {sorted_cases[0].crime_type} first")

        print("\n✅ All Phase 3 modules working!")

asyncio.run(test())
