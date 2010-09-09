import Queue

__events = Queue.Queue()

class Event(object):
    def __init__(self, type, **kwargs):
        self.type = type
        self.__dict__.update(kwargs)
        
def __handle_pygame_all(pygame):
    for event in pygame.event.get():
        __handle_pygame(pygame, event)
            
def __handle_pygame(pygame, event):
    if event.type is pygame.MOUSEBUTTONDOWN:
        assert event.pos
        __events.put(Event('M%d' % event.button,
                           pos = event.pos, 
                           pressed = True))
        __events.put(Event('M%d~' % event.button,
                           pos = event.pos, 
                           pressed = True))
    elif event.type is pygame.MOUSEBUTTONUP:
        assert event.pos
        __events.put(Event('M%d~' % event.button,
                           pos = event.pos, 
                           pressed = False))
    elif event.type is pygame.MOUSEMOTION:
        assert event.pos
        for button in range(1, 3+1):
            if event.buttons[button - 1]:
                __events.put(Event('M%d~' % button,
                                pos = event.pos, 
                                pressed = True))
    elif event.type is pygame.KEYDOWN:
        __events.put(Event(event.unicode))
    elif event.type is pygame.QUIT:
        __events.put(Event('Quit'))
    else:
        __events.put(Event('Unknown'))

def __handle_events(lib):
    if lib.__name__ == 'pygame':
        __handle_pygame_all(lib)
    else:
        raise ValueError, 'Unimplemented event source: %s' % lib.__name__
        
def get(libs):
    for lib in libs:
        __handle_events(lib)
    result = []
    try:
        while 1:
            result.append(__events.get(False))
    except Queue.Empty:
        pass
    return result
    