#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for updating dictionary data.

Please note that it is resource-heavy: it requires > 3Gb free RAM and about
500M on HDD for temporary files.
"""

from __future__ import absolute_import, unicode_literals
import logging
import os
import datetime
import shutil

from pymorphy2 import opencorpora_dict
from pymorphy2.cli import download_xml, compile_dict, logger, show_dict_meta
from pymorphy2.opencorpora_dict.storage import CURRENT_FORMAT_VERSION

ROOT = os.path.dirname(__file__)

OUT_PATH = os.path.join(ROOT, 'pymorphy2_dicts', 'data')
XML_NAME = os.path.join(ROOT, 'dict.xml')
VERSION_FILE_PATH = os.path.join(ROOT, 'pymorphy2_dicts', 'version.py')

def rebuild_dictionary():
    download_xml(XML_NAME, True)
    shutil.rmtree(OUT_PATH)
    compile_dict(XML_NAME, OUT_PATH)
    os.unlink(XML_NAME)

def write_version():
    dct = opencorpora_dict.load(OUT_PATH)
    contents = '__version__ = "{format_version}.{source_revision}"'.format(
        format_version=CURRENT_FORMAT_VERSION,
        source_revision=dct.meta['source_revision']
    )
    with open(VERSION_FILE_PATH, 'wb') as f:
        f.write(contents.encode('utf8'))


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    start = datetime.datetime.now()
    rebuild_dictionary()

    print('-'*20)
    print("Done in %s\n" % (datetime.datetime.now() - start))

    write_version()
    show_dict_meta(OUT_PATH)

