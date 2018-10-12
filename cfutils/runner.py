import os
from os.path import join, abspath, splitext, exists, getmtime
from shlex import quote
from hashlib import md5
import subprocess
from .common import tmp_base

class BaseRunner:
    def __init__(self, config, filename):
        self._cmd_compile = config.get('compile', None)
        self._cmd_execute = config.get('execute', None)
        self._cmd_cleanup = config.get('cleanup', None)
        self._source = filename
        self._target = splitext(filename)[0]
        self._target_file = self._target

    def _cache_unchanged(self):
        if not exists(self._source) or not exists(self._target_file):
            return False
        source_hash = md5(abspath(self._source).encode()).hexdigest()
        cache_file = join(tmp_base, source_hash)
        if not exists(cache_file):
            return False
        mtimes = [int(getmtime(f)) for f in [self._source, self._target_file]]
        with open(cache_file) as f:
            cached_mtimes = [int(t) for t in f.readlines()]
        return mtimes == cached_mtimes

    def _write_cache(self):
        source_hash = md5(abspath(self._source).encode()).hexdigest()
        cache_file = join(tmp_base, source_hash)
        with open(cache_file, 'w') as f:
            print(int(getmtime(self._source)), file=f)
            print(int(getmtime(self._target_file)), file=f)

    def __enter__(self):
        if not self._cache_unchanged():
            cmd = self._cmd_compile.format(quote(self._source), quote(self._target_file))
            subprocess.run(cmd, shell=True, check=True)
            self._write_cache()
        return self

    def run(self, input=None):
        cmd = self._cmd_execute.format(quote(self._target))
        output = None if input is None else subprocess.PIPE
        return subprocess.run(cmd, shell=True, input=input, stdout=output, stderr=output, encoding='utf8')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._cmd_cleanup:
            cmd = self._cmd_cleanup.format(quote(self._target_file))
            subprocess.run(cmd, shell=True, check=True)


class CompileRunner(BaseRunner):
    def __init__(self, config, filename):
        super().__init__(config, filename)
        if os.name == 'nt':
            self._target_file += '.exe'


class InterpretRunner(BaseRunner):
    def __init__(self, config, filename):
        super().__init__(config, filename)
        self._target = filename

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class JvmRunner(BaseRunner):
    def __init__(self, config, filename):
        super().__init__(config, filename)
        self._target_file += '.class'
