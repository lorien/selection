# from __future__ import annotations

import typing
from typing import Any, cast

from pyquery import PyQuery  # pylint: disable=import-error
from six.moves.collections_abc import Iterable  # pylint: disable=import-error

from .backend_lxml import LxmlNodeSelector, LxmlNodeT

__all__ = ["PyquerySelector"]


class PyquerySelector(LxmlNodeSelector[LxmlNodeT]):
    __slots__ = ()

    def pyquery_node(self):
        # type: () -> Any
        return PyQuery(self.node())

    def process_query(self, query):
        # type: (str) -> Iterable[LxmlNodeT]
        # pylint: disable=deprecated-typing-alias
        return cast(typing.Iterable[LxmlNodeT], self.pyquery_node().find(query))
