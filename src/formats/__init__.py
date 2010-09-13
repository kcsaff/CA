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


#Implementations of file formats should handle resources in terms of qdict's,
# as defined in qdict.qdict.

def read(filename, file=None):
    if filename.endswith('.zip'):
        import native
        return native.read(filename, file)
    elif filename.endswith('.mcl'):
        import mcell
        return mcell.read(filename, file)
    elif filename.endswith('.png'):
        import png
        return png.read(filename, file)
    elif filename.endswith('.fits'):
        import fits
        return fits.read(filename, file)
    elif filename.startswith('meta') and filename.endswith('txt'):
        import meta
        return meta.read(filename, file)
    else:
        raise ValueError, 'Do not understand how to read file "%s"' % filename

def write(filename, data, file=None, chart=(0,0)):
    if filename.endswith('.zip'):
        import native
        return native.write(filename, data, file, chart)
    elif filename.endswith('.fits'):
        import fits
        return fits.write(filename, data, file, chart)
    else:
        raise ValueError, 'Do not understand how to write file "%s"' % filename

def unwrap(world, view, data):
    if 'rule' in data:
        world.rule = data['rule']
    atlases = get_atlases(data)
    if len(atlases) > 0:
        world.charts = atlases[0]
    if len(atlases) > 1:
        world._scratch_charts = atlases[1]
            
    if 'topology' in data:
        world.topology = data['topology']
    if 'toys' in data:
        world.toys = data['toys']
        
    if 'palette' in data:
        view.palette = data['palette']
    if 'speed' in data:
        view.speed = data['speed']
        
        
def wrap(world, view):
    result = {'rule': world.rule,
              'topology': world.topology,
              'toys': world.toys,
              'generation': world.generation,
            
              'palette': view.palette,
              'speed': view.speed,
              'zoom': view.zoom,
              'center': view.center,
              }
    set_atlases(result, world)
    return result
    
def set_atlases(resource, world):
    if getattr(world.rule, 'history', False):
        atlases = (world.charts, world._scratch_charts)
    else:
        atlases = (world.charts,)
    for x, atlas in enumerate(atlases):
        for y, chart in enumerate(atlas):
            resource['chart(%d,%d)' % (x, y)] = chart
    
def get_atlases(resource):
    atlases = []
    for key in resource.keys():
        if key.startswith('chart('):
            nos = [int(x) for x in key.strip('chart()').split(',')]
            while len(atlases) <= nos[0]:
                atlases.append([])
            while len(atlases[nos[0]]) <= nos[1]:
                atlases[nos[0]].append(None)
            atlases[nos[0]][nos[1]] = resource[key]
    return atlases

def get_subscripts(filename):
    try:
        return tuple([int(x) for x in filename.split('.')[1].split('-')])
    except IndexError:
        return (0,0)
    