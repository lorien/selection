# coding: utf-8
from unittest import TestCase

from lxml.html import fromstring

from selection.backend_lxml import XpathSelector
from selection.backend_pyquery import PyquerySelector
from selection.base import RexResultList
from selection.errors import DataNotFoundError

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


class PyqueryTestCase(TestCase):
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_pyquery_selector(self):
        sel = PyquerySelector(self.tree)
        self.assertEqual("one", sel.select("li").text())
        self.assertEqual("yet one", sel.select(".li-1").text())

    def test_nested_selector(self):
        sel = PyquerySelector(self.tree)
        sel2 = sel.select("ul")
        self.assertEqual("yet one", sel2.select("li[@class]").text())


# class CSSTestCase(TestCase):
#    def setUp(self):
#        self.tree = fromstring(HTML)
#
#    def test_css_selector(self):
#        sel = CssSelector(self.tree)
#        self.assertEqual('one', sel.select('li').text())
#        self.assertEqual('three', sel.select('li:contains("ree")').text())
#        self.assertEqual('yet one', sel.select('.li-1').text())
#
#    # TODO: That does not work!
#    def test_nested_selector(self):
#        sel = CssSelector(self.tree)
#        sel2 = sel.select('ul')
#        self.assertEqual('yet one', sel2.select('li[@class]').text())


