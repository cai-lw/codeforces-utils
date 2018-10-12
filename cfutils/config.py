import json
from .common import config_file


class ConfigDict:
    def __init__(self, data):
        self._data = data

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __getattr__(self, key):
        return self._data[key]

    def __getitem__(self, key):
        return self._data[key]


class ConfigList:
    def __init__(self, data=None):
        self._data = data

    def __getitem__(self, i):
        return self._data[i]


def configify(obj):
    if isinstance(obj, dict):
        return ConfigDict({k: configify(v) for k, v in obj.items()})
    elif isinstance(obj, list):
        return ConfigList([configify(o) for o in obj])
    else:
        return obj


with open(config_file) as f:
    config = configify(json.load(f))