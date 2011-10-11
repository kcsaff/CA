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
import itertools
import numpy

def cc1_evolve(input, output, lookup):
    """Evolve it."""
    output[:,:,0] *= lookup[9] #history
    X = input.shape[0]
    Y = input.shape[1]
    for i, (y,x) in enumerate( itertools.product((-1,0,1), (-1,0,1)) ):
        if lookup[i]:
            output[+1:-1,+1:-1,0] += input[x+1:X+x-1,y+1:Y+y-1,0] * lookup[i]
    if lookup[10]:
        output[:,:,0] += lookup[10] * input[:,:,1]
    if lookup[11]:
        denom = lookup[11]
        output[:,:,0] *= denom / (input[:,:,1] + denom)
    output[:,:,1] = input[:,:,1]
    M = numpy.max(numpy.abs(output[:,:,0]))
    if M > 10:
        #M = numpy.sum(numpy.square(numpy.abs(output[:,:,0])))
        print 'rescaling %s' % M
        output[:,:,0] /= M
        input[:,:,0] /= M
    else:
        print '.'
    return
    
    return generate.inline("""
    PyArrayObject *input;
    PyArrayObject *output;
    PyArrayObject *lookup;
    char h = 0;
    unsigned xstride, ystride;
    unsigned xa, x0, x1, xM;
    unsigned ya, y0, y1, yM;

    double daa, d0a, d1a;
    double da0, d00, d10;
    double da1, d01, d11;
    double d00d;

    double damp;
    double excite;

    double z;
    double rmin, rmax;
    double rn, rp;

    double *ind, *oud, *look;

    if (!PyArg_ParseTuple(args, "O!O!O!",
            &PyArray_Type, &input,
            &PyArray_Type, &output,
            &PyArray_Type, &lookup
            ))
        return NULL;
    xstride = input-> strides[0] >> 3;
    ystride = input-> strides[1] >> 3;

    xM = (input-> dimensions[0] - 1) * xstride;
    yM = (input-> dimensions[1] - 1) * ystride;

    ind = (double*)(input-> data);
    oud = (double*)(output-> data);
    look = (double*)(lookup-> data);
    daa = look[0];
    d0a = look[1];
    d1a = look[2];
    da0 = look[3];
    d00 = look[4];
    d10 = look[5];
    da1 = look[6];
    d01 = look[7];
    d11 = look[8];
    d00d= look[9];
    damp= look[10];
    excite= look[11];
    rmin = look[12];
    rmax = look[13];
    rn = look[14];
    rp = look[15];

    for (x0 = xstride; x0 < xM; x0 += xstride)
    {
        xa = x0 - xstride;
        x1 = x0 + xstride;
        for (y0 = ystride; y0 < yM; y0 += ystride)
        {
            ya = y0 - ystride;
            y1 = y0 + ystride;
            
            z = ind[xa + ya] * daa +
                ind[x0 + ya] * d0a +
                ind[x1 + ya] * d1a +
                ind[xa + y0] * da0 +
                ind[x0 + y0] * d00 +
                ind[x1 + y0] * d10 +
                ind[xa + y1] * da1 +
                ind[x0 + y1] * d01 +
                ind[x1 + y1] * d11 +
                oud[x0 + y0] * d00d;
            z *= damp;
            z += excite;
            if (z < rmin)
                z = rn;
            else if (z > rmax)
                z = rp;
            oud[x0 + y0] = z;
        }
    }
    return PyFloat_FromDouble(1.0);
    """)(input, output, lookup)

import numpy

from _util import register
from _algorithm import algorithm

@register('compile_rule', type='complex', quality=1.0)
def _complex(X):
    lookup = list(X.moore)
    lookup.append(X.history)
    lookup.append(X.potential)
    lookup.append(X.denom)
    return algorithm('complexscan', 
                     evolve=cc1_evolve,
                     table=numpy.asarray(lookup, dtype = numpy.complex128),
                     planes=2)
