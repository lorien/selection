from selection.backend.lxml_base import LxmlBaseSelector


class PyquerySelector(LxmlBaseSelector):
    __slots__ = ()

    def pyquery_node(self):
        return PyQuery(self.node)

    def process_query(self, query):
        return self.pyquery_node().find(pyquery)
