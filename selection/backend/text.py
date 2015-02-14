from tools.const import NULL

from selection.backend.lxml_base import LxmlBaseSelector
from selection.error import SelectionRuntimeError


class TextSelector(LxmlBaseSelector):
    __slots__ = ()

    def select(self, xpath=None):
        raise SelectionRuntimeError('TextSelector does not allow select method') 

    def html(self, encoding='unicode'):
        return self.node

    def attr(self, key, default=NULL):
        raise SelectionRuntimeError('TextSelector does not allow attr method') 
