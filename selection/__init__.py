from selection.backend_lxml import XpathSelector
from selection.base import RexResultList, Selector, SelectorList
from selection.errors import SelectionNotFoundError

__all__ = [
    "RexResultList",
    "SelectionNotFoundError",
    "Selector",
    "SelectorList",
    "XpathSelector",
]

__version__ = "1.0.0"
