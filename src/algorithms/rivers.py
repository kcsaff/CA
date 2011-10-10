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
    
#define ABS(X) ((X) < 0 ? -(X) : +(X))
#define POS(X) ((X) > 0 ? (X) : 0)
#define NEG(X) ((X) < 0 ? (X) : 0)
#define MIN(X, Y) ((X) < (Y) ? (X) : (Y))
#define MAX(X, Y) ((X) > (Y) ? (X) : (Y))
#define VS 0.001
#define WS 0.2
#define WIN(V0, W0, V1, W1) (POS(MIN((W1), ((V1)+(W1))-((V0)+(W0)) )))
#define WOUT(V0, W0, V1, W1) (WIN((V1), (W1), (V0), (W0)))
#define THRESH 0.2
// These define soil/water when we transform
#define TRANSERODE 1.0
#define TRANSDEPOSIT 1.0
// These define rate of erosion/deposition per velocity unit
#define RATEERODE 0.01
#define RATEDEPOSIT 0.001
    
    PyArrayObject *input;
    PyArrayObject *output;
    PyArrayObject *lookup;
    char h = 0;
    unsigned xstride, ystride, zstride;
    unsigned xa, x0, x1, xM;
    unsigned ya, y0, y1, yM;

    double *ind, *oud, *look;
    
    double v00, va0, v10, v0a, v01;
    double w00, wa0, w10, w0a, w01;
    double win, wout;
    double wvel, Dw, Dv;

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
            
            // v00 is sediment, w00 is water.
            v00 = ind[x0 + y0 + 0*zstride];
            va0 = ind[xa + y0 + 0*zstride];
            v10 = ind[x1 + y0 + 0*zstride];
            v0a = ind[x0 + ya + 0*zstride];
            v01 = ind[x0 + y1 + 0*zstride];
            
            w00 = ind[x0 + y0 + 1*zstride];
            wa0 = ind[xa + y0 + 1*zstride];
            w10 = ind[x1 + y0 + 1*zstride];
            w0a = ind[x0 + ya + 1*zstride];
            w01 = ind[x0 + y1 + 1*zstride];
            
            // Determine water flow in.
            
            win = 0;
            win += WIN(v00, w00, va0, wa0);
            win += WIN(v00, w00, v10, w10);
            win += WIN(v00, w00, v0a, w0a);
            win += WIN(v00, w00, v01, w01);
            win *= WS;
            
            // Determine water flow out.
            
            wout = 0;
            wout += WOUT(v00, w00, va0, wa0);
            wout += WOUT(v00, w00, v10, w10);
            wout += WOUT(v00, w00, v0a, w0a);
            wout += WOUT(v00, w00, v01, w01);
            wout *= WS;
            
            w00 = POS(w00 + win - wout);
            
            Dw = Dv = 0;
            // Determine water velocity.
            if (w00 > 0) {
                wvel = win / w00;
                // Perform erosion.
                if (wvel > THRESH) { // Erosion
                    Dw = (wvel - THRESH) * RATEERODE;
                    Dv = -Dw * TRANSERODE;
                } else { // Deposition
                    Dw = -MIN(w00, (THRESH - wvel) * RATEDEPOSIT);
                    Dv = -Dw * TRANSDEPOSIT;
                }
            }
            
            // Determine sediment shift.
            
            Dv += VS * (va0 + v10 + v0a + v01 - 4 * v00);
            
            // Write results.
            
            oud[x0 + y0 + 0*zstride] = v00 + Dv;
            oud[x0 + y0 + 1*zstride] = w00 + Dw;
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
