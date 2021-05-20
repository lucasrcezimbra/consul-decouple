import json
import os

from consul import Consul as Consul
from decouple import DEFAULT_ENCODING
from decouple import AutoConfig as AutoConfigBase
from decouple import Config as ConfigBase
from decouple import RepositoryEmpty
from requests.exceptions import ConnectionError, InvalidURL


class RepositoryConsulJson(RepositoryEmpty):
    def __init__(self, consul, key, encoding=DEFAULT_ENCODING):
        self.consul = consul
        self.key = key
        self.encoding = encoding
        self._data = None

    def load_data(self):
        _, rawdata = self.consul.kv.get(self.key)
        if rawdata:
            decoded_value = rawdata['Value'].decode(self.encoding)
            self._data = json.loads(decoded_value)
        else:
            self._data = {}

    @property
    def data(self):
        if self._data is None:
            self.load_data()

        return self._data

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]


class RepositoryConsulKV(RepositoryEmpty):
    def __init__(self, consul, encoding=DEFAULT_ENCODING):
        self.consul = consul
        self.encoding = encoding
        self.data = {}

    def load_key(self, key):
        _, rawdata = self.consul.kv.get(key)
        if rawdata:
            value = rawdata['Value'].decode(self.encoding)
            self.data[key] = value

    def __contains__(self, key):
        if key not in self.data:
            self.load_key(key)
        return key in self.data

    def __getitem__(self, key):
        key in self  # ensures load
        return self.data[key]


class AutoConfig(AutoConfigBase):
    def __init__(self, consul=None, json_kv=None, *args, **kwargs):
        """
        :param consul: Consul client used to get values
            If it's received, it will try to create from enviroment variables.
        :param json_kv: When receive this param will read only this key from Consul,
            parse as JSON and read keys from this JSON
        """
        self.consul = consul or self.consul_from_env()
        self.json_kv = json_kv
        super().__init__(*args, **kwargs)

    @staticmethod
    def consul_from_env():
        kwargs = {}
        expected_kwargs = {'host', 'port', 'token', 'scheme'}

        for key, value in os.environ.items():
            if not key.startswith('CONSUL'): continue
            kwarg = '_'.join(key.split('_')[1:]).lower()
            if kwarg in expected_kwargs:
                kwargs[kwarg] = value

        return Consul(**kwargs)

    def _load(self, path):
        if self.has_consul_connection():
            self._load_consul()
        else:
            super()._load(path)

    def _load_consul(self):
        if self.json_kv:
            self.config = ConfigBase(RepositoryConsulJson(self.consul, self.json_kv))
        else:
            self.config = ConfigBase(RepositoryConsulKV(self.consul))

    def has_consul_connection(self):
        try:
            self.consul.kv.get('ANY_KEY')
            return True
        except (ConnectionError, InvalidURL):
            return False


config = AutoConfig()
