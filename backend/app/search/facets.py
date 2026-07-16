from typing import List, Dict


class FacetEngine:
    @staticmethod
    def compute(items: List[Dict], fields: List[str]) -> Dict[str, Dict[str, int]]:
        facets = {}
        for field in fields:
            counts = {}
            for item in items:
                value = item.get(field, "unknown")
                if isinstance(value, str):
                    counts[value] = counts.get(value, 0) + 1
            facets[field] = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
        return facets
