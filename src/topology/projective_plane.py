
def stitch(array, margin = 1):
    if margin == 1: #optimization
        return stitch_1(array, margin)
    array[-margin:,:] = array[margin:margin * 2,::-1]
    array[:margin,:] = array[-margin * 2:-margin,::-1]
    array[:,-margin:] = array[::-1,margin:margin * 2]
    array[:,:margin] = array[::-1,-margin * 2:-margin]

def stitch_1(array, margin = 1):
    array[-1,:] = array[1,::-1]
    array[0,:] = array[-2,::-1]
    array[:,-1] = array[::-1,1]
    array[:,0] = array[::-1,-2]

def map_point(point, array, margin = 1):
    d = [int(point[i] / (array.shape[i] - margin*2)) % 2 for i in (0, 1)]
    r = [((point[i] - 1) % (array.shape[i] - margin*2)) + 1 for i in (0, 1)]
    for i in (0, 1):
        if d[i]:
            r[i] = array.shape[i] - 1 - r[i]
    return r

def map_slice(upper_left, array, margin = 1):
    x0, y0 = map_point(upper_left, array, margin)
    x1, y1 = (array.shape[0] - margin*2,
              array.shape[1] - margin*2)
    return array[x0:x1, y0:y1]
    