import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life
import time

def simple_display(pixels, palette, field):
    pixels[:,:] = numpy.take(palette, field)
    pygame.display.flip()
    
def torus_display(pixels, palette, field, origin = (0,0)):
    x = y = 0
    next_x = next_y = 0
    while x < pixels.shape[0]:
        y = next_y = 0
        while y < pixels.shape[1]:
            view = life.map_torus_slice((origin[0] + x, origin[1] + y),
                                        field, 1)
            next_x = min(x + view.shape[0], pixels.shape[0])
            next_y = min(y + view.shape[1], pixels.shape[1])
            pixels[x:next_x, y:next_y] = numpy.take(palette, view[:next_x-x,:next_y-y])
            y = next_y
        x = next_x
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
    
    origin = [0, 0]
    began_click = None

    
    while 1:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.QUIT): 
                sys.exit()
            elif event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
                began_click = event.pos
            elif began_click and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
                origin = [origin[i] - event.pos[i] + began_click[i] 
                          for i in range(2)]
                began_click = event.pos
            elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
                origin = [origin[i] - event.pos[i] + began_click[i] 
                          for i in range(2)]
                began_click = None
                
            
        torus_display(pixels, palette, field0, origin)
        
        for iteration in range(1):
            xx.evolve(field0, field1, lookup)
            field0, field1 = field1, field0
            life.stitch_torus(field0)
            
        clock.tick()
        print clock.get_fps()
        
        #xx.randomize(pixels)
    
    return

if __name__ == '__main__':
    main()