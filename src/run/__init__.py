
def run(function, fps, toolkit = None):
    if toolkit.__name__ == 'pygame':
        _pygame_run(function, fps)
    else:
        raise ValueError, 'Unimplemented toolkit: %s' % toolkit.__name__        
    
def _pygame_run(function, fps):
    import pygame
    clock = pygame.time.Clock()
    
    while 1:
        
        function()
        
        if callable(fps):
            clock.tick(fps())
        else:
            clock.tick(fps)