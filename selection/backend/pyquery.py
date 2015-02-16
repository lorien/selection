from __future__ import absolute_import  # needs for pyquery_node method
from selection.backend.lxml import LxmlSelector

__all__ = ('PyquerySelector',)


class PyquerySelector(LxmlSelector):
    __slots__ = ()

    def pyquery_node(self):
        from pyquery import PyQuery

        return PyQuery(self.node())

    def process_query(self, query):
        return self.pyquery_node().find(query)
