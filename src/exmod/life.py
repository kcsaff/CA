import numpy

bit_count = [0]
while (len(bit_count) < 512):
    bit_count += [x + 1 for x in bit_count]
    
    
def lifelike(birth, survival):
    
    lookup0 = []
    
    for i in range(0x200):
        if bit_count[i & 0x1EF] in (birth, survival)[(i & 0x10) and 1]:
            lookup0.append(1)
        else:
            lookup0.append(0)
            
    return numpy.tile(numpy.asarray(lookup0, dtype = numpy.uint8), 0x80)
    
def brainlike(birth, survival, decay):
    
    lookup = numpy.ndarray(shape=0x10000, dtype=numpy.uint8)
    
    mdecay = 2 * (decay + 1)
    
    if mdecay > 256:
        mdecay = 256
    
    for i in range(0x10000):
        if i & 0x10: #alive
            if bit_count[i & 0x1EF] in survival:
                lookup[i] = 1
            else:
                lookup[i] = 2 % mdecay
        elif i < 0x200: #dead
            lookup[i] = bit_count[i & 0x1FF] in birth and 1 or 0
        else: #dying
            lookup[i] = ((i >> 9) * 2 + 2) % mdecay
            
    return lookup
    
    
def life():
    birth = set([3])
    survival = set([2, 3]) 
    return lifelike(birth, survival)

def vote():
    birth = set([8, 7, 6, 4])
    survival = set([8, 7, 6, 5, 3])
    return lifelike(birth, survival)

def brain():
    return brainlike([2], [], 1)

def starwars():
    return brainlike([2], set([3,4,5]), 2)

def amoeba():
    return lifelike(set([3,5,7]), set([1,3,5,8]))

def maze():
    return lifelike(set([3]), set([1,2,3,4,5]))

