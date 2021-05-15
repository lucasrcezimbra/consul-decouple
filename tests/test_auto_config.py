import json
from pathlib import Path

from consul import Consul

from consul_decouple import AutoConfig


def test_config_environ(mocker):
    key, value = 'foo', 'bar'
    mocker.patch.dict('os.environ', {key: value})

    config = AutoConfig(key=key)

    assert config(key) == value


def test_init(mocker):
    consul, key, search_path = mocker.MagicMock(), 'key', './'

    config = AutoConfig(consul=consul, key=key, search_path=search_path)

    assert config.consul == consul
    assert config.key == key
    assert config.search_path == search_path
    assert config.config is None


def test_init_consul_from_env(mocker):
    host = 'localhost'
    port = '8600'
    token = 'RANDOM_TOKEN'
    scheme = 'https'
    mocker.patch.dict('os.environ', {
        'CONSUL_HOST': host,
        'CONSUL_PORT': port,
        'CONSUL_SCHEME': scheme,
        'CONSUL_TOKEN': token,
    })

    config = AutoConfig()

    assert config.consul.http.host == host
    assert config.consul.http.port == port
    assert config.consul.token == token
    assert config.consul.http.scheme == scheme


def test_consul_from_env(mocker):
    host = 'localhost'
    port = '8600'
    token = 'RANDOM_TOKEN'
    scheme = 'https'
    mocker.patch.dict('os.environ', {
        'CONSUL_HOST': host,
        'CONSUL_PORT': port,
        'CONSUL_SCHEME': scheme,
        'CONSUL_TOKEN': token,
    })

    consul = AutoConfig.consul_from_env()

    assert consul.http.host == host
    assert consul.http.port == port
    assert consul.token == token
    assert consul.http.scheme == scheme


def test_has_consul_connection(consul):
    assert AutoConfig(consul).has_consul_connection() is True

    consul_without_connection = Consul(host='wrong_host')
    assert AutoConfig(consul_without_connection).has_consul_connection() is False


def test_autoconfig_consul_key(consul):
    key, value = 'k1', {'v1': '1', 'v2': '2'}
    consul.kv.put(key, json.dumps(value))

    config = AutoConfig(consul, key=key)

    assert config('v1') == '1'
    assert config('v2') == '2'


def test_autoconfig_consul_from_env(consul):
    key, value = 'k1', {'v1': '1', 'v2': '2'}
    consul.kv.put(key, json.dumps(value))

    config = AutoConfig(key=key)

    assert config('v1') == '1'
    assert config('v2') == '2'


def test_autoconfig_ini(mocker):
    consul_without_connection = Consul(host='wrong_host')
    config = AutoConfig(consul=consul_without_connection)
    path = Path(__file__).parent / 'ini'
    mocker.patch.object(config, '_caller_path', return_value=path)

    assert config('KEY') == 'INI'


def test_autoconfig_env(mocker):
    consul_without_connection = Consul(host='wrong_host')
    config = AutoConfig(consul=consul_without_connection)
    path = Path(__file__).parent / 'env'
    mocker.patch.object(config, '_caller_path', return_value=path)

    assert config('KEY') == 'ENV'


def test_autoconfig_consul_without_key(consul):
    key, value = 'k1', 'v1'
    consul.kv.put(key, value)

    config = AutoConfig(consul)

    assert config(key) == 'v1'
