import numpy
from topology import torus
from exmod import xx
from exmod import life

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

class View(cascading_object):
    pass

def default_view():
    result = View(source='default')
    result.center = (0,0)
    result.zoom = 1
    result.palette = (0, 0xFFFFFF, 0xFF0000, 0, 0xCC9900)
    result.speed = 60
    return result
    
def _default_chart():
    chart = numpy.zeros(shape=(640, 480), dtype=numpy.uint8)
    chart[:,:] = numpy.random.randint(0, 2, size=chart.shape)
    return chart
    
class World(cascading_object):
    _scratch_charts = None
    
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
            
def default_world():
    result = World(source='default')
    result.topology = torus
    result.charts = [_default_chart()]
    result.algorithm = xx.evolve
    result.table = life.life()
    result.objects = []
    result.generation = 0
    return result
        