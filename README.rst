=========
Selection
=========

.. image:: https://travis-ci.org/lorien/selection.png?branch=master
    :target: https://travis-ci.org/lorien/selection

.. image:: https://coveralls.io/repos/lorien/selection/badge.svg?branch=master
    :target: https://coveralls.io/r/lorien/selection?branch=master

.. image:: https://img.shields.io/pypi/dm/selection.svg
    :target: https://pypi.python.org/pypi/selection

.. image:: https://img.shields.io/pypi/v/selection.svg
    :target: https://pypi.python.org/pypi/selection

API to extract data from HTML and XML documents.


Usage Example
=============

Example:

.. code:: python

    from selection import XpathSelector
    from lxml.html import fromstring

    html = '<div><h1>test</h1><ul id="items"><li>1</li><li>2</li></ul></div>'
    sel = XpathSelector(fromstring(html))
    print(sel.select('//h1')).text()
    print(sel.select('//li').text_list()
    print(sel.select('//ul').attr('id')


Installation
============

Run:

.. code:: bash

    pip install -U pip setuptools
    pip install -U selection


Dependencies
============

* lxml
* tools
* six
