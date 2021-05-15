import json
import os

from consul import Consul as Consul
from decouple import DEFAULT_ENCODING
from decouple import AutoConfig as AutoConfigBase
from decouple import Config as ConfigBase
from decouple import RepositoryEmpty
from requests.exceptions import ConnectionError


class RepositoryConsulJson(RepositoryEmpty):
    def __init__(self, consul, key, encoding=DEFAULT_ENCODING):
        self.consul = consul
        self.key = key
        self.encoding = encoding
        self._data = None

    @property
    def data(self):
        if self._data is None:
            _, rawdata = self.consul.kv.get(self.key)
            decoded_value = rawdata['Value'].decode(self.encoding)
            self._data = json.loads(decoded_value)

        return self._data

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]


class AutoConfig(AutoConfigBase):
    def __init__(self, consul=None, key=None, *args, **kwargs):
        # TODO: docs
        self.consul = consul or self.consul_from_env()
        self.key = key
        super().__init__(*args, **kwargs)

    @staticmethod
    def consul_from_env():
        kwargs = {
            '_'.join(k.split('_')[1:]).lower(): v
            for k, v in os.environ.items()
            if k.startswith('CONSUL')
        }
        return Consul(**kwargs)

    def _load(self, path):
        if self.has_consul_connection():
            self.config = ConfigBase(RepositoryConsulJson(self.consul, self.key))
        else:
            super()._load(path)

    def has_consul_connection(self):
        try:
            self.consul.kv.get('ANY_KEY')
            return True
        except ConnectionError:
            return False
