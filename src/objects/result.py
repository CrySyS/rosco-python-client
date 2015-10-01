class Result(object):
    def __init__(self, api, elements, object_type = None):
        self.api = api
        self.elements = elements
        self.object_type = object_type

    def __iter__(self):
        return self

    def next(self):
        if len(self.elements) > 0:
            hash = self.elements.pop(0)
            result = self.api.get_object(hash, self.object_type)
            return result
        raise StopIteration

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return '<ROSCO Result object at %s>' % (hex(id(self)))

    def __str__(self):
        return_string = ""
        for element in self.elements:
            return_string += str(element) + '\n'
        return return_string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.elements == other.elements
        return False

    def extend(self, other):
        self.elements.extend(other.elements)


class ConnectedResult(object):
    def __init__(self, contain, verifiy):
        self.contain = contain
        self.verify = verifiy

    def __len__(self):
        return len(self.contain) + len(self.verify)

    def __repr__(self):
        return '<ROSCO Connected Result object at %s>' % (hex(id(self)))

    def __str__(self):
        return_string = ""
        if len(self.contain) > 0:
            return_string += "contain:" + '\n'
            return_string += str(self.contain)
        if len(self.contain) > 0 and len(self.verify) > 0:
            return_string += '\n'
        if len(self.verify) > 0:
            return_string += "verify:" + '\n'
            return_string += str(self.verify)
        return return_string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.contain.elements == other.contain.elements and self.verify.elements == other.verify.elements
        return False
