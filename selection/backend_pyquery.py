from typing import Any, Iterable, cast  # noqa: PEA001

from pyquery import PyQuery

from .backend_lxml import LxmlNodeSelector, LxmlNodeT

__all__ = ["PyquerySelector"]


class PyquerySelector(LxmlNodeSelector[LxmlNodeT]):
    __slots__ = ()

    def pyquery_node(self) -> Any:
        return PyQuery(self.node())

    def process_query(self, query: str) -> Iterable[LxmlNodeT]:
        return cast(Iterable[LxmlNodeT], self.pyquery_node().find(query))
