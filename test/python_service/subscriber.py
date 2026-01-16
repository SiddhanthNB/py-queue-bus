from datetime import datetime, timezone
from py_queue_bus import Bus, Rider

# NOTE: Hardcoded config for local testing. In production, consider using env vars or a config file.
CONNECTION = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "namespace": "resque",
}

APP_KEY = "py_service"
PRIORITY = "default"
QUEUE = f"{APP_KEY}_{PRIORITY}"


def _log(msg):
    now = datetime.now(timezone.utc).isoformat()
    print(f"[PY SUB {now}] {msg}", flush=True)

# Explicit handlers
def handle_node_event(payload):
    _log(f"handle_node_event received payload: {payload}")

def handle_python_event(payload):
    _log(f"handle_python_event received payload: {payload}")

def handle_python_event_delayed(payload):
    _log(f"handle_python_event_delayed received payload: {payload}")

def handle_python_event_scheduled(payload):
    _log(f"handle_python_event_scheduled received payload: {payload}")

def handle_heartbeat(payload):
    _log(f"handle_heartbeat received payload: {payload}")

jobs = {
    "node_event": handle_node_event,
    "python_event": handle_python_event,
    "python_event_delayed": handle_python_event_delayed,
    "python_event_scheduled": handle_python_event_scheduled,
    "heartbeat_minutes": handle_heartbeat,
}


def main():
    bus = Bus(connection=CONNECTION)
    bus.connect()

    bus.subscribe(APP_KEY, PRIORITY, "node_event", {"bus_event_type": "node_event"})
    bus.subscribe(APP_KEY, PRIORITY, "python_event", {"bus_event_type": "python_event"})
    bus.subscribe(APP_KEY, PRIORITY, "python_event_delayed", {"bus_event_type": "python_event_delayed"})
    bus.subscribe(APP_KEY, PRIORITY, "python_event_scheduled", {"bus_event_type": "python_event_scheduled"})
    bus.subscribe(APP_KEY, PRIORITY, "heartbeat_minutes", {"bus_event_type": "heartbeat_minutes"})
    _log(f"Subscribed to events on queue {QUEUE}")

    rider = Rider(connection=CONNECTION, jobs=jobs, queues=[QUEUE], to_drive=True)
    rider.connect()
    _log("Starting rider...")
    rider.start()


if __name__ == "__main__":
    main()
