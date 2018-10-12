import os
import json
import requests
from bs4 import BeautifulSoup
from .common import tmp_base

class SampleFetcher:
    def __init__(self):
        pass

    def get(self):
        raise NotImplementedError


class CodeforcesSampleFetcher(SampleFetcher):
    def __init__(self, problem_id):
        super().__init__()
        self._url = 'https://codeforces.com/contest/{}/problem/{}'.format(problem_id[:-1], problem_id[-1])
        self._cache_file = os.path.join(tmp_base, 'CF' + problem_id + '.json')

    def get(self):
        if os.path.exists(self._cache_file):
            with open(self._cache_file) as f:
                return json.load(f)
        result = requests.get(self._url)
        result.raise_for_status()
        soup = BeautifulSoup(result.text, 'html.parser')
        inputs = []
        outputs = []
        for div in soup.find_all('div', class_='input'):
            inputs.append('\n'.join(div.find('pre').stripped_strings))
        for div in soup.find_all('div', class_='output'):
            outputs.append('\n'.join(div.find('pre').stripped_strings))
        ret = list(zip(inputs, outputs))
        with open(self._cache_file, 'w') as f:
            json.dump(ret, f, indent=2)
        return ret
