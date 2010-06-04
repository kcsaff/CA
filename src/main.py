import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life

import format

from tool import *
from display import create_display

from topology import torus, projective_plane, rectangle
  
class locator(object):
    zoom = 1
    def __init__(self, center=[0,0]):
        self.center = center

from optparse import OptionParser
parser = OptionParser()

def main():
    
    descriptor = {}
    options, args = parser.parse_args()
    for filename in args:
        descriptor.update(format.read(filename))
    
    #pixels[:,::3] = (0,255,255)

    if 'field' not in descriptor:
        field0 = numpy.zeros(shape=size, dtype=numpy.uint8)
        field1 = numpy.zeros(shape=size, dtype=numpy.uint8)
        field0[:,:] = numpy.random.randint(0, 2, size=field0.shape)
        field1[:,:] = field0.copy()
    else:
        field0 = descriptor['field'].copy()
        field1 = descriptor['field'].copy()
        
    print field0.shape
    
    palette = (0, 0xFFFFFF, 0xFF0000, 0, 0xCC9900)
    
    if 'evolve' not in descriptor:
        evolve = xx.evolve
        table = life.starwars()
    else:
        evolve = descriptor['evolve']
        table = descriptor['table']
    
    if 'topology' not in descriptor:
        #topology = rectangle
        #topology = projective_plane
        topology = torus
    else:
        topology = descriptor['topology']
    
    clock = pygame.time.Clock()
    speed_of_light = 60 #pixels/second.
    generation = 0
    iteration = 0
    
    center = [x // 2 for x in field0.shape]
    
    #display = simple_displayer()
    display = create_display(descriptor, pygame)

    current_tool = drag_and_zoom_tool(descriptor)
    #current_tool = draw_and_zoom_tool(location, topology.map_point, (field0, field1), screen)
    
    while 1:
        current_tool.handle_events()
            
        display(pixels, palette, field0)
        
        if location.zoom <= 1 or iteration % location.zoom == 0:
            for _ in range(1):
                evolve(field0, field1, table)
                field0, field1 = field1, field0
                topology.stitch(field0)
                generation += 1
            
        iteration += 1
            
        clock.tick(speed_of_light)
        #print clock.get_fps()
        
        #xx.randomize(pixels)
    
    return

if __name__ == '__main__':
    main()