#!/bin/sh

./setup.py sdist --formats=gztar,bztar upload
./setup.py bdist_wheel upload
