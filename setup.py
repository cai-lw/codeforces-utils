from setuptools import setup
from cfutils.common import base, template_base, tmp_base
import os

setup(
    name='codeforces-utils',
    version='0.0.1',
    packages=['cfutils'],
    install_requires=['beautifulsoup4', 'requests'],
    data_files=[
        (template_base, [os.path.join('templates', file) for file in os.listdir('templates')]),
        (base, ['config.json']),
        (tmp_base, [])
    ],
    entry_points={
        'console_scripts': [
            'cf = cfutils.__main__:main'
        ]
    }
)
