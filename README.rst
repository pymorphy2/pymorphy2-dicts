pymorphy2-dicts
===============

Scripts for updating pymorphy2_ dictionaries. License is MIT.

To compile a dictionary from a source XML file in OpenCorpora XML format
use ``build-dict.py`` script.

``./cookiecutter-pymorphy2-dicts`` folder contains cookiecutter_ template
for creating language-specific pymorphy2-dicts-... packages.

``update-ru.py`` is a script for building pymorphy2-dicts-ru package with
Russian dictionaries for pymorphy2. It downloads data from
http://opencorpora.org, compiles the dictionary using ``build-dict.py`` script
and creates pymorphy2-dicts-ru package using cookiecutter_.

.. _pymorphy2: https://github.com/kmike/pymorphy2
.. _cookiecutter: https://github.com/audreyr/cookiecutter
