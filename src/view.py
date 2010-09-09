from cascading_object import cascading_object

class View(cascading_object):
    pass

def default():
    result = View(source='default')
    result.center = (0,0)
    result.zoom = 1
    result.palette = (0, 0xFFFFFF, 0xFF0000, 0, 0xCC9900)
    result.speed = 60
    return result
    
        