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

import lib.png as png
import qdict
import views
import numpy

def read(filename, file=None):
    result = qdict.qdict()
    p = png.Reader(file=file or open(filename, 'rb'))
    width, height, pixels, meta = p.read()
    result['palette', 0.7, filename] = views.palette.from_rgb(p.palette())
    chart = numpy.zeros(shape=(width, height), dtype=numpy.uint8)
    chart[:,:] = numpy.transpose(list(pixels))
    result['chart', 1.0, filename] = chart
    return result

def write(filename, data):
    raise NotImplementedError
    pass