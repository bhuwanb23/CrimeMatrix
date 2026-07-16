import uuid
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import structlog

logger = structlog.get_logger()


class NotificationStore:
    def __init__(self):
        self._notifications: Dict[str, dict] = defaultdict(dict)

    def create(self, user_id: str, title: str, message: str, notif_type: str = "info", data: dict = None) -> dict:
        notif_id = uuid.uuid4().hex[:12]
        notification = {
            "id": notif_id,
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notif_type,
            "data": data or {},
            "read": False,
            "created_at": datetime.now().isoformat(),
        }
        self._notifications[user_id][notif_id] = notification
        logger.info("notification_created", user_id=user_id, type=notif_type)
        return notification

    def get_user_notifications(self, user_id: str, limit: int = 50, offset: int = 0) -> List[dict]:
        notifs = list(self._notifications.get(user_id, {}).values())
        notifs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return notifs[offset:offset + limit]

    def get_unread_count(self, user_id: str) -> int:
        notifs = self._notifications.get(user_id, {})
        return sum(1 for n in notifs.values() if not n.get("read", False))

    def mark_read(self, user_id: str, notif_id: str) -> bool:
        notif = self._notifications.get(user_id, {}).get(notif_id)
        if notif:
            notif["read"] = True
            return True
        return False

    def mark_all_read(self, user_id: str) -> int:
        count = 0
        for notif in self._notifications.get(user_id, {}).values():
            if not notif.get("read", False):
                notif["read"] = True
                count += 1
        return count

    def delete(self, user_id: str, notif_id: str) -> bool:
        user_notifs = self._notifications.get(user_id, {})
        if notif_id in user_notifs:
            del user_notifs[notif_id]
            return True
        return False

    def get_notification(self, user_id: str, notif_id: str) -> Optional[dict]:
        return self._notifications.get(user_id, {}).get(notif_id)
