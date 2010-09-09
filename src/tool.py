import pygame, sys

    
class tool(object):
    couldnt_handle = object()
    
    def handle_event(self, event, window):
        if event.type in (pygame.KEYDOWN, pygame.QUIT): 
            sys.exit()
            
    def handle_events(self, window):
        for event in pygame.event.get():
            self.handle_event(event, window)     
#            
#class composite_tool(tool):
#    
#    def __init__(self, *tools):
#        self.tools = tools
#        
#    def handle_event(self, event):
#        for tool in reversed(self.tools):
#            if tool.handle_event(event) is not tool.couldnt_handle:
#                break
#        else:
#            return tool.couldnt_handle

class drag_scroll_tool(tool):
    
    began_click = None
    began_center = None
    
    def handle_event(self, event, window):
        tool.handle_event(self, event, window)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.began_click = event.pos
            self.began_center = window.view.center
        elif self.began_click and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            window.view.center = [self.began_center[i] 
                                    + (self.began_click[i] - event.pos[i]) // window.view.zoom
                      for i in range(2)]
        elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
            window.view.center = [self.began_center[i] 
                                    + (self.began_click[i] - event.pos[i]) // window.view.zoom
                      for i in range(2)]
            self.began_click = None
            self.began_center = None
        else:
            return tool.couldnt_handle
            
class drag_and_zoom_tool(drag_scroll_tool):
    
    def _fix_zoom(self, window):
        if window.view.zoom >= 1:
            window.view.zoom = int(round(window.view.zoom))
    
    def handle_event(self, event, window):
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 4:
            window.view.zoom *= 2
            self._fix_zoom(window)
        elif event.type is pygame.MOUSEBUTTONDOWN and event.button == 5:
            window.view.zoom /= 2.0
            self._fix_zoom(window)
        else:
            drag_scroll_tool.handle_event(self, event, window)
              
class draw_tool(tool):
    
    last_point= None
        
    def _point(self, event, window):
        return [window.view.center[i] + (event.pos[i] - window.display.screen.get_size()[i] // 2) / window.view.zoom
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
    
    def handle_event(self, event, window):
        tool.handle_event(self, event, window)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.last_point = self._point(event, window)
            self._draw(window, self.last_point)
        elif self.last_point and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            next_point = self._point(event, window)
            self._draw(window, self.last_point, next_point)
            self.last_point = next_point
        elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
            self._draw(window, self.last_point, self._point(event, window))
            self.last_point = None
        else:
            return tool.couldnt_handle
            
    def handle_events(self, window):
        tool.handle_events(self, window)
        if self.last_point:
            self._draw(window, self.last_point)
       
class draw_and_zoom_tool(draw_tool):
    
    def _fix_zoom(self, window):
        if window.view.zoom >= 1:
            window.view.zoom = int(round(window.view.zoom))
    
    def handle_event(self, event, window):
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 4:
            window.view.zoom *= 2
            self._fix_zoom(window)
        elif event.type is pygame.MOUSEBUTTONDOWN and event.button == 5:
            window.view.zoom /= 2.0
            self._fix_zoom(window)
        else:
            draw_tool.handle_event(self, event, window)
                                    