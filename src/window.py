from cascading_object import cascading_object
from run import run
import world, view, display
from tool import *
import format
  
class Window(cascading_object):
    
    def get_fps(self):
        return self.view.speed
    
    def _run(self):
        iteration = 0
        while 1:
            self.tool.handle_events(self)
                
            self.display(self.world, self.view)
            
            if self.view.zoom <= 1 or iteration % self.view.zoom == 0:
                self.world.evolve()
            
            iteration += 1
            yield
        
    def run(self):
        run(self._run().next, self.get_fps, self.lib)

def create(options, args, lib):

    window = Window()
    
    window.world, window.view = world.default(), view.default()
    
    window.lib = lib
    
    for filename in args:
        new_world, new_view = format.read(filename)
        window.world.update(new_world)
        window.view.update(new_view)
    
    #display = simple_displayer()
    window.display = display.create(window.world, window.view, lib)

    window.tool = drag_and_zoom_tool()
    #current_tool = draw_and_zoom_tool(location, topology.map_point, (field0, field1), screen)

    return window