from __future__ import absolute_import
from selection.backend.lxml_base import LxmlBaseSelector


class PyquerySelector(LxmlBaseSelector):
    __slots__ = ()

    def pyquery_node(self):
        from pyquery import PyQuery

        return PyQuery(self.node)

    def process_query(self, query):
        return self.pyquery_node().find(query)