class TestXpathSelector(TestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_in_general(self):
        XpathSelector(self.tree)

    def test_select_node(self):
        sel = XpathSelector(self.tree)
        # pylint: disable=protected-access
        self.assertEqual("test", sel.select("//h1")[0]._node.text)  # noqa: SLF001
        # pylint: enable=protected-access

    def test_html(self):
        sel = XpathSelector(self.tree.xpath("//h1")[0])
        self.assertEqual("<h1>test</h1>", sel.html().strip())

    def test_sel_list_number(self):
        sel = XpathSelector(self.tree)
        self.assertEqual(4, sel.select("//ul/li[last()]").number())
        self.assertEqual(6, sel.select("//ul/li[last()]/@id").number())

    def test_sel_list_number_does_not_exist(self):
        sel = XpathSelector(self.tree).select("//ul/li[1]")
        self.assertEqual("DEFAULT", sel.number(default="DEFAULT"))
        self.assertRaises(DataNotFoundError, sel.number)

    def test_selector_number(self):
        sel = XpathSelector(self.tree)
        self.assertEqual(4, sel.select("//ul/li[last()]").one().number())
        self.assertEqual(6, sel.select("//ul/li[last()]/@id").one().number())

    def test_selector_number_does_not_exist(self):
        sel = XpathSelector(self.tree).select("//ul/li[1]").one()
        self.assertEqual("DEFAULT", sel.number(default="DEFAULT"))
        self.assertRaises(DataNotFoundError, sel.number)

    def test_text_selector(self):
        sel = XpathSelector(self.tree).select("//li/text()").one()
        self.assertTrue(sel.is_text_node())
        self.assertEqual("one", XpathSelector(self.tree).select("//li/text()").text())

    def test_text_method_normalize_space(self):
        sel = XpathSelector(self.tree).select("//li[2]/text()")
        self.assertEqual("two", sel.text())
        self.assertEqual(" two ", sel.text(normalize_space=False))

    def test_select_select(self):
        root = XpathSelector(self.tree)
        self.assertEqual(
            {"one", "yet one"},
            {x.text() for x in root.select("//ul").select("./li[1]")},
        )

    def test_text_list(self):
        root = XpathSelector(self.tree)
        self.assertEqual({"one", "yet one"}, set(root.select("//ul/li[1]").text_list()))

    def test_attr(self):
        root = XpathSelector(self.tree)
        self.assertEqual("second-list", root.select("//ul[2]").attr("id"))

    def test_attr_with_default_value(self):
        root = XpathSelector(self.tree)
        self.assertEqual("z", root.select("//ul[2]").attr("id-xxx", default="z"))

    def test_attr_does_not_exist(self):
        root = XpathSelector(self.tree)
        self.assertRaises(
            DataNotFoundError, lambda: root.select("//ul[1]").attr("id-xxx")
        )

    def test_attr_list(self):
        root = XpathSelector(self.tree)
        self.assertEqual(
            {"li-1", "li-2"},
            set(root.select('//ul[@id="second-list"]/li').attr_list("class")),
        )

    def test_rex_method(self):
        sel = XpathSelector(self.tree)
        self.assertTrue(isinstance(sel.select("//li").rex(r"\w*"), RexResultList))

    def test_text_selector_select(self):
        sel = XpathSelector(self.tree).select("//li/text()").one()
        self.assertRaises(TypeError, lambda: sel.select("foo"))

    def test_text_selector_html(self):
        sel = XpathSelector(self.tree).select("//li/text()").one()
        self.assertEqual("one", sel.html())

    def test_text_selector_attr(self):
        sel = XpathSelector(self.tree).select("//li/text()").one()
        self.assertRaises(TypeError, sel.attr, "foo")

    def test_regexp(self):
        html = '<div><h1 id="h1">foo</h1><h2>bar</h2></div>'
        sel = XpathSelector(fromstring(html))
        self.assertEqual("h2", sel.select('//*[re:test(text(), "b.r")]').node().tag)
        self.assertEqual(
            "foo", sel.select(r'//*[re:test(@id, "^h\d+$")]/text()').text()
        )

    def test_xpath_concat_function(self):
        html = '<a href="index.html"></a>'
        sel = XpathSelector(fromstring(html))
        self.assertEqual("/index.html", sel.select('concat("/",//a/@href)').text())

    def test_context_manager_select_text(self):
        html = "<b>one</b><b>two</b>"
        with XpathSelector(fromstring(html)).select("b") as elem:
            self.assertEqual("one", elem.text())

    def test_context_manager_select_iter(self):
        html = "<b>one</b><b>two</b>"
        with XpathSelector(fromstring(html)).select("b") as qs:
            vals = [x.text() for x in qs]
            self.assertEqual({"one", "two"}, set(vals))


class TestXpathSelectorList(TestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_one(self):
        sel = XpathSelector(self.tree).select("//ul/li")
        self.assertEqual(
            "one",
            sel.one()._node.text,  # pylint: disable=protected-access # noqa: SLF001
        )
        self.assertEqual("one", sel.text())

    def test_one_default(self):
        sel = XpathSelector(self.tree).select("//ul/li[10]")
        self.assertRaises(DataNotFoundError, sel.one)
        self.assertEqual("DEFAULT", sel.one(default="DEFAULT"))

    def test_node(self):
        sel = XpathSelector(self.tree).select("//ul/li")
        self.assertEqual(self.tree.xpath("//ul/li")[0], sel.node())

    def test_node_default(self):
        sel = XpathSelector(self.tree).select("//ul/li[10]")
        self.assertRaises(DataNotFoundError, sel.node)
        self.assertEqual("DEFAULT", sel.node(default="DEFAULT"))

    def test_text(self):
        sel = XpathSelector(self.tree).select("//ul/li")
        self.assertEqual("one", sel.text())

    def test_text_default(self):
        sel = XpathSelector(self.tree).select("//ul/li[10]")
        self.assertRaises(DataNotFoundError, sel.text)
        self.assertEqual("DEFAULT", sel.text(default="DEFAULT"))

    def test_html(self):
        sel = XpathSelector(self.tree).select("//ul/li")
        self.assertEqual("<li>one</li>", sel.html().strip())

    def test_html_default(self):
        sel = XpathSelector(self.tree).select("//ul/li[10]")
        self.assertRaises(DataNotFoundError, sel.html)
        self.assertEqual("DEFAULT", sel.html(default="DEFAULT"))

    def test_inner_html(self):
        sel = XpathSelector(self.tree).select('//ul[@id="second-list"]')
        self.assertEqual(
            '<li class="li-1">yet one</li>\n            <li class="li-2">yet two</li>',
            sel.inner_html().strip(),
        )

    def test_inner_html_default(self):
        sel = XpathSelector(self.tree).select("//ul/li[10]")
        self.assertRaises(DataNotFoundError, sel.inner_html)
        self.assertEqual("DEFAULT", sel.inner_html(default="DEFAULT"))

    def test_number(self):
        sel = XpathSelector(self.tree).select("//ul/li[4]")
        self.assertEqual(4, sel.number())

    def test_number_default(self):
        sel = XpathSelector(self.tree).select("//ul/li[10]")
        self.assertRaises(DataNotFoundError, sel.number)
        self.assertEqual("DEFAULT", sel.number(default="DEFAULT"))

    def test_exists(self):
        sel = XpathSelector(self.tree).select("//ul/li[4]")
        self.assertEqual(True, sel.exists())

        sel = XpathSelector(self.tree).select("//ul/li[5]")
        self.assertEqual(False, sel.exists())

    def test_incorrect_xpath(self):
        # The lxml xpath function return boolean for following xpath
        # This breaks selector internal logic that assumes that only
        # list could be returnsed
        # So it was fixed and this test was crated
        sel = XpathSelector(self.tree).select('//ul/li/text()="oops"')
        self.assertEqual(False, sel.exists())

        # Selector list is always empty in this special case
        # Even if the xpath return True on lxml level
        self.assertEqual(True, self.tree.xpath('//ul[1]/li[1]/text()="one"'))
        sel = XpathSelector(self.tree).select('//ul[1]/li[1]/text()="one"')
        self.assertEqual(False, sel.exists())

    def test_attr(self):
        sel = XpathSelector(self.tree).select("//ul[2]/li")
        self.assertEqual("li-1", sel.attr("class"))

    def test_attr_default(self):
        sel = XpathSelector(self.tree).select("//ul[2]/li[10]")
        self.assertRaises(DataNotFoundError, lambda: sel.attr("class"))
        self.assertEqual("DEFAULT", sel.attr("class", default="DEFAULT"))

    def test_rex(self):
        sel = XpathSelector(self.tree).select("//ul/li")
        self.assertTrue(isinstance(sel.rex(r"(\w+)"), RexResultList))

    def test_rex_default(self):
        sel = XpathSelector(self.tree).select("//ul/li[10]")
        self.assertRaises(DataNotFoundError, lambda: sel.rex("zz"))
        self.assertEqual("DEFAULT", sel.rex("zz", default="DEFAULT"))

    def test_node_list(self):
        sel = XpathSelector(self.tree).select("//ul/li")
        self.assertEqual(self.tree.xpath("//ul/li"), sel.node_list())

    def test_iteration(self):
        for elem in XpathSelector(self.tree).select("//ul/li"):
            print(elem)
        # self.assertEqual(self.tree.xpath("//ul/li"), sel.node_list())

    def test_require(self):
        XpathSelector(self.tree).select("//ul").require()

        self.assertRaises(
            DataNotFoundError, XpathSelector(self.tree).select("//foo").require
        )


class RexResultListTestCase(TestCase):
    def setUp(self):
        self.tree = fromstring(HTML)

    def test_one(self):
        sel = XpathSelector(self.tree).select("//ul/li")
        # Match object class has different names in different python versions
        self.assertTrue(
            sel.rex("one").one().__class__.__name__ in {"Match", "SRE_Match"}
        )

    def test_text(self):
        sel = XpathSelector(self.tree).select("//ul/li/text()")
        self.assertEqual("one", sel.rex(r"(\w+)").text())

    def test_text_no_default(self):
        sel = XpathSelector(self.tree).select("//ul/li/text()")
        self.assertRaises(DataNotFoundError, lambda: sel.rex("(zz)").text())

    def test_text_default_value(self):
        sel = XpathSelector(self.tree).select("//ul/li/text()")
        self.assertEqual("DEFAULT", sel.rex("(zz)").text(default="DEFAULT"))

    def test_number(self):
        sel = XpathSelector(self.tree).select("//ul/li[4]/text()")
        self.assertEqual(4, sel.rex(r"(\d+)").number())
