import pygame, numpy
from pygame import surfarray
import tk_dialogs


class simple_displayer(object):
        
    def display(self, pixels, palette, field):
        pixels[:,:] = numpy.take(palette, field)
        pygame.display.flip()
        
    def __call__(self, *args):
        self.display(*args)          
            
class scrollable_displayer(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((800,800), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.size = self.screen.get_size()
        self.pixels = surfarray.pixels2d(self.screen)

        
    def display(self, world, view):
        pixels = self.pixels
        palette = view.palette
        chart = world.charts[0]
        center = view.center
        fun = world.topology.map_slice
        self.do_display(pixels, palette, chart, center, fun)
        
    @classmethod
    def do_display(cls, pixels, palette, chart, center, fun):
        if isinstance(pixels, pygame.Surface):
            pixels = surfarray.pixels2d(pixels)
        x = y = 0
        next_x = next_y = 0
        
        origin = [center[i] - pixels.shape[i] // 2 for i in (0,1)]

        if chart.dtype == numpy.uint8:
            pass #okay
        elif chart.dtype == numpy.float:
            chart = numpy.cast[numpy.uint8](chart)
        
        try:
            while x < pixels.shape[0]:
                y = next_y = 0
                while y < pixels.shape[1]:
                    view = fun((origin[0] + x, origin[1] + y),
                                chart, 1)
                    next_x = min(x + view.shape[0], pixels.shape[0])
                    next_y = min(y + view.shape[1], pixels.shape[1])
                    pixels[x:next_x, y:next_y] = numpy.take(palette, view[:next_x-x,:next_y-y])
                    if next_y <= y:
                        break
                    y = next_y
                if next_x <= x:
                    break
                x = next_x
        except IndexError as ie:
            #Didn't have a palette entry for some value, figure it out.
            states = set()
            for x in range(chart.shape[0]):
                for y in range(chart.shape[1]):
                    states.add(chart[x, y])
            print states
            raise ie
        pygame.display.flip()
        
    def __call__(self, *args):
        self.display(*args)
    
            
class scrollable_zoomable_displayer(scrollable_displayer):
    
    temp_surface = None
        
    def display(self, world, view):
        pixels = self.pixels
        palette = view.palette
        chart = world.charts[0]
        center = view.center
        zoom = view.zoom
        fun = world.topology.map_slice
        
        if zoom == 1:
            return scrollable_displayer.display(self, world, view)
        else:
            temp_shape = [d // zoom + 1 for d in pixels.shape]
            if self.temp_surface is None or self.temp_surface.get_size() != temp_shape:
                self.temp_surface = pygame.Surface(temp_shape, depth=32)
            scrollable_displayer.do_display(self.temp_surface, palette, chart, center, fun)
            if zoom > 1:
                pygame.transform.scale(self.temp_surface, pixels.shape, pygame.display.get_surface())
            else: #Way zoomed out.
                pygame.transform.smoothscale(self.temp_surface, pixels.shape, pygame.display.get_surface())
            
            
