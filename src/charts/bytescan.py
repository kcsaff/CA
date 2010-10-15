from registry import register
from _chart import chart
import numpy
import _bytescan
    
def _bytescan_data(x, y):
    data = numpy.zeros(shape=(x, y), dtype=numpy.uint8)
    data[:,:] = numpy.random.randint(0, 2, size=data.shape)
    return data
 
@register('create_chart', type=('bytescan', 'torus'), quality=1.0)
def _bytescan_torus(_, top):
    return chart('bytescan',
                 data=_bytescan_data(top.width, top.height),
                 topology=_bytescan.torus
                 )
 
@register('create_chart', type=('bytescan', 'rectangle'), quality=1.0)
def _bytescan_rectangle(_, top):
    return chart('bytescan',
                 data=_bytescan_data(top.width, top.height),
                 topology=_bytescan.rectangle
                 )
 
@register('create_chart', type=('bytescan', 'projective_plane'), quality=1.0)
def _bytescan_projective_plane(_, top):
    return chart('bytescan',
                 data=_bytescan_data(top.width, top.height),
                 topology=_bytescan.projective_plane
                 )
 
@register('change_topology', type=('bytescan', 'torus'), quality=1.0)
def _bytescan_to_torus(c, top):
    return chart('bytescan',
                 data=c.data,
                 topology=_bytescan.torus
                 )
 
@register('change_topology', type=('bytescan', 'rectangle'), quality=1.0)
def _bytescan_to_rectangle(c, top):
    return chart('bytescan',
                 data=c.data,
                 topology=_bytescan.rectangle
                 )
 
@register('change_topology', type=('bytescan', 'projective_plane'), quality=1.0)
def _bytescan_to_projective_plane(c, top):
    return chart('bytescan',
                 data=c.data,
                 topology=_bytescan.projective_plane
                 )

@register('convert_chart', type=('bytescan', 'bytescan'), quality=1.0)
def _bytescan_convert(source, _):
    return source