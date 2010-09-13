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
import lib.png, lib.fits
from views import palette
from StringIO import StringIO
import numpy
import worlds, views
import common
from rules._rule import rule
from topologies._topology import topology
import qdict
import meta
            
#    result.toys = set() #doesn't matter too much yet.
#    TODO: need info about how chart data is stored.
#    TODO: save palette when using FITS for charts.
#    TODO: put metadata in PNG and FITS files when possible.

def read(filename, file=None):
    import formats
    result = qdict.qdict()
    z = zipfile.ZipFile(file or filename, 'r')
    resources = z.namelist()
    for resource in resources:
        result.update(formats.read(resource, z.open(resource) ))
    return result

def _write_charts_fits(z, data):
    import formats
    s = StringIO()
    formats.write('charts.fits', data, s)
    z.writestr('charts.fits', s.getvalue())

def _write_charts(z, data):
    
    if data['chart(0,0)'].dtype == numpy.dtype(numpy.uint8):
        ext = 'png'
    elif data['chart(0,0)'].dtype == numpy.dtype(numpy.float64):
        _write_charts_fits(z, data)
        return
    else:
        ext = 'png'
        
    import formats
    for atlasno, atlas in enumerate(formats.get_atlases(data)):
        for chartno, _ in enumerate(atlas):
            s = StringIO()
            filename = 'chart.%d-%d.%s' % (atlasno, chartno, ext)
            formats.write(filename, data, s, (atlasno, chartno))
            z.writestr('chart.%d-%d.%s' % (atlasno, chartno, ext), 
                       s.getvalue())


def write(filename, data, file=None, chart=None):
    f = zipfile.ZipFile(file or filename, 'w', zipfile.ZIP_DEFLATED)
    #First try to save PNG data (charts with palettes)
    _write_charts(f, data)
    f.writestr('meta.txt', meta.encode(data))
    f.close()
                       
                       

    
