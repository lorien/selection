# from __future__ import annotations

from abc import abstractmethod
from typing import Any, List, TypeVar, cast

from lxml.etree import XPath, _Element
from six.moves.collections_abc import Iterable  # pylint: disable=import-error

from . import util
from .base import Selector, SelectorList
from .const import UNDEFINED
from .errors import DataNotFoundError

__all__ = ["XpathSelector"]
XPATH_CACHE = {}
REGEXP_NS = "http://exslt.org/regular-expressions"
LxmlNodeT = TypeVar("LxmlNodeT", bound=_Element)


class LxmlNodeSelector(Selector[LxmlNodeT]):
    __slots__ = ()

    @abstractmethod
    def process_query(self, query):
        # type: (str) -> Iterable[LxmlNodeT]
        raise NotImplementedError

    def is_text_node(self):
        # type: () -> bool
        return isinstance(self.node(), str)

    def select(self, query):
        # type: (str) -> SelectorList[LxmlNodeT]
        if self.is_text_node():
            raise TypeError("Text node selectors do not allow select method")
        return super(LxmlNodeSelector, self).select(query)  # noqa: UP008

    def html(self):
        # type: () -> str
        if self.is_text_node():
            return str(self.node())
        return util.render_html(cast(_Element, self.node()))

    def attr(self, key, default=UNDEFINED):
        # type: (str, Any) -> Any
        if self.is_text_node():
            raise TypeError("Text node selectors do not allow attr method")
        if default is UNDEFINED:
            if key in self.node().attrib:
                return self.node().get(key)
            raise DataNotFoundError("No such attribute: {}".format(key))
        return self.node().get(key, default)

    def text(self, smart=False, normalize_space=True):
        # type: (bool, bool) -> str
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

    def process_query(self, query):
        # type: (str) -> Iterable[LxmlNodeT]
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
