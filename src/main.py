import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life

import format

from tool import *
from view import *
from display import create_display

from topology import torus, projective_plane, rectangle
  
class locator(object):
    zoom = 1
    def __init__(self, center=[0,0]):
        self.center = center

from optparse import OptionParser
parser = OptionParser()


def main():
    
    world, view = default_world(), default_view()
    
    options, args = parser.parse_args()
    for filename in args:
        new_world, new_view = format.read(filename)
        world.update(new_world)
        view.update(new_view)
    
    clock = pygame.time.Clock()
    
    #display = simple_displayer()
    display = create_display(world, view, pygame)

    current_tool = drag_and_zoom_tool(view)
    #current_tool = draw_and_zoom_tool(location, topology.map_point, (field0, field1), screen)
    
    iteration = 0
    
    while 1:
        current_tool.handle_events()
            
        display(world, view)
        
        if view.zoom <= 1 or iteration % view.zoom == 0:
            world.evolve()
            
        iteration += 1
            
        clock.tick(view.speed)
        #print clock.get_fps()
        
        #xx.randomize(pixels)
    
    return

if __name__ == '__main__':
    main()