#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for updating Russian pymoprhy2 dictionaries.

Please note that it is resource-heavy: it requires > 3GB free RAM and about
1GB on HDD for temporary files.

Usage:
    update-ru.py (download|compile|package|cleanup) ...
    update-ru.py all
    update-ru.py -h | --help

"""
from __future__ import print_function
import os
import shutil
import subprocess

from docopt import docopt
from cookiecutter.main import cookiecutter
from pymorphy2 import opencorpora_dict


DICT_URL = "http://opencorpora.org/files/export/dict/dict.opcorpora.xml.bz2"
CORPORA_URL = "http://opencorpora.org/files/export/annot/annot.opcorpora.xml.bz2"
DICT_XML = "dict.opcorpora.xml"
CORPORA_XML = "annot.corpus.xml"
OUT_PATH = "compiled-dicts"


def _download_bz2(url, out_name):
    subprocess.check_call("curl --progress-bar '%s' | bunzip2 > '%s'" % (url, out_name), shell=True)


def download():
    print("Downloading OpenCorpora dictionary...")
    _download_bz2(DICT_URL, DICT_XML)
    print("Downloading OpenCorpora corpus...")
    _download_bz2(CORPORA_URL, CORPORA_XML)
    print("")


def build_dict():
    print("Compiling the dictionary")
    subprocess.check_call(["./build-dict.py", DICT_XML, OUT_PATH,
                           "--lang", "ru",
                           "--corpus", CORPORA_XML,
                           "--clear"])
    print("")


def gen_package():
    print("Creating Python package")
    cookiecutter("cookiecutter-pymorphy2-dicts", no_input=True, extra_context={
        'lang': 'ru',
        'lang_full': 'Russian',
        'version': get_version(),
    })


def cleanup():
    shutil.rmtree(OUT_PATH, ignore_errors=True)
    if os.path.exists(DICT_XML):
        os.unlink(DICT_XML)
    if os.path.exists(CORPORA_XML):
        os.unlink(CORPORA_XML)


def get_version():
    meta = dict(opencorpora_dict.load(OUT_PATH).meta)
    return "{format_version}.{source_revision}.{corpus_revision}".format(**meta)


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['all']:
        args['download'] = args['compile'] = args['package'] = True

    if args['download']:
        download()

    if args['compile']:
        build_dict()

    if args['package']:
        gen_package()

    if args['cleanup']:
        cleanup()
