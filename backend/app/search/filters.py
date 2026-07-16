from typing import List, Dict, Any


class FilterEngine:
    @staticmethod
    def apply(items: List[Dict], filters: List[Dict]) -> List[Dict]:
        result = items
        for f in filters:
            field = f.get("field", "")
            operator = f.get("operator", "eq")
            value = f.get("value")

            if operator == "eq":
                result = [i for i in result if i.get(field) == value]
            elif operator == "ne":
                result = [i for i in result if i.get(field) != value]
            elif operator == "in":
                result = [i for i in result if i.get(field) in value]
            elif operator == "like":
                result = [i for i in result if value.lower() in str(i.get(field, "")).lower()]
            elif operator == "gt":
                result = [i for i in result if (i.get(field) or 0) > value]
            elif operator == "lt":
                result = [i for i in result if (i.get(field) or 0) < value]
            elif operator == "gte":
                result = [i for i in result if (i.get(field) or 0) >= value]
            elif operator == "lte":
                result = [i for i in result if (i.get(field) or 0) <= value]
        return result
