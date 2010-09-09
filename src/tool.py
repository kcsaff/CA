import sys
import events
import tk_dialogs
from toys.block import block
        
def do_nothing(*args, **kwargs):
    return

def quit(*args, **kwargs):
    sys.exit()

def handle_events(window, event_map):
    for event in events.get([window.lib]):
        fun = event_map.get(event.type, do_nothing)
        fun(window, event)
    
class mouse_handler(object):
    
    first_position = None
    from_position = None
    
    def __call__(self, window, event):
        if event.pressed:
            if not self.first_position:
                self.first_position = event.pos
                self.from_position = event.pos
                self.press(window, self.from_position)
            else:
                self.drag(window, self.first_position, self.from_position, event.pos)
                self.from_position = event.pos
        elif self.first_position:
            self.release(window, self.first_position, self.from_position, event.pos)
            self.from_position = event.pos
            self.first_position = None
        
    def press(self, window, position):
        pass
    def drag(self, window, first_position, from_position, to_position):
        pass
    def release(self, window, first_position, from_position, to_position):
        self.drag(window, first_position, from_position, to_position)


class drag_scroll(mouse_handler):
    
    began_click = None
    began_center = None
    
    def press(self, window, position):
        self.began_center = window.view.center
    def drag(self, window, first_position, _, to_position):
        if not self.began_center:
            self.press(window, first_position)
        window.view.center = [self.began_center[i] 
                              + (first_position[i] - to_position[i]) // window.view.zoom
                              for i in range(2)]

           
class drag_draw(mouse_handler):
    
    state = 1
    toy = None
        
    def _draw(self, window, point0, point1 = None):
        if point1 is None or point0 == point1:
            window.world.set(point0, self.state)
            return
        
        diff = [abs(point0[i] - point1[i]) for i in (0, 1)]
        if diff[0] >= diff[1]:
            if point0[0] > point1[0]:
                point0, point1 = point1, point0
            for x in range(point0[0], point1[0] + 1):
                p = (x - point0[0]) * 1.0 / diff[0]
                y = int((1 - p) * point0[1] + p * point1[1])
                window.world.set((x, y), self.state)
        else:
            if point0[1] > point1[1]:
                point0, point1 = point1, point0
            for y in range(point0[1], point1[1] + 1):
                p = (y - point0[1]) * 1.0 / diff[1]
                x = int((1 - p) * point0[0] + p * point1[0])
                window.world.set((x, y), self.state)
        
    def _make_toy(self, window, position):
        self.toy = block(window.map_point(position), self.state)
        window.world.toys.add(self.toy)
        
    def _destroy_toy(self, window):
        if self.toy is not None:
            window.world.toys.remove(self.toy)
        self.toy = None
        
    def press(self, window, position):
        self._draw(window, 
                   window.map_point(position))
        self._make_toy(window, position)
    def drag(self, window, _, from_position, to_position):
        self._destroy_toy(window)
        self._draw(window, 
                   window.map_point(from_position), 
                   window.map_point(to_position))
        self._make_toy(window, to_position)
    def release(self, window, _, from_position, to_position):
        self._destroy_toy(window)
        self._draw(window, 
                   window.map_point(from_position), 
                   window.map_point(to_position))

           
def __fix_zoom(window):
    if window.view.zoom >= 1:
        window.view.zoom = int(round(window.view.zoom))
    
           
def zoom_in(window, event):
    window.view.zoom *= 2
    __fix_zoom(window)
           
def zoom_out(window, event):
    window.view.zoom /= 2.0
    __fix_zoom(window)
    
def file_open(window, event):
    window.file_open(event.filename)
    
drag_map = {'M1~': drag_scroll(),
            'M3~': drag_draw(),
            'M4': zoom_in,
            'M5': zoom_out,
            'o': tk_dialogs.file_open_dialog,
            'file_open': file_open,
            'Quit': quit,
            }
           