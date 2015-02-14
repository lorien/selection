from selection.selector import BaseSelector
from selection.selector_list import SelectorList, RexResultList
from tools.const import NULL
from selection.backend.xpath import XpathSelector
from selection.backend.text import TextSelector

version_info = (0, 0, 3)
version = '.'.join(map(str, version_info))
