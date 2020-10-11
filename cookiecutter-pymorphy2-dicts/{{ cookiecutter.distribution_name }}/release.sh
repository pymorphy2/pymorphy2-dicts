#!/bin/sh
./setup.py sdist --formats=gztar upload
./setup.py bdist_wheel upload
