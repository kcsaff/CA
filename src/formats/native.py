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
from lib import png, fits
from views import palette
from StringIO import StringIO
import numpy
import worlds, views
import common
from rules._rule import rule
from topologies._topology import topology
import qdict
            
#    result.toys = set() #doesn't matter too much yet.
#    TODO: need info about how chart data is stored.
#    TODO: save palette when using FITS for charts.
#    TODO: put metadata in PNG and FITS files when possible.

class _reader(object):

    def __init__(self):
        self.atlases = []

    def _insert_chart(self, chart, atlasno, chartno):
        while len(self.atlases) <= atlasno:
            self.atlases.append([])
        while len(self.atlases[atlasno]) <= chartno:
            self.atlases[atlasno].append([])
        self.atlases[atlasno][chartno] = chart

    def _read_chart_png(self, name, resource):
        nos = name.strip('chart.png').split('-')
        nos = [int(x) for x in nos]
        p = png.Reader(file=resource)
        width, height, pixels, meta = p.read()
        self.view.palette = views.palette.from_rgb(p.palette())
        chart = numpy.zeros(shape=(width, height), dtype=numpy.uint8)
        chart[:,:] = numpy.transpose(list(pixels))
        self._insert_chart(chart, *nos)

    def _read_chart_fits(self, name, resource):
        nos = name.strip('chart.fits').split('-')
        nos = [int(x) for x in nos]
        chart, _ = fits.read(resource)
        self._insert_chart(chart.transpose(), *nos)
        self.view.palette = palette.grays

    def _read_chart(self, name, resource):
        if name.endswith('.png'):
            self._read_chart_png(name, resource)
        elif name.endswith('.fits'):
            self._read_chart_fits(name, resource)

    def _read_meta(self, _, resource):
        defaults = {'SPEED': 2000.0 / 60.0,
                    'ZOOM': 1,
                    'CENTER': '0 0',
                    'GENERATION': 0,
                    }
        evals = {'SPEED': float, #~milliseconds between frames
                 'ZOOM': eval,
                 'CENTER': str.split, #get later
                 'GENERATION': int,
                 }

        data=common.read_hash(resource,
                              evals=evals,
                              defaults=defaults)

        self.view.speed = 2000.0 / data['SPEED']
        self.view.zoom = data['ZOOM']
        self.view.center = [int(x) for x in data['CENTER']]
        self.world.generation = data['GENERATION']
        if 'RULE' in data:
            self.world.rule = eval('rule(%s)' % data['RULE'])
        if 'WRAP' in data:
            self.world.topology = eval('topology(%s)' % data['WRAP'])

    def _read(self, name, resource):
        if name.startswith('chart'):
            self._read_chart(name, resource)
        elif name == 'meta.txt':
            self._read_meta(name, resource)
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
        else:
            self.world._scratch_charts = None

        return self.world, self.view

def read(filename, file=None):
    import formats
    result = qdict.qdict()
    z = zipfile.ZipFile(file or filename, 'r')
    resources = z.namelist()
    for resource in resources:
        result.update(formats.read(resource, z.open(resource) ))
    return result

def _write_charts_png(z, data):
    w = png.Writer(size=data['chart'].shape,
                   bitdepth=8,
                   palette=palette.to_rgb(data['palette']))
    for atlasno, atlas in enumerate(data['atlases']):
        for chartno, chart in enumerate(atlas):
            s = StringIO()
            w.write(s, numpy.transpose(chart))
            z.writestr('chart%d-%d.png' % (atlasno, chartno), 
                     s.getvalue())

def _write_charts_fits(z, data):
    for atlasno, atlas in enumerate(data['atlases']):
        for chartno, chart in enumerate(atlas):
            s = StringIO()
            fits.write(s, chart.transpose())
            z.writestr('chart%d-%d.fits' % (atlasno, chartno), 
                       s.getvalue())

def _write_charts(z, data):
    if data['chart'].dtype == numpy.dtype(numpy.uint8):
        _write_charts_png(z, data)
    elif data['chart'].dtype == numpy.dtype(numpy.float64):
        _write_charts_fits(z, data)
    else:
        _write_charts_png(z, data)


def _write_meta(z, data):
    meta = {'SPEED': [2000.0 / data['speed']],
            'ZOOM': [data['zoom']],
            'CENTER': ['%s %s' % tuple(data['center'])],
            'GENERATION': [data['generation']],
            'RULE': [data['rule'].format_args()],
            'WRAP': [data['topology'].format_args()],
            }
    s = StringIO()
    common.write_hash_raw(s, meta)
    z.writestr('meta.txt', s.getvalue())

def write(filename, data):
    f = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    #First try to save PNG data (charts with palettes)
    _write_charts(f, data)
    _write_meta(f, data)
    f.close()
                       
                       

    
