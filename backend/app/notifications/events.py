import uuid
from datetime import datetime
from typing import Dict, List
from app.notifications.store import NotificationStore
from app.notifications.subscriptions import SubscriptionManager
import structlog

logger = structlog.get_logger()


class EventDispatcher:
    def __init__(self, store: NotificationStore, subs: SubscriptionManager):
        self.store = store
        self.subs = subs

    async def dispatch(self, event_type: str, title: str, message: str, data: dict = None) -> dict:
        subscribers = self.subs.get_subscribers(event_type)
        notifications = []

        for sub in subscribers:
            notif = self.store.create(
                user_id=sub["user_id"],
                title=title,
                message=message,
                notif_type=event_type,
                data=data or {},
            )
            notifications.append(notif)

        logger.info("event_dispatched", event_type=event_type, subscribers=len(subscribers))
        return {
            "event_type": event_type,
            "subscribers_notified": len(subscribers),
            "notifications": notifications,
        }

    def get_event_history(self) -> List[dict]:
        return []
