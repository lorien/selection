# coding: utf-8
from unittest import TestCase
from selection import XpathSelector
from selection.backend.text import TextSelector
from lxml.html import fromstring

HTML = """
<html>
    <body>
        <h1>test</h1>
        <ul>
            <li>one</li>
            <li>two</li>
            <li>three</li>
            <li id="6">z 4 foo</li>
        </ul>
        <ul id="second-list">
            <li class="li-1">yet one</li>
            <li class="li-2">yet two</li>
        </ul>
    </body>
</html>
"""

class TestSelector(TestCase):
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_in_general(self):
        sel = XpathSelector(self.tree)

    def test_select_node(self):
        self.assertEquals('test', XpathSelector(self.tree).select('//h1')[0].node.text)

    def test_html(self):
        sel = XpathSelector(self.tree.xpath('//h1')[0])
        self.assertEquals('<h1>test</h1>', sel.html().strip())

    def test_textselector(self):
        self.assertEquals('one', XpathSelector(self.tree).select('//li/text()').text())

    def test_number(self):
        self.assertEquals(4, XpathSelector(self.tree).select('//ul/li[last()]').number())
        self.assertEquals(6, XpathSelector(self.tree).select('//ul/li[last()]/@id').number())

    def test_text_selector(self):
        sel = XpathSelector(self.tree).select('//li/text()').one()
        self.assertTrue(isinstance(sel, TextSelector))

    def test_select_select(self):
        root = XpathSelector(self.tree)
        self.assertEquals(set(['one', 'yet one']),
                          set([x.text() for x in root.select('//ul').select('./li[1]')]),
                          )

    def test_text_list(self):
        root = XpathSelector(self.tree)
        self.assertEquals(set(['one', 'yet one']),
                          set(root.select('//ul/li[1]').text_list()),
                          )

    def test_attr_list(self):
        root = XpathSelector(self.tree)
        self.assertEquals(set(['li-1', 'li-2']),
                          set(root.select('//ul[@id="second-list"]/li')\
                                  .attr_list('class'))
                          )


class TestSelectorList(TestCase):
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_one(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertEquals('one', sel.one().node.text)
        self.assertEquals('one', sel.text())

    def test_number(self):
        sel = XpathSelector(self.tree).select('//ul/li[4]')
        self.assertEquals(4, sel.number())

    def test_exists(self):
        sel = XpathSelector(self.tree).select('//ul/li[4]')
        self.assertEquals(True, sel.exists())

        sel = XpathSelector(self.tree).select('//ul/li[5]')
        self.assertEquals(False, sel.exists())

    def test_incorrect_xpath(self):
        # The lxml xpath function return boolean for following xpath
        # This breaks selector internal logic that assumes that only
        # list could be returnsed
        # So it was fixed and this test was crated
        sel = XpathSelector(self.tree).select('//ul/li/text()="oops"')
        self.assertEquals(False, sel.exists())

        # Selector list is always empty in this special case
        # Even if the xpath return True on lxml level
        self.assertEquals(True, self.tree.xpath('//ul[1]/li[1]/text()="one"'))
        sel = XpathSelector(self.tree).select('//ul[1]/li[1]/text()="one"')
        self.assertEquals(False, sel.exists())
