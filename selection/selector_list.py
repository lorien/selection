from tools.const import NULL
from tools.error import DataNotFound


class SelectorList(object):
    __slots__ = ('selector_list', 'origin_selector_class', 'origin_query')

    def __init__(self, selector_list, origin_selector_class, origin_query):
        self.selector_list = selector_list
        self.origin_selector_class = origin_selector_class
        self.origin_query = origin_query

    def __getitem__(self, x):
        return self.selector_list[x]

    def __len__(self):
        return self.count()

    def count(self):
        return len(self.selector_list)

    def one(self, default=NULL):
        try:
            return self.selector_list[0]
        except IndexError:
            if default is NULL:
                m = 'Could not get first item for %s query of class %s'\
                    % (self.origin_query, self.origin_selector_class.__name__)
                raise DataNotFound(m)
            else:
                return default

    def node(self, default=NULL):
        try:
            return self.one().node
        except IndexError:
            if default is NULL:
                m = 'Could not get first item for %s query of class %s'\
                    % (self.origin_query, self.origin_selector_class.__name__)
                raise DataNotFound(m)
            else:
                return default

    def text(self, default=NULL, smart=False, normalize_space=True):
        try:
            sel = self.one()
        except IndexError:
            if default is NULL:
                raise
            else:
                return default
        else:
            return sel.text(smart=smart, normalize_space=normalize_space)

    def text_list(self, smart=False, normalize_space=True):
        result_list = []
        for item in self.selector_list:
            result_list.append(item.text())
        return result_list

    def html(self, default=NULL, encoding='unicode'):
        try:
            sel = self.one()
        except IndexError:
            if default is NULL:
                raise
            else:
                return default
        else:
            return sel.html(encoding=encoding)

    def number(self, default=NULL, ignore_spaces=False,
               smart=False, make_int=True):
        """
        Find number in normalized text of node which matches the given xpath.
        """

        try:
            sel = self.one()
        except IndexError:
            if default is NULL:
                raise
            else:
                return default
        else:
            return sel.number(ignore_spaces=ignore_spaces, smart=smart,
                              default=default, make_int=make_int)

    def exists(self):
        """
        Return True if selector list is not empty.
        """

        return len(self.selector_list) > 0

    def assert_exists(self):
        """
        Return True if selector list is not empty.
        """

        if not self.exists():
            raise DataNotFound(u'Node does not exists, query: %s, query type: %s' % (
                self.origin_query, self.origin_selector_class.__name__))

    def attr(self, key, default=NULL):
        try:
            sel = self.one()
        except IndexError:
            if default is NULL:
                raise
            else:
                return default
        else:
            return sel.attr(key, default=default)

    def attr_list(self, key, default=NULL):
        result_list = []
        for item in self.selector_list:
            result_list.append(item.attr(key, default=default))
        return result_list

    def rex(self, regexp, flags=0, byte=False, default=NULL):
        try:
            sel = self.one()
        except IndexError:
            if default is NULL:
                raise
            else:
                return default
        else:
            return self.one().rex(regexp, flags=flags, byte=byte)

    def node_list(self):
        return [x.node for x in self.selector_list]

    def select(self, query):
        result = SelectorList([], self.origin_selector_class,
                              self.origin_query + ' + ' + query)
        for count, selector in enumerate(self.selector_list):
            result.selector_list.extend(selector.select(query))
        return result


class RexResultList(object):
    __slots__ = ('items', 'source_rex')

    def __init__(self, items, source_rex):
        self.items = items
        self.source_rex = source_rex

    def one(self):
        return self.items[0]

    def text(self, default=NULL):
        try:
            return normalize_space(decode_entities(self.one().group(1)))
        except (AttributeError, IndexError):
            if default is NULL:
                raise
            else:
                return default

    def number(self):
        return int(self.text())
