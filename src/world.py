import numpy
from topology import torus
from exmod import xx
from exmod import life
from cascading_object import cascading_object

def _default_chart():
    chart = numpy.zeros(shape=(640, 480), dtype=numpy.uint8)
    chart[:,:] = numpy.random.randint(0, 2, size=chart.shape)
    return chart
    
class World(cascading_object):
    _scratch_charts = None
    generation = 0
    
    def evolve(self, generations = 1):
        self._create_scratch_charts()
        for _ in range(generations):
            for chart, scratch in zip(self.charts, self._scratch_charts):
                self.algorithm(chart, scratch, self.table)
            self.charts, self._scratch_charts = self._scratch_charts, self.charts
            self.topology.stitch(self.charts)
            self.generation += 1
        
    def _create_scratch_charts(self):
        if self._scratch_charts is None:
            self._scratch_charts = [chart.copy() for chart in self.charts]
            
def default():
    result = World(source='default')
    result.topology = torus
    result.charts = [_default_chart()]
    result.algorithm = xx.evolve
    result.table = life.life()
    result.objects = []
    result.generation = 0
    return result