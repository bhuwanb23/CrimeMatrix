from fastapi import APIRouter
from app.api.v1 import (
    health, ai, status, config, metadata, version, statistics, uploads,
    crimes, persons, criminals, victims, witnesses, officers, stations,
    districts, vehicles, phones, locations, crimetypes,
    notes, bookmarks, timeline_events, attachments, case_links, case_status,
    search, graph_api, analytics_api, reports_api, notifications_api, audit_api,
    memory_api, embedding_api, monitoring_api, storage_api, copilot,
    search_saved, search_history, semantic_search, search_district,
    similar_cases_api,
    investigations_api,
    investigation_analysis,
    recommendations_api
)

router = APIRouter(prefix="/api/v1")

# Core APIs
router.include_router(health.router, tags=["Health"])
router.include_router(status.router, tags=["System"])
router.include_router(config.router, tags=["Configuration"])
router.include_router(metadata.router, tags=["Metadata"])
router.include_router(version.router, tags=["Version"])
router.include_router(statistics.router, tags=["Statistics"])
router.include_router(uploads.router, tags=["Uploads"])
router.include_router(ai.router, prefix="/ai", tags=["AI"])

# Search APIs
router.include_router(search.router, prefix="/search", tags=["Search"])

# Crime Data APIs
router.include_router(crimes.router, prefix="/crimes", tags=["Crimes"])
router.include_router(persons.router, prefix="/persons", tags=["Persons"])
router.include_router(criminals.router, prefix="/criminals", tags=["Criminals"])
router.include_router(victims.router, prefix="/victims", tags=["Victims"])
router.include_router(witnesses.router, prefix="/witnesses", tags=["Witnesses"])
router.include_router(officers.router, prefix="/officers", tags=["Officers"])
router.include_router(stations.router, prefix="/stations", tags=["Stations"])
router.include_router(districts.router, prefix="/districts", tags=["Districts"])
router.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
router.include_router(phones.router, prefix="/phones", tags=["Phones"])
router.include_router(locations.router, prefix="/locations", tags=["Locations"])
router.include_router(crimetypes.router, prefix="/crime-types", tags=["Crime Types"])

# Investigation Layer APIs
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
router.include_router(bookmarks.router, prefix="/bookmarks", tags=["Bookmarks"])
router.include_router(timeline_events.router, prefix="/timeline", tags=["Timeline"])
router.include_router(attachments.router, prefix="/attachments", tags=["Attachments"])
router.include_router(case_links.router, prefix="/case-links", tags=["Case Links"])
router.include_router(case_status.router, prefix="/case-status", tags=["Case Status"])

# Graph APIs
router.include_router(graph_api.router, prefix="/graph", tags=["Graph"])

# Analytics APIs
router.include_router(analytics_api.router, prefix="/analytics", tags=["Analytics"])

# Reports APIs
router.include_router(reports_api.router, prefix="/reports", tags=["Reports"])

# Notification APIs
router.include_router(notifications_api.router, prefix="/notifications", tags=["Notifications"])

# Audit APIs
router.include_router(audit_api.router, prefix="/audit", tags=["Audit"])

# Memory Persistence APIs
router.include_router(memory_api.router, prefix="/memory", tags=["Memory"])

# Embedding Persistence APIs
router.include_router(embedding_api.router, prefix="/embeddings", tags=["Embeddings"])

# Monitoring APIs
router.include_router(monitoring_api.router, prefix="/monitoring", tags=["Monitoring"])

# Storage APIs
router.include_router(storage_api.router, prefix="/storage", tags=["Storage"])

# Copilot APIs
router.include_router(copilot.router, prefix="/copilot", tags=["Copilot"])

# Search Saved & History APIs
router.include_router(search_saved.router, prefix="/search/saved", tags=["Search Saved"])
router.include_router(search_history.router, prefix="/search/history", tags=["Search History"])

# Semantic Search APIs
router.include_router(semantic_search.router, prefix="/search/semantic", tags=["Semantic Search"])

# Cross-District Search APIs
router.include_router(search_district.router, prefix="/search/district", tags=["District Search"])

# Similar Case Discovery APIs
router.include_router(similar_cases_api.router, prefix="/similar-cases", tags=["Similar Cases"])

# Investigation Workspace APIs
router.include_router(investigations_api.router, prefix="/investigations", tags=["Investigations"])

# Investigation Analysis APIs
router.include_router(investigation_analysis.router, prefix="/investigations", tags=["Investigation Analysis"])

# Recommendation APIs
router.include_router(recommendations_api.router, prefix="/recommendations", tags=["Recommendations"])
