
import numpy

def stitch(array, margin = 1):
    return

def map_point(point, array, margin = 1):
    return point

def map_slice(upper_left, array, margin = 1):
    x, y = map_point(upper_left, array, margin)
    if x < 0 and y < 0:
        return numpy.zeros(shape=(-x, -y), dtype=numpy.uint8)
    elif x < 0:
        return numpy.zeros(shape=(-x, array.shape[1]), dtype=numpy.uint8)
    elif y < 0:
        return numpy.zeros(shape=(array.shape[0], -y), dtype=numpy.uint8)
    elif x >= array.shape[0] or y >= array.shape[0]:
        return numpy.zeros(shape=array.shape, dtype=numpy.uint8)
    else:
        return array[x:, y:]