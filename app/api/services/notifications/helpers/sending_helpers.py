from ..utils.sse import _format_sse
from .stream import _user_streams
from .stream import _lock

def push_to_user(user_id: int, event: str, data: dict) -> None:
    msg = _format_sse(event, data)
    with _lock:
        for q in _user_streams.get(user_id, ()):
            q.put(msg)

def push_to_all(event: str, data: dict) -> None:
    msg = _format_sse(event, data)
    with _lock:
        for queues in _user_streams.values():
            for q in queues:
                q.put(msg)
