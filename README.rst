pymorphy2-dicts
===============

This is a package with pre-compiled OpenCorpora.org dictionary
data for `pymorphy2`_.

.. _pymorphy2: https://github.com/kmike/pymorphy2

Installation
------------

Install::

    $ pip install pymorphy2-dicts

Remove::

    $ pip uninstall pymorphy2-dicts

Usage
-----

You can get a path to the installed dataset using
``pymorphy2_dicts.get_path()`` method. Usually you don't have to do so,
because if all of the following apply:

a) this package is installed;
b) dictionary path is not passed to ``pymorphy2.MorphAnalyzer`` constructor;
c) ``PYMORPHY2_DICTIONARY_PATH`` environment variable is not set,

then ``pymorphy2.MorphAnalyzer()`` uses dictionaries from this
package automatically.


Development
-----------

The main repo is https://github.com/kmike/pymorphy2-dicts/. The repository
doesn't contain the data itself: only package template and update
scripts are stored in VCS.

There is a hg/bitbucket mirror at https://bitbucket.org/kmike/pymorphy2-dicts/.

License for Python code in this package is MIT. The data
is licensed under `Creative Commons Attribution-Share Alike`_.

.. _Creative Commons Attribution-Share Alike: http://creativecommons.org/licenses/by-sa/3.0/
