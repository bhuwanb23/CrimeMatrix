from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.analytics.statistics import StatisticsEngine
from app.analytics.aggregations import AggregationEngine
from app.analytics.heatmaps import HeatmapEngine
from app.analytics.trends import TrendEngine
from app.analytics.districts import DistrictAnalytics
from app.analytics.crime_counts import CrimeCountEngine
from app.analytics.time_series import TimeSeriesEngine
from app.core.response import success_response
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.db.phase1_store import store_list, using_phase1_store

router = APIRouter()


class AggregateRequest(BaseModel):
    entity: str
    group_by: str
    metric: str = "count"


# Statistics
@router.get("/stats/overview")
async def stats_overview(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all

        return success_response(
            data={
                "crimes": len(await fetch_all("crimes")),
                "districts": len(await fetch_all("districts")),
                "cases": len(await fetch_all("cases")),
                "investigations": len(await fetch_all("investigations")),
                "source": "phase1_store",
            }
        )
    engine = StatisticsEngine(db)
    data = await engine.get_overview()
    return success_response(data=data)


@router.get("/stats/summary")
async def stats_summary(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        return await stats_overview(db)
    engine = StatisticsEngine(db)
    data = await engine.get_summary()
    return success_response(data=data)


# Aggregations
@router.post("/aggregate")
async def aggregate(data: AggregateRequest, db: AsyncSession = Depends(get_db)):
    engine = AggregationEngine(db)
    result = await engine.aggregate(data.entity, data.group_by, data.metric)
    return success_response(data=result)


# Heatmaps
@router.get("/heatmap/district")
async def district_heatmap(db: AsyncSession = Depends(get_db)):
    engine = HeatmapEngine(db)
    data = await engine.district_heatmap()
    return success_response(data=data)


@router.get("/heatmap/timeline")
async def timeline_heatmap(db: AsyncSession = Depends(get_db)):
    engine = HeatmapEngine(db)
    data = await engine.timeline_heatmap()
    return success_response(data=data)


# Trends
@router.get("/trends/crimes")
async def crime_trends(
    period: str = "daily",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        from app.db.phase1_aggregations import bucket_crimes_by_day, fetch_all

        crimes = await fetch_all("crimes")
        data = bucket_crimes_by_day(crimes)
        if start_date:
            data = [d for d in data if d["date"] >= start_date]
        if end_date:
            data = [d for d in data if d["date"] <= end_date]
        return success_response(data={"period": period, "data": data})
    engine = TrendEngine(db)
    data = await engine.crime_trends(period, start_date, end_date)
    return success_response(data=data)


@router.get("/trends/cases")
async def case_trends(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        from app.db.phase1_aggregations import count_by_key, fetch_all

        cases = await fetch_all("cases")
        rows = count_by_key(cases, "status")
        return success_response(data={"data": [{"status": r["key"], "count": r["value"]} for r in rows]})
    engine = TrendEngine(db)
    data = await engine.case_trends(start_date, end_date)
    return success_response(data=data)


@router.get("/trends/resolution")
async def resolution_trend(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all, resolution_from_crimes

        crimes = await fetch_all("crimes")
        return success_response(data=resolution_from_crimes(crimes))
    engine = TrendEngine(db)
    data = await engine.resolution_trend()
    return success_response(data=data)


# District Analytics
@router.get("/districts")
async def all_districts(db: AsyncSession = Depends(get_db)):
    engine = DistrictAnalytics(db)
    data = await engine.get_all_districts()
    return success_response(data=data)


@router.get("/districts/{district_id}")
async def district_detail(district_id: int, db: AsyncSession = Depends(get_db)):
    engine = DistrictAnalytics(db)
    data = await engine.get_district_detail(district_id)
    return success_response(data=data)


# Crime Counts
@router.get("/counts/by-type")
async def count_by_type(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all, id_name_map, resolve_and_count

        crimes = await fetch_all("crimes")
        names = await id_name_map("crime_types")
        return success_response(data=resolve_and_count(crimes, "crime_type_id", names))
    engine = CrimeCountEngine(db)
    data = await engine.count_by_type()
    return success_response(data=data)


@router.get("/counts/by-status")
async def count_by_status(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import count_by_key, fetch_all

        crimes = await fetch_all("crimes")
        return success_response(data=count_by_key(crimes, "status"))
    engine = CrimeCountEngine(db)
    data = await engine.count_by_status()
    return success_response(data=data)


@router.get("/counts/by-district")
async def count_by_district(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all, id_name_map, resolve_and_count

        crimes = await fetch_all("crimes")
        names = await id_name_map("districts")
        return success_response(data=resolve_and_count(crimes, "district_id", names))
    engine = CrimeCountEngine(db)
    data = await engine.count_by_district()
    return success_response(data=data)


@router.get("/counts/by-priority")
async def count_by_priority(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import count_by_key, fetch_all

        crimes = await fetch_all("crimes")
        return success_response(data=count_by_key(crimes, "priority"))
    engine = CrimeCountEngine(db)
    data = await engine.count_by_priority()
    return success_response(data=data)


# Time Series
@router.get("/timeseries/crimes")
async def crime_time_series(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        try:
            data = await store_list("crimes", page=1, page_size=100)
            buckets: dict[str, int] = {}
            for item in data.get("items") or []:
                raw = item.get("occurred_at") or item.get("CREATEDTIME") or item.get("created_at")
                day = str(raw)[:10] if raw else "unknown"
                buckets[day] = buckets.get(day, 0) + 1
            return success_response(data=[{"date": d, "value": v} for d, v in sorted(buckets.items())])
        except Exception:
            return success_response(data=[])
    engine = TimeSeriesEngine(db)
    data = await engine.crime_series(start_date, end_date)
    return success_response(data=data)


@router.get("/timeseries/cases")
async def case_time_series(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        try:
            data = await store_list("cases", page=1, page_size=100)
            buckets: dict[str, int] = {}
            for item in data.get("items") or []:
                status = str(item.get("status") or "unknown")
                buckets[status] = buckets.get(status, 0) + 1
            return success_response(data=[{"date": d, "value": v} for d, v in sorted(buckets.items())])
        except Exception:
            return success_response(data=[])
    engine = TimeSeriesEngine(db)
    data = await engine.case_series(start_date, end_date)
    return success_response(data=data)


@router.get("/timeseries/activity")
async def activity_time_series(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        try:
            data = await store_list("crimes", page=1, page_size=100)
            series: dict[str, dict] = {}
            for item in data.get("items") or []:
                raw = item.get("occurred_at") or item.get("CREATEDTIME") or item.get("created_at")
                day = str(raw)[:10] if raw else "unknown"
                if day not in series:
                    series[day] = {"date": day, "crimes": 0, "total": 0}
                series[day]["crimes"] += 1
                series[day]["total"] += 1
            return success_response(data=sorted(series.values(), key=lambda x: x["date"]))
        except Exception:
            return success_response(data=[])
    engine = TimeSeriesEngine(db)
    data = await engine.activity_series(start_date, end_date)
    return success_response(data=data)
