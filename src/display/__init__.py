
def create_display(world, view, toolkit):
    if toolkit.__name__ == 'pygame':
        from for_pygame import *
        return scrollable_zoomable_displayer()