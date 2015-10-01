class Filter(object):
    class FilterException(Exception):
        def __init__(self, message):
            Exception.__init__(self, message)
        def __str__(self):
            return str(self.message)

    def __init__(self, prefix = None, start = None, stop = None, substring = None):
        if (prefix or start or stop or substring) is None:
            raise self.FilterException("All filter argument cannot be None")

        if prefix is not None:
            self.prefix = str(prefix)
        if start is not None:
            self.start = str(start)
        if stop is not None:
            self.stop = str(stop)
        if substring is not None:
            self.substring = str(substring)
