from tools.const import NULL

from selection.mixin.lxml import LxmlSelectorMixin
from selection.mixin.common import CommonSelectorMixin
from selection.error import SelectionRuntimeError
from selection.selector import SelectorInterface


class TextSelector(CommonSelectorMixin, LxmlSelectorMixin,
                   SelectorInterface):
    __slots__ = ()

    def select(self, xpath=None):
        raise SelectionRuntimeError('TextSelector does not '
                                    'allow select method')

    def html(self, encoding='unicode'):
        return self._node

    def attr(self, key, default=NULL):
        raise SelectionRuntimeError('TextSelector does not allow attr method')
