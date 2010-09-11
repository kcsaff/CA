# Copyright (C) 2010 by Kevin Saff

# This file is part of the CA scanner.

# The CA scanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The CA scanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the CA scanner.  If not, see <http://www.gnu.org/licenses/>.

import zipfile
from lib import png
from views import palette
from StringIO import StringIO
import numpy
import worlds, views
            
#def default():
#    from algorithms.xx2 import algorithm, life
#    result = World(source='default')
#    result.topology = torus
#    result.charts = [_default_chart()]
#    result.algorithm = algorithm.evolve
#    result.table = life.life()
#    result.toys = set()
#    result.generation = 0
#    return result          
#def default():
#    result = View(source='default')
#    result.center = (0,0)
#    result.zoom = 1
#    result.palette = palette.default
#    result.speed = 60
#    return result

class _reader(object):

    def __init__(self):
        self.atlases = []

    def _insert_chart(self, chart, atlasno, chartno):
        while len(self.atlases) <= atlasno:
            self.atlases.append([])
        while len(self.atlases[atlasno]) <= chartno:
            self.atlases[atlasno].append([])
        self.atlases[atlasno][chartno] = chart

    def _read_chart(self, name, resource):
        nos = name.strip('chart.png').split('-')
        nos = [int(x) for x in nos]
        p = png.Reader(file=resource)
        width, height, pixels, meta = p.read()
        self.view.palette = views.palette.from_rgb(p.palette())
        print meta
        chart = numpy.zeros(shape=(width, height), dtype=numpy.uint8)
        chart[:,:] = numpy.transpose(list(pixels))
        self._insert_chart(chart, *nos)

    def _read(self, name, resource):
        if name.startswith('chart'):
            self._read_chart(name, resource)
        else:
            raise ValueError, 'Unknown native resource: %s.' % name

    def read(self, filename):
        self.world = worlds.World(source=filename)
        self.view = views.View(source=filename)

        f = zipfile.ZipFile(filename, 'r')
        resources = f.namelist()
    
        for resource in resources:
            self._read(resource, f.open(resource))
        
        if len(self.atlases) > 0:
            self.world.charts = self.atlases[0]
        if len(self.atlases) > 1:
            self.world._scratch_charts = self.atlases[1]

        return self.world, self.view

def read(filename):
    return _reader().read(filename)

def write(filename, world, view):
    f = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    #First try to save PNG data (charts with palettes)
    for atlasno, atlas in enumerate((world.charts, 
                                     world._scratch_charts)):
        for chartno, chart in enumerate(atlas):
            s = StringIO()
            w = png.Writer(size=chart.shape,
                           bitdepth=8,
                           palette=palette.to_rgb(view.palette))
            w.write(s, numpy.transpose(chart))
            f.writestr('chart%d-%d.png' % (atlasno, chartno), 
                       s.getvalue())
    f.close()
                       
                       

    
