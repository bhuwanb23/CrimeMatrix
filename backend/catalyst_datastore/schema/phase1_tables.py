"""Phase 1 Catalyst Data Store table definitions.

Maps CrimeMatrix SQLAlchemy models to Catalyst column types.
Every Catalyst table also has system columns: ROWID, CREATORID, CREATEDTIME, MODIFIEDTIME.

API `id` is mapped from ROWID by the provider layer.
`legacy_id` stores the original SQLite integer id for seed/FK remapping.
"""

from __future__ import annotations

from typing import Any

# Catalyst data types used below:
# varchar, text, int, double, boolean, datetime, date, bigint

Col = dict[str, Any]


def col(
    name: str,
    data_type: str,
    *,
    mandatory: bool = False,
    unique: bool = False,
    max_length: int | None = None,
    search_index: bool = False,
) -> Col:
    c: Col = {
        "column_name": name,
        "data_type": data_type,
        "is_mandatory": mandatory,
        "is_unique": unique,
        "search_index_enabled": search_index,
    }
    if max_length is not None:
        c["max_length"] = max_length
    return c


def legacy() -> Col:
    return col("legacy_id", "bigint", search_index=True)


def lookup_name_code(extra: list[Col] | None = None) -> list[Col]:
    cols = [
        legacy(),
        col("name", "varchar", mandatory=True, max_length=100, search_index=True),
        col("code", "varchar", mandatory=True, max_length=50, search_index=True),
    ]
    if extra:
        cols.extend(extra)
    return cols


# ZCQL SELECT max 20 columns — list endpoints must use these projections.
LIST_PROJECTIONS: dict[str, list[str]] = {}


def _proj(table: str, columns: list[str]) -> None:
    # Always include ROWID; keep <= 19 custom columns
    LIST_PROJECTIONS[table] = ["ROWID"] + columns[:19]


