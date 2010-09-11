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
    
def water():
    
    lookup = [0.0, 0.5, 0.0,
              0.5, 0.0, 0.5,
              0.0, 0.5, 0.0,
              -1.0,
              0.97, 
              128 * 0.015,
              0.0, 255.9,
              0.0, 255.9]
    return numpy.asarray(lookup, dtype = numpy.float)
    
def boiling_water():
    
    lookup = [0.15, 0.35, 0.15,
              0.35, 0.00, 0.35,
              0.15, 0.35, 0.15,
              -1.0,
              0.995, 
              1,
              0.0, 255.9,
              0.0, 0.0]
    return numpy.asarray(lookup, dtype = numpy.float)
    
def dunes():
    
    lookup = [0.15, 0.30, 0.10,
              0.40, 0.00, 0.20,
              0.15, 0.30, 0.10,
              -0.7,
              1.0, 
              0,
              0.0, 255.9,
              0.0, 255.9]
    return numpy.asarray(lookup, dtype = numpy.float)
    
def aurora():
    
    lookup = [0.10, 0.20, 0.10,
              0.20, 0.00, 0.20,
              0.10, 0.20, 0.10,
              -0.20,
              1.0, 
              1.0,
              0.0, 255.9,
              0.0, 0.0]
    result = numpy.asarray(lookup, dtype = numpy.float)
    print result
    return result
