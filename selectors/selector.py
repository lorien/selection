"""
Selector module provides high usability interface to lxml tree
"""
import logging
import time
try:
    from pyquery import PyQuery
except ImportError:
    pass
from abc import ABCMeta, abstractmethod

from grab.tools.lxml_tools import get_node_text, render_html
from grab.tools.text import find_number, normalize_space as normalize_space_func
from grab.error import GrabMisuseError, DataNotFound, warn
from grab.tools import rex as rex_tools
from grab.tools.text import normalize_space
from grab.tools.html import decode_entities

from selectors.const import NULL

__all__ = ['Selector', 'TextSelector', 'XpathSelector', 'PyquerySelector']
XPATH_CACHE = {}
logger = logging.getLogger('grab.selector.selector')

metaclass_ABCMeta = ABCMeta('metaclass_ABCMeta', (object, ), {})


class BaseSelector(metaclass_ABCMeta):
    __slots__ = ('node',)

    def __init__(self, node):
        self.node = node

    def select(self, query):
        start = time.time()
        selector_list = self.wrap_node_list(self.process_query(query), query)
        total = time.time() - start
        return selector_list

    def wrap_node_list(self, nodes, query):
        selector_list = []
        for node in nodes:
            if isinstance(node, basestring):
                selector_list.append(TextSelector(node))
            else:
                selector_list.append(self.__class__(node))
        return SelectorList(selector_list, self.__class__, query)

    @abstractmethod
    def html(self):
        raise NotImplementedError

    @abstractmethod
    def attr(self):
        raise NotImplementedError

    @abstractmethod
    def text(self):
        raise NotImplementedError

    def number(self, default=NULL, ignore_spaces=False,
               smart=False, make_int=True):
        try:
            return find_number(self.text(smart=smart),
                               ignore_spaces=ignore_spaces,
                               make_int=make_int)
        except IndexError:
            if default is NULL:
                raise
            else:
                return default

    def rex(self, regexp, flags=0, byte=False):
        norm_regexp = rex_tools.normalize_regexp(regexp, flags)
        matches = list(norm_regexp.finditer(self.html()))
        return RexResultList(matches, source_rex=norm_regexp)
