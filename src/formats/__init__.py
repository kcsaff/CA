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
    elif filename.startswith('meta') and filename.endswith('txt'):
        import meta
        return meta.read(filename, file)
    else:
        raise ValueError, 'Do not understand how to read file "%s"' % filename

def write(filename, data):
    import native
    return native.write(filename, data)

def unwrap(world, view, data):
    if 'rule' in data:
        world.rule = data['rule']
    if 'chart' in data:
        world.charts = [data['chart']]
    if 'charts' in data:
        world.charts = [data['charts']]
        world._scratch_charts = None
    if 'atlases' in data:
        atlases = data['atlases']
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
    if getattr(world.rule, 'history', False):
        atlases = (world.charts, world._scratch_charts)
    else:
        atlases = (world.charts,)
    return {'rule': world.rule,
            'chart': world.charts[0],
            'charts': world.charts,
            'atlases': atlases,
            'topology': world.topology,
            'toys': world.toys,
            'generation': world.generation,
            
            'palette': view.palette,
            'speed': view.speed,
            'zoom': view.zoom,
            'center': view.center,
            }
    
