import six
from tools.etree import get_node_text, render_html
from tools.text import normalize_space as normalize_space_func
from tools.const import NULL
from tools.error import DataNotFound

__all__ = ('LxmlSelectorMixin',)


class LxmlSelectorMixin(object):
    __slots__ = ()

    def html(self, encoding='unicode'):
        return render_html(self._node, encoding=encoding)

    def attr(self, key, default=NULL):
        if default is NULL:
            if key in self._node.attrib:
                return self._node.get(key)
            else:
                raise DataNotFound(u'No such attribute: %s' % key)
        else:
            return self._node.get(key, default)

    def text(self, smart=False, normalize_space=True):
        if isinstance(self._node, six.string_types):
            if normalize_space:
                return normalize_space_func(self._node)
            else:
                return self._node
        else:
            return get_node_text(self._node, smart=smart,
                                 normalize_space=normalize_space)
