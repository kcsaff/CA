from registry import register
from _chart import chart
import numpy
import _bytescan
    
def _floatscan_data(x, y):
    data = numpy.zeros(shape=(x, y), dtype=numpy.float)
    data[:,:] = numpy.random.rand(*data.shape)
    data *= 255.9
    return data
 
@register('create_chart', type=('floatscan', 'torus'), quality=1.0)
def _floatscan_torus(_, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width, top.height),
                 topology=_bytescan.torus
                 )
 
@register('create_chart', type=('floatscan', 'rectangle'), quality=1.0)
def _floatscan_rectangle(_, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width, top.height),
                 topology=_bytescan.rectangle
                 )
 
@register('create_chart', type=('floatscan', 'projective_plane'), quality=1.0)
def _floatscan_projective_plane(_, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width, top.height),
                 topology=_bytescan.projective_plane
                 )
 
@register('change_topology', type=('floatscan', 'torus'), quality=1.0)
def _floatscan_to_torus(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_bytescan.torus
                 )
 
@register('change_topology', type=('floatscan', 'rectangle'), quality=1.0)
def _floatscan_to_rectangle(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_bytescan.rectangle
                 )
 
@register('change_topology', type=('floatscan', 'projective_plane'), quality=1.0)
def _floatscan_to_projective_plane(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_bytescan.projective_plane
                 )

@register('convert_chart', type=('floatscan', 'floatscan'), quality=1.0)
def _floatscan_convert(source, _):
    return source