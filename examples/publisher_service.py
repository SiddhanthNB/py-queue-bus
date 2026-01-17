"""
Publisher-only example: sends events to the bus.

Run:
    python publisher_service.py

Note:
    Config is hardcoded for clarity here. In production, pull from env/config. See README for deployment details.
"""
from datetime import datetime, timezone
from py_queue_bus import Bus

CONNECTION = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "namespace": "resque",
}
# Or use: CONNECTION = {"url": "redis://:password@127.0.0.1:6379/0", "namespace": "resque"}


def _log(msg):
    now = datetime.now(timezone.utc).isoformat()
    print(f"[PUB {now}] {msg}", flush=True)


def main():
    bus = Bus(connection=CONNECTION)
    bus.connect()

    payload = {"order_id": 101, "total": 12.34}
    bus.publish("order_created", payload)
    _log("Published order_created")

    payload = {"order_id": 103, "reason": "inventory_shortage"}
    bus.publish("order_failed", payload)
    _log("Published order_failed")

    bus.publish_heartbeat()
    _log("Published heartbeat_minutes trigger")


if __name__ == "__main__":
    main()
