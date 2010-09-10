import logging, numpy
import views
import worlds

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
            for a in range(max(1, runlength)):
                yield value
            runlength = modifier = 0

def _raw_read(input):
    result = {}
    for line in input:
        if '#' in line:
            normalized_line = line.split('#', 1) [1]
            key, value = normalized_line.split(' ', 1)
            result.setdefault(key, []).append(value.strip())
    
    return result

    
def _parse_rule(rulestring, format):
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

def _create_rule(game, rule, ccolors, coloring):
    from algorithms.exmod import life, xx
    print rule
    if coloring != 1:
        raise ValueError, 'Alternate coloring not yet supported.'
    if game == 'Life':
        evolve = xx.evolve
        survival, birth = _parse_rule(rule, 's/s')
        print birth, survival
        table = life.lifelike(set(birth), set(survival))
        return evolve, table, range(2)
    elif game == 'Generations':
        evolve = xx.evolve
        survival, birth, count = _parse_rule(rule, 's/s/n')
        print birth, survival, count
        table = life.brainlike(set(birth), set(survival), count - 2)
        states = range(2) + range(2, (count - 1) * 2, 2)     
        return evolve, table, states
    else:
        raise ValueError, 'Game "%s" not yet implemented.' % game
            
def _create_field(board, L):
    margin = 1
    dimensions = [int(d) + 2 * margin for d in board.strip().split('x')]
    result = numpy.zeros(dimensions, dtype=numpy.uint8)
    print L
    x = y = margin
    for value in _rle_iterator(L):
        if value is END_LINE:
            x = margin
            y += 1
            print '\n',
        else:
            result[x, y] = value
            x += 1
            print value,
    return result

def _create_topology(wrap):
    from topology import rectangle, torus
    if wrap:
        return torus
    else:
        return rectangle
    
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

def _get(data, key):
    if key not in data:
        return _defaults[key]
    
    if key in _line_join:
        return _line_join[key].join(data[key])
    else:
        result = data[key][0]
        if len(data[key]) > 1:
            logger.warn("Only the first value of '%s' (%s) will be used.",
                        key, result)
        return result
            
def _interpret_raw(data):
    if 'MCell' not in data:
        raise ValueError, 'Not recognized as an MCell file.'

    algorithm, table, states = _create_rule(_get(data, 'GAME'), 
                                            _get(data, 'RULE'), 
                                            _get(data, 'CCOLORS'),
                                            _get(data, 'COLORING'),
                                            )
    
    chart = _create_field(_get(data, 'BOARD'),
                          _get(data, 'L'))
    
    #Fix states.
    #The state numbers used to define the grid may be different
    # from those we use internally, so we have to map them over.
    for x in range(chart.shape[0]):
        for y in range(chart.shape[1]):
            chart[x,y] = states[chart[x,y]]
    
    topology = _create_topology(_get(data, 'WRAP'))
    
    palette = _create_palette(_get(data, 'PALETTE'))
    
    delay = float(_get(data, 'SPEED')) / 1000.0 #seconds to delay between frames
    
    description = _get(data, 'D')
    
    objects = _create_objects(_get(data, 'DIV'))
    
    world = worlds.World()
    view = views.View()
    
    if algorithm:
        world.algorithm, world.table = algorithm, table
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
    return _interpret_raw(_raw_read(file))
        