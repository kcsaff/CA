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

class _torus(object):
    @staticmethod
    def stitch(array, margin = 1):
        if isinstance(array, list):
            for chart in array:
                _torus.stitch(chart, margin)
            return
    
        if margin == 1: #optimization
            return _torus.stitch_1(array, margin)
    
        array[-margin:,:] = array[margin:margin * 2,:]
        array[:margin,:] = array[-margin * 2:-margin,:]
        array[:,-margin:] = array[:,margin:margin * 2]
        array[:,:margin] = array[:,-margin * 2:-margin]

    @staticmethod
    def stitch_1(array, margin = 1):
        array[-1,:] = array[1,:]
        array[0,:] = array[-2,:]
        array[:,-1] = array[:,1]
        array[:,0] = array[:,-2]

    @staticmethod
    def map_point(point, array, margin = 1):
        return (point[0] % (array.shape[0] - margin*2),
                point[1] % (array.shape[1] - margin*2))

    @staticmethod
    def map_slice(upper_left, array, margin = 1):
        x0, y0 = _torus.map_point(upper_left, array, margin)
        x1, y1 = (array.shape[0] - margin*2,
                  array.shape[1] - margin*2)
        return array[x0:x1, y0:y1]

@register('compile_topology', type='torus')
def _go(*args):
    return _torus

def torus():
    return topology('torus')
