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

import numpy

class torus(object):
    @staticmethod
    def stitch(array, margin=1):
        if isinstance(array, list):
            for chart in array:
                torus.stitch(chart, margin)
            return
    
        if margin == 1: #optimization
            return torus.stitch_1(array, margin)
    
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
        x0, y0 = torus.map_point(upper_left, array, margin)
        x1, y1 = (array.shape[0] - margin*2,
                  array.shape[1] - margin*2)
        return array[x0:x1, y0:y1]
    
def torusfall(fall):
    class torusfall(torus):
        @staticmethod
        def stitch(array, margin=1):
            if isinstance(array, list):
                for chart in array:
                    torusfall.stitch(chart, margin)
                return
            torus.stitch(array, margin)
            array[:,:margin] += fall
            array[:,-margin:] -= fall
    return torusfall

class rectangle(object):
    @staticmethod
    def stitch(array, margin = 1):
        return

    @staticmethod
    def map_point(point, array, margin = 1):
        return point

    @staticmethod
    def map_slice(upper_left, array, margin = 1):
        x, y = rectangle.map_point(upper_left, array, margin)
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
        
class projective_plane(object):
    @staticmethod
    def stitch(array, margin = 1):
        if margin == 1: #optimization
            return projective_plane.stitch_1(array, margin)
        array[-margin:,:] = array[margin:margin * 2,::-1]
        array[:margin,:] = array[-margin * 2:-margin,::-1]
        array[:,-margin:] = array[::-1,margin:margin * 2]
        array[:,:margin] = array[::-1,-margin * 2:-margin]

    @staticmethod
    def stitch_1(array, margin = 1):
        array[-1,:] = array[1,::-1]
        array[0,:] = array[-2,::-1]
        array[:,-1] = array[::-1,1]
        array[:,0] = array[::-1,-2]

    @staticmethod
    def map_point(point, array, margin = 1):
        d = [(point[i] // (array.shape[i] - margin*2)) % 2 for i in (0, 1)]
        r = [(point[i] % (array.shape[i] - margin*2)) + margin for i in (0, 1)]
        for i in (0, 1):
            if d[1 - i]:
                r[i] = array.shape[i] - 1 - r[i]
        return r

    @staticmethod
    def map_slice(upper_left, array, margin = 1):
        d = [(upper_left[i] // (array.shape[i] - margin*2)) % 2 for i in (0, 1)]
        x0, y0 = projective_plane.map_point(upper_left, array, margin)
        if not d[1]:
            x1 = array.shape[0] - margin
        else:
            x1 = margin - 1
        if not d[0]:
            y1 = array.shape[1] - margin
        else:
            y1 = margin - 1
    
        return array[x0:x1:(1 - 2*d[1]), y0:y1:(1 - 2*d[0])]

