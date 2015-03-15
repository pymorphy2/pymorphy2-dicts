#!/usr/bin/env bash
PACKAGE_DATA="{{ cookiecutter.package_name }}/data"

rm -r $PACKAGE_DATA
cp -r ../compiled-dicts $PACKAGE_DATA
