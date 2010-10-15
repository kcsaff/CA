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
def _floatscan_torus(alg, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin),
                 topology=_bytescan.torus,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('floatscan', 'rectangle'), quality=1.0)
def _floatscan_rectangle(alg, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin),
                 topology=_bytescan.rectangle,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('floatscan', 'projective_plane'), quality=1.0)
def _floatscan_projective_plane(alg, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin),
                 topology=_bytescan.projective_plane,
                 margin=alg.margin
                 )
 
@register('change_topology', type=('floatscan', 'torus'), quality=1.0)
def _floatscan_to_torus(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_bytescan.torus,
                 margin=c.margin
                 )
 
@register('change_topology', type=('floatscan', 'rectangle'), quality=1.0)
def _floatscan_to_rectangle(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_bytescan.rectangle,
                 margin=c.margin
                 )
 
@register('change_topology', type=('floatscan', 'projective_plane'), quality=1.0)
def _floatscan_to_projective_plane(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_bytescan.projective_plane,
                 margin=c.margin
                 )

@register('convert_chart', type=('floatscan', 'floatscan'), quality=1.0)
def _floatscan_convert(source, _):
    return source