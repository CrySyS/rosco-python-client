from filter import Filter

class BaseObjectSearch(object):
    class SearchException(Exception):
        def __init__(self, message):
            Exception.__init__(self, message)
        def __str__(self):
            return str(self.message)

    class Filters(object):
        pass

    def add_filter(self, name, prefix = None, start = None, stop = None, substring = None):
        if name not in self.Filters.__dict__.values():
            raise self.SearchException("'%(name)s' is not compatible filter type for '%(search)s'" % {
                'name': name,
                'search': self.__class__.__name__
            })

        if hasattr(self, name):
            raise self.SearchException("'%(name)s' is already added for '%(search)s'" % {
                'name': name,
                'search': self.__class__.__name__
            })

        filter = Filter(prefix, start, stop, substring)
        setattr(self, name, filter)
