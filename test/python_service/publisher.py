import time
from datetime import datetime, timezone
from py_queue_bus import Bus

# NOTE: Hardcoded config for local testing. In production, consider using env vars or a config file.
CONNECTION = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "namespace": "resque",
}


def _log(msg):
    now = datetime.now(timezone.utc).isoformat()
    print(f"[PY PUB {now}] {msg}", flush=True)


def main():
    bus = Bus(connection=CONNECTION)
    bus.connect()

    # Single explicit event to demonstrate cross-service publish
    payload = {"msg": "hello from python", "ts": time.time()}
    bus.publish("python_event", payload)
    _log(f"Published python_event -> {payload}")

    # Scheduled events (require RQ worker running)
    now_ms = int(time.time() * 1000)
    bus.publish_in(2000, "python_event_delayed", {"msg": "delayed via publish_in", "ts": time.time()})
    _log("Scheduled python_event_delayed via publish_in (2s) [requires RQ worker]")

    future_ms = now_ms + 4000
    bus.publish_at(future_ms, "python_event_scheduled", {"msg": "scheduled via publish_at", "ts": time.time()})
    _log("Scheduled python_event_scheduled via publish_at (4s) [requires RQ worker]")


if __name__ == "__main__":
    main()
