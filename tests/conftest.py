import pytest
from consul import Consul

# TODO: docker-compose up consul


@pytest.fixture
def consul():
    consul = Consul()
    yield consul
    _, keys = consul.kv.get('', keys=True)
    if keys:
        [consul.kv.delete(k) for k in keys]
