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

from _rule import rule

def water(moore=[0.0, 0.5, 0.0,
                 0.5, 0.0, 0.5,
                 0.0, 0.5, 0.0],
          history = -1.0,
          damping = 0.03,
          heat = 0,
          min = 0.0, max = 255.9,
          under = 0.0, over = 255.9
          ):
    return rule('water',
                moore=moore,
                history=history,
                damping=damping,
                heat=heat,
                min=min, max=max,
                under=under, over=over)
    
def boiling_water():
    return water(moore=[0.15, 0.35, 0.15,
                        0.35, 0.00, 0.35,
                        0.15, 0.35, 0.15],
                 history = -1.0,
                 damping = 0.005,
                 heat = 1,
                 min = 0.0, max = 255.9,
                 under = 0.0, over = 0.0)
    
def dunes():
    return water(moore=[0.15, 0.30, 0.10,
                        0.40, 0.00, 0.20,
                        0.15, 0.30, 0.10],
                 history = -0.7,
                 damping = 0.0,
                 heat = 0,
                 min = 0.0, max = 255.9,
                 under = 0.0, over = 255.9)
    
def aurora():
    
    lookup = [0.10, 0.20, 0.10,
              0.20, 0.00, 0.20,
              0.10, 0.20, 0.10,
              -0.20,
              1.0, 
              1.0,
              0.0, 255.9,
              0.0, 0.0]
    return numpy.asarray(lookup, dtype = numpy.float)

    
