import numpy
from ..util import bit_count

    
def life(birth = [3], survival = [2,3]):
    
    lookup0 = []
    
    for i in range(0x200):
        if bit_count[i & 0x1EF] in (birth, survival)[(i & 0x10) and 1]:
            lookup0.append(1)
        else:
            lookup0.append(0)
            
    return numpy.tile(numpy.asarray(lookup0, dtype = numpy.uint8), 0x80)
    
def brain(birth = [2], survival = [], decay = 1):
    
    lookup = numpy.ndarray(shape=0x20000, dtype=numpy.uint8)
    
    mdecay = decay + 2
    
    if mdecay > 256:
        mdecay = 256
    
    for i in range(0x20000):
        if i & 0x10: #alive
            if bit_count[i & 0x1EF] in survival:
                lookup[i] = 1
            else:
                lookup[i] = 2 % mdecay
        elif i < 0x200: #dead
            lookup[i] = bit_count[i & 0x1FF] in birth and 1 or 0
        else: #dying
            lookup[i] = ((i >> 9) + 1) % mdecay
            
    return lookup
