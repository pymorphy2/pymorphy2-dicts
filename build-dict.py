#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for compiling dictionaries from OpenCorpora XML format
into pymorphy2 format.

Usage:
    build-dict.py <dict.xml> <out-folder> [--corpus <corpus.xml>] [options]
    build-dict.py -h | --help

Options:
    --lang <lang>                     Language constants to use. Allowed values are "ru" and "uk" [default: ru]
    --corpus <corpus.xml>             Path to an XML file with a corpus in OpenCorpora format used to estimate P(tag|word).
    --source-name <name>              Name of the source to put into dict meta [default: opencorpora.org]
    --clear                           Remove all files from <out-path>
    --min-ending-freq <NUM>           Prediction: min. number of suffix occurances [default: 2]
    --min-paradigm-popularity <NUM>   Prediction: min. number of lexemes for the paradigm [default: 3]
    --max-suffix-length <NUM>         Prediction: max. length of prediction suffixes [default: 5]
    --min-word-freq <NUM>             P(tag|word) estimation: min. word count in source corpus [default: 1]

Please note that it is can be resource-heavy, e.g. processing of
opencorpora.org Russian dictionary requires 3GB+ free RAM and 1GB+
on HDD for temporary files.
"""

from __future__ import absolute_import, unicode_literals
import sys
import os
import shutil
import logging

import opencorpora
from docopt import docopt

import pymorphy2.lang
from pymorphy2 import opencorpora_dict
from pymorphy2.opencorpora_dict.probability import add_conditional_tag_probability
from pymorphy2.opencorpora_dict.storage import update_meta


logger = logging.getLogger('pymorphy2')

ROOT = os.path.dirname(__file__)
OUT_PATH = os.path.join(ROOT, 'pymorphy2_dicts', 'data')
VERSION_FILE_PATH = os.path.join(ROOT, 'pymorphy2_dicts', 'version.py')


def write_version(format_version, dict_revision, corpus_revision):
    contents = '__version__ = "{format_version}.{dict_revision}.{corpus_revision}"'.format(
        format_version=format_version,
        dict_revision=dict_revision,
        corpus_revision=corpus_revision,
    )
    with open(VERSION_FILE_PATH, 'wb') as f:
        f.write(contents.encode('utf8'))


def get_corpus_revision(path):
    return opencorpora.CorpusReader(path).get_annotation_info()['revision']


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-6s %(asctime)s  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    args = docopt(__doc__)

    dict_xml = args['<dict.xml>']
    out_path = args['<out-folder>']

    try:
        lang = getattr(pymorphy2.lang, args['--lang'])
    except AttributeError:
        print("Unknown language code: %r" % args['--lang'])
        sys.exit(1)

    if os.path.exists(out_path):
        if args['--clear']:
            shutil.rmtree(out_path)
        else:
            logger.error("Output path exists: %r", out_path)
            sys.exit(1)

    compile_options = dict(
        (key.replace('-', '_'), int(args['--' + key]))
        for key in ('min-ending-freq', 'min-paradigm-popularity', 'max-suffix-length')
    )
    compile_options["paradigm_prefixes"] = lang.PARADIGM_PREFIXES

    opencorpora_dict.convert_to_pymorphy2(
        opencorpora_dict_path=dict_xml,
        out_path=out_path,
        source_name=args['--source-name'],
        language_code=args['--lang'],
        compile_options=compile_options,
    )

    if args["--corpus"]:
        add_conditional_tag_probability(
            corpus_filename=args["--corpus"],
            out_path=out_path,
            min_word_freq=int(args['--min-word-freq']),
            logger=logger,
        )
        rev = get_corpus_revision(args["--corpus"])
        meta_filename = os.path.join(out_path, "meta.json")
        update_meta(meta_filename, {"corpus_revision": rev})
