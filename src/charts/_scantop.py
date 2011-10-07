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
    
        array[-margin:,...] = array[margin:margin * 2,...]
        array[:margin,...] = array[-margin * 2:-margin,...]
        array[:,-margin:,...] = array[:,margin:margin * 2,...]
        array[:,:margin,...] = array[:,-margin * 2:-margin,...]

    @staticmethod
    def stitch_1(array, margin = 1):
        array[-1,:,...] = array[1,:,...]
        array[0,:,...] = array[-2,:,...]
        array[:,-1,...] = array[:,1,...]
        array[:,0,...] = array[:,-2,...]

    @staticmethod
    def map_point(point, array, margin = 1):
        return (point[0] % (array.shape[0] - margin*2) + margin,
                point[1] % (array.shape[1] - margin*2) + margin)

    @staticmethod
    def map_slice(upper_left, array, margin = 1):
        x0, y0 = torus.map_point(upper_left, array, margin)
        x1, y1 = (array.shape[0] - margin,
                  array.shape[1] - margin)
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
        return (point[0] + margin, point[1] + margin)

    @staticmethod
    def map_slice(upper_left, array, margin = 1):
        x, y = rectangle.map_point(upper_left, array, margin)
        if x < margin and y < margin:
            return numpy.zeros(shape=(margin-x, margin-y), dtype=numpy.uint8)
        elif x < margin:
            return numpy.zeros(shape=(margin-x, 
                                      array.shape[1]-2*margin), 
                               dtype=numpy.uint8)
        elif y < margin:
            return numpy.zeros(shape=(array.shape[0]-2*margin, 
                                      margin-y), 
                               dtype=numpy.uint8)
        elif x >= array.shape[0] - margin or y >= array.shape[1] - margin:
            return numpy.zeros(shape=array.shape, dtype=array.dtype)
        else:
            if margin:
                return array[x:-margin, y:-margin]
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

class patchwork(object):
    def __init__(self, connections):
        self.connections = connections
        
        # Setup some stuff for mapping points.
        self.next = [{}, {}]
        self.prev = [{}, {}]
        for connection in connections:
            first, second = connection[:2]
            assert first <= second
            direction = connection[2]
            sign = -1 if direction.startswith('-') else +1
            dim = 'xy'.index(direction[-1])
            self.next[dim][first] = (second, sign)
            self.prev[dim][first] = (second, sign)
    
    def stitch(array, margin=1):
        for connection in self.connections:
            first, second = connection[:2]
            direction = connection[2]
            fun = connection[3] if len(connection) > 3 else None
            invfun = connection[4] if len(connection) > 4 else None
            if not fun:
                fun = invfun = lambda x: x
            elif isinstance(fun, (int, float, long)):
                fun = lambda x: x + fun
                invfun = lambda x: x - fun
            elif isinstance(fun, tuple):
                fun = lambda x: (x + fun[0]) % fun[1]
                fun = lambda x: (x - fun[0]) % fun[1]
            if direction.startswith('-'):
                D = -1
            else:
                D = +1
            if direction.endswith('x'):
                array[second][-margin:,:] = fun(array[first][margin:margin * 2,::D])
                array[first][:margin,:] = fun(array[second][-margin * 2:-margin,::D])
            elif direction.endswith('y'):
                array[second][:,-margin:] = fun(array[first][::D,margin:margin * 2])
                array[first][:,:margin] = fun(array[second][::D,-margin * 2:-margin])

    def map_point(point, array, margin = 1):
        off = [0, 0]
        sign = [1, 1]
        index = 0
        for i in (0, 1):
            while off[i] + array[index].shape[i] - margin*2 < point:
                off[i] += array[index].shape[i] - margin*2
                if index not in self.next[i]:
                    return None
                index, ns = self.next[i][index]
                sign[i] *= ns
            while off[i] > point:
                if index not in self.prev[i]:
                    return None
                index, ns = self.prev[i][index]
                sign[i] *= ns
                off[i] -= array[index].shape[i] - margin*2
        return (index, 
                point[0] - off[0] + margin, 
                point[1] - off[1] + margin)

    def map_slice(upper_left, array, margin = 1):
        index, x0, y0 = self.map_point(upper_left, array, margin)
        x1, y1 = (array[index].shape[0] - margin,
                  array[index].shape[1] - margin)
        return array[index][x0:x1, y0:y1]
    
