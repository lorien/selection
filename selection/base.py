# from __future__ import annotations

import logging
import re
from abc import abstractmethod

try:  # noqa: SIM105
    # for type checking with mypy
    # mypy runs on modern python version
    from re import Match, Pattern
except ImportError:
    pass

from types import TracebackType
from typing import Any, Generic, TypeVar

from six.moves.collections_abc import Iterable, Iterator  # pylint: disable=import-error

from . import util
from .const import UNDEFINED
from .errors import DataNotFoundError

__all__ = ["RexResultList", "Selector", "SelectorList"]
LOG = logging.getLogger("selection.base")
T = TypeVar("T")


class Selector(Generic[T]):
    __slots__ = ("_node",)

    def __init__(self, node):
        # type: (T) -> None
        self._node = node

    def node(self):
        # type: () -> T
        return self._node

    @abstractmethod
    def process_query(self, query):
        # type: (str) -> Iterable[T]
        raise NotImplementedError

    def select(self, query):
        # type: (str) -> SelectorList[T]
        return self._wrap_node_list(self.process_query(query), query)

    def _wrap_node_list(self, nodes, query):
        # type: (Iterable[T], str) -> SelectorList[T]
        selectors = [self.__class__(x) for x in nodes]
        return SelectorList(selectors, self.__class__, query)

    def is_text_node(self):
        # type: ()-> bool
        raise NotImplementedError

    @abstractmethod
    def html(self):
        # type: () -> str
        raise NotImplementedError

    def attr(self, key, default=UNDEFINED):
        # type: (str, Any) -> Any
        raise NotImplementedError

    def text(self, smart=False, normalize_space=True):
        # type: (bool, bool) -> str
        raise NotImplementedError

    def number(
        self,
        default=UNDEFINED,  # type: Any
        ignore_spaces=False,  # type: bool
        smart=False,  # type: bool
        make_int=True,  # type: bool
    ):
        # type: (...) -> Any
        try:
            return util.find_number(
                self.text(smart=smart), ignore_spaces=ignore_spaces, make_int=make_int
            )
        except DataNotFoundError:
            if default is UNDEFINED:
                raise
            return default

    def rex(self, regexp, flags=0):  # pylint: disable=used-before-assignment
        # type: (str|Pattern[str], int) -> RexResultList
        if isinstance(regexp, str):
            regexp = re.compile(regexp, flags)
        matches = list(regexp.finditer(self.html()))
        return RexResultList(matches, source_rex=regexp)


