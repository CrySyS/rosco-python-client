class BaseObject(object):
    def _to_string(self, width = 0, blacklist=list(), prefix = ""):
        return_string = ""
        for attribute, value in sorted(self.__dict__.iteritems()):
            if attribute not in blacklist:
                return_string += prefix
                return_string += (str(attribute).replace('_', ' ').capitalize() + ": ").ljust(width)
                return_string += str(value) + "\n"
        return return_string





