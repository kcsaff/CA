from registry import register
from _chart import chart
import numpy
import _scantop
    
def _complexscan_data(x, y, planes=1):
    if planes <= 1:
        data = numpy.zeros(shape=(x, y), dtype=numpy.complex)
    else:
        data = numpy.zeros(shape=(x, y, planes), dtype=numpy.complex)
    data[...] = numpy.random.rand(*data.shape) + numpy.random.rand(*data.shape) * 1j 
    data[...] -= (.5 + .5j)
    data[:,:,1:] = numpy.zeros(shape=(x, y, planes-1), dtype=numpy.complex)
    return data
 
@register('create_chart', type=('complexscan', 'torus'), quality=1.0)
def _complexscan_torus(alg, top):
    return chart('complexscan',
                 data=_complexscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.torus,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('complexscan', 'torusfall'), quality=1.0)
def _complexscan_torusfall(alg, top):
    return chart('complexscan',
                 data=_complexscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.torusfall(top.fall),
                 margin=alg.margin
                 )
 
@register('create_chart', type=('complexscan', 'rectangle'), quality=1.0)
def _complexscan_rectangle(alg, top):
    return chart('complexscan',
                 data=_complexscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.rectangle,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('complexscan', 'projective_plane'), quality=1.0)
def _complexscan_projective_plane(alg, top):
    return chart('complexscan',
                 data=_complexscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.projective_plane,
                 margin=alg.margin
                 )
 
@register('change_topology', type=('complexscan', 'torus'), quality=1.0)
def _complexscan_to_torus(c, top):
    return chart('complexscan',
                 data=c.data,
                 topology=_scantop.torus,
                 margin=c.margin
                 )
 
@register('change_topology', type=('complexscan', 'rectangle'), quality=1.0)
def _complexscan_to_rectangle(c, top):
    return chart('complexscan',
                 data=c.data,
                 topology=_scantop.rectangle,
                 margin=c.margin
                 )
 
@register('change_topology', type=('complexscan', 'projective_plane'), quality=1.0)
def _complexscan_to_projective_plane(c, top):
    return chart('complexscan',
                 data=c.data,
                 topology=_scantop.projective_plane,
                 margin=c.margin
                 )

@register('convert_chart', type=('complexscan', 'complexscan'), quality=1.0)
def _complexscan_convert(source, what):
    source.margin = what.margin
    return source