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
    
    points = []
    
    def __call__(self, window, event):
        self.points.append(event.pos)
        self._call(window, self.points, event.pressed)
        if not event.pressed:
            self.points = []

    def _call(self, window, points, pressed):
        if len(points) == 1:
            self.grab(window, points[0])
        elif not pressed:
            self.drop(window, points)
        else:
            self.drag(window, points, pressed)

    def grab(self, window, point):
        self.drag(window, [point], True)
    def drag(self, window, points, pressed):
        pass
    def drop(self, window, points):
        self.drag(window, points, False)

class query(mouse_handler):
    def grab(self, window, position):
        point = window.map_point(position)
        print '%s@%s' % (window.world.get(point), point)

class drag_scroll(mouse_handler):
    began_center = None

    def grab(self, window, point):
        self.began_center = window.view.center
    def drag(self, window, points, _):
        window.view.center = [self.began_center[i] 
                              + (points[0][i] - points[-1][i]) // window.view.zoom
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
        
    def grab(self, window, point):
        self._draw(window,
                   window.map_point(point))
        self._make_toy(window, point)
        
    def drag(self, window, points, pressed):
        self._destroy_toy(window)
        self._draw(window, 
                   window.map_point(points[-2]), 
                   window.map_point(points[-1]))
        if pressed:
            self._make_toy(window, points[-1])

           
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
    
def file_open_dialog(window, event):
    window.file_open_dialog()
    
def toggle_pause(window, event):
    window.toggle_pause()
    
def step(window, event):
    window.world.evolve()
    
drag_map = {'M1~': drag_scroll(),
            'M2~': query(),
            'M3~': drag_draw(),
            'M4': zoom_in,
            'M5': zoom_out,
            'o': file_open_dialog,
            'p': toggle_pause,
            ' ': step,
            'file_open': file_open,
            'Quit': quit,
            }
           
