import numpy

bit_count = [0]
while (len(bit_count) < 512):
    bit_count += [x + 1 for x in bit_count]
    
    
def lifelike(birth, survival):
    
    lookup0 = []
    
    for i in range(0x200):
        if bit_count[i] in (birth, survival)[(i & 0x10) and 1]:
            lookup0.append(1)
        else:
            lookup0.append(0)
            
    return numpy.tile(numpy.asarray(lookup0, dtype = numpy.uint8), 0x80)
    
def brainlike(birth, decay):
    
    lookup = numpy.ndarray(shape=0x10000, dtype=numpy.uint8)
    
    mdecay = 2 * (decay + 1)
    
    if mdecay > 256:
        mdecay = 256
    
    for i in range(0x10000):
        if i & 0x10:
            lookup[i] = 2 % mdecay
        elif i < 0x200:
            lookup[i] = bit_count[i & 0x1FF] in birth and 1 or 0
        else:
            lookup[i] = ((i >> 9) * 2 + 2) % mdecay
            
    return lookup
    
    
def life():
    
    birth = set([3])
    survival = set([3, 4]) #includes self
    return lifelike(birth, survival)

def vote():
    
    birth = set([8, 7, 6, 4])
    survival = set([9, 8, 7, 6, 4])
    return lifelike(birth, survival)

def brain():
    
    return brainlike([2], 1)

def stitch_torus(array, margin = 1):
    array[-margin:,:] = array[margin:margin * 2,:]
    array[:margin,:] = array[-margin * 2:-margin,:]
    array[:,-margin:] = array[:,margin:margin * 2]
    array[:,:margin] = array[:,-margin * 2:-margin]
    
def stitch_torus_1(array):
    array[-1,:] = array[1,:]
    array[0,:] = array[-2,:]
    array[:,-1] = array[:,1]
    array[:,0] = array[:,-2]
    
def map_torus(point, array, margin = 1):
    return (point[0] % (array.shape[0] - margin*2),
            point[1] % (array.shape[1] - margin*2))

