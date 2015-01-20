#!/bin/sh
cd pymorphy2-dicts
./setup.py sdist --formats=gztar,bztar upload
./setup.py bdist_wheel upload
