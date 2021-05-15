from consul_decouple import RepositoryConsulKV


def test_init(consul):
    repository = RepositoryConsulKV(consul, encoding='utf')

    assert repository.consul == consul
    assert repository.encoding == 'utf'


def test_data(consul):
    key, value = 'foo', 'bar'
    consul.kv.put(key, value)

    repository = RepositoryConsulKV(consul)

    assert key in repository
    assert repository[key] == value


def test_getitem_without_contains(consul):
    key, value = 'foo', 'bar'
    consul.kv.put(key, value)

    repository = RepositoryConsulKV(consul)

    assert repository[key] == value
