import pygame, sys

    
class tool(object):
    couldnt_handle = object()
    
    def handle_event(self, event):
        if event.type in (pygame.KEYDOWN, pygame.QUIT): 
            sys.exit()
            
    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)     
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
    
    def __init__(self, location):
        self.location = location
        self.began_click = None
        self.began_center = None
    
    def handle_event(self, event):
        tool.handle_event(self, event)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.began_click = event.pos
            self.began_center = self.location.center
        elif self.began_click and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            self.location.center = [self.began_center[i] 
                                    + (self.began_click[i] - event.pos[i]) // self.location.zoom
                      for i in range(2)]
        elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
            self.location.center = [self.began_center[i] 
                                    + (self.began_click[i] - event.pos[i]) // self.location.zoom
                      for i in range(2)]
            self.began_click = None
            self.began_center = None
        else:
            return tool.couldnt_handle
            
class drag_and_zoom_tool(drag_scroll_tool):
    
    def _fix_zoom(self):
        if self.location.zoom >= 1:
            self.location.zoom = int(round(self.location.zoom))
    
    def handle_event(self, event):
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.location.zoom *= 2
            self._fix_zoom()
        elif event.type is pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.location.zoom /= 2.0
            self._fix_zoom()
        else:
            drag_scroll_tool.handle_event(self, event)
              
class draw_tool(tool):
    
    def __init__(self, location, map, fields, surface):
        self.location = location
        self.map = map
        self.fields = fields
        self.last_point= None
        self.surface = surface
        
    def _point(self, event):
        return [self.location.center[i] + (event.pos[i] - self.surface.get_size()[i] // 2) / self.location.zoom
                for i in (0, 1)]
    
    def _map(self, point):
        return self.map(point, self.fields[0])
    
    def _draw(self, point0, point1 = None):
        if point1 is None or point0 == point1:
            for field in self.fields:
                field[self._map(point0)] = 1
            return
        
        diff = [abs(point0[i] - point1[i]) for i in (0, 1)]
        if diff[0] >= diff[1]:
            for x in range(point0[0], point1[0] + 1):
                p = (x - point0[0]) * 1.0 / diff[0]
                y = int((1 - p) * point0[1] + p * point1[1])
                self._draw((x, y))
        else:
            for y in range(point0[1], point1[1] + 1):
                p = (y - point0[1]) * 1.0 / diff[1]
                x = int((1 - p) * point0[0] + p * point1[0])
                self._draw((x, y))
    
    def handle_event(self, event):
        tool.handle_event(self, event)
        
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.last_point = self._point(event)
            self._draw(self.last_point)
        elif self.last_point and event.type is pygame.MOUSEMOTION and 1 in event.buttons:
            next_point = self._point(event)
            self._draw(self.last_point, next_point)
            self.last_point = next_point
        elif event.type is pygame.MOUSEBUTTONUP and event.button == 1:
            self._draw(self.last_point, self._point(event))
            self.last_point = None
        else:
            return tool.couldnt_handle
            
    def handle_events(self):
        tool.handle_events(self)
        if self.last_point:
            self._draw(self.last_point)
       
class draw_and_zoom_tool(draw_tool):
    
    def _fix_zoom(self):
        if self.location.zoom >= 1:
            self.location.zoom = int(round(self.location.zoom))
    
    def handle_event(self, event):
        if event.type is pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.location.zoom *= 2
            self._fix_zoom()
        elif event.type is pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.location.zoom /= 2.0
            self._fix_zoom()
        else:
            draw_tool.handle_event(self, event)
                                    