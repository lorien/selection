from __future__ import absolute_import  # needs for pyquery_node method
from selection.mixin.lxml import LxmlSelectorMixin
from selection.mixin.common import CommonSelectorMixin
from selection.selector import SelectorInterface

__all__ = ('PyquerySelector',)


class PyquerySelector(CommonSelectorMixin, LxmlSelectorMixin,
                      SelectorInterface):
    __slots__ = ()

    def pyquery_node(self):
        from pyquery import PyQuery

        return PyQuery(self._node)

    def process_query(self, query):
        return self.pyquery_node().find(query)
