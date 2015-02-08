========
Selector
========

.. image:: https://travis-ci.org/lorien/selector.png
    :target: https://travis-ci.org/lorien/selector

.. image:: https://coveralls.io/repos/lorien/selector/badge.svg
    :target: https://coveralls.io/r/lorien/selector

API to extract data from HTML and XML documents.


Usage Example
=============

Example::

    from selector import HtmlSelector
    from lxml.html import fromstring

    html = '<div><h1>test</h1><ul id="items"><li>1</li><li>2</li></ul></div>'
    sel = HtmlSelector(fromstring(html))
    print(sel.select('//h1')).text()
    print(sel.select('//li').text_list()
    print(sel.select('//ul').attr('id')


Dependencies
============

* lxml
