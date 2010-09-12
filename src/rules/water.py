from simple import typed_object as rule

def water(moore=[0.0, 0.5, 0.0,
                 0.5, 0.0, 0.5,
                 0.0, 0.5, 0.0],
          history = -1.0,
          damping = 0.03,
          heat = 0,
          min = 0.0, max = 255.9,
          under = 0.0, over = 255.9
          ):
    return rule('water',
                moore=moore,
                history=history,
                damping=damping,
                heat=heat,
                min=min, max=max,
                under=under, over=over)
    
def boiling_water():
    return water(moore=[0.15, 0.35, 0.15,
                        0.35, 0.00, 0.35,
                        0.15, 0.35, 0.15],
                 history = -1.0,
                 damping = 0.005,
                 heat = 1,
                 min = 0.0, max = 255.9,
                 under = 0.0, over = 0.0)
    
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
    return numpy.asarray(lookup, dtype = numpy.float)

    
