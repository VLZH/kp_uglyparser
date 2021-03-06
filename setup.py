from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='kpuglyparser',
    version='1.7',
    packages=find_packages(),
    install_requires=[
        'grab',
        'htmlmin',
        'dateparser',
        'delorean',
        'bs4',
        'requests',
        'beaker',
        'fake-useragent',
        'pydash',
    ]
)
