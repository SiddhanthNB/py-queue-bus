import sys
from pathlib import Path

import pytest
import fakeredis


root = Path(__file__).resolve().parents[1]
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))


@pytest.fixture()
def fake_redis(monkeypatch):
    """Provide a shared fakeredis instance and patch redis.Redis to use it."""
    server = fakeredis.FakeServer()
    client = fakeredis.FakeRedis(server=server, decode_responses=True)

    class PatchedFakeRedis(fakeredis.FakeRedis):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("server", server)
            kwargs.setdefault("decode_responses", True)
            super().__init__(*args, **kwargs)

    import redis

    # Patch the class to return FakeRedis instances (with same shared server)
    monkeypatch.setattr(redis, "Redis", PatchedFakeRedis)
    monkeypatch.setattr(
        redis,
        "from_url",
        lambda url, **kwargs: fakeredis.FakeRedis.from_url(
            url, server=server, decode_responses=kwargs.get("decode_responses", True)
        ),
    )
    return client


@pytest.fixture()
def default_connection():
    return {"host": "127.0.0.1", "port": 6379, "db": 0, "namespace": "resque"}
