import pygame, sys
from event import Event
    
            
def translate_pygame(event):
    result = []
    if event.type is pygame.MOUSEBUTTONDOWN:
        result.append(Event('M%d' % event.button,
                            pos = event.pos, 
                            pressed = True))
        result.append(Event('M%d~' % event.button,
                            pos = event.pos, 
                            pressed = True))
    elif event.type is pygame.MOUSEBUTTONUP:
        result.append(Event('M%d~' % event.button,
                            pos = event.pos, 
                            pressed = False))
    elif event.type is pygame.MOUSEMOTION:
        print event.buttons
        for button in range(1, 3+1):
            if event.buttons[button - 1]:
                result.append(Event('M%d~' % button,
                                    pos = event.pos, 
                                    pressed = True))
    elif event.type is pygame.QUIT:
        result.append(Event('Quit'))
    else:
        result.append(Event('Unknown'))
    return result
        
def do_nothing(*args, **kwargs):
    return

def quit(*args, **kwargs):
    sys.exit()

def handle_events(window, event_map):
    for pyevent in pygame.event.get():
        for event in translate_pygame(pyevent):
            print event.type
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
        else:
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
        window.view.center = [self.began_center[i] 
                              + (first_position[i] - to_position[i]) // window.view.zoom
                              for i in range(2)]

           
class drag_draw(mouse_handler):
        
    def _point(self, window, position):
        return [window.view.center[i] + (position[i] - window.display.screen.get_size()[i] // 2) / window.view.zoom
                for i in (0, 1)]
    
    def _map(self, window, point):
        return window.world.topology.map_point(point, window.world.charts[0])
    
    def _draw(self, window, point0, point1 = None):
        if point1 is None or point0 == point1:
            for field in window.world.charts:
                field[self._map(window, point0)] = 1
            return
        
        diff = [abs(point0[i] - point1[i]) for i in (0, 1)]
        if diff[0] >= diff[1]:
            for x in range(point0[0], point1[0] + 1):
                p = (x - point0[0]) * 1.0 / diff[0]
                y = int((1 - p) * point0[1] + p * point1[1])
                self._draw(window, (x, y))
        else:
            for y in range(point0[1], point1[1] + 1):
                p = (y - point0[1]) * 1.0 / diff[1]
                x = int((1 - p) * point0[0] + p * point1[0])
                self._draw(window, (x, y))
        
    def press(self, window, position):
        self._draw(window, 
                   self._point(window, position))
    def drag(self, window, _, from_position, to_position):
        self._draw(window, 
                   self._point(window, from_position), 
                   self._point(window, to_position))

           
def __fix_zoom(window):
    if window.view.zoom >= 1:
        window.view.zoom = int(round(window.view.zoom))
    
           
def zoom_in(window, event):
    window.view.zoom *= 2
    __fix_zoom(window)
           
def zoom_out(window, event):
    window.view.zoom /= 2.0
    __fix_zoom(window)
    
drag_map = {'M1~': drag_scroll(),
            'M3~': drag_draw(),
            'M4': zoom_in,
            'M5': zoom_out,
            'Quit': quit,
            }
           