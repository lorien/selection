from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, List, TypeVar, cast

from lxml.etree import XPath, _Element

from . import util
from .base import Selector, SelectorList
from .const import UNDEFINED

__all__ = ["XpathSelector"]
XPATH_CACHE = {}
REGEXP_NS = "http://exslt.org/regular-expressions"
LxmlNodeT = TypeVar("LxmlNodeT", bound=_Element)  # LxmlNodeProtocol)


class LxmlNodeSelector(Selector[LxmlNodeT]):
    __slots__ = ()

    @abstractmethod
    def process_query(self, query: str) -> Iterable[LxmlNodeT]:
        raise NotImplementedError

    def is_text_node(self) -> bool:
        return isinstance(self.node(), str)

    def select(self, query: str) -> SelectorList[LxmlNodeT]:
        if self.is_text_node():
            raise TypeError("Text node selectors do not allow select method")
        return super().select(query)

    def html(self) -> str:
        if self.is_text_node():
            return str(self.node())
        return util.render_html(cast(_Element, self.node()))

    def attr(self, key: str, default: Any = UNDEFINED) -> Any:
        if self.is_text_node():
            raise TypeError("Text node selectors do not allow attr method")
        if default is UNDEFINED:
            if key in self.node().attrib:
                return self.node().get(key)
            raise IndexError("No such attribute: %s" % key)
        return self.node().get(key, default)

    def text(self, smart: bool = False, normalize_space: bool = True) -> str:
        if self.is_text_node():
            if normalize_space:
                return util.normalize_spaces(cast(str, self.node()))
            return str(self.node())
        return str(
            util.get_node_text(
                cast(_Element, self.node()),
                smart=smart,
                normalize_space=normalize_space,
            )
        )


class XpathSelector(LxmlNodeSelector[LxmlNodeT]):
    __slots__ = ()

    def process_query(self, query: str) -> Iterable[LxmlNodeT]:
        if query not in XPATH_CACHE:
            obj = XPath(query, namespaces={"re": REGEXP_NS})
            XPATH_CACHE[query] = obj
        xpath_obj = XPATH_CACHE[query]

        result = xpath_obj(cast(_Element, self.node()))

        # If you query XPATH like //some/crap/@foo="bar" then xpath function
        # returns boolean value instead of list of something.
        # To work around this problem I just returns empty list.
        # This is not great solutions but it produces less confusing error.
        if isinstance(result, bool):
            result = []

        if isinstance(result, str):
            result = [result]

        # pylint: disable=deprecated-typing-alias
        return cast(List[LxmlNodeT], result)
