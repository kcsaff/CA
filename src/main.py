import pygame, sys
from pygame import surfarray
import numpy
from exmod import xx, life
import time
from topology import torus, projective_plane, rectangle

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
        self.last_point= None
        
    def _point(self, event):
        return [self.location.origin[i] + event.pos[i] for i in (0, 1)]
    
    def _map(self, point):
        return self.map(point, self.field)
    
    def _draw(self, point0, point1 = None):
        if point1 is None or point0 == point1:
            self.field[self._map(point0)] = 1
            return
        
        diff = [abs(point0[i] - point1[i]) for i in (0, 1)]
        if diff[0] >= diff[1]:
            for x in range(point0[0], point1[0] + 1):
                p = (x - point0[0]) * 1.0 / diff[0]
                y = int((1 - p) * point0[1] + p * point1[1])
                self._draw((x, y))
        else:
            for y in range(point0[1], point1[1] + 1):
                p = (y - point0[1]) * 1.0 / diff[1]
                x = int((1 - p) * point0[0] + p * point1[0])
                self._draw((x, y))
    
    def handle_event(self, event):
        tool.handle_event(self, event)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.last_point = self._point(event)
            self._draw(self.last_point)
        elif self.last_point and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            next_point = self._point(event)
            self._draw(self.last_point, next_point)
            self.last_point = next_point
        elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
            self._draw(self.last_point, self._point(event))
            self.last_point = None
            
    

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
    
    topology = rectangle
    #topology = projective_plane
    
    clock = pygame.time.Clock()
    
    location = locator()
    
    #display = simple_displayer()
    display = scrollable_displayer(location, topology.map_slice)

    current_tool = drag_scroll_tool(location)
    #current_tool = draw_tool(location, topology.map_point, field0)
    
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