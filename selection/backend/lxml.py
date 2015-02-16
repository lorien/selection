import six
from tools.etree import get_node_text, render_html
from tools.text import normalize_space as normalize_space_func
from tools.const import NULL
from tools.error import DataNotFound
from selection.error import SelectionRuntimeError
from selection.backend.common import CommonSelector

__all__ = ('LxmlSelector',)


class LxmlSelector(CommonSelector):
    __slots__ = ()

    def is_text_node(self):
        return isinstance(self.node(), six.string_types)

    def select(self, query=None):
        if self.is_text_node():
            raise SelectionRuntimeError('Text node selectors do not '
                                        'allow select method')
        return super(LxmlSelector, self).select(query)

    def html(self, encoding='unicode'):
        if self.is_text_node():
            return self.node()
        else:
            return render_html(self.node(), encoding=encoding)

    def attr(self, key, default=NULL):
        if self.is_text_node():
            raise SelectionRuntimeError('Text node selectors do not '
                                        'allow attr method')
        if default is NULL:
            if key in self.node().attrib:
                return self.node().get(key)
            else:
                raise DataNotFound(u'No such attribute: %s' % key)
        else:
            return self.node().get(key, default)

    def text(self, smart=False, normalize_space=True):
        if self.is_text_node():
            if normalize_space:
                return normalize_space_func(self.node())
            else:
                return self.node()
        else:
            return get_node_text(self.node(), smart=smart,
                                 normalize_space=normalize_space)
