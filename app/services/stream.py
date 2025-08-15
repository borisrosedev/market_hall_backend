# notifications_sse.py
from __future__ import annotations
import queue
import threading
import time
from typing import Dict, Set

# Map user_id -> Set[Queue[str]]
_user_streams: Dict[int, Set[queue.Queue]] = {}
_lock = threading.Lock()

def _get_user_queues(user_id: int) -> Set[queue.Queue]:
    with _lock:
        return _user_streams.setdefault(user_id, set())

def _register_client(user_id: int) -> queue.Queue:
    q: queue.Queue = queue.Queue()
    with _lock:
        _get_user_queues(user_id).add(q)
    return q

def _unregister_client(user_id: int, q: queue.Queue) -> None:
    with _lock:
        qs = _user_streams.get(user_id)
        if not qs: 
            return
        qs.discard(q)
        if not qs:
            _user_streams.pop(user_id, None)


def event_stream(user_id):
        q = _register_client(user_id)
        # first "ping" to fast open the stream client-side
        yield ": connected\n\n"
        try:
            last_ping = time.time()
            while True:
                try:
                    # attend un message (ou ping périodique)
                    msg = q.get(timeout=10)
                    yield msg
                except queue.Empty:
                    # heartbeat toutes les ~15s pour éviter les timeouts reverse proxy
                    now = time.time()
                    if now - last_ping > 15:
                        yield ": ping\n\n"
                        last_ping = now
        except GeneratorExit:
            pass
        finally:
            _unregister_client(user_id, q)
