pymorphy2-dicts
===============

Scripts for updating pymorphy2_ dictionaries. License is MIT.

To compile a dictionary from a source XML file in OpenCorpora XML format
use ``build-dict.py`` script.

``./cookiecutter-pymorphy2-dicts`` folder contains cookiecutter_ template
for creating language-specific pymorphy2-dicts-... packages.

``update.py`` is a script for building pymorphy2-dicts-ru and
pymorphy2-dicts-uk packages with Russian and Ukrainian dictionaries
for pymorphy2.

For Russian it downloads data from http://opencorpora.org,
compiles the dictionary using ``build-dict.py`` script
and creates pymorphy2-dicts-ru package using cookiecutter_.

For Ukrainian it downloads LanguageTool_ data from Google Drive,
converts dictionary to OpenCorpora format using LT2OpenCorpora_, then
compiles it and creates pymorphy2-dicts-uk package.

.. _LanguageTool: https://languagetool.org/
.. _LT2OpenCorpora: https://github.com/dchaplinsky/LT2OpenCorpora
.. _pymorphy2: https://github.com/kmike/pymorphy2
.. _cookiecutter: https://github.com/audreyr/cookiecutter
