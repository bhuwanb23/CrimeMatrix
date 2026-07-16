import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.notifications.manager import ConnectionManager
from app.notifications.store import NotificationStore
from app.notifications.alerts import AlertQueue
from app.notifications.subscriptions import SubscriptionManager
from app.notifications.events import EventDispatcher
from app.core.response import success_response
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

manager = ConnectionManager()
store = NotificationStore()
alert_queue = AlertQueue()
subscriptions = SubscriptionManager()
dispatcher = EventDispatcher(store, subscriptions)


# WebSocket
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("type") == "subscribe":
                    manager.subscribe_client(client_id, msg.get("channel", "default"))
                    await websocket.send_json({"type": "subscribed", "channel": msg.get("channel")})
                elif msg.get("type") == "unsubscribe":
                    manager.unsubscribe_client(client_id, msg.get("channel", "default"))
                    await websocket.send_json({"type": "unsubscribed", "channel": msg.get("channel")})
                else:
                    await websocket.send_json({"type": "echo", "data": msg})
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
    except WebSocketDisconnect:
        manager.disconnect(client_id)


# Notifications CRUD
@router.get("/notifications")
async def list_notifications(user_id: str = "default", limit: int = 50, offset: int = 0):
    notifs = store.get_user_notifications(user_id, limit, offset)
    return success_response(data={"notifications": notifs, "total": len(notifs)})


@router.get("/notifications/unread-count")
async def unread_count(user_id: str = "default"):
    count = store.get_unread_count(user_id)
    return success_response(data={"count": count})


@router.put("/notifications/{notif_id}/read")
async def mark_read(notif_id: str, user_id: str = "default"):
    result = store.mark_read(user_id, notif_id)
    return success_response(message="Marked as read" if result else "Not found")


@router.put("/notifications/read-all")
async def mark_all_read(user_id: str = "default"):
    count = store.mark_all_read(user_id)
    return success_response(data={"marked": count})


@router.delete("/notifications/{notif_id}")
async def delete_notification(notif_id: str, user_id: str = "default"):
    result = store.delete(user_id, notif_id)
    return success_response(message="Deleted" if result else "Not found")


class SendNotificationRequest(BaseModel):
    user_id: str = "default"
    title: str
    message: str
    notif_type: str = "info"
    data: Optional[Dict[str, Any]] = None


@router.post("/notifications/send")
async def send_notification(data: SendNotificationRequest):
    notif = store.create(data.user_id, data.title, data.message, data.notif_type, data.data)
    await manager.broadcast({"type": "notification", "data": notif})
    return success_response(data=notif, message="Notification sent")


# Subscriptions
class SubscriptionRequest(BaseModel):
    user_id: str = "default"
    event_type: str
    channel: Optional[str] = None


@router.get("/subscriptions")
async def list_subscriptions(user_id: str = "default"):
    subs = subscriptions.get_user_subscriptions(user_id)
    return success_response(data=subs)


@router.post("/subscriptions")
async def create_subscription(data: SubscriptionRequest):
    sub = subscriptions.create(data.user_id, data.event_type, data.channel)
    return success_response(data=sub, message="Subscription created")


@router.delete("/subscriptions/{sub_id}")
async def remove_subscription(sub_id: str):
    result = subscriptions.remove(sub_id)
    return success_response(message="Removed" if result else "Not found")


# Alerts
class AlertSubmitRequest(BaseModel):
    alert_type: str
    title: str
    message: str
    priority: str = "medium"
    data: Optional[Dict[str, Any]] = None


@router.post("/alerts")
async def submit_alert(data: AlertSubmitRequest):
    alert = alert_queue.submit(data.alert_type, data.title, data.message, data.priority, data.data)
    await manager.broadcast({"type": "alert", "data": alert})
    return success_response(data=alert, message="Alert submitted")


@router.get("/alerts")
async def list_alerts(status: str = None):
    alerts = alert_queue.list_alerts(status)
    stats = alert_queue.get_stats()
    return success_response(data={"alerts": alerts, "stats": stats})


@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    alert = alert_queue.get_alert(alert_id)
    if not alert:
        return success_response(message="Alert not found")
    return success_response(data=alert)


# Event Push
class PushEventRequest(BaseModel):
    event_type: str
    title: str
    message: str
    data: Optional[Dict[str, Any]] = None


@router.post("/push")
async def push_event(data: PushEventRequest):
    result = await dispatcher.dispatch(data.event_type, data.title, data.message, data.data)
    await manager.broadcast({"type": "event", "event_type": data.event_type, "title": data.title})
    return success_response(data=result, message="Event pushed")


# Connection Info
@router.get("/connections")
async def get_connections():
    return success_response(data={
        "connected_clients": manager.get_connected_clients(),
        "client_count": manager.get_client_count(),
    })
