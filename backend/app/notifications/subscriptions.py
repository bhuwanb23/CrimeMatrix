import uuid
from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()


class SubscriptionManager:
    def __init__(self):
        self._subscriptions: Dict[str, dict] = {}

    def create(self, user_id: str, event_type: str, channel: str = None) -> dict:
        sub_id = uuid.uuid4().hex[:12]
        subscription = {
            "id": sub_id,
            "user_id": user_id,
            "event_type": event_type,
            "channel": channel or event_type,
            "active": True,
            "created_at": __import__("datetime").datetime.now().isoformat(),
        }
        self._subscriptions[sub_id] = subscription
        logger.info("subscription_created", user_id=user_id, event_type=event_type)
        return subscription

    def get_user_subscriptions(self, user_id: str) -> List[dict]:
        return [s for s in self._subscriptions.values() if s["user_id"] == user_id]

    def get_subscribers(self, event_type: str) -> List[dict]:
        return [
            s for s in self._subscriptions.values()
            if s["event_type"] == event_type and s["active"]
        ]

    def remove(self, sub_id: str) -> bool:
        if sub_id in self._subscriptions:
            del self._subscriptions[sub_id]
            return True
        return False

    def get_subscription(self, sub_id: str) -> Optional[dict]:
        return self._subscriptions.get(sub_id)

    def list_all(self) -> List[dict]:
        return list(self._subscriptions.values())
