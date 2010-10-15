import simple

class algorithm(simple.typed_object):
    margin = 1
    def __call__(self, source, target):
        self.evolve(source.data, target.data, self.table)