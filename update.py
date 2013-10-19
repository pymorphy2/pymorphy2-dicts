#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for updating pymorphy2 dictionary data.

Please note that it is resource-heavy: it requires > 3GB free RAM and about
1GB on HDD for temporary files.

Usage:
    update.py [--no-download] [--no-unlink] [--no-dict] [--no-prob]
    update.py -h | --help

Options:
    --no-download   Don't download XML files from opencorpora.org and and don't unlink them after processing
    --no-unlink     Don't unlink XML files after processing
    --no-dict       Don't compile fictionary
    --no-prob       Don't update P(t|w) estimates

"""

from __future__ import absolute_import, unicode_literals
import logging
import os
import datetime
import shutil

from pymorphy2.vendor.docopt import docopt
from pymorphy2 import opencorpora_dict
from pymorphy2 import cli
from pymorphy2.opencorpora_dict.storage import CURRENT_FORMAT_VERSION

ROOT = os.path.dirname(__file__)

OUT_PATH = os.path.join(ROOT, 'pymorphy2_dicts', 'data')
DICT_XML = os.path.join(ROOT, 'dict.xml')
CORPUS_XML = os.path.join(ROOT, 'annot.corpus.xml')
VERSION_FILE_PATH = os.path.join(ROOT, 'pymorphy2_dicts', 'version.py')


def rebuild_dictionary(download=True, unlink=True):
    cli.logger.info("download: %s, unlink: %s", download, unlink)
    if download or not os.path.exists(DICT_XML):
        cli.download_dict_xml(DICT_XML, True)
    shutil.rmtree(OUT_PATH)
    cli.compile_dict(DICT_XML, OUT_PATH)
    if unlink:
        os.unlink(DICT_XML)


def reestimate_cpd(download=True, unlink=True):
    if download or not os.path.exists(CORPUS_XML):
        cli.download_corpus_xml(CORPUS_XML)
    cli.estimate_tag_cpd(CORPUS_XML, OUT_PATH, 1)
    if unlink:
        os.unlink(CORPUS_XML)


def write_version():
    dct = opencorpora_dict.load(OUT_PATH)
    contents = '__version__ = "{format_version}.{source_revision}"'.format(
        format_version=CURRENT_FORMAT_VERSION,
        source_revision=dct.meta['source_revision']
    )
    with open(VERSION_FILE_PATH, 'wb') as f:
        f.write(contents.encode('utf8'))


if __name__ == '__main__':
    start = datetime.datetime.now()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-6s %(asctime)s  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    for handler in cli.logger.handlers:
        cli.logger.removeHandler(handler)

    args = docopt(__doc__)
    should_download = not args['--no-download']
    should_unlink = not (args['--no-unlink'] or args['--no-download'])

    if not args['--no-dict']:
        rebuild_dictionary(download=should_download, unlink=should_unlink)

    if not args['--no-prob']:
        reestimate_cpd(download=should_download, unlink=should_unlink)

    print('-'*20)
    print("Done in %s\n" % (datetime.datetime.now() - start))

    write_version()
    cli.show_dict_meta(OUT_PATH)

