# coding: utf-8
from unittest import TestCase
from lxml.html import fromstring
from tools.error import DataNotFound

from selection import XpathSelector
from selection.backend.text import TextSelector
from selection.backend.pyquery import PyquerySelector
from selection.selector_list import RexResultList
from selection.selector import BaseSelector
from selection.error import SelectionRuntimeError


HTML = """
<html>
    <body>
        <h1>test</h1>
        <ul>
            <li>one</li>
            <li> two </li>
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

    def test_sel_list_number(self):
        self.assertEquals(4, XpathSelector(self.tree).select('//ul/li[last()]').number())
        self.assertEquals(6, XpathSelector(self.tree).select('//ul/li[last()]/@id').number())

    def test_sel_list_number_does_not_exist(self):
        sel = XpathSelector(self.tree).select('//ul/li[1]')
        self.assertEquals('DEFAULT', sel.number(default='DEFAULT'))
        self.assertRaises(DataNotFound, lambda: sel.number())

    def test_selector_number(self):
        self.assertEquals(4, XpathSelector(self.tree).select('//ul/li[last()]').one().number())
        self.assertEquals(6, XpathSelector(self.tree).select('//ul/li[last()]/@id').one().number())

    def test_selector_number_does_not_exist(self):
        sel = XpathSelector(self.tree).select('//ul/li[1]').one()
        self.assertEquals('DEFAULT', sel.number(default='DEFAULT'))
        self.assertRaises(DataNotFound, lambda: sel.number())

    def test_text_selector(self):
        sel = XpathSelector(self.tree).select('//li/text()').one()
        self.assertTrue(isinstance(sel, TextSelector))
        self.assertEquals('one', XpathSelector(self.tree).select('//li/text()').text())

    def test_text_method_normalize_space(self):
        sel = XpathSelector(self.tree).select('//li[2]/text()')
        self.assertEquals('two', sel.text())
        self.assertEquals(' two ', sel.text(normalize_space=False))

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

    def test_attr(self):
        root = XpathSelector(self.tree)
        self.assertEqual('second-list', root.select('//ul[2]').attr('id'))

    def test_attr_with_default_value(self):
        root = XpathSelector(self.tree)
        self.assertEqual('z', root.select('//ul[2]').attr('id-xxx', default='z'))

    def test_attr_does_not_exist(self):
        root = XpathSelector(self.tree)
        self.assertRaises(DataNotFound, lambda: root.select('//ul[1]').attr('id-xxx'))

    def test_attr_list(self):
        root = XpathSelector(self.tree)
        self.assertEquals(set(['li-1', 'li-2']),
                          set(root.select('//ul[@id="second-list"]/li')\
                                  .attr_list('class'))
                          )

    def test_rex_method(self):
        sel = XpathSelector(self.tree)
        self.assertTrue(isinstance(sel.select('//li').rex('\w*'), RexResultList))

    def test_pyquery_selector(self):
        sel = PyquerySelector(self.tree)
        self.assertEquals('one', sel.select('li').text())

    def test_text_selector_select(self):
        sel = XpathSelector(self.tree).select('//li/text()').one()
        self.assertRaises(SelectionRuntimeError, lambda: sel.select('foo'))

    def test_text_selector_html(self):
        sel = XpathSelector(self.tree).select('//li/text()').one()
        self.assertEquals(u'one', sel.html())

    def test_text_selector_attr(self):
        sel = XpathSelector(self.tree).select('//li/text()').one()
        self.assertRaises(SelectionRuntimeError, lambda: sel.attr('foo'))

    """
    def test_base_selector_html(self):
        class ChildSelector(BaseSelector):
            def html(self):
                pass

            def text(self):
                pass

        sel = ChildSelector(self.tree)
    """


class TestSelectorList(TestCase):
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_one(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertEquals('one', sel.one().node.text)
        self.assertEquals('one', sel.text())

    def test_one_default(self):
        sel = XpathSelector(self.tree).select('//ul/li[10]')
        self.assertRaises(DataNotFound, lambda: sel.one())
        self.assertEqual('DEFAULT', sel.one(default='DEFAULT'))

    def test_node(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertEquals(self.tree.xpath('//ul/li')[0], sel.node())

    def test_node_default(self):
        sel = XpathSelector(self.tree).select('//ul/li[10]')
        self.assertRaises(DataNotFound, lambda: sel.node())
        self.assertEqual('DEFAULT', sel.node(default='DEFAULT'))

    def test_text(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertEquals('one', sel.text())

    def test_text_default(self):
        sel = XpathSelector(self.tree).select('//ul/li[10]')
        self.assertRaises(DataNotFound, sel.text)
        self.assertEquals('DEFAULT', sel.text(default='DEFAULT'))

    def test_html(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertEquals(u'<li>one</li>', sel.html().strip())

    def test_html_default(self):
        sel = XpathSelector(self.tree).select('//ul/li[10]')
        self.assertRaises(DataNotFound, sel.html)
        self.assertEquals('DEFAULT', sel.html(default='DEFAULT'))

    def test_number(self):
        sel = XpathSelector(self.tree).select('//ul/li[4]')
        self.assertEquals(4, sel.number())

    def test_number_default(self):
        sel = XpathSelector(self.tree).select('//ul/li[10]')
        self.assertRaises(DataNotFound, sel.number)
        self.assertEquals('DEFAULT', sel.number(default='DEFAULT'))

    def test_assert_exists(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        sel.assert_exists()

        sel = XpathSelector(self.tree).select('//ul/li[10]')
        self.assertRaises(DataNotFound, sel.assert_exists)

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

    def test_attr(self):
        sel = XpathSelector(self.tree).select('//ul[2]/li')
        self.assertEquals('li-1', sel.attr('class'))

    def test_attr_default(self):
        sel = XpathSelector(self.tree).select('//ul[2]/li[10]')
        self.assertRaises(DataNotFound, lambda: sel.attr('class'))
        self.assertEquals('DEFAULT', sel.attr('class', default='DEFAULT'))

    def test_rex(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertTrue(isinstance(sel.rex('(\w+)'), RexResultList))

    def test_rex_default(self):
        sel = XpathSelector(self.tree).select('//ul/li[10]')
        self.assertRaises(DataNotFound, lambda: sel.rex('zz'))
        self.assertEquals('DEFAULT', sel.rex('zz', default='DEFAULT'))

    def test_node_list(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertEquals(self.tree.xpath('//ul/li'), sel.node_list())


class RexResultListTestCase(TestCase):
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_one(self):
        sel = XpathSelector(self.tree).select('//ul/li')
        self.assertEquals('SRE_Match', sel.rex('one').one().__class__.__name__)

    def test_text(self):
        sel = XpathSelector(self.tree).select('//ul/li/text()')
        self.assertEquals('one', sel.rex('(\w+)').text())

    def test_text_no_default(self):
        sel = XpathSelector(self.tree).select('//ul/li/text()')
        self.assertRaises(DataNotFound, lambda: sel.rex('(zz)').text())

    def test_text_default_value(self):
        sel = XpathSelector(self.tree).select('//ul/li/text()')
        self.assertEquals('DEFAULT', sel.rex('(zz)').text(default='DEFAULT'))

    def test_number(self):
        sel = XpathSelector(self.tree).select('//ul/li[4]/text()')
        self.assertEquals(4, sel.rex('(\d+)').number())
