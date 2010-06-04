
def create_display(descriptor, toolkit):
    if toolkit.__name__ == 'pygame':
        from for_pygame import *
        return scrollable_zoomable_displayer(descriptor)