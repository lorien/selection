from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, Protocol, TypeVar, cast

from lxml.etree import XPath, _Element
from weblib.error import DataNotFound
from weblib.etree import get_node_text, render_html
from weblib.text import normalize_space as normalize_space_func

from selection.base import Selector, SelectorList
from selection.const import UNDEFINED
from selection.error import SelectionRuntimeError

__all__ = ["XpathSelector"]
XPATH_CACHE = {}
REGEXP_NS = "http://exslt.org/regular-expressions"


class LxmlNodeProtocol(Protocol):
    attrib: dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        pass


LxmlNodeT = TypeVar("LxmlNodeT", bound=LxmlNodeProtocol)


class LxmlNodeSelector(Selector[LxmlNodeT]):
    __slots__ = ()

    @abstractmethod
    def process_query(self, query: str) -> Iterable[LxmlNodeT]:
        raise NotImplementedError

    def is_text_node(self) -> bool:
        return isinstance(self.node(), str)

    def select(self, query: str) -> SelectorList[LxmlNodeT]:
        if self.is_text_node():
            raise SelectionRuntimeError(
                "Text node selectors do not allow select method"
            )
        return super().select(query)

    def html(self, encoding: str = "unicode") -> str:
        if self.is_text_node():
            return str(self.node())
        return str(render_html(self.node(), encoding=encoding))

    def attr(self, key: str, default: Any = UNDEFINED) -> Any:
        if self.is_text_node():
            raise SelectionRuntimeError("Text node selectors do not allow attr method")
        if default is UNDEFINED:
            if key in self.node().attrib:
                return self.node().get(key)
            raise DataNotFound("No such attribute: %s" % key)
        return self.node().get(key, default)

    def text(self, smart: bool = False, normalize_space: bool = True) -> str:
        if self.is_text_node():
            if normalize_space:
                return str(normalize_space_func(self.node()))
            return str(self.node())
        return str(
            get_node_text(self.node(), smart=smart, normalize_space=normalize_space)
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

        return cast(list[LxmlNodeT], result)
