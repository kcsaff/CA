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
    
def boiling_water():
    
    lookup = [0.15, 0.35, 0.15,
              0.35, 0.00, 0.35,
              0.15, 0.35, 0.15,
              -1.0,
              0.995, 
              1,
              0.0, 255.9,
              0.0, 0.0]
    return numpy.asarray(lookup, dtype = numpy.float)
    
def dunes():
    
    lookup = [0.15, 0.30, 0.10,
              0.40, 0.00, 0.20,
              0.15, 0.30, 0.10,
              -0.7,
              1.0, 
              0,
              0.0, 255.9,
              0.0, 255.9]
    return numpy.asarray(lookup, dtype = numpy.float)
    
def aurora():
    
    lookup = [0.10, 0.20, 0.10,
              0.20, 0.00, 0.20,
              0.10, 0.20, 0.10,
              -0.20,
              1.0, 
              1.0,
              0.0, 255.9,
              0.0, 0.0]
    result = numpy.asarray(lookup, dtype = numpy.float)
    print result
    return result
