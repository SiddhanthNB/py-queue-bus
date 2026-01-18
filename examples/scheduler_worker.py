"""
Minimal scheduler worker example using the official RQ CLI pattern.

Run under a supervisor (systemd/docker) so it restarts if Redis drops the connection:

    export REDIS_URL=redis://:password@host:port/db
    rq worker --with-scheduler --url "$REDIS_URL" queue_bus_schedule

This script shows the connection hash alongside a URL option for local testing.
"""
from datetime import datetime, timezone
from py_queue_bus.scheduler import run_scheduler_worker

# Hardcoded for clarity; in production, pull from env/config.
CONNECTION = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "namespace": "resque",
}
# Or use: CONNECTION = {"url": "redis://:password@127.0.0.1:6379/0", "namespace": "resque"}



def _log(msg: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    print(f"[SCHEDULER {now}] {msg}", flush=True)


def main() -> None:
    _log("Starting scheduler worker...")
    run_scheduler_worker(CONNECTION, with_scheduler=True)


if __name__ == "__main__":
    main()
