
"""
This algorithm handles 256 states, packed at 1 cell per byte.
A cell is considered 'active' if its low bit is 1.  Otherwise, it is inactive.
The state of a cell after evolution depends on its complete 8-bite state
and on the activity of the 8 cells in its Margolus(1) neighborhood.

The bits for the lookup table are as follows:
[ 0][ 1][ 2]
[ 3][*4][ 5]
[ 6][ 7][ 8]

Bits 9-15 are the remainder of the state, minus the activity bit.
"""

import generate

functions = [
('evolve', 'Evolve it.',
"""
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
        z = ((input-> data[xa + 0 * ystride] & 1) << 0x3) |
            ((input-> data[x0 + 0 * ystride] & 1) << 0x4) |
            ((input-> data[x1 + 0 * ystride] & 1) << 0x5) |
            ((input-> data[xa + 1 * ystride] & 1) << 0x6) |
            ((n & 1) << 0x7) |
            ((input-> data[x1 + 1 * ystride] & 1) << 0x8) ;
        for (y0 = ystride; y0 < yM; y0 += ystride)
        {
            z >>= 3;
            y1 = y0 + ystride;
            c = n;
            n = input-> data[x0 + y1];
            z |=((input-> data[xa + y1] & 1) << 0x6) |
                ((n & 1) << 0x7) |
                ((input-> data[x1 + y1] & 1) << 0x8) ;
            r = lookup-> data[z | ((c & 0xFE) << 8)];
            output-> data[x0 + y0] = (char)r;
        }
    }
    return PyFloat_FromDouble(1.0);
"""),
]
             


generate.auto_generate(__name__, 'algorithm')
    
    