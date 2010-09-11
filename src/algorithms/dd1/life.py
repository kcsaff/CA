import numpy
    
def water():
    
    lookup = [0.0, 0.5, 0.0,
              0.5, 0.0, 0.5,
              0.0, 0.5, 0.0,
              -1.0,
              0.97, 
              128 * 0.015,
              0.0, 255.9,
              0.0, 255.9]
    return numpy.asarray(lookup, dtype = numpy.float)
