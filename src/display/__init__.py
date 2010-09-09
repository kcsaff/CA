
def create(world, view, toolkit = None):
    if toolkit.__name__ == 'pygame':
        from for_pygame import *
        from tk_dialogs import *
        return scrollable_zoomable_displayer()
    else:
        raise ValueError, 'Unimplemented toolkit: %s' % toolkit.__name__
    