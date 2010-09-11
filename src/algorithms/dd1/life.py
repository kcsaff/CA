import numpy
    
def water():
    
    lookup = [0.0, 0.5, 0.0,
              0.5, 0.0, 0.5,
              0.0, 0.5, 0.0,
              -1.0,
              0.97,
              -1.0, +1.0]
    return numpy.asarray(lookup, dtype = numpy.float)
