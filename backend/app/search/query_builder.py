from typing import List, Dict, Any, Optional


class QueryBuilder:
    def __init__(self):
        self.filters: List[Dict] = []
        self.sort: Optional[Dict] = None
        self.page: int = 1
        self.page_size: int = 20
        self.facets: List[str] = []
        self.entities: List[str] = []

    def add_filter(self, field: str, operator: str = "eq", value: Any = None):
        self.filters.append({"field": field, "operator": operator, "value": value})
        return self

    def set_sort(self, field: str, direction: str = "asc"):
        self.sort = {"field": field, "direction": direction}
        return self

    def set_page(self, page: int, page_size: int = 20):
        self.page = page
        self.page_size = page_size
        return self

    def add_facet(self, field: str):
        self.facets.append(field)
        return self

    def add_entity(self, entity: str):
        self.entities.append(entity)
        return self

    def build(self) -> Dict[str, Any]:
        return {
            "filters": self.filters,
            "sort": self.sort,
            "page": self.page,
            "page_size": self.page_size,
            "facets": self.facets,
            "entities": self.entities,
        }

    def to_dict(self) -> Dict[str, Any]:
        return self.build()
