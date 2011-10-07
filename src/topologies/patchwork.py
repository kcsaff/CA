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

from _topology import topology

def patchwork(dimensions, connections):
    """
    `dimensions` should be a list of (width, height) pairs representing
    different charts.  
    `connections` are connections between those charts.  These are tuples
    of the form (2, 3, 'x', fun, invfun), where the third item is either 'x' or
    'y', describing if this connection is side-to-side or top-to-bottom.  
    The first two are the charts to connect. `fun` is the map, if any,
    to transform the margin when taking the first to the second.  `invfun`
    should be the reverse of this.  By default no transformation is applied.
    If `fun` is only a number, this is added for the transformation.  If
    `fun` is a pair, the first number is added and the second is taken modulo.
    In these cases `invfun` is not necessary.  If direction begins with '-'
    then the margin is reversed when being pasted.
    """
    return topology('patchwork',
                    dimensions=dimensions,
                    connections=connections,
                    )
    
def torus(width, height):
    return patchwork([(width, height)], [(0, 0, 'x'), (0, 0, 'y')])

def rectangle(width, height):
    return patchwork([(width, height)], [])
    