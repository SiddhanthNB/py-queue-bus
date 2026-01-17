"""
Scheduler worker example for queue_bus_schedule.

Recommended: use the official RQ CLI and your Redis URL under a supervisor:

    export REDIS_URL=redis://:password@host:port/db
    rq worker --with-scheduler --url "$REDIS_URL" queue_bus_schedule

Note:
1. RQ must be initialized with `--with-scheduler` to process scheduled jobs.
2. RQ CLI only supports Redis URL for connection config.
3. RQ CLI must specify the queue name `queue_bus_schedule` to process scheduled publishes.

This file is kept as a pointer to the recommended command.
"""

if __name__ == "__main__":
    print(__doc__)
