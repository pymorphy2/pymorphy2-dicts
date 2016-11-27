{{ cookiecutter.distribution_name }}
==========================================================

{{ cookiecutter.lang_full }} dictionaries for `pymorphy2`_.

.. _pymorphy2: https://github.com/kmike/pymorphy2

Installation
------------

Install::

    $ pip install {{ cookiecutter.distribution_name }}

Usage
-----

To use these dictionaries with pymorphy2 create MorphAnalyzer
with ``lang='{{ cookiecutter.lang }}'`` parameter:

>>> import pymorphy2
>>> morph = pymorphy2.MorphAnalyzer(lang='{{ cookiecutter.lang }}')

To get a path to the installed dictionary data use
``{{ cookiecutter.package_name }}.get_path()`` method.

Development
-----------

The main repo is https://github.com/kmike/pymorphy2-dicts/. The repository
doesn't contain the data itself: only package template and update
scripts are stored in VCS.

License for Python code in this package is MIT.
The data is licensed under
{{ cookiecutter.data_license }}.
