import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life
import time
from topology import torus, projective_plane

def simple_display(pixels, palette, field):
    pixels[:,:] = numpy.take(palette, field)
    pygame.display.flip()
    
    
class scrollable_displayer(object):
    def __init__(self):
        self.origin = [0, 0]
        
    def display(self, pixels, palette, field, fun):
        x = y = 0
        next_x = next_y = 0
        while x < pixels.shape[0]:
            y = next_y = 0
            while y < pixels.shape[1]:
                view = fun((self.origin[0] + x, self.origin[1] + y),
                           field, 1)
                next_x = min(x + view.shape[0], pixels.shape[0])
                next_y = min(y + view.shape[1], pixels.shape[1])
                pixels[x:next_x, y:next_y] = numpy.take(palette, view[:next_x-x,:next_y-y])
                y = next_y
            x = next_x
        pygame.display.flip()
        
    def __call__(self, *args):
        self.display(*args)
    
class tool(object):
    def handle_event(self, event):
        if event.type in (pygame.KEYDOWN, pygame.QUIT): 
            sys.exit()
            
    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)        

class drag_scroll_tool(tool):
    
    def __init__(self, displayer):
        self.displayer = displayer
        self.began_click = None
    
    def handle_event(self, event):
        tool.handle_event(self, event)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.began_click = event.pos
        elif self.began_click and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            self.displayer.origin = [self.displayer.origin[i] - event.pos[i] + self.began_click[i] 
                      for i in range(2)]
            self.began_click = event.pos
        elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
            self.displayer.origin = [self.displayer.origin[i] - event.pos[i] + self.began_click[i] 
                      for i in range(2)]
            self.began_click = None

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
    lookup = life.life()
    
    topology = torus
    
    clock = pygame.time.Clock()
    
    display = scrollable_displayer()

    current_tool = drag_scroll_tool(display)
    
    while 1:
        current_tool.handle_events()
            
        display(pixels, palette, field0, topology.map_slice)
        
        for _ in range(1):
            xx.evolve(field0, field1, lookup)
            field0, field1 = field1, field0
            topology.stitch(field0)
            
        clock.tick()
        print clock.get_fps()
        
        #xx.randomize(pixels)
    
    return

if __name__ == '__main__':
    main()