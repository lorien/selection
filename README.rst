=========
Selection
=========

.. image:: https://travis-ci.org/lorien/selection.png
    :target: https://travis-ci.org/lorien/selection

.. image:: https://coveralls.io/repos/lorien/selection/badge.svg
    :target: https://coveralls.io/r/lorien/selection

API to extract data from HTML and XML documents.


Usage Example
=============

Example::

    from selection import XpathSelector
    from lxml.html import fromstring

    html = '<div><h1>test</h1><ul id="items"><li>1</li><li>2</li></ul></div>'
    sel = XpathSelector(fromstring(html))
    print(sel.select('//h1')).text()
    print(sel.select('//li').text_list()
    print(sel.select('//ul').attr('id')


Dependencies
============

* lxml
