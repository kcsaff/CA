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

"""
This algorithm handles 256 states, packed at 1 cell per byte.
A cell is considered 'active' ONLY if it is 1.  Otherwise, it is inactive.
The state of a cell after evolution depends on its complete 8-bite state
and on the activity of the 8 cells in its Moore(1) neighborhood.

The bits for the lookup table are as follows:
[ 0][ 1][ 2]
[ 3][*4][ 5]
[ 6][ 7][ 8]

Bits 9-16 are the entirety of the state.

"""

import generate

@generate.c
def evolve():
    """Evolve it."""
    return """
    PyArrayObject *input;
    PyArrayObject *output;
    PyArrayObject *lookup;
    char h = 0;
    unsigned xstride, ystride;
    unsigned xa, x0, x1, xM;
    unsigned /*ya,*/ y0, y1, yM;
    unsigned z;
    char c, n, r;

    if (!PyArg_ParseTuple(args, "O!O!O!",
            &PyArray_Type, &input,
            &PyArray_Type, &output,
            &PyArray_Type, &lookup
            ))
        return NULL;
    xstride = input-> strides[0];
    ystride = input-> strides[1];

    xM = (input-> dimensions[0] - 1) * xstride;
    yM = (input-> dimensions[1] - 1) * ystride;

    xa = 0;

    for (x0 = xstride; x0 < xM; x0 += xstride)
    {
        xa = x0 - xstride;
        x1 = x0 + xstride;
        n = input-> data[x0 + 1 * ystride];
        z = ((input-> data[xa + 0 * ystride] == 1) << 0x3) |
            ((input-> data[x0 + 0 * ystride] == 1) << 0x4) |
            ((input-> data[x1 + 0 * ystride] == 1) << 0x5) |
            ((input-> data[xa + 1 * ystride] == 1) << 0x6) |
            ((n == 1) << 0x7) |
            ((input-> data[x1 + 1 * ystride] == 1) << 0x8) ;
        for (y0 = ystride; y0 < yM; y0 += ystride)
        {
            z >>= 3;
            y1 = y0 + ystride;
            c = n;
            n = input-> data[x0 + y1];
            z |=((input-> data[xa + y1] == 1) << 0x6) |
                ((n == 1) << 0x7) |
                ((input-> data[x1 + y1] == 1) << 0x8) ;
            r = lookup-> data[z | (c << 9)];
            output-> data[x0 + y0] = (char)r;
        }
    }
    return PyFloat_FromDouble(1.0);
    """
             


generate.auto_generate(__name__)


import numpy
from _util import bit_count, register

@register('compile_rule', type='life', quality=0.9)
def _life(X):
    birth, survival = X.birth, X.survival
    
    lookup0 = []
    
    for i in range(0x200):
        if bit_count[i & 0x1EF] in (birth, survival)[(i & 0x10) and 1]:
            lookup0.append(1)
        else:
            lookup0.append(0)
            
    return (evolve,
            numpy.tile(numpy.asarray(lookup0, dtype = numpy.uint8), 0x80),
            (0,1))
    
@register('compile_rule', type='brain', quality=1.0)
def _brain(X):
    
    print X
    
    birth, survival, decay = X.birth, X.survival, X.decay
    
    lookup = numpy.ndarray(shape=0x20000, dtype=numpy.uint8)
    
    mdecay = decay + 2
    
    if mdecay > 256:
        mdecay = 256
    
    for i in range(0x20000):
        if i & 0x10: #alive
            if bit_count[i & 0x1EF] in survival:
                lookup[i] = 1
            else:
                lookup[i] = 2 % mdecay
        elif i < 0x200: #dead
            lookup[i] = bit_count[i & 0x1FF] in birth and 1 or 0
        else: #dying
            lookup[i] = ((i >> 9) + 1) % mdecay
            
    return evolve, lookup, range(decay + 2)

#[ 0][ 1][ 2]
#[ 3][*4][ 5]
#[ 6][ 7][ 8]
@register('compile_rule', type='banks', quality=1.0)
def _banks(X,
           out_to_in = None): 

    birth, survival, decay = X.birth, X.survival, X.decay
    
    if out_to_in is None:
        #in order NESW, like mcell
        if len(birth) <= 16:
            out_to_in = {1 << 1:1 << 0, 
                         1 << 3:1 << 3, 
                         1 << 5:1 << 1, 
                         1 << 7:1 << 2}
        else:
            out_to_in = {1 << 0:1 << 7,
                         1 << 1:1 << 0,
                         1 << 2:1 << 1,
                         1 << 3:1 << 6,
                         1 << 5:1 << 2,
                         1 << 6:1 << 5,
                         1 << 7:1 << 4,
                         1 << 8:1 << 3}
    
    lookup = numpy.ndarray(shape=0x20000, dtype=numpy.uint8)
    
    mdecay = decay + 2
    
    if mdecay > 256:
        mdecay = 256
    
    for i in range(0x20000):
        target = 0
        for obit, ibit in out_to_in.items():
            if i & obit:
                target |= ibit
            
        if i & 0x10: #alive
            if survival[target]:
                lookup[i] = survival[target]
            else:
                lookup[i] = 2 % mdecay
        elif i < 0x200: #dead
            lookup[i] = birth[target]
        else: #dying
            lookup[i] = ((i >> 9) + 1) % mdecay
            
    return evolve, lookup, range(decay + 2)
    
