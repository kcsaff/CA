import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life
import time
from topology import torus, projective_plane

def simple_display(pixels, palette, field):
    pixels[:,:] = numpy.take(palette, field)
    pygame.display.flip()
    
class locator(object):
    origin = [0, 0]
    
class simple_displayer(object):
        
    def display(self, pixels, palette, field):
        pixels[:,:] = numpy.take(palette, field)
        pygame.display.flip()
        
    def __call__(self, *args):
        self.display(*args)
        
            
class scrollable_displayer(object):
    def __init__(self, location, fun):
        self.location = location
        self.fun = fun
        
    def display(self, pixels, palette, field):
        x = y = 0
        next_x = next_y = 0
        while x < pixels.shape[0]:
            y = next_y = 0
            while y < pixels.shape[1]:
                view = self.fun((self.location.origin[0] + x, self.location.origin[1] + y),
                                field, 1)
                next_x = min(x + view.shape[0], pixels.shape[0])
                next_y = min(y + view.shape[1], pixels.shape[1])
                pixels[x:next_x, y:next_y] = numpy.take(palette, view[:next_x-x,:next_y-y])
                if next_y <= y:
                    break
                y = next_y
            if next_x <= x:
                break
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
    
    def __init__(self, location):
        self.location = location
        self.began_click = None
    
    def handle_event(self, event):
        tool.handle_event(self, event)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.began_click = event.pos
        elif self.began_click and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            self.location.origin = [self.location.origin[i] - event.pos[i] + self.began_click[i] 
                      for i in range(2)]
            self.began_click = event.pos
        elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
            self.location.origin = [self.location.origin[i] - event.pos[i] + self.began_click[i] 
                      for i in range(2)]
            self.began_click = None
            
class draw_tool(tool):
    
    def __init__(self, location, map, field):
        self.location = location
        self.map = map
        self.field = field
    
    def handle_event(self, event):
        tool.handle_event(self, event)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1 or \
                event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            point = [self.location.origin[i] + event.pos[i] for i in (0,1)]
            self.field[self.map(point, self.field)] = 1
        
    

def main():
    screen = pygame.display.set_mode((800,800), pygame.DOUBLEBUF | pygame.HWSURFACE)
    size = [z / 1 for z in screen.get_size()]
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
    #topology = projective_plane
    
    clock = pygame.time.Clock()
    
    location = locator()
    
    #display = simple_displayer()
    display = scrollable_displayer(location, topology.map_slice)

    #current_tool = drag_scroll_tool(location)
    current_tool = draw_tool(location, topology.map_point, field0)
    
    while 1:
        current_tool.handle_events()
            
        display(pixels, palette, field0)
        
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