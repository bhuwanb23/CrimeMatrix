from typing import Dict, List, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger()


class RecordMerger:
    def __init__(self):
        self._merge_log: List[dict] = []

    def merge(self, primary: Dict, secondary: Dict, entity_type: str = "person") -> Dict:
        merged = dict(primary)

        for key, value in secondary.items():
            if key in ("id", "created_at", "updated_at"):
                continue
            existing = merged.get(key)
            if not existing and value:
                merged[key] = value
            elif existing and value and key not in merged:
                merged[key] = value
            elif existing and value:
                if isinstance(value, str) and len(str(value)) > len(str(existing)):
                    merged[key] = value

        merge_record = {
            "primary_id": primary.get("id"),
            "secondary_id": secondary.get("id"),
            "entity_type": entity_type,
            "merged_at": datetime.now().isoformat(),
            "fields_updated": [k for k in secondary if k not in ("id", "created_at", "updated_at") and secondary.get(k)],
        }
        self._merge_log.append(merge_record)
        logger.info("records_merged", primary=primary.get("id"), secondary=secondary.get("id"))

        return merged

    def merge_batch(self, records: List[Dict], entity_type: str = "person") -> Dict:
        if not records:
            return {}

        primary = records[0]
        for secondary in records[1:]:
            primary = self.merge(primary, secondary, entity_type)
        return primary

    def get_merge_log(self) -> List[dict]:
        return list(self._merge_log)

    def suggest_best_fields(self, records: List[Dict]) -> Dict:
        if not records:
            return {}

        best = {}
        all_keys = set()
        for r in records:
            all_keys.update(r.keys())

        for key in all_keys:
            if key in ("id", "created_at", "updated_at"):
                continue
            values = [(r.get(key), len(str(r.get(key, "")))) for r in records if r.get(key)]
            if values:
                best[key] = max(values, key=lambda x: x[1])[0]
        return best
