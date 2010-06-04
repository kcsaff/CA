import pygame, numpy
from pygame import surfarray

class simple_displayer(object):
        
    def display(self, pixels, palette, field):
        pixels[:,:] = numpy.take(palette, field)
        pygame.display.flip()
        
    def __call__(self, *args):
        self.display(*args)          
            
class scrollable_displayer(object):
    def __init__(self, descriptor):
        #self.location = descriptor['location']
        #self.fun = descriptor['topology'].map_slice
            
        self.screen = pygame.display.set_mode((800,800), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.size = self.screen.get_size()
        self.pixels = surfarray.pixels2d(self.screen)

        
    def display(self, descriptor):
        pixels = self.pixels
        palette = descriptor['palette']
        field = descriptor['field']
        center = descriptor['center']
        self.do_display(pixels, palette, field, center)
        
    def do_display(self, pixels, palette, field, center):
        if isinstance(self.pixels, pygame.Surface):
            pixels = surfarray.pixels2d(self.pixels)
        x = y = 0
        next_x = next_y = 0
        
        origin = [center[i] - pixels.shape[i] // 2 for i in (0,1)]
        
        while x < pixels.shape[0]:
            y = next_y = 0
            while y < pixels.shape[1]:
                view = self.fun((origin[0] + x, origin[1] + y),
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
    
            
class scrollable_zoomable_displayer(scrollable_displayer):
    
    temp_surface = None
        
    def display(self, descriptor):
        pixels = self.pixels
        palette = descriptor['palette']
        field = descriptor['field']
        center = descriptor['center']
        
        if self.location.zoom  == 1:
            return scrollable_displayer.display(self, pixels, palette, field, center)
        else:
            temp_shape = [d // self.location.zoom + 1 for d in pixels.shape]
            if self.temp_surface is None or self.temp_surface.get_size() != temp_shape:
                self.temp_surface = pygame.Surface(temp_shape, depth=32)
            scrollable_displayer.display(self, self.temp_surface, palette, field, center)
            if self.location.zoom > 1:
                pygame.transform.scale(self.temp_surface, pixels.shape, pygame.display.get_surface())
            else: #Way zoomed out.
                pygame.transform.smoothscale(self.temp_surface, pixels.shape, pygame.display.get_surface())
            