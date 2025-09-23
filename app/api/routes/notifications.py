from flask import Blueprint, jsonify, session, abort, stream_with_context, Response
from ..services.notifications.helpers.stream import event_stream
from ..services.decorators.auth import session_required



api_v1_notifications = Blueprint('api_v1_notifications', __name__, url_prefix="/api/v1/notifications")


@api_v1_notifications.route('/', methods=["GET"])
def get_filtered_notifications():
    """ get specific notifications (ex: unread and from 0 -> 10) """
    return jsonify(message="read filtered notifications")

@api_v1_notifications.route('/read-all', methods=["PATCH"])
def change_all_notifications_status_to_read():
    """ read all notifications so the status changes into read"""
    return jsonify(message="read-all")

@api_v1_notifications.route('/<int:notification_id>/read', methods=["PATCH"])
def change_notification_status_to_read(notification_id:int):
    return jsonify(message=f"{notification_id} - status: read")

# SSE Notifications

@api_v1_notifications.route('/stream', methods=["GET"])
@session_required
def stream_notifications():
    """ SSE authenticated by session cookie """
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        # useful when behind Engine-X to avoid buffering
        "X-Accel-Buffering": "no",
    }
    return Response(stream_with_context(event_stream(user_id=user_id)), headers=headers)

