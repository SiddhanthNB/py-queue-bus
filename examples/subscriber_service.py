"""
Subscriber + rider: registers subscriptions and runs the worker.

Run (blocking):
    python subscriber_service.py

Note:
    Config is hardcoded for clarity here. In production, pull from env/config.
"""
from datetime import datetime, timezone
from py_queue_bus import Bus, Rider

CONNECTION = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "namespace": "resque",
}
APP_KEY = "example_service"
PRIORITY = "default"
QUEUE_NAME = f"{APP_KEY}_{PRIORITY}"


def _log(msg):
    now = datetime.now(timezone.utc).isoformat()
    print(f"[SUB {now}] {msg}", flush=True)


def order_created_handler(payload):
    _log(f"order_created_handler received: {payload}")


def order_failed_handler(payload):
    _log(f"order_failed_handler received: {payload}")


def heartbeat_handler(payload):
    _log(f"heartbeat_handler received: {payload}")


JOBS = {
    "order_created_job": order_created_handler,
    "order_failed_job": order_failed_handler,
    "heartbeat_job": heartbeat_handler,
}


def main():
    bus = Bus(connection=CONNECTION)
    bus.connect()

    # Register subscriptions
    bus.subscribe(APP_KEY, PRIORITY, "order_created_job", {"bus_event_type": "order_created"})
    bus.subscribe(APP_KEY, PRIORITY, "order_failed_job", {"bus_event_type": "order_failed"})
    bus.subscribe(APP_KEY, PRIORITY, "heartbeat_job", {"bus_event_type": "heartbeat_minutes"})
    _log(f"Subscribed to events on queue {QUEUE_NAME}")

    # Start rider to consume fanned-out jobs
    rider = Rider(connection=CONNECTION, jobs=JOBS, queues=[QUEUE_NAME], to_drive=True)
    rider.connect()
    _log("Starting rider...")
    rider.start()  # blocking


if __name__ == "__main__":
    main()
