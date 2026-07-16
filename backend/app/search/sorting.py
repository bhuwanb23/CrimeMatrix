from typing import List, Dict


class SortEngine:
    @staticmethod
    def sort(items: List[Dict], sort_config: Dict = None) -> List[Dict]:
        if not sort_config:
            return items

        field = sort_config.get("field", "id")
        direction = sort_config.get("direction", "asc")
        reverse = direction == "desc"

        return sorted(items, key=lambda x: x.get(field, ""), reverse=reverse)
