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

import logging

logger = logging.getLogger('file.common')

def read_hash_raw(input):
    result = {}
    for line in input:
        if '#' in line:
            normalized_line = line.split('#', 1) [1]
            key, value = normalized_line.split(' ', 1)
            result.setdefault(key, []).append(value.strip())

    return result

def read_hash(input, 
              joins={},
              defaults={},
              evals={}):
    result = read_hash_raw(input)
    
    for key in list(result.keys()):
        if key in joins:
            result[key] = joins[key].join(result[key])
        else:
            values = result[key]
            if len(values) != 1:
                logger.warn("Only the first value of '%s' (%s) will be used.",
                            key, result)
            result[key] = result[key][0]

        if key in evals:
            result[key] = evals[key](result[key])

    for key, value in defaults.items():
        if key not in result:
            result[key] = value
    
    return result

def write_hash_raw(output, dict):
    for key, value in dict.items():
        for line in value:
            output.write('#%s %s' % (key, line))
            output.write('\n')
