from cascading_object import cascading_object
from run import run
import worlds, views, display
import tool
import format
import Queue
import tk_dialogs
import sys
  
class Window(cascading_object):
    
    last_filename = sys.argv[0]
    
    playing = True
    
    def get_fps(self):
        return self.view.speed
    
    def file_open(self, filename):
        new_world, new_view = format.read(filename)
        self.world.update(new_world)
        self.view.update(new_view)    
        self.last_filename = filename    
        
    def file_open_dialog(self):
        tk_dialogs.file_open_dialog(self.last_filename)
        
    def toggle_pause(self):
        self.playing = not self.playing
    
    def _run(self):
        iteration = 0
        while 1:
            tool.handle_events(self, self.tool)
                
            self.display(self.world, self.view)
            
            if self.playing:
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
    
    window.world, window.view = worlds.water(), views.water()
    
    window.lib = lib
    
    for filename in args:
        window.file_open(filename)
    
    window.display = display.create(window.world, window.view, lib)

    window.tool = tool.drag_map

    return window
