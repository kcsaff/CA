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
This algorithm handles double-precision states.
Rules are defined using 10 weights, 2 modifiers, 2 limits, and 2 setpoints.

The first 9 weights describe the amount of each of the neighbors to
use to generate the new value:
[ 0][ 1][ 2]
[ 3][*4][ 5]
[ 6][ 7][ 8]
The tenth weight is the amount to weight the cell's second-to-last value.

One modifier is the dampener; the total will be multiplied by this.
The other modifier is the exciter; this will be added to the total.

The limits identify what the minimum and maximum allowed values are.

Finally, the two setpoints indicate what to do if the total goes out of range.
One indicates what to set the value to if it goes below the min, the other
if it goes above the max.
"""

import generate

def rivers_evolve(input, output, lookup):
    """Evolve it."""
    return generate.inline("""
    
#define ABS(X) ((X < 0 ? -X : +X))
#define INF 0.5
#define OUTF 0.2
#define STATF 0.3
    
    PyArrayObject *input;
    PyArrayObject *output;
    PyArrayObject *lookup;
    char h = 0;
    unsigned xstride, ystride, zstride;
    unsigned xa, x0, x1, xM;
    unsigned ya, y0, y1, yM;

    double *ind, *oud, *look;
    
    double v00, vX, vY;
    double vXa, vX1, vYa, vY1;
    double va0, v10, v0a, v01;
    double d00, dX, dY;
    double temp, accum;

    if (!PyArg_ParseTuple(args, "O!O!O!",
            &PyArray_Type, &input,
            &PyArray_Type, &output,
            &PyArray_Type, &lookup
            ))
        return NULL;
    xstride = input-> strides[0] >> 3;
    ystride = input-> strides[1] >> 3;
    zstride = input-> strides[2] >> 3;

    xM = (input-> dimensions[0] - 1) * xstride;
    yM = (input-> dimensions[1] - 1) * ystride;
    //zM = (input-> dimensions[2] - 1) * zstride;

    ind = (double*)(input-> data);
    oud = (double*)(output-> data);
    look = (double*)(lookup-> data);

    for (x0 = xstride; x0 < xM; x0 += xstride)
    {
        xa = x0 - xstride;
        x1 = x0 + xstride;
        for (y0 = ystride; y0 < yM; y0 += ystride)
        {
            ya = y0 - ystride;
            y1 = y0 + ystride;
            
            d00 = dX = dY = 0;
            
            // v00 is stationary, vX is X-motion, vY is Y-motion
            v00 = ind[x0 + y0 + 0*zstride];
            vX = ind[x0 + y0 + 1*zstride];
            vY = ind[x0 + y0 + 2*zstride];
            
            va0 = ind[xa + y0 + 0*zstride];
            v10 = ind[x1 + y0 + 0*zstride];
            v0a = ind[x0 + ya + 0*zstride];
            v01 = ind[x0 + y1 + 0*zstride];
            
            vXa = ind[xa + y0 + 1*zstride];
            vX1 = ind[x1 + y0 + 1*zstride];
            vYa = ind[x0 + ya + 2*zstride];
            vY1 = ind[x0 + y1 + 2*zstride];
            
            // Determine new total water level.
            
            d00 = v00 + INF * (vXa - vX1 + vYa - vY1);
            
            // Determine new X flow.
            
            dX = OUTF * (vXa + vX + vX1) + STATF * (va0 - v10);
            
            // Determine new Y flow.
            
            dY = OUTF * (vYa + vY + vY1) + STATF * (v0a - v01);
            
            // Cap outward flow.
            
            temp = ABS(dX) + ABS(dY);
            if (temp > d00) {
                dX *= (ABS(dX) / temp);
                dY *= (ABS(dY) / temp);
            }
            
            oud[x0 + y0 + 0*zstride] = d00;
            oud[x0 + y0 + 1*zstride] = dX;
            oud[x0 + y0 + 2*zstride] = dY;
        }
    }
    return PyFloat_FromDouble(1.0);
    """)(input, output, lookup)

import numpy

from _util import register
from _algorithm import algorithm

@register('compile_rule', type='rivers', quality=1.0)
def _rivers(X):
    lookup = list()
    return algorithm('floatscan', 
                     planes=3,
                     evolve=rivers_evolve,
                     table=numpy.asarray(lookup, dtype = numpy.float))
