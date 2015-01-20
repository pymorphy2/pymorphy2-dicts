#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for updating pymorphy2 dictionary data.

Please note that it is resource-heavy: it requires > 3GB free RAM and about
1GB on HDD for temporary files.

Usage:
    update.py ru [--no-download] [--no-unlink] [--no-dict] [--no-prob]
    update.py -h | --help

Options:
    --no-download   Don't download XML files from opencorpora.org and and don't unlink them after processing
    --no-unlink     Don't unlink XML files after processing
    --no-dict       Don't compile fictionary
    --no-prob       Don't update P(t|w) estimates

"""

from __future__ import absolute_import, unicode_literals
import os
import bz2
import sys
import shutil
import logging
import datetime
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import opencorpora
from docopt import docopt

from pymorphy2 import opencorpora_dict
from pymorphy2 import cli
from pymorphy2.opencorpora_dict.storage import CURRENT_FORMAT_VERSION


ROOT = os.path.dirname(__file__)
OUT_PATH = os.path.join(ROOT, 'pymorphy2-dicts', 'pymorphy2_dicts', 'data')
VERSION_FILE_PATH = os.path.join(ROOT, 'pymorphy2-dicts', 'pymorphy2_dicts', 'version.py')
DICT_XML = os.path.join(ROOT, 'dict.xml')
CORPUS_XML = os.path.join(ROOT, 'annot.corpus.xml')

OPENCORPORA_XML_BZ2_URL = "http://opencorpora.org/files/export/dict/dict.opcorpora.xml.bz2"


def download_bz2(url, out_fp, chunk_size=256*1024, on_chunk=lambda: None):
    """
    Download a bz2-encoded file from ``url`` and write it to ``out_fp`` file.
    """
    decompressor = bz2.BZ2Decompressor()
    fp = urlopen(url, timeout=30)

    while True:
        data = fp.read(chunk_size)
        if not data:
            break
        out_fp.write(decompressor.decompress(data))
        on_chunk()


def download_opencorpora_dict(out_filename, verbose):
    """ Download an updated dictionary XML from OpenCorpora """
    def on_chunk():
        if verbose:
            sys.stdout.write('.')
            sys.stdout.flush()

    cli.logger.info('Creating %s from %s' % (out_filename, OPENCORPORA_XML_BZ2_URL))
    with open(out_filename, "wb") as f:
        download_bz2(OPENCORPORA_XML_BZ2_URL, f, on_chunk=on_chunk)

    cli.logger.info('\nDone.')


def download_opencorpora_corpus(out_filename):
    """ Download OpenCorpora corpus """
    from opencorpora.cli import _download, FULL_CORPORA_URL_BZ2
    return _download(
        out_file=out_filename,
        decompress=True,
        disambig=False,
        url=FULL_CORPORA_URL_BZ2,
        verbose=True
    )


def rebuild_dictionary(download=True, unlink=True):
    cli.logger.info("download: %s, unlink: %s", download, unlink)
    if download or not os.path.exists(DICT_XML):
        download_opencorpora_dict(DICT_XML, True)
    shutil.rmtree(OUT_PATH)
    cli.compile_dict(DICT_XML, OUT_PATH)
    if unlink:
        os.unlink(DICT_XML)


def reestimate_cpd(download=True, unlink=True):
    if download or not os.path.exists(CORPUS_XML):
        download_opencorpora_corpus(CORPUS_XML)
    cli.estimate_tag_cpd(CORPUS_XML, OUT_PATH, 1)
    rev = _get_corpus_revision(CORPUS_XML)
    if unlink:
        os.unlink(CORPUS_XML)
    return rev


def write_version(format_version, dict_revision, corpus_revision):
    contents = '__version__ = "{format_version}.{dict_revision}.{corpus_revision}"'.format(
        format_version=format_version,
        dict_revision=dict_revision,
        corpus_revision=corpus_revision,
    )
    with open(VERSION_FILE_PATH, 'wb') as f:
        f.write(contents.encode('utf8'))


def _get_corpus_revision(path):
    return opencorpora.CorpusReader(path).get_annotation_info()['revision']


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

    if args['ru']:
        should_download = not args['--no-download']
        should_unlink = not (args['--no-unlink'] or args['--no-download'])

        if not args['--no-dict']:
            rebuild_dictionary(should_download, should_unlink)

        corpus_rev = None
        if not args['--no-prob']:
            corpus_rev = reestimate_cpd(should_download, should_unlink)
        if corpus_rev is None:
            corpus_rev = _get_corpus_revision(CORPUS_XML)

        print('-' * 20)
        print("Done in %s\n" % (datetime.datetime.now() - start))

        write_version(
            CURRENT_FORMAT_VERSION,
            opencorpora_dict.load(OUT_PATH).meta['source_revision'],
            corpus_rev,
        )
        cli.show_dict_meta(OUT_PATH)

