from selection.backend.lxml_base import LxmlBaseSelector
from tools.const import NULL


class TextSelector(LxmlBaseSelector):
    __slots__ = ()

    def select(self, xpath=None):
        raise GrabMisuseError('TextSelector does not allow select method') 

    def html(self, encoding='unicode'):
        return self.node

    def attr(self, key, default=NULL):
        raise GrabMisuseError('TextSelector does not allow attr method') 
