from setuptools import setup, find_packages
from os.path import join, dirname

import tracker


setup(
    name='tracker',
    version=tracker.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    )
