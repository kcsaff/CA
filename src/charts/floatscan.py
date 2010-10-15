from registry import register
import numpy
    
@register('create_chart', type='floatscan', quality=1.0)
def _floatscan_chart(x, y):
    chart = numpy.zeros(shape=(640, 480), dtype=numpy.float)
    chart[:,:] = numpy.random.rand(*chart.shape)
    chart *= 255.9
    return chart
