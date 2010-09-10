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

#[ 0][ 1][ 2]
#[ 3][*4][ 5]
#[ 6][ 7][ 8]
def banks(birth = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
          survival = [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
          decay = 0,
          out_to_in = None): 
    
    if out_to_in is None:
        #in order NESW, like mcell
        if len(birth) <= 16:
            out_to_in = {1 << 1:1 << 0, 
                         1 << 3:1 << 3, 
                         1 << 5:1 << 1, 
                         1 << 7:1 << 2}
        else:
            out_to_in = {1 << 0:1 << 7,
                         1 << 1:1 << 0,
                         1 << 2:1 << 1,
                         1 << 3:1 << 6,
                         1 << 5:1 << 2,
                         1 << 6:1 << 5,
                         1 << 7:1 << 4,
                         1 << 8:1 << 3}
    
    lookup = numpy.ndarray(shape=0x20000, dtype=numpy.uint8)
    
    mdecay = decay + 2
    
    if mdecay > 256:
        mdecay = 256
    
    for i in range(0x20000):
        target = 0
        for obit, ibit in out_to_in.items():
            if i & obit:
                target |= ibit
            
        if i & 0x10: #alive
            if survival[target]:
                lookup[i] = survival[target]
            else:
                lookup[i] = 2 % mdecay
        elif i < 0x200: #dead
            lookup[i] = birth[target]
        else: #dying
            lookup[i] = ((i >> 9) + 1) % mdecay
            
    return lookup
    