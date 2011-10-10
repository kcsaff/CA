# Copyright (C) 2010 by Kevin Saff

# This file is part of the CA scanner.

# The CA scanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The CA scanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the CA scanner.  If not, see <http://www.gnu.org/licenses/>.

from cascading_object import cascading_object
from run import run
import worlds, views, display
import tool
import formats
import Queue
import tk_dialogs
import sys
import qdict
  
class Window(cascading_object):
    
    last_filename = sys.argv[0]
    
    playing = True
    
    def __init__(self):
        self.resources = qdict.qdict()
    
    def get_fps(self):
        return self.view.speed
    
    def file_open(self, filename):
        self.resources.update(formats.read(filename), True)
        formats.unwrap(self.world, self.view, self.resources)
        self.last_filename = filename    
    
    def file_save(self, filename):
        self.resources.update(formats.wrap(self.world, self.view), True)
        formats.write(filename, self.resources)
        self.last_filename = filename    
        
    def file_open_dialog(self):
        if sys.platform.startswith('linux'):
            self.file_open('/home/kevin/temp.png')
            return
        tk_dialogs.file_open_dialog(self.last_filename)
        
    def file_save_dialog(self):
        if sys.platform.startswith('linux'):
            self.file_save('/home/kevin/temp.png')
            return
        tk_dialogs.file_save_dialog(self.last_filename)
        
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
    
    window.world, window.view = worlds.schroedinger(), views.schroedinger()
    
    assert window.world
    assert window.view
    
    window.lib = lib
    
    for filename in args:
        window.file_open(filename)
    
    window.display = display.create(window.world, window.view, lib)

    window.tool = tool.drag_map

    return window
