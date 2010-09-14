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

from simple import rule

def redox(
          activation = {1: {(-1,-1): (0, 1),
                            (-1, 0): (0, 1),
                            (-1, 1): (0, 1),
                            ( 0,-1): (0, 1),
                            ( 0, 0): (1, 0),
                            ( 0, 1): (0, 1),
                            ( 1,-1): (0, 1),
                            ( 1, 0): (0, 1),
                            ( 1, 1): (0, 1),
          }},
          reduction = [[0, 0, 0, 1, 0, 0, 0, 0, 0],
                       [0, 0, 1, 1, 0, 0, 0, 0, 0]],
          quiescent = 0
          ):
    return rule('redox', 
                activation=activation, 
                reduction=reduction,
                quiescent=quiescent)
