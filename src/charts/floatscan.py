from registry import register
from _chart import chart
import numpy
import _scantop
    
def _floatscan_data(x, y, planes=1):
    if planes <= 1:
        data = numpy.zeros(shape=(x, y), dtype=numpy.float)
    else:
        data = numpy.zeros(shape=(x, y, planes), dtype=numpy.float)
    data[...] = numpy.random.rand(*data.shape)
    return data
 
@register('create_chart', type=('floatscan', 'torus'), quality=1.0)
def _floatscan_torus(alg, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.torus,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('floatscan', 'torusfall'), quality=1.0)
def _floatscan_torusfall(alg, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.torusfall(top.fall),
                 margin=alg.margin
                 )
 
@register('create_chart', type=('floatscan', 'rectangle'), quality=1.0)
def _floatscan_rectangle(alg, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.rectangle,
                 margin=alg.margin
                 )
 
@register('create_chart', type=('floatscan', 'projective_plane'), quality=1.0)
def _floatscan_projective_plane(alg, top):
    return chart('floatscan',
                 data=_floatscan_data(top.width + 2*alg.margin, 
                                      top.height + 2*alg.margin,
                                      getattr(alg, 'planes', 1)),
                 topology=_scantop.projective_plane,
                 margin=alg.margin
                 )
 
@register('change_topology', type=('floatscan', 'torus'), quality=1.0)
def _floatscan_to_torus(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_scantop.torus,
                 margin=c.margin
                 )
 
@register('change_topology', type=('floatscan', 'rectangle'), quality=1.0)
def _floatscan_to_rectangle(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_scantop.rectangle,
                 margin=c.margin
                 )
 
@register('change_topology', type=('floatscan', 'projective_plane'), quality=1.0)
def _floatscan_to_projective_plane(c, top):
    return chart('floatscan',
                 data=c.data,
                 topology=_scantop.projective_plane,
                 margin=c.margin
                 )

@register('convert_chart', type=('floatscan', 'floatscan'), quality=1.0)
def _floatscan_convert(source, what):
    source.margin = what.margin
    return source