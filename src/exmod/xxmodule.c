#include "Python.h"
#include <stdlib.h>
#include "numpy/arrayobject.h"

static PyObject *ErrorObject;

/* Function of two integers returning integer */

PyDoc_STRVAR(xx_foo_doc,
"foo(i,j)\n\
\n\
Return the sum of i and j.");

static PyObject *
xx_foo(PyObject *self, PyObject *args)
{
	long i, j;
	long res;
	if (!PyArg_ParseTuple(args, "ll:foo", &i, &j))
		return NULL;
	res = i+j; /* XXX Do something here */
	return PyInt_FromLong(res);
}

PyDoc_STRVAR(xx_randomize_doc,
"randomize(array)\n\
\n\
Randomize it.");

static PyObject *
xx_randomize(PyObject *self, PyObject *args)
{
	PyArrayObject *array;
	int x, y;
	int xstride, ystride;
	int color;

	if (!PyArg_ParseTuple(args, "O!",
			&PyArray_Type, &array))
		return NULL;
	xstride = array-> strides[0];
	ystride = array-> strides[1];
	for (x = 0; x < array-> dimensions[0]; ++x)
		for (y = 0; y < array-> dimensions[1]; ++y)
		{
			color ^= rand() & 0xFFF;
			color <<= 12;
			color ^= rand() & 0xFFF;
			color &= 0xFFFFFF;
			*((int*)&((array-> data)[x * xstride + y * ystride])) = color;
		}
	return PyFloat_FromDouble(1.0);
}

PyDoc_STRVAR(xx_evolve_doc,
"evolve(input, output, lookup)\n\
\n\
Evolve it.");

static PyObject *
xx_evolve(PyObject *self, PyObject *args)
{
	PyArrayObject *input;
	PyArrayObject *output;
	PyArrayObject *lookup;
	char h = 0;
	unsigned xstride, ystride;
	unsigned xa, x0, x1, xM;
	unsigned ya, y0, y1, yM;
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
}


/* List of functions defined in the module */

static PyMethodDef xx_methods[] = {
	{"foo",		xx_foo,		METH_VARARGS,
		 	xx_foo_doc},
	{"randomize",		xx_randomize,		METH_VARARGS,
			xx_randomize_doc},
	{"evolve",		xx_evolve,		METH_VARARGS,
			xx_evolve_doc},
	{NULL,		NULL}		/* sentinel */
};

PyDoc_STRVAR(module_doc,
"This is a template module just for instruction.");

/* Initialization function for the module (*must* be called initxx) */

PyMODINIT_FUNC
initxx(void)
{
	PyObject *m;

	/* Create the module and add the functions */
	m = Py_InitModule3("xx", xx_methods, module_doc);
	if (m == NULL)
		return;

	//Use numpy arrays.
	import_array();

}
