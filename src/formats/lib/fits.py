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
import time
from compat import OrderedDict

logger = logging.getLogger('lib.fits')

KEY_SIZE = 8
CARD_SIZE = 80
CARDS_PER_RECORD = 36
RECORD_SIZE = CARD_SIZE * CARDS_PER_RECORD #2880
SPECIAL_RECORD_ID = 'SIMPLE  '

class Hdu(object):
    headers = OrderedDict()
    data = None
    def __getitem__(self, key):
        if key.endswith('n'):
            result = []
            for n in range(1, 1000):
                keyn = '%s%d' % (key, n)
                if keyn in self.headers:
                    result.append(self.headers[keyn])
                else:
                    return result
        elif key in self.headers:
            return self.headers[key]
        else:
            raise KeyError
    def __setitem__(self, key, value):
        if key.endswith('n'):
            for n, subval in enumerate(value):
                self.headers['%s%d' % (key, n + 1)] = subval
        else:
            self.headers[key] = value

class Fits(object):
    hdus = []
    special_records = []

def _to_record_multiple(value):
    return value + (-value % RECORD_SIZE)

def _read_partwise(file, amount):
    """
    Use when a filelike object doesn't always return enough bytes from
    a .read method.
    """
    result = []
    while amount > 0:
        result.append(file.read(amount))
        length = len(result[-1])
        amount -= length
        if length == 0:
            break
    return ''.join(result)

def _read_value(value):
    if value == 'T':
        return True
    elif value == 'F':
        return False
    elif value.startswith("'") and value.endswith("'"):
        return value[1:-1]
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
        return 'T'.rjust(20)
    elif value is False:
        return 'F'.rjust(20)
    elif isinstance(value, (int, float)):
        return repr(value).rjust(20)
    else:
        return "'%s'" % value

def _read_all_headers(file):
    end_found = False
    headers = []
    while not end_found:
        for _ in range(CARDS_PER_RECORD):
            header = file.read(CARD_SIZE)
            key = header[:KEY_SIZE].strip() or None
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
    result = OrderedDict()
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

def _byte_reorder(string, length):
    if length == 1:
        return string
    result = []
    for i in range(0, len(string), length):
        result.append(string[i:i+length][::-1])
    return ''.join(result)

def _read_data(file, headers):
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
    bytedata = _read_partwise(file, _to_record_multiple(count * abs(bitpix) // 8))
    open('temp.dat', 'wb').write(_byte_reorder(bytedata, abs(bitpix) // 8))
    data = numpy.fromfile(open('temp.dat', 'rb'),
                          dtype=_rtypes[bitpix],
                          count=count)
    #And actually the whole temp file here is a workaround for numpy.fromfile
    # not being able to use the filelike object here.
    try:
        data = data.reshape(shape)
    except ValueError:
        print shape, data.shape, count
        raise
    
    return data.transpose()
    
def _read_special_records(file):
    result = []
    while True:
        record = _read_partwise(file, RECORD_SIZE)
        if record:
            result.append(record)
        else:
            return result
    
def _read_fits(file):
    result = Fits()
    hdu = Hdu()
    hdu.headers = _read_headers(file)
    hdu.data = _read_data(file, result.headers)
    result.hdus = [hdu]
    result.special_records = _read_special_records(file)
    return result

def _write_card(key, value, comment):
    result = []
    result.append(key[:KEY_SIZE].ljust(KEY_SIZE))
    if value is not None:
        result.append('= ')
        result.append(_write_value(value))
    if comment is not None:
        result.append(' /')
        result.append(comment)
    return ''.join(result)[:CARD_SIZE].ljust(CARD_SIZE)
    

def _write_all_headers(file, headers):
    for header in headers:
        file.write(_write_card(*header))
    count = len(headers)
    while count % CARDS_PER_RECORD != 0:
        file.write(' ' * CARD_SIZE)
        count += 1

def _write_headers(file, data, headers={}, ctype=[]):
    headerlist = []
    
    bigshape = []
    indata = data
    while not hasattr(indata, 'shape'):
        bigshape.append(len(indata))
        indata = indata[0]
    
    headerlist.append(('SIMPLE', True, None))
    headerlist.append(('BITPIX', _wtypes[indata.dtype], None))
    headerlist.append(('NAXIS', len(bigshape) + len(indata.shape), None))
    for i, dim in enumerate(reversed(bigshape + list(indata.shape))):
        headerlist.append(('NAXIS%d' % (i + 1), dim, None))
        
    for key, values in headers.items():
        for value in values.split('\n'):
            headerlist.append((key, value, None))
    for i, ctypestr in enumerate(ctype):
        headerlist.append(('CTYPE%d' % (i + 1), ctypestr, None))
    if 'DATE' not in headers:
        headerlist.append(('DATE', 
                           time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime()),
                           None
                           ))
    headerlist.append(('END', None, None))
    _write_all_headers(file, headerlist)
    
def _do_write_data(file, data):
    if hasattr(data, 'tofile'):
        data.tofile(file)
    else:
        for item in data:
            _do_write_data(file, item)
            
def _get_in_data(data, attr):
    while not hasattr(data, attr):
        data = data[0]
    return getattr(data, attr)

def _write_data(file, data):
    
    _do_write_data(open('temp.dat', 'wb'), data) #workaround
    #data.tofile(file) #doesn't work for StringIO :(
    bytedata = _byte_reorder(open('temp.dat', 'rb').read(), 
                             _get_in_data(data, 'dtype').itemsize)
    file.write(bytedata)
    lenfill = -len(bytedata) % RECORD_SIZE
    file.write(chr(0) * lenfill)
    
def _write_special_record(file, record):
    if not record.startswith(SPECIAL_RECORD_ID):
        record = SPECIAL_RECORD_ID + record
    file.write(record[:RECORD_SIZE].ljust(RECORD_SIZE))

def _write_fits(file, data, 
                headers={}, 
                special_records=[],
                ctype=[]):
    _write_headers(file, data, headers, ctype=ctype)
    _write_data(file, data)
    for record in special_records:
        _write_special_record(file, record)

def read(filename):
    if hasattr(filename, 'read'):
        file = filename
    else:
        file = open(filename, 'rb')
    return _read_fits(file)

def write(filename, data, headers={}, special_records=[], ctype=[]):
    if hasattr(filename, 'write'):
        file = filename
    else:
        file = open(filename, 'wb')
    return _write_fits(file, data, 
                       headers=headers, 
                       special_records=special_records,
                       ctype=ctype)
