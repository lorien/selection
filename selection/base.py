from __future__ import annotations

import logging
import re
from abc import abstractmethod
from collections.abc import Iterable
from re import Match, Pattern
from types import TracebackType
from typing import Any, Generic, TypeVar

from . import util
from .const import UNDEFINED

__all__ = ["Selector", "SelectorList", "RexResultList"]
LOG = logging.getLogger("selection.base")
T = TypeVar("T")


class Selector(Generic[T]):
    __slots__ = ("_node",)

    def __init__(self, node: T):
        self._node = node

    def node(self) -> T:
        return self._node

    @abstractmethod
    def process_query(self, query: str) -> Iterable[T]:
        raise NotImplementedError

    def select(self, query: str) -> "SelectorList[T]":
        return self._wrap_node_list(self.process_query(query), query)

    def _wrap_node_list(self, nodes: Iterable[T], query: str) -> "SelectorList[T]":
        selectors = [self.__class__(x) for x in nodes]
        return SelectorList(selectors, self.__class__, query)

    def is_text_node(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def html(self) -> str:
        raise NotImplementedError

    def attr(self, key: str, default: Any = UNDEFINED) -> Any:
        raise NotImplementedError

    def text(self, smart: bool = False, normalize_space: bool = True) -> str:
        raise NotImplementedError

    def number(
        self,
        default: Any = UNDEFINED,
        ignore_spaces: bool = False,
        smart: bool = False,
        make_int: bool = True,
    ) -> Any:
        try:
            return util.find_number(
                self.text(smart=smart), ignore_spaces=ignore_spaces, make_int=make_int
            )
        except IndexError:
            if default is UNDEFINED:
                raise
            return default

    def rex(
        self, regexp: str | Pattern[str], flags: int = 0
    ) -> "RexResultList":  # pylint: disable=used-before-assignment

        if isinstance(regexp, str):
            regexp = re.compile(regexp, flags)
        matches = list(regexp.finditer(self.html()))
        return RexResultList(matches, source_rex=regexp)


class SelectorList(Generic[T]):
    __slots__ = ("selector_list", "origin_selector_class", "origin_query")

    def __init__(
        self,
        selector_list: list[Selector[T]],
        origin_selector_class: type[Selector[T]],
        origin_query: str,
    ) -> None:
        self.selector_list = selector_list
        self.origin_selector_class = origin_selector_class
        self.origin_query = origin_query

    def __enter__(self) -> "SelectorList[T]":
        return self

    def __exit__(
        self, exc_type: type[Exception], exc_value: Exception, traceback: TracebackType
    ) -> None:
        pass

    def __getitem__(self, index: int) -> Selector[T]:
        return self.selector_list[index]

    def __len__(self) -> int:
        return self.count()

    def count(self) -> int:
        return len(self.selector_list)

    def one(self, default: Any = UNDEFINED) -> Any:
        try:
            return self.selector_list[0]
        except IndexError as ex:
            if default is UNDEFINED:
                raise IndexError(
                    "Could not get first item for %s query of class %s"
                    % (
                        self.origin_query,
                        self.origin_selector_class.__name__,
                    )
                ) from ex
            return default

    def node(self, default: Any = UNDEFINED) -> Any:
        try:
            return self.one().node()
        except IndexError as ex:
            if default is UNDEFINED:
                raise IndexError(
                    "Could not get first item for %s query of class %s"
                    % (
                        self.origin_query,
                        self.origin_selector_class.__name__,
                    )
                ) from ex
            return default

    def text(
        self,
        default: Any = UNDEFINED,
        smart: bool = False,
        normalize_space: bool = True,
    ) -> Any:
        try:
            sel = self.one()
        except IndexError:
            if default is UNDEFINED:
                raise
            return default
        else:
            return sel.text(smart=smart, normalize_space=normalize_space)

    def text_list(self, smart: bool = False, normalize_space: bool = True) -> list[str]:
        result_list = []
        for item in self.selector_list:
            result_list.append(item.text(normalize_space=normalize_space, smart=smart))
        return result_list

    def html(self, default: Any = UNDEFINED) -> Any:
        try:
            sel = self.one()
        except IndexError:
            if default is UNDEFINED:
                raise
            return default
        else:
            return sel.html()

    def inner_html(self, default: Any = UNDEFINED) -> Any:
        try:
            sel = self.one()
        except IndexError:
            if default is UNDEFINED:
                raise
            return default
        else:
            result_list = [item.html() for item in sel.select("./*")]
            return "".join(result_list).strip()

    def number(
        self,
        default: Any = UNDEFINED,
        ignore_spaces: bool = False,
        smart: bool = False,
        make_int: bool = True,
    ) -> Any:
        """Find number in normalized text of node which matches the given xpath."""
        try:
            sel = self.one()
        except IndexError:
            if default is UNDEFINED:
                raise
            return default
        else:
            return sel.number(
                ignore_spaces=ignore_spaces,
                smart=smart,
                default=default,
                make_int=make_int,
            )

    def exists(self) -> bool:
        """Return True if selector list is not empty."""
        return len(self.selector_list) > 0

    def require(self) -> None:
        """Raise IndexError if selector data does not exist."""
        if not self.exists():
            raise IndexError(
                "Node does not exists, query: %s, query type: %s"
                % (
                    self.origin_query,
                    self.origin_selector_class.__name__,
                )
            )

    def attr(self, key: str, default: Any = UNDEFINED) -> Any:
        try:
            sel = self.one()
        except IndexError:
            if default is UNDEFINED:
                raise
            return default
        else:
            return sel.attr(key, default=default)

    def attr_list(self, key: str, default: Any = UNDEFINED) -> Any:
        result_list = []
        for item in self.selector_list:
            result_list.append(item.attr(key, default=default))
        return result_list

    def rex(
        self, regexp: Pattern[str], flags: int = 0, default: Any = UNDEFINED
    ) -> Any:
        try:
            sel = self.one()
        except IndexError:
            if default is UNDEFINED:
                raise
            return default
        else:
            return sel.rex(regexp, flags=flags)

    def node_list(self) -> list[Any]:
        return [x.node() for x in self.selector_list]

    def __iter__(self) -> Iterable[Selector[T]]:
        return iter(self.selector_list)

    def select(self, query: str) -> "SelectorList[T]":
        result: SelectorList[T] = SelectorList(
            [], self.origin_selector_class, self.origin_query + " + " + query
        )
        for selector in self.selector_list:
            result.selector_list.extend(iter(selector.select(query)))
        return result


class RexResultList:
    __slots__ = ("items", "source_rex")

    def __init__(self, items: list[Match[str]], source_rex: Pattern[str]) -> None:
        self.items = items
        self.source_rex = source_rex

    def one(self) -> Match[str]:
        return self.items[0]

    def text(self, default: Any = UNDEFINED) -> Any:
        try:
            return util.normalize_spaces(util.decode_entities(self.one().group(1)))
        except (AttributeError, IndexError) as ex:
            if default is UNDEFINED:
                raise IndexError from ex
            return default

    def number(self) -> int:
        return int(self.text())