class SelectorList(Generic[T]):
    __slots__ = ("origin_query", "origin_selector_class", "selector_list")

    def __init__(
        self,
        selector_list,  # type: list[Selector[T]]
        origin_selector_class,  # type: type[Selector[T]]
        origin_query,  # type: str
    ):
        # type: (...) -> None
        self.selector_list = selector_list
        self.origin_selector_class = origin_selector_class
        self.origin_query = origin_query

    def __enter__(self):
        # type: () -> SelectorList[T]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # type: (type[Exception], Exception, TracebackType) -> None
        pass

    def __getitem__(self, index):
        # type: (int) -> Selector[T]
        return self.selector_list[index]

    def __len__(self):
        # type: () -> int
        return self.count()

    def __iter__(self):
        # type: () -> Iterator[Selector[T]]
        return iter(self.selector_list)

    def count(self):
        # type: () -> int
        return len(self.selector_list)

    def one(self, default=UNDEFINED):
        # type: (Any) -> Any
        try:
            return self.selector_list[0]
        except IndexError:  # as ex:
            if default is UNDEFINED:
                raise DataNotFoundError(
                    "Could not get first item for {} query of class {}".format(
                        self.origin_query,
                        self.origin_selector_class.__name__,
                    )
                )  # from ex
            return default

    def node(self, default=UNDEFINED):
        # type: (Any) -> Any
        try:
            return self.one().node()
        except DataNotFoundError:  # as ex:
            if default is UNDEFINED:
                raise DataNotFoundError(
                    "Could not get first item for {} query of class {}".format(
                        self.origin_query,
                        self.origin_selector_class.__name__,
                    )
                )  # from ex
            return default

    def text(
        self,
        default=UNDEFINED,  # type: Any
        smart=False,  # type: bool
        normalize_space=True,  # type: bool
    ):
        # type: (...) -> Any
        try:
            sel = self.one()
        except DataNotFoundError:
            if default is UNDEFINED:
                raise
            return default
        return sel.text(smart=smart, normalize_space=normalize_space)

    def text_list(self, smart=False, normalize_space=True):
        # type: (bool, bool) -> list[str]
        result_list = []
        for item in self.selector_list:
            result_list.append(item.text(normalize_space=normalize_space, smart=smart))
        return result_list

    def html(self, default=UNDEFINED):
        # type: (Any) -> Any
        try:
            sel = self.one()
        except DataNotFoundError:
            if default is UNDEFINED:
                raise
            return default
        return sel.html()

    def inner_html(self, default=UNDEFINED):
        # type: (Any) -> Any
        try:
            sel = self.one()
        except DataNotFoundError:
            if default is UNDEFINED:
                raise
            return default
        result_list = [item.html() for item in sel.select("./*")]
        return "".join(result_list).strip()

    def number(
        self,
        default=UNDEFINED,  # type: Any
        ignore_spaces=False,  # type: bool
        smart=False,  # type: bool
        make_int=True,  # type: bool
    ):
        # type: (...) -> Any
        """Find number in normalized text of node which matches the given xpath."""
        try:
            sel = self.one()
        except DataNotFoundError:
            if default is UNDEFINED:
                raise
            return default
        return sel.number(
            ignore_spaces=ignore_spaces,
            smart=smart,
            default=default,
            make_int=make_int,
        )

    def exists(self):
        # type: () -> bool
        """Return True if selector list is not empty."""
        return len(self.selector_list) > 0

    def require(self):
        # type: () -> None
        """Raise DataNotFoundError if selector data does not exist."""
        if not self.exists():
            raise DataNotFoundError(
                "Node does not exists, query: {}, query type: {}".format(
                    self.origin_query,
                    self.origin_selector_class.__name__,
                )
            )

    def attr(self, key, default=UNDEFINED):
        # type: (str, Any) -> Any
        try:
            sel = self.one()
        except DataNotFoundError:
            if default is UNDEFINED:
                raise
            return default
        return sel.attr(key, default=default)

    def attr_list(self, key, default=UNDEFINED):
        # type: (str, Any) -> Any
        result_list = []
        for item in self.selector_list:
            result_list.append(item.attr(key, default=default))
        return result_list

    def rex(self, regexp, flags=0, default=UNDEFINED):
        # type: (Pattern[str], int, Any) -> Any
        try:
            sel = self.one()
        except DataNotFoundError:
            if default is UNDEFINED:
                raise
            return default
        return sel.rex(regexp, flags=flags)

    def node_list(self):
        # type: () -> list[Any]
        return [x.node() for x in self.selector_list]

    def select(self, query):
        # type: (str) -> SelectorList[T]
        result = SelectorList(
            [], self.origin_selector_class, self.origin_query + " + " + query
        )
        for selector in self.selector_list:
            result.selector_list.extend(iter(selector.select(query)))
        return result


class RexResultList:
    __slots__ = ("items", "source_rex")

    def __init__(self, items, source_rex):
        # type: (list[Match[str]], Pattern[str]) -> None
        self.items = items
        self.source_rex = source_rex

    def one(self):
        # type: () -> Match[str]
        try:
            return self.items[0]
        except IndexError:
            raise DataNotFoundError

    def text(self, default=UNDEFINED):
        # type: (Any) -> Any
        try:
            return util.normalize_spaces(util.decode_entities(self.one().group(1)))
        except (AttributeError, DataNotFoundError):  # as ex:
            if default is UNDEFINED:
                raise DataNotFoundError  # from ex
            return default

    def number(self):
        # type: () -> int
        return int(self.text())
