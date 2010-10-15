from registry import register
from _chart import chart
import numpy
import _bytescan
    
def _bytescan_data(x, y):
    data = numpy.zeros(shape=(x, y), dtype=numpy.uint8)
    data[:,:] = numpy.random.randint(0, 2, size=data.shape)
    return data
 
@register('create_chart', type=('bytescan', 'torus'), quality=1.0)
def _bytescan_torus(alg, top):
    return chart('bytescan',
                 data=_bytescan_data(top.width + 2*alg.margin, 
                                     top.height + 2*alg.margin),
                 topology=_bytescan.torus,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('bytescan', 'rectangle'), quality=1.0)
def _bytescan_rectangle(alg, top):
    return chart('bytescan',
                 data=_bytescan_data(top.width + 2*alg.margin, 
                                     top.height + 2*alg.margin),
                 topology=_bytescan.rectangle,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('bytescan', 'projective_plane'), quality=1.0)
def _bytescan_projective_plane(alg, top):
    return chart('bytescan',
                 data=_bytescan_data(top.width + 2*alg.margin, 
                                     top.height + 2*alg.margin),
                 topology=_bytescan.projective_plane,
                 margin=alg.margin
                 )
 
@register('change_topology', type=('bytescan', 'torus'), quality=1.0)
def _bytescan_to_torus(c, top):
    return chart('bytescan',
                 data=c.data,
                 topology=_bytescan.torus,
                 margin=c.margin
                 )
 
@register('change_topology', type=('bytescan', 'rectangle'), quality=1.0)
def _bytescan_to_rectangle(c, top):
    return chart('bytescan',
                 data=c.data,
                 topology=_bytescan.rectangle,
                 margin=c.margin
                 )
 
@register('change_topology', type=('bytescan', 'projective_plane'), quality=1.0)
def _bytescan_to_projective_plane(c, top):
    return chart('bytescan',
                 data=c.data,
                 topology=_bytescan.projective_plane,
                 margin=c.margin
                 )

@register('convert_chart', type=('bytescan', 'bytescan'), quality=1.0)
def _bytescan_convert(source, _):
    return source