#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for updating pymoprhy2 dictionaries (Russian and Ukrainian).

Please note that it is resource-heavy: it requires > 3GB free RAM and about
1GB on HDD for temporary files.

Usage:
    update.py (ru|uk) (download|compile|package|cleanup) ...
    update.py (ru|uk) all
    update.py -h | --help

"""
from __future__ import print_function
import os
import time
import shutil
import subprocess

from docopt import docopt
from cookiecutter.main import cookiecutter
from pymorphy2 import opencorpora_dict

OUT_PATH = "compiled-dicts"

RU_DICT_URL = "http://opencorpora.org/files/export/dict/dict.opcorpora.xml.bz2"
RU_CORPORA_URL = "http://opencorpora.org/files/export/annot/annot.opcorpora.xml.bz2"
RU_DICT_XML = "dict.opcorpora.xml"
RU_CORPORA_XML = "annot.corpus.xml"

UK_DICT_URL = "https://drive.google.com/uc?id=0B4mUAylazDVbUXFIRGJ2S01ibGM&export=download"
UK_DICT_XML = "full-uk.xml"


def _download_bz2(url, out_name):
    subprocess.check_call("curl --progress-bar '%s' | bunzip2 > '%s'" % (url, out_name), shell=True)


class RussianBuilder(object):
    def download(self):
        print("Downloading OpenCorpora dictionary...")
        _download_bz2(RU_DICT_URL, RU_DICT_XML)
        print("Downloading OpenCorpora corpus...")
        _download_bz2(RU_CORPORA_URL, RU_CORPORA_XML)
        print("")

    def compile(self):
        print("Compiling the dictionary")
        subprocess.check_call(["./build-dict.py", RU_DICT_XML, OUT_PATH,
                               "--lang", "ru",
                               "--corpus", RU_CORPORA_XML,
                               "--clear"])
        print("")

    def package(self):
        print("Creating Python package")
        cookiecutter("cookiecutter-pymorphy2-dicts", no_input=True, extra_context={
            'lang': 'ru',
            'lang_full': 'Russian',
            'version': get_version(corpus=True, timestamp=False),
        })

    def cleanup(self):
        shutil.rmtree(OUT_PATH, ignore_errors=True)
        if os.path.exists(RU_DICT_XML):
            os.unlink(RU_DICT_XML)
        if os.path.exists(RU_CORPORA_XML):
            os.unlink(RU_CORPORA_XML)


class UkrainianBuilder(object):
    def download(self):
        print("Downloading and converting LanguageTool dictionary...")
        subprocess.check_call(['lt_convert.py', UK_DICT_URL, UK_DICT_XML])
        print("")

    def compile(self):
        print("Compiling the dictionary")
        subprocess.check_call(["./build-dict.py", UK_DICT_XML, OUT_PATH,
                               "--lang", "uk",
                               "--clear"])
        print("")

    def package(self):
        print("Creating Python package")
        cookiecutter("cookiecutter-pymorphy2-dicts", no_input=True, extra_context={
            'lang': 'uk',
            'lang_full': 'Ukrainian',
            'version': get_version(corpus=False, timestamp=True),
        })

    def cleanup(self):
        shutil.rmtree(OUT_PATH, ignore_errors=True)
        if os.path.exists(RU_DICT_XML):
            os.unlink(RU_DICT_XML)


def get_version(corpus=False, timestamp=False):
    meta = dict(opencorpora_dict.load(OUT_PATH).meta)
    if corpus:
        tpl = "{format_version}.{source_revision}.{corpus_revision}"
    else:
        tpl = "{format_version}.{source_revision}.1"
    if timestamp:
        tpl += ".%s" % (int(time.time()))
    return tpl.format(**meta)


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['all']:
        args['download'] = args['compile'] = args['package'] = True

    if args['ru']:
        builder = RussianBuilder()
    elif args['uk']:
        builder = UkrainianBuilder()
    else:
        raise ValueError("Language is not known")

    if args['download']:
        builder.download()

    if args['compile']:
        builder.compile()

    if args['package']:
        builder.package()

    if args['cleanup']:
        builder.cleanup()
