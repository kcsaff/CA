import simple

class history(simple.typed_object):
    pass

class atlas(simple.typed_object):
    pass

class chart(simple.typed_object):
    def copy(self):
        return chart(self.type,
                     data=self.data.copy(),
                     topology=self.topology,
                     margin=self.margin)
        
    def map_slice(self, upper_left, data = None):
        if data is None:
            data = self.data
        return self.topology.map_slice(upper_left, data, margin=self.margin)
    
    def stitch(self, charts=None):
        self.topology.stitch([chart.data for chart in charts] or [self.data],
                             margin=self.margin)
        
    def map_point(self, point):
        return self.topology.map_point(point, self.data, margin=self.margin)
    
    def __getitem__(self, point):
        return self.data[self.map_point(point)]    
    
    def __setitem__(self, point, value):
        self.data[self.map_point(point)] = value