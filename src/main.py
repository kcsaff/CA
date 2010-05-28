import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life

def main():
    size = (2500, 800)
    screen = pygame.display.set_mode((0,0), pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HWSURFACE)
    pixels = surfarray.pixels2d(screen)
    #pixels[:,::3] = (0,255,255)

    field0 = numpy.zeros(shape=size, dtype=numpy.uint8)
    field1 = numpy.zeros(shape=size, dtype=numpy.uint8)
    field0[:,:] = numpy.random.randint(0, 2, size=field0.shape)
    field1[:,:] = field0.copy()
    
    
    palette = (0, 0xFFFFFF, 0xFF0000)
    lookup = life.brain()
    
    while 1:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.QUIT): 
                sys.exit()
            
        #pixels[:,:] = numpy.random.randint(0, 0x1000000, size=pixels.shape)
        pixels[:,:] = numpy.take(palette, field0)
        xx.evolve(field0, field1, lookup)
        field0, field1 = field1, field0
        #xx.randomize(pixels)
        pygame.display.flip()
    
    return

if __name__ == '__main__':
    main()