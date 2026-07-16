from typing import List, Dict, Any


class PaginationManager:
    @staticmethod
    def paginate(items: List[Dict], page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = items[start:end]

        return {
            "items": paginated,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if total > 0 else 0,
        }
