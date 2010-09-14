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

import qdict
import common

def _interpret(data):
    result = qdict.qdict()

    if 'SPEED' in data:
        result['speed'] = 2000.0 / data['SPEED']
    if 'ZOOM' in data:
        result['zoom'] = data['ZOOM']
    if 'CENTER' in data:
        result['center'] = tuple([int(x) for x in data['CENTER']])
    if 'GENERATION' in data:
        result['generation'] = data['GENERATION']

    if 'RULE' in data:
        from rules._rule import rule
        result['rule'] = eval('rule(%s)' % data['RULE'])
    if 'WRAP' in data:
        from topologies._topology import topology
        result['topology'] = eval('topology(%s)' % data['WRAP'])
        
    return result

_evals = {'SPEED': float, #~milliseconds between frames
          'ZOOM': eval,
          'CENTER': str.split, #get later
          'GENERATION': int,
          }

def read(filename, file=None):
    return _interpret(common.read_hash(file or open(filename, 'r'),
                                       evals=_evals))


def encode(data):
    from StringIO import StringIO
    meta = {'SPEED': [2000.0 / data['speed']],
            'ZOOM': [data['zoom']],
            'CENTER': ['%s %s' % tuple(data['center'])],
            'GENERATION': [data['generation']],
            'RULE': [data['rule'].format_args()],
            'WRAP': [data['topology'].format_args()],
            }
    s = StringIO()
    common.write_hash_raw(s, meta)
    return s.getvalue()


def decode(data):
    from StringIO import StringIO
    return _interpret(common.read_hash(StringIO(data),
                                       evals=_evals))
    

def write(filename, data):
    raise NotImplementedError
    pass
