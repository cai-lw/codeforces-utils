import os
import json
from warnings import warn

_config_file = os.path.expanduser('~/.cfutils/config.json')
_config = None


def _get_config():
    global _config
    if _config is None:
        with open(_config_file) as f:
            _config = json.load(f)
    return _config


class Config:
    def __init__(self):
        pass

    @staticmethod
    def get_default_template(ext):
        obj = _get_config()['extension'].get(ext)
        if obj is None or obj.get('template') is None:
            warn('No template configuration for extension "{}". Creating blank file'.format(ext), RuntimeWarning)
            return ''
        return obj['template']

    @staticmethod
    def get_default_command(ext):
        obj = _get_config()['extension'].get(ext)
        if obj is None or obj.get('command') is None:
            raise ValueError('No command configuration for extension "{}"'.format(ext))
        return Config.get_command(obj['command'])

    @staticmethod
    def get_command(cmd):
        obj = _get_config()['command'].get(cmd)
        if obj is None or obj.get('run') is None:
            raise ValueError('No command configuration named "{}".'.format(cmd))
        return obj.get('compile', ''), obj['run']