PHASE1_TABLES: dict[str, list[Col]] = {
    # --- Lookups / geo / org ---
    "states": lookup_name_code(
        [col("nationality_id", "bigint"), col("active", "boolean")]
    ),
    "unit_types": lookup_name_code(
        [
            col("city_dist_state", "varchar", max_length=50),
            col("hierarchy", "int"),
            col("description", "text"),
            col("active", "boolean"),
        ]
    ),
    "ranks": lookup_name_code(
        [
            col("hierarchy", "int"),
            col("description", "text"),
            col("active", "boolean"),
        ]
    ),
    "designations": lookup_name_code(
        [
            col("active", "boolean"),
            col("sort_order", "int"),
            col("description", "text"),
        ]
    ),
    "genders": lookup_name_code([col("description", "text")]),
    "crime_types": lookup_name_code(
        [
            col("description", "text"),
            col("severity_level", "int"),
            col("is_active", "int"),
        ]
    ),
    "crime_heads": lookup_name_code(
        [col("description", "text"), col("active", "boolean")]
    ),
    "crime_sub_heads": lookup_name_code(
        [
            col("crime_head_id", "bigint", search_index=True),
            col("seq_id", "int"),
            col("description", "text"),
        ]
    ),
    "case_categories": lookup_name_code(
        [col("description", "text"), col("active", "boolean")]
    ),
    "case_status_master": lookup_name_code([col("description", "text")]),
    "acts": [
        legacy(),
        col("name", "varchar", mandatory=True, max_length=200, search_index=True),
        col("code", "varchar", max_length=50),
        col("act_code", "varchar", mandatory=True, max_length=50, unique=True, search_index=True),
        col("short_name", "varchar", max_length=50),
        col("description", "text"),
        col("active", "boolean"),
    ],
    "sections": [
        legacy(),
        col("name", "varchar", mandatory=True, max_length=200, search_index=True),
        col("code", "varchar", max_length=50),
        col("section_code", "varchar", mandatory=True, max_length=50, search_index=True),
        col("act_id", "bigint", search_index=True),
        col("description", "text"),
        col("active", "boolean"),
    ],
    "districts": [
        legacy(),
        col("name", "varchar", mandatory=True, max_length=100, search_index=True),
        col("code", "varchar", mandatory=True, max_length=20, search_index=True),
        col("state", "varchar", max_length=50),
        col("state_id", "bigint", search_index=True),
        col("population", "int"),
        col("area_sq_km", "int"),
        col("active", "boolean"),
    ],
    "stations": [
        legacy(),
        col("name", "varchar", mandatory=True, max_length=100, search_index=True),
        col("code", "varchar", mandatory=True, max_length=20, search_index=True),
        col("type_id", "bigint"),
        col("parent_unit", "bigint"),
        col("nationality_id", "bigint"),
        col("state_id", "bigint", search_index=True),
        col("district_id", "bigint", search_index=True),
        col("address", "varchar", max_length=200),
        col("phone", "varchar", max_length=20),
        col("type", "varchar", max_length=50),
        col("active", "boolean"),
    ],
    "officers": [
        legacy(),
        col("badge_number", "varchar", mandatory=True, max_length=20, search_index=True),
        col("rank", "varchar", max_length=50),
        col("rank_id", "bigint"),
        col("station_id", "bigint", search_index=True),
        col("unit_id", "bigint"),
        col("designation_id", "bigint"),
        col("district_id", "bigint", search_index=True),
        col("kgid", "varchar", max_length=20),
        col("first_name", "varchar", max_length=100, search_index=True),
        col("dob", "date"),
        col("gender_id", "bigint"),
        col("blood_group_id", "bigint"),
        col("physically_challenged", "boolean"),
        col("appointment_date", "date"),
        col("specialization", "varchar", max_length=100),
        col("phone", "varchar", max_length=20),
        col("status", "varchar", max_length=20),
    ],
    # --- Core investigation ---
    "firs": [
        legacy(),
        col("fir_number", "varchar", mandatory=True, max_length=50, unique=True, search_index=True),
        col("title", "varchar", mandatory=True, max_length=200, search_index=True),
        col("description", "text"),
        col("crime_type", "varchar", mandatory=True, max_length=50, search_index=True),
        col("district", "varchar", mandatory=True, max_length=100, search_index=True),
        col("station", "varchar", max_length=100),
        col("status", "varchar", max_length=20),
        col("complainant_name", "varchar", max_length=100),
        col("complainant_phone", "varchar", max_length=20),
        col("date_filed", "datetime"),
    ],
    "cases": [
        legacy(),
        col("case_number", "varchar", mandatory=True, max_length=50, unique=True, search_index=True),
        col("crime_no", "varchar", max_length=50),
        col("title", "varchar", mandatory=True, max_length=200, search_index=True),
        col("description", "text"),
        col("crime_type", "varchar", mandatory=True, max_length=50, search_index=True),
        col("district", "varchar", mandatory=True, max_length=100, search_index=True),
        col("status", "varchar", max_length=20, search_index=True),
        col("priority", "varchar", max_length=20),
        col("officer_id", "bigint"),
        col("fir_id", "bigint", search_index=True),
        col("incident_from_date", "datetime"),
        col("incident_to_date", "datetime"),
        col("info_received_ps_date", "datetime"),
        col("latitude", "double"),
        col("longitude", "double"),
        col("brief_facts", "text"),
        col("case_category_id", "bigint"),
        col("gravity_offence_id", "bigint"),
        col("crime_major_head_id", "bigint"),
        col("crime_minor_head_id", "bigint"),
        col("case_status_id", "bigint"),
        col("court_id", "bigint"),
        col("police_person_id", "bigint"),
        col("police_station_id", "bigint"),
    ],
    "crimes": [
        legacy(),
        col("title", "varchar", mandatory=True, max_length=200, search_index=True),
        col("description", "text"),
        col("crime_type_id", "bigint", search_index=True),
        col("district_id", "bigint", search_index=True),
        col("location_id", "bigint"),
        col("status", "varchar", max_length=20, search_index=True),
        col("priority", "varchar", max_length=20),
        col("reported_by", "bigint"),
        col("occurred_at", "datetime", search_index=True),
    ],
    "persons": [
        legacy(),
        col("first_name", "varchar", mandatory=True, max_length=50, search_index=True),
        col("last_name", "varchar", mandatory=True, max_length=50, search_index=True),
        col("date_of_birth", "varchar", max_length=10),
        col("gender", "varchar", max_length=10),
        col("phone", "varchar", max_length=20),
        col("email", "varchar", max_length=100),
        col("address", "text"),
        col("district", "varchar", max_length=100, search_index=True),
        col("aadhar_number", "varchar", max_length=20),
    ],
    "criminals": [
        legacy(),
        col("person_id", "bigint", search_index=True),
        col("alias", "varchar", max_length=100, search_index=True),
        col("risk_score", "double"),
        col("status", "varchar", max_length=20),
        col("mo_description", "text"),
        col("behavioral_profile", "text"),
        col("first_offense_date", "varchar", max_length=10),
    ],
    "suspects": [
        legacy(),
        col("name", "varchar", mandatory=True, max_length=100, search_index=True),
        col("age", "int"),
        col("gender", "varchar", max_length=10),
        col("district", "varchar", max_length=100, search_index=True),
        col("status", "varchar", max_length=20),
        col("risk_score", "double"),
        col("description", "text"),
        col("physical_description", "text"),
        col("aliases", "text"),
    ],
    "victims": [
        legacy(),
        col("case_id", "bigint", mandatory=True, search_index=True),
        col("name", "varchar", mandatory=True, max_length=200, search_index=True),
        col("age_year", "int"),
        col("gender_id", "bigint"),
        col("is_police", "boolean"),
    ],
    "witnesses": [
        legacy(),
        col("person_id", "bigint", search_index=True),
        col("case_id", "bigint", search_index=True),
        col("statement", "text"),
        col("reliability", "varchar", max_length=20),
    ],
    "complainants": [
        legacy(),
        col("case_id", "bigint", mandatory=True, search_index=True),
        col("name", "varchar", mandatory=True, max_length=200, search_index=True),
        col("age_year", "int"),
        col("occupation_id", "bigint"),
        col("religion_id", "bigint"),
        col("caste_id", "bigint"),
        col("gender_id", "bigint"),
    ],
    "accused": [
        legacy(),
        col("case_id", "bigint", mandatory=True, search_index=True),
        col("name", "varchar", mandatory=True, max_length=200, search_index=True),
        col("age_year", "int"),
        col("gender_id", "bigint"),
        col("person_id", "varchar", max_length=10),
    ],
    "evidence": [
        legacy(),
        col("case_id", "bigint", search_index=True),
        col("evidence_type", "varchar", mandatory=True, max_length=50, search_index=True),
        col("description", "text"),
        col("status", "varchar", max_length=20),
        col("file_path", "varchar", max_length=500),
        col("file_id", "varchar", max_length=100, search_index=True),
        col("folder_id", "varchar", max_length=100),
        col("recorded_by", "bigint"),
    ],
    "vehicles": [
        legacy(),
        col("registration_number", "varchar", mandatory=True, max_length=20, unique=True, search_index=True),
        col("make", "varchar", max_length=50),
        col("model", "varchar", max_length=50),
        col("color", "varchar", max_length=30),
        col("type", "varchar", max_length=30),
        col("owner_id", "bigint"),
        col("status", "varchar", max_length=20),
    ],
    "phones": [
        legacy(),
        col("number", "varchar", mandatory=True, max_length=20, search_index=True),
        col("owner_id", "bigint", search_index=True),
        col("carrier", "varchar", max_length=50),
        col("type", "varchar", max_length=20),
        col("status", "varchar", max_length=20),
    ],
    "locations": [
        legacy(),
        col("name", "varchar", mandatory=True, max_length=200, search_index=True),
        col("address", "varchar", max_length=300),
        col("latitude", "double"),
        col("longitude", "double"),
        col("district_id", "bigint", search_index=True),
        col("type", "varchar", max_length=50),
    ],
    "investigations": [
        legacy(),
        col("case_id", "bigint", search_index=True),
        col("title", "varchar", mandatory=True, max_length=200, search_index=True),
        col("description", "text"),
        col("status", "varchar", max_length=20, search_index=True),
        col("priority", "varchar", max_length=20),
        col("officer_id", "bigint"),
        col("progress", "int"),
        col("district", "varchar", max_length=100, search_index=True),
        col("last_accessed", "datetime"),
    ],
    "notes": [
        legacy(),
        col("investigation_id", "bigint", mandatory=True, search_index=True),
        col("content", "text", mandatory=True),
        col("author_id", "bigint"),
    ],
    "timeline_events": [
        legacy(),
        col("investigation_id", "bigint", mandatory=True, search_index=True),
        col("title", "varchar", mandatory=True, max_length=200),
        col("description", "text"),
        col("event_type", "varchar", mandatory=True, max_length=50, search_index=True),
        col("event_date", "datetime", search_index=True),
    ],
    "case_links": [
        legacy(),
        col("investigation_id", "bigint", mandatory=True, search_index=True),
        col("linked_case_id", "bigint", mandatory=True, search_index=True),
        col("link_type", "varchar", mandatory=True, max_length=50),
        col("description", "varchar", max_length=200),
    ],
    "case_status_logs": [
        legacy(),
        col("investigation_id", "bigint", mandatory=True, search_index=True),
        col("old_status", "varchar", max_length=20),
        col("new_status", "varchar", mandatory=True, max_length=20),
        col("changed_by", "bigint"),
        col("notes", "text"),
        col("changed_at", "datetime"),
    ],
    "attachments": [
        legacy(),
        col("investigation_id", "bigint", mandatory=True, search_index=True),
        col("filename", "varchar", mandatory=True, max_length=200),
        col("file_path", "varchar", mandatory=True, max_length=500),
        col("file_id", "varchar", max_length=100, search_index=True),
        col("folder_id", "varchar", max_length=100),
        col("file_size", "int"),
        col("file_type", "varchar", max_length=50),
        col("uploaded_by", "bigint"),
    ],
}

# Seed / FK order (parents before children)
SEED_ORDER: list[str] = [
    "states",
    "unit_types",
    "ranks",
    "designations",
    "genders",
    "crime_types",
    "crime_heads",
    "crime_sub_heads",
    "case_categories",
    "case_status_master",
    "acts",
    "sections",
    "districts",
    "stations",
    "officers",
    "locations",
    "persons",
    "firs",
    "cases",
    "crimes",
    "criminals",
    "suspects",
    "complainants",
    "victims",
    "accused",
    "witnesses",
    "evidence",
    "vehicles",
    "phones",
    "investigations",
    "notes",
    "timeline_events",
    "case_links",
    "case_status_logs",
    "attachments",
]

FILE_STORE_FOLDER = "cm_uploads"

# Populate list projections (keep under 20 cols including ROWID)
_proj("states", ["legacy_id", "name", "code", "active"])
_proj("districts", ["legacy_id", "name", "code", "state", "state_id", "population", "active"])
_proj("stations", ["legacy_id", "name", "code", "district_id", "state_id", "phone", "active"])
_proj("officers", ["legacy_id", "badge_number", "first_name", "rank", "district_id", "station_id", "status", "phone"])
_proj("firs", ["legacy_id", "fir_number", "title", "crime_type", "district", "station", "status", "date_filed"])
_proj(
    "cases",
    [
        "legacy_id",
        "case_number",
        "title",
        "crime_type",
        "district",
        "status",
        "priority",
        "fir_id",
        "latitude",
        "longitude",
    ],
)
_proj(
    "crimes",
    [
        "legacy_id",
        "title",
        "crime_type_id",
        "district_id",
        "location_id",
        "status",
        "priority",
        "reported_by",
        "occurred_at",
    ],
)
_proj("persons", ["legacy_id", "first_name", "last_name", "phone", "district", "gender"])
_proj("criminals", ["legacy_id", "person_id", "alias", "risk_score", "status"])
_proj("suspects", ["legacy_id", "name", "age", "district", "status", "risk_score"])
_proj("investigations", ["legacy_id", "case_id", "title", "status", "priority", "officer_id", "progress", "district"])
_proj("notes", ["legacy_id", "investigation_id", "author_id"])
_proj("timeline_events", ["legacy_id", "investigation_id", "title", "event_type", "event_date"])
_proj("evidence", ["legacy_id", "case_id", "evidence_type", "status", "file_id", "folder_id"])
_proj("attachments", ["legacy_id", "investigation_id", "filename", "file_id", "folder_id", "file_size", "file_type"])
_proj("vehicles", ["legacy_id", "registration_number", "make", "model", "color", "status"])
_proj("phones", ["legacy_id", "number", "owner_id", "carrier", "status"])
_proj("locations", ["legacy_id", "name", "district_id", "latitude", "longitude", "type"])
_proj("complainants", ["legacy_id", "case_id", "name", "age_year", "gender_id"])
_proj("victims", ["legacy_id", "case_id", "name", "age_year", "gender_id"])
_proj("accused", ["legacy_id", "case_id", "name", "age_year", "gender_id"])
_proj("witnesses", ["legacy_id", "case_id", "person_id", "reliability"])
_proj("case_links", ["legacy_id", "investigation_id", "linked_case_id", "link_type"])
_proj("case_status_logs", ["legacy_id", "investigation_id", "old_status", "new_status", "changed_at"])
_proj("genders", ["legacy_id", "name", "code"])
_proj("crime_types", ["legacy_id", "name", "code", "severity_level"])
_proj("crime_heads", ["legacy_id", "name", "code", "active"])
_proj("crime_sub_heads", ["legacy_id", "name", "code", "crime_head_id"])
_proj("case_categories", ["legacy_id", "name", "code", "active"])
_proj("case_status_master", ["legacy_id", "name", "code"])
_proj("acts", ["legacy_id", "name", "act_code", "short_name", "active"])
_proj("sections", ["legacy_id", "name", "section_code", "act_id", "active"])
_proj("ranks", ["legacy_id", "name", "code", "hierarchy", "active"])
_proj("designations", ["legacy_id", "name", "code", "sort_order", "active"])
_proj("unit_types", ["legacy_id", "name", "code", "hierarchy", "active"])


def export_schema_json() -> dict[str, Any]:
    return {
        "phase": 1,
        "file_store_folder": FILE_STORE_FOLDER,
        "seed_order": SEED_ORDER,
        "list_projections": LIST_PROJECTIONS,
        "tables": {
            name: {"columns": cols} for name, cols in PHASE1_TABLES.items()
        },
        "notes": [
            "System columns ROWID/CREATORID/CREATEDTIME/MODIFIEDTIME are automatic.",
            "API id maps from ROWID; legacy_id holds original SQLite PK for seed remaps.",
            "ZCQL SELECT is limited to 20 columns and 300 rows — use list_projections + paging.",
            "Text fields max 10,000 characters in Data Store.",
        ],
    }
