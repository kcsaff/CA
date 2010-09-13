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

import logging, numpy
import views
import worlds
import common
import rules.life
from topologies._topology import topology
import registry

#Basic MCell file format is ascii extension of Life 1.05.

END_LINE = object()

special_chars = {'.' : 0,
                 '*' : 1,
                 '$' : END_LINE,
                 }

logger = logging.getLogger('file.mcell')

def _rle_iterator(rle):
    runlength = 0
    modifier = 0
    for i, x in enumerate(rle):
        if '0' <= x <= '9': #runlength encoding
            if runlength:
                runlength *= 10
            runlength += ord(x) - ord('0')
        elif 'a' <= x <= 'j': #adds 24*n to a character.
            modifier = (ord(x) - ord(x) + 1) * 24
        else: #An actual value: . is 0 and A, B, C, and up are 1, 2, 3, etc
            value = special_chars.get(x, ord(x) - ord('A') + 1)
            if modifier != 0:
                value += modifier
            if value is not END_LINE and not (0 <= value < 256):
                logger.warn("Invalid character '%s' (#%d) seen in RLE mcell file",
                            x, i)
            for _ in range(max(1, runlength)):
                yield value
            runlength = modifier = 0
            
def _rle_mirek_iterator(rle):
    runlength = 0
    for i, x in enumerate(rle):
        if '0' <= x <= '9': #runlength encoding
            if runlength:
                runlength *= 10
            runlength += ord(x) - ord('0')
        else: #An actual value: a is 0 and b, c, d, and up are 1, 2, 3, etc
            value = ord(x) - ord('a')
            if not (0 <= value < 256):
                logger.warn("Invalid character '%s' (#%d) seen in RLE mcell file",
                            x, i)
            for _ in range(max(1, runlength)):
                yield value
            runlength = 0

    
def _parse_life_rule(rulestring, format):
    formats = format.split('/')
    rulestrings = rulestring.split('/')
    if len(formats) != len(rulestrings):
        raise ValueError, 'Rule "%s" does not fit format "%s".' % (rulestring, format)
    result = []
    for r, f in zip(rulestrings, formats):
        if f == 's':
            result.append([ord(x) - ord('0') for x in r])
        elif f == 'n':
            result.append(int(r))
        else:
            raise ValueError, 'Unknown rule format "%s".' % f
        
    return result

def _parse_mirek_rule(rulestring):
    
    def my_split(part):
        part = part.strip()
        return part[0], part[1:]
    
    parts = dict([my_split(part) for part in rulestring.split(',')])
    if 'C' in parts:
        parts['C'] = max(2, int(parts['C'])) #count of number of states
        
    return parts

def _Life(game, rule, ccolors, coloring):
    survival, birth = _parse_life_rule(rule, 's/s')
    print birth, survival
    return rules.life.life(set(birth), set(survival))

def _Generations(game, rule, ccolors, coloring):
    survival, birth, count = _parse_life_rule(rule, 's/s/n')
    print birth, survival, count
    return rules.life.brain(set(birth), set(survival), count - 2)

def _General_binary(game, rule, ccolors, coloring):
    parts = _parse_mirek_rule(rule)
    birth = [x for x in _rle_mirek_iterator(parts['B'])]
    survival = [x for x in _rle_mirek_iterator(parts['S'])]
    count = parts['C']
    print parts
    
    if parts['N'] not in ['N', 'M']:
        raise ValueError, 'Neighborhood "%s" not implemented for general binary.' % parts['N']
    return rules.life.banks(birth, survival, count-2)
    

__rules = {'Life': _Life,
           'Generations': _Generations,
           'General binary': _General_binary,
           }

def _create_rule(game, rule, ccolors, coloring):
    print rule
    if coloring != 1:
        raise ValueError, 'Alternate coloring not yet supported.'
    rule_generator = __rules.get(game, None)
    if rule_generator is not None:
        return rule_generator(game, rule, ccolors, coloring)
    else:
        raise ValueError, 'Game "%s" not yet implemented.' % game
            
def _create_field(board, L):
    margin = 1
    dimensions = [int(d) + 2 * margin for d in board.strip().split('x')]
    result = numpy.zeros(dimensions, dtype=numpy.uint8)
    #print L
    x = y = margin
    for value in _rle_iterator(L):
        if value is END_LINE:
            x = margin
            y += 1
            #print '\n',
        else:
            result[x, y] = value
            x += 1
            #print value,
    return result

def _create_topology(wrap):
    if wrap:
        return topology('torus')
    else:
        return topology('rectangle')
    
def _create_palette(palette):
    if palette:
        raise ValueError, 'Unable to load palette "%s".' % palette
    return None
            
def _create_objects(objects):
    if objects:
        raise ValueError, 'Unable to create any objects.' 
    return None

_line_join = {'RULE': '',
              'D': '\n',
              'L': '',
              'DIV': '\n',
              }

_defaults = {'GAME': 'Life',
             'RULE': '23/3',
             'SPEED': 0,
             'BOARD': None,
             'CCOLORS': 0,
             'COLORING': 1,
             'WRAP': 0,
             'PALETTE': None,
             'D': '(No description)',
             'L': None,
             'DIV': ''
             }

_evals = {'SPEED': float,
          'CCOLORS': int,
          'COLORING': int,
          'WRAP': int,
          }

def _interpret_raw(data):
    if 'MCell' not in data:
        raise ValueError, 'Not recognized as an MCell file.'

    rule = _create_rule(data['GAME'], 
                        data['RULE'], 
                        data['CCOLORS'],
                        data['COLORING'],
                        )

    _, _, states = registry.get.compile_rule(rule)
    
    chart = _create_field(data['BOARD'],
                          data['L'])
    
    #Fix states.
    #The state numbers used to define the grid may be different
    # from those we use internally, so we have to map them over.
    for x in range(chart.shape[0]):
        for y in range(chart.shape[1]):
            chart[x,y] = states[chart[x,y]]
    
    topology = _create_topology(data['WRAP'])
    
    palette = _create_palette(data['PALETTE'])
    
    delay = data['SPEED'] / 1000.0 #seconds to delay between frames
    
    description = data['D']
    
    objects = _create_objects(data['DIV'])
    
    world = worlds.World()
    view = views.View()
    
    if rule:
        world.rule = rule
    if chart is not None:
        world.charts = [chart]
    if topology:
        world.topology = topology
        
    if palette:
        view.palette = palette
    else:
        view.palette = views.palette.mcell(states)
    if delay:
        view.speed = 2.0 / delay
    if description:
        world.description = view.description = description
    if objects:
        world.objects = objects
        
    return world, view
        
def read(file):
    if isinstance(file, (str, unicode)): #just a filename
        file = open(file, 'r')
    return _interpret_raw(common.read_hash(file,
                                           joins=_line_join,
                                           defaults=_defaults,
                                           evals=_evals))
        
