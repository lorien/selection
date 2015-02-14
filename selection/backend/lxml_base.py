import six
from tools.etree import get_node_text, render_html
from tools.text import find_number, normalize_space as normalize_space_func
from tools import rex as rex_tools

from selection.selector import BaseSelector
from selection.selector_list import RexResultList
from tools.const import NULL
from tools.error import DataNotFound


class LxmlBaseSelector(BaseSelector):
    __slots__ = ()

    def html(self, encoding='unicode'):
        return render_html(self.node, encoding=encoding)

    def attr(self, key, default=NULL):
        if default is NULL:
            if key in self.node.attrib:
                return self.node.get(key)
            else:
                raise DataNotFound(u'No such attribute: %s' % key)
        else:
            return self.node.get(key, default)

    def text(self, smart=False, normalize_space=True):
        elem = self.node
        if isinstance(elem, six.string_types):
            if normalize_space:
                return normalize_space_func(elem)
            else:
                return elem
        else:
            return get_node_text(elem, smart=smart,
                                 normalize_space=normalize_space)
