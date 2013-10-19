#!/usr/bin/env python
from distutils.core import setup

def get_version():
    with open("pymorphy2_dicts/version.py", "rt") as f:
        return f.readline().split("=")[1].strip(' "\n')

setup(
    name = 'pymorphy2-dicts',
    version = get_version(),
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',
    url = 'https://github.com/kmike/pymorphy2-dicts/',

    description = 'OpenCorpora.org dictionaries pre-compiled for pymorphy2',
    long_description = open('README.rst').read(),

    license = 'MIT license',
    packages = ['pymorphy2_dicts'],
    package_data = {'pymorphy2_dicts': ['data/*']},

    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Russian',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing :: Linguistic',
    ],
)
