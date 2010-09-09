
class Event(object):
    def __init__(self, type, **kwargs):
        self.type = type
        self.__dict__.update(kwargs)