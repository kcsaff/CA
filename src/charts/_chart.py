import simple

class history(simple.typed_object):
    pass

class atlas(simple.typed_object):
    pass

class chart(simple.typed_object):
    def copy(self):
        return chart(self.type,
                     data=self.data.copy(),
                     topology=self.topology)
        
    def map_slice(self, upper_left):
        return self.topology.map_slice(upper_left, self.data)
    
    def stitch(self, charts=None):
        self.topology.stitch([chart.data for chart in charts] or [self.data])