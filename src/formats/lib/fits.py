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
This is intended to be a lightweight implementation of the FITS
data format, described at 
http://fits.gsfc.nasa.gov/fits_documentation.html

It may not implement all features, and is not intended to compete
with either pyfits or pfits.  It is intended to be a drop-in, single
python file that should work anywhere numpy is available.
"""

import logging
import numpy
import operator

logger = logging.getLogger('lib.fits')

def _read_value(value):
    if value == 'T':
        return True
    elif value == 'F':
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value #is string?

def _write_value(value):
    if value is True:
        return 'T'
    elif value is False:
        return 'F'
    elif isinstance(value, (int, float)):
        return repr(value)
    else:
        return value

def _read_all_headers(file):
    end_found = False
    headers = []
    while not end_found:
        for _ in range(36):
            header = file.read(80)
            key = header[:8].strip() or None
            if header[8] == '=':
                value = header[10:].split('/')[0].strip()
                value = _read_value(value)
            else:
                value = None
            if '/' in header:
                comment = header.split('/')[1]
            else:
                comment = None
            if key == 'END':
                end_found = True
            elif key:
                headers.append((key, value, comment))
    return headers

def _read_headers(file):
    headers = _read_all_headers(file)
    result = {}
    for key, value, comment in headers:
        if key in result:
            result[key] = '\n'.join((result[key], value))
        else:
            result[key] = value
    return result

_rtypes = {8: numpy.uint8,
           16: numpy.int16,
           32: numpy.int32,
           -32: numpy.float32,
           -64: numpy.float64,
           }

_wtypes = {numpy.dtype(numpy.uint8):8,
           numpy.dtype(numpy.int16):16,
           numpy.dtype(numpy.int32):32,
           numpy.dtype(numpy.float32):-32,
           numpy.dtype(numpy.float64):-64,
           }
    
def _read_fits(file):
    headers = _read_headers(file)
    naxis = headers['NAXIS']
    shape = [1] * naxis
    for n in range(naxis):
        shape[n] = headers['NAXIS%d' % (n+1)]
    shape = list(reversed(shape))
    bitpix = headers['BITPIX']
    count = reduce(operator.mul, shape)

    #Would be this:
    #open('temp.dat', 'wb').write(file.read(count * abs(bitpix) // 8))
    #But zipfile has a bug when reading more than a few thousand 
    # characters at once (probably 16 bit ints in there) so we do this:
    open('temp.dat', 'wb').write(file.read())
    data = numpy.fromfile(open('temp.dat', 'rb'),
                          dtype=_rtypes[bitpix],
                          count=count)
    #And actually the whole temp file here is a workaround for numpy.fromfile
    # not being able to use the filelike object here.
    data = data.reshape(shape)
    return data, headers

def _write_all_headers(file, headers):
    for header in headers:
        fheader = [header[0][:8].ljust(8)]
        if header[1] is not None:
            fheader.append('= ')
            fheader.append(_write_value(header[1]))
        if header[2] is not None:
            fheader.append(' /')
            fheader.append(header[2])
        file.write(''.join(fheader)[:80].ljust(80))
    count = len(headers)
    while count % 36 != 0:
        file.write(' ' * 80)
        count += 1
    print len(file.getvalue()), 36 * 80

def _write_headers(file, data, headers={}):
    headerlist = []
    headerlist.append(('SIMPLE', True, None))
    headerlist.append(('BITPIX', _wtypes[data.dtype], None))
    headerlist.append(('NAXIS', len(data.shape), None))
    for i, dim in enumerate(reversed(data.shape)):
        headerlist.append(('NAXIS%d' % (i + 1), dim, None))
    for key, values in headers.items():
        for value in values.split('\n'):
            headerlist.append((key, value, None))
    headerlist.append(('END', None, None))
    _write_all_headers(file, headerlist)

def _write_data(file, data):
    data.tofile(open('temp.dat', 'wb')) #workaround
    #data.tofile(file) #doesn't work for StringIO :(
    file.write(open('temp.dat', 'rb').read())

def _write_fits(file, data, headers={}):
    _write_headers(file, data, headers)
    _write_data(file, data)

def read(filename):
    if hasattr(filename, 'read'):
        file = filename
    else:
        file = open(filename, 'rb')
    return _read_fits(file)

def write(filename, data, headers={}):
    if hasattr(filename, 'write'):
        file = filename
    else:
        file = open(filename, 'wb')
    return _write_fits(file, data, headers)
