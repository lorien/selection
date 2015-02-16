from __future__ import absolute_import
from selection.backend.lxml import LxmlSelector

__all__ = ('XpathSelector',)
XPATH_CACHE = {}


class XpathSelector(LxmlSelector):
    __slots__ = ()

    def process_query(self, query):
        from lxml.etree import XPath

        if query not in XPATH_CACHE:
            obj = XPath(query)
            XPATH_CACHE[query] = obj
        xpath_obj = XPATH_CACHE[query]

        result = xpath_obj(self.node())

        # If you query XPATH like //some/crap/@foo="bar" then xpath function
        # returns boolean value instead of list of something.
        # To work around this problem I just returns empty list.
        # This is not great solutions but it produces less confusing error.
        if isinstance(result, bool):
            result = []

        return result
