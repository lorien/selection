from selection.backend.lxml_base import LxmlBaseSelector


XPATH_CACHE = {}


class XpathSelector(LxmlBaseSelector):
    __slots__ = ()

    def process_query(self, query):
        from lxml.etree import XPath

        if not query in XPATH_CACHE:
            obj = XPath(query)
            XPATH_CACHE[query] = obj
        xpath_obj = XPATH_CACHE[query]

        result = xpath_obj(self.node)

        # If you query XPATH like //some/crap/@foo="bar" then xpath function
        # returns boolean value instead of list of something.
        # To work around this problem I just returns empty list.
        # This is not great solutions but it produces less confusing error.
        if isinstance(result, bool):
            result = []

        return result
