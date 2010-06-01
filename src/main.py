import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life
import time

def simple_display(pixels, palette, field):
    pixels[:,:] = numpy.take(palette, field)
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((1400,800), pygame.DOUBLEBUF | pygame.HWSURFACE)
    size = screen.get_size()
    print size
    pixels = surfarray.pixels2d(screen)
    #pixels[:,::3] = (0,255,255)

    field0 = numpy.zeros(shape=size, dtype=numpy.uint8)
    field1 = numpy.zeros(shape=size, dtype=numpy.uint8)
    field0[:,:] = numpy.random.randint(0, 2, size=field0.shape)
    field1[:,:] = field0.copy()
    
    palette = (0, 0xFFFFFF, 0xFF0000)
    lookup = life.brain()
    
    clock = pygame.time.Clock()
    
    while 1:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.QUIT): 
                sys.exit()
            
        simple_display(pixels, palette, field0)
        
        for iteration in range(1):
            xx.evolve(field0, field1, lookup)
            field0, field1 = field1, field0
            life.stitch_torus_1(field0)
            
        clock.tick()
        print clock.get_fps()
        
        #xx.randomize(pixels)
    
    return

if __name__ == '__main__':
    main()