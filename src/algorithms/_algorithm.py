import simple

class algorithm(simple.typed_object):
    def __call__(self, source, target):
        self.evolve(source, target, self.table)