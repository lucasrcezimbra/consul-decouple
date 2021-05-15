import json

import pytest

from consul_decouple import RepositoryConsulJson


def test_init(consul):
    repository = RepositoryConsulJson(consul, 'key')

    assert repository.consul == consul
    assert repository.key == 'key'


def test_data(consul):
    key = 'foo'
    value = {
        'k1': 'v1',
        'k2': 'v2',
    }
    consul.kv.put(key, json.dumps(value))

    repository = RepositoryConsulJson(consul, key)

    assert repository.data == value


def test_data_empty_should_call_consul_once(mocker, consul):
    key, value = 'foo', {}
    consul.kv.put(key, json.dumps(value))

    repository = RepositoryConsulJson(consul, key)

    get_spy = mocker.spy(repository.consul.kv, 'get')
    repository.data
    repository.data
    get_spy.assert_called_once_with(key)


def test_contains(consul):
    key = 'foo'
    value = {
        'k1': 'v1',
        'k2': 'v2',
    }
    consul.kv.put(key, json.dumps(value))

    repository = RepositoryConsulJson(consul, key)

    assert 'k1' in repository
    assert 'k2' in repository
    assert 'k3' not in repository


def test_getitem(consul):
    key = 'foo'
    value = {
        'k1': 'v1',
        'k2': 'v2',
    }
    consul.kv.put(key, json.dumps(value))

    repository = RepositoryConsulJson(consul, key)

    assert repository['k1'] == 'v1'
    assert repository['k2'] == 'v2'
    with pytest.raises(KeyError):
        repository['k3']


def test_get_nonexistent(consul):
    json_kv = 'nonexistent'

    repository = RepositoryConsulJson(consul, json_kv)

    assert repository.data == {}
