import sys

from setuptools import find_packages
from setuptools import setup

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, "Hive Plug & Play requires Python 3.6 or newer"

setup(
    name='hive_plug_play',
    version='0.2.0',
    description='Customizable block streaming and parsing microservice for custom_json ops on Hive.',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['scripts']),
    install_requires=[
        'psycopg2',
        'requests',
        'aiohttp',
        'jsonrpcserver'
    ],
    entry_points = {
        'console_scripts': [
            'hive_plug_play = hive_plug_play.run_plug_play:run'
        ]
    }
)