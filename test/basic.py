from lxml.html import fromstring
from unittest import TestCase

HTML = """
<html>
<body>
<h1>Header 1</h1>
<ul id="ul-1">
    <li>Item 1</li>
    <li>Item 2</li>
"""


class BasicTestCase(TestCase):
    def test_lxml_fromstring(self):
        tree = fromstring(HTML)
        self.assertEqual('Header 1', tree.xpath('//h1')[0].text_content())
        self.assertEqual('Item 2', tree.xpath('//li[2]')[0].text_content())
