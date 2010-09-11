import numpy
from topology import torus
from cascading_object import cascading_object

def _default_chart():
    chart = numpy.zeros(shape=(640, 480), dtype=numpy.uint8)
    chart[:,:] = numpy.random.randint(0, 2, size=chart.shape)
    return chart

def _water_chart():
    chart = numpy.zeros(shape=(640, 480), dtype=numpy.float)
    chart[:,:] = numpy.random.rand(*chart.shape)
    chart *= 255.9
    return chart
    
class World(cascading_object):
    _scratch_charts = None
    generation = 0
    
    def _stitch(self):
        self.topology.stitch(self.charts)
        
    def evolve(self, generations = 1):
        if self.generation == 0:
            self._stitch()
            self._create_scratch_charts()
            
        for _ in range(generations):
            for chart, scratch in zip(self.charts, self._scratch_charts):
                self.algorithm(chart, scratch, self.table)
            self.charts, self._scratch_charts = self._scratch_charts, self.charts
            self._stitch()
            for toy in self.toys:
                toy.evolve(self)
            self.generation += 1
        
    def _create_scratch_charts(self):
        self._scratch_charts = [chart.copy() for chart in self.charts]
            
    def set(self, point, state):
        #print 'setting', point, state
        mapped_point = self.topology.map_point(point, self.charts[0])
        for chart in self.charts: #This can't be _quite_ right.
            chart[mapped_point] = state   
            
    def get(self, point):
        mapped_point = self.topology.map_point(point, self.charts[0])
        return self.charts[0][mapped_point]    
            
def default():
    from algorithms.xx2 import algorithm, life
    result = World(source='default')
    result.topology = torus
    result.charts = [_default_chart()]
    result.algorithm = algorithm.evolve
    result.table = life.life()
    result.toys = set()
    result.generation = 0
    return result          
  
def water():
    from algorithms.dd1 import algorithm, life
    result = World(source='water')
    result.topology = torus
    result.charts = [_water_chart()]
    result.algorithm = algorithm.evolve
    result.table = life.boiling_water()
    result.toys = set()
    result.generation = 0
    return result
