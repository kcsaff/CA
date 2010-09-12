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

from _topology import register, topology
import numpy

class _rectangle(object):
    @staticmethod
    def stitch(array, margin = 1):
        return

    @staticmethod
    def map_point(point, array, margin = 1):
        return point

    @staticmethod
    def map_slice(upper_left, array, margin = 1):
        x, y = _rectangle.map_point(upper_left, array, margin)
        if x < 0 and y < 0:
            return numpy.zeros(shape=(-x, -y), dtype=numpy.uint8)
        elif x < 0:
            return numpy.zeros(shape=(-x, array.shape[1]), dtype=numpy.uint8)
        elif y < 0:
            return numpy.zeros(shape=(array.shape[0], -y), dtype=numpy.uint8)
        elif x >= array.shape[0] or y >= array.shape[0]:
            return numpy.zeros(shape=array.shape, dtype=numpy.uint8)
        else:
            return array[x:, y:]


@register('compile_topology', type='rectangle')
def _go(*args):
    return _rectangle

def rectangle():
    return topology('rectangle')
