from registry import register
from _chart import chart
import numpy
import _bytescan
    
def _multifloatscan_data(width, height, planes):
    data = numpy.zeros(shape=(width, height, planes), dtype=numpy.float)
    data[:,:] = numpy.random.rand(*data.shape)
    data *= 255.9
    return data
 
@register('create_chart', type=('multifloatscan', 'torus'), quality=1.0)
def _multifloatscan_torus(alg, top):
    return chart('multifloatscan',
                 data=_multifloatscan_data(top.width + 2*alg.margin, 
                                           top.height + 2*alg.margin,
                                           alg.planes),
                 topology=_bytescan.torus,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('multifloatscan', 'rectangle'), quality=1.0)
def _multifloatscan_rectangle(alg, top):
    return chart('multifloatscan',
                 data=_multifloatscan_data(top.width + 2*alg.margin, 
                                           top.height + 2*alg.margin,
                                           alg.planes),
                 topology=_bytescan.rectangle,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('multifloatscan', 'projective_plane'), quality=1.0)
def _multifloatscan_projective_plane(alg, top):
    return chart('multifloatscan',
                 data=_multifloatscan_data(top.width + 2*alg.margin, 
                                           top.height + 2*alg.margin,
                                           alg.planes),
                 topology=_bytescan.projective_plane,
                 margin=alg.margin
                 )
 
@register('change_topology', type=('multifloatscan', 'torus'), quality=1.0)
def _multifloatscan_to_torus(c, top):
    return chart('multifloatscan',
                 data=c.data,
                 topology=_bytescan.torus,
                 margin=c.margin
                 )
 
@register('change_topology', type=('multifloatscan', 'rectangle'), quality=1.0)
def _multifloatscan_to_rectangle(c, top):
    return chart('multifloatscan',
                 data=c.data,
                 topology=_bytescan.rectangle,
                 margin=c.margin
                 )
 
@register('change_topology', type=('multifloatscan', 'projective_plane'), quality=1.0)
def _multifloatscan_to_projective_plane(c, top):
    return chart('multifloatscan',
                 data=c.data,
                 topology=_bytescan.projective_plane,
                 margin=c.margin
                 )

@register('convert_chart', type=('multifloatscan', 'multifloatscan'), quality=1.0)
def _multifloatscan_convert(source, what):
    source.margin = what.margin
    return source