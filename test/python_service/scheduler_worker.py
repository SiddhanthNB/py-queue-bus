from py_queue_bus import scheduler

# NOTE: Hardcoded config for local testing. In production, consider using env vars or a config file.
CONNECTION = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "namespace": "resque",
}


def main():
    try:
        scheduler.run_scheduler_worker(CONNECTION)
    except KeyboardInterrupt:
        print("Scheduler worker interrupted, exiting...")


if __name__ == "__main__":
    main()
