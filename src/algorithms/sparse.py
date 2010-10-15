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

import operator

def evolve(input, output, lookup):
    #activate
    output.clear()
    for location, state in input.items():
        if state in lookup.activation:
            for relative, adjustment in lookup.activation:
                pos = tuple(map(operator.add, location, relative))
                if pos in output:
                    output[pos] = tuple(map(operator.add, output[pos], adjustment))
                else:
                    output[pos] = adjustment
    #reduce
    for location, activated_state in list(output.items()):
        reduced_state = lookup.reduction[activated_state]
        if reduced_state is not lookup.quiescent:
            output[location] = reduced_state
        else:
            del output[location]
    #return
    return 1.0
        

from _util import register
from _algorithm import algorithm
import numpy
    
@register('compile_rule', type='redox', quality=1.0)
def _redox(X):
    lookup = X.copy()
    lookup.reduction = numpy.array(lookup.reduction, numpy.uint8)
    states = range(max(lookup.activation.keys()) + 1)
    return algorithm('redox',
                     evolve=evolve,
                     table=lookup,
                     states=states,
                     chart='sparse')
    