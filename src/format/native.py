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

def save(filename, world, view):
    f = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    #First try to save PNG data (charts with palettes)
    for chartno, chart in enumerate(world.charts):
        s = StringIO()
        w = png.Writer(size=chart.shape,
                       bitdepth=8,
                       palette=palette.to_rgb(view.palette))
        w.write(s, numpy.transpose(chart))
        f.writestr('chart%d.png' % chartno, 
                   s.getvalue())
    f.close()
                       
                       

    
