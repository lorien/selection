from tools.text import find_number
from tools import rex as rex_tools

from tools.const import NULL
from selection.selector_list import RexResultList
from selection.selector import SelectorInterface

__all__ = ('CommonSelector',)


class CommonSelector(SelectorInterface):
    __slots__ = ()

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

    def rex(self, regexp, flags=0):
        norm_regexp = rex_tools.normalize_regexp(regexp, flags)
        matches = list(norm_regexp.finditer(self.html()))
        return RexResultList(matches, source_rex=norm_regexp)
