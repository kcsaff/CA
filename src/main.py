import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life

from tool import *
from display import *

from topology import torus, projective_plane, rectangle
  
class locator(object):
    zoom = 1
    def __init__(self, center=[0,0]):
        self.center = center

from optparse import OptionParser


def main():
    screen = pygame.display.set_mode((800,800), pygame.DOUBLEBUF | pygame.HWSURFACE)
    size = screen.get_size()
    print size
    pixels = surfarray.pixels2d(screen)
    #pixels[:,::3] = (0,255,255)

    field0 = numpy.zeros(shape=size, dtype=numpy.uint8)
    field1 = numpy.zeros(shape=size, dtype=numpy.uint8)
    field0[:,:] = numpy.random.randint(0, 2, size=field0.shape)
    field1[:,:] = field0.copy()
    
    palette = (0, 0xFFFFFF, 0xFF0000, 0, 0xCC9900)
    lookup = life.starwars()
    
    #topology = rectangle
    #topology = projective_plane
    topology = torus
    
    clock = pygame.time.Clock()
    speed_of_light = 60 #pixels/second.
    generation = 0
    iteration = 0
    
    location = locator([x // 2 for x in size])
    
    #display = simple_displayer()
    display = scrollable_zoomable_displayer(location, topology.map_slice)

    current_tool = drag_and_zoom_tool(location)
    #current_tool = draw_and_zoom_tool(location, topology.map_point, (field0, field1), screen)
    
    while 1:
        current_tool.handle_events()
            
        display(pixels, palette, field0)
        
        if location.zoom <= 1 or iteration % location.zoom == 0:
            for _ in range(1):
                xx.evolve(field0, field1, lookup)
                field0, field1 = field1, field0
                topology.stitch(field0)
                generation += 1
            
        iteration += 1
            
        clock.tick(speed_of_light)
        print clock.get_fps()
        
        #xx.randomize(pixels)
    
    return

if __name__ == '__main__':
    main()