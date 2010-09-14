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


import lib.fits as fits
import qdict
import views
import formats
import meta

SPECIAL_RECORD_HEADER = 'SIMPLE  = CA SCANNER META\n'
SPECIAL_RECORD_SIZE = fits.RECORD_SIZE - len(SPECIAL_RECORD_HEADER)

def read(filename, file=None):
    result = qdict.qdict()
    data = fits.read(file or open(filename, 'rb'))
    extra = ''.join([record[len(SPECIAL_RECORD_HEADER):] 
                     for record in data.special_records
                     if record.startswith(SPECIAL_RECORD_HEADER)])
    result.update(meta.decode(extra))

    result.reduce_quality(0.2) #We want these overridden by external data if necessary.
    result['palette', 0.1, filename] = views.palette.grays
   
    naxis = data.hdu[0]['NAXIS*']
    ctype = data.hdu[0]['CTYPE*']
    crpix = data.hdu[0]['CRPIX*']
    if crpix:
        result['center', 1.0, filename] = (crpix[0] - 1, crpix[1] - 1)
    if ctype and ctype[-1] == 'HISTORY' and ctype[-2] == 'CHART':
        atlases = []
        for atlasno in range(naxis[-1]):
            atlas = []
            atlases.append(atlas)
            for chartno in range(naxis[-2]):
                chart = data.hdu[0].data[atlasno, chartno, ...]
                atlas.append(chart.transpose())
        formats.set_atlases(result, atlases)
        
    else:
        chart = data.hdu[0].data.transpose()
        result['chart(%d,%d)' % formats.get_subscripts(filename), 1.0, filename] = chart
        
    return result

def write(filename, data, file=None, chart=(0,0)):
    atlases = formats.get_atlases(data)
    for i, atlas in enumerate(list(atlases)):
        for j, chart in enumerate(list(atlas)):
            atlases[i][j] = chart.transpose()
            
    meta_to_store = dict(data)
    del meta_to_store['center'] #put in CRPIX in header.
    extra = meta.encode(meta_to_store)
    special_records = []
    while extra:
        special_records.append(SPECIAL_RECORD_HEADER + extra[:SPECIAL_RECORD_SIZE])
        extra = extra[SPECIAL_RECORD_SIZE:]

    if 'center' in data:
        center = data['center']
        crpix = [center[0] + 1, center[1] + 1, 1, 1]
        
    fits.write(file or open(filename, 'wb'), 
               atlases,
               special_records=special_records,
               ctype=('X', 'Y', 'CHART', 'HISTORY'),
               crpix=crpix
               )
