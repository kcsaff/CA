
class cascading_object(object):
    def __init__(self,
                 parent = None,
                 source = None,
                 description = None,
                 author = None,
                 timestamp = None):
        self.parent = parent
        self.source = source
        self.description = description
        self.author = author
        self.timestamp = timestamp
        
    def __getattr__(self, what):
        if self.parent is not None:
            return getattr(self.parent, what)
        else:
            return object.__getattr__(self, what)
        
    def update(self, other):
        new_parent = cascading_object()
        new_parent.__dict__ = self.__dict__
        self.__dict__ = other.__dict__
        self.parent = new_parent
