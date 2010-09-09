from cascading_object import cascading_object
from run import run
import world, view, display
import tool
import format
import Queue
  
class Window(cascading_object):
    
    def get_fps(self):
        return self.view.speed
    
    def file_open(self, filename):
        new_world, new_view = format.read(filename)
        self.world.update(new_world)
        self.view.update(new_view)        
    
    def _run(self):
        iteration = 0
        while 1:
            tool.handle_events(self, self.tool)
                
            self.display(self.world, self.view)
            
            if self.view.zoom <= 1 or iteration % self.view.zoom == 0:
                self.world.evolve()
            
            iteration += 1
            yield
        
    def run(self):
        run(self._run().next, self.get_fps, self.lib)
        
    def map_point(self, point):
        return [self.view.center[i] + (point[i] - self.display.screen.get_size()[i] // 2) / self.view.zoom
                for i in (0, 1)]

def create(options, args, lib):

    window = Window()
    
    window.world, window.view = world.default(), view.default()
    
    window.lib = lib
    
    for filename in args:
        window.file_open(filename)
    
    #display = simple_displayer()
    window.display = display.create(window.world, window.view, lib)

    #window.tool = drag_and_zoom_tool()
    #window.tool = draw_and_zoom_tool()
    #current_tool = draw_and_zoom_tool(location, topology.map_point, (field0, field1), screen)
    window.tool = tool.drag_map

    return window