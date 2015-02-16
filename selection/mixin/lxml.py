import six
from tools.etree import get_node_text, render_html
from tools.text import normalize_space as normalize_space_func
from tools.const import NULL
from tools.error import DataNotFound
from selection.error import SelectionRuntimeError

__all__ = ('LxmlSelectorMixin',)


class LxmlSelectorMixin(object):
    __slots__ = ()

    def html(self, encoding='unicode'):
        if self.is_text_node():
            return self._node
        else:
            return render_html(self._node, encoding=encoding)

    def is_text_node(self):
        return isinstance(self._node, six.string_types)

    def select(self, query=None):
        if self.is_text_node():
            raise SelectionRuntimeError('Text node selectors do not '
                                        'allow select method')
        return super(LxmlSelectorMixin, self).select(query)

    def attr(self, key, default=NULL):
        if self.is_text_node():
            raise SelectionRuntimeError('Text node selectors do not '
                                        'allow attr method')
        if default is NULL:
            if key in self._node.attrib:
                return self._node.get(key)
            else:
                raise DataNotFound(u'No such attribute: %s' % key)
        else:
            return self._node.get(key, default)

    def text(self, smart=False, normalize_space=True):
        if self.is_text_node():
            if normalize_space:
                return normalize_space_func(self._node)
            else:
                return self._node
        else:
            return get_node_text(self._node, smart=smart,
                                 normalize_space=normalize_space)
