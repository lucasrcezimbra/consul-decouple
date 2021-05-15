import pytest
from consul import Consul

# TODO: docker-compose up consul


@pytest.fixture
def consul():
    consul = Consul()
    yield consul
    # TODO: improves to don't delete all
    _, keys = consul.kv.get('', keys=True)
    if keys:
        [consul.kv.delete(k) for k in keys]
