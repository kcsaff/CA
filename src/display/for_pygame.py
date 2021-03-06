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

import pygame, numpy
from pygame import surfarray
import tk_dialogs


class simple_displayer(object):
        
    def display(self, pixels, palette, field):
        pixels[:,:] = numpy.take(palette, field)
        pygame.display.flip()
        
    def __call__(self, *args):
        self.display(*args)          
        
MENU = (
    'Help',
    'Quit',
        )
            
class scrollable_displayer(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((800,800), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.size = self.screen.get_size()
        self.pixels = surfarray.pixels2d(self.screen)
        from gamelib.popup_menu import NonBlockingPopupMenu
        self.menu = NonBlockingPopupMenu(MENU)
        
    def display(self, world, view):
        self.do_display(self.pixels, view, world.charts[0])
        
    @classmethod
    def restyle(cls, chart):
        data = chart.data
        if data.dtype == numpy.uint8:
            return data #okay
        elif data.dtype == numpy.float:
            return numpy.cast[numpy.uint8](data)
        
        
    @classmethod
    def do_display(cls, pixels, view, chart):
        center = view.center
        if isinstance(pixels, pygame.Surface):
            pixels = surfarray.pixels2d(pixels)
        x = y = 0
        next_x = next_y = 0
        
        origin = [center[i] - pixels.shape[i] // 2 for i in (0,1)]

        colors = view(chart)
        
        try:
            while x < pixels.shape[0]:
                y = next_y = 0
                while y < pixels.shape[1]:
                    view = chart.map_slice((origin[0] + x, origin[1] + y), colors)
                    next_x = min(x + view.shape[0], pixels.shape[0])
                    next_y = min(y + view.shape[1], pixels.shape[1])
                    pixels[x:next_x, y:next_y] = view[:next_x-x,:next_y-y]
                    if next_y <= y:
                        break
                    y = next_y
                if next_x <= x:
                    break
                x = next_x
        except IndexError as ie:
            #Didn't have a palette entry for some value, figure it out.
            states = set()
            for x in range(chart.shape[0]):
                for y in range(chart.shape[1]):
                    states.add(chart[x, y])
            print states, palette
            raise ie
        pygame.display.flip()
        
    def __call__(self, *args):
        self.display(*args)
    
            
class scrollable_zoomable_displayer(scrollable_displayer):
    
    temp_surface = None
        
    def display(self, world, view):
        if view.zoom == 1:
            return scrollable_displayer.display(self, world, view)
        else:
            temp_shape = [d // view.zoom + 1 for d in self.pixels.shape]
            if self.temp_surface is None or self.temp_surface.get_size() != temp_shape:
                self.temp_surface = pygame.Surface(temp_shape, depth=32)
            scrollable_displayer.do_display(self.temp_surface, view, world.charts[0])
            if view.zoom > 1:
                pygame.transform.scale(self.temp_surface, self.pixels.shape, pygame.display.get_surface())
            else: #Way zoomed out.
                pygame.transform.smoothscale(self.temp_surface, self.pixels.shape, pygame.display.get_surface())
            
            
