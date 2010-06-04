
def stitch(array, margin = 1):
    if isinstance(array, list):
        for chart in array:
            stitch(chart, margin)
        return
            
    if margin == 1: #optimization
        return stitch_1(array, margin)
    
    array[-margin:,:] = array[margin:margin * 2,:]
    array[:margin,:] = array[-margin * 2:-margin,:]
    array[:,-margin:] = array[:,margin:margin * 2]
    array[:,:margin] = array[:,-margin * 2:-margin]

def stitch_1(array, margin = 1):
    array[-1,:] = array[1,:]
    array[0,:] = array[-2,:]
    array[:,-1] = array[:,1]
    array[:,0] = array[:,-2]

def map_point(point, array, margin = 1):
    return (point[0] % (array.shape[0] - margin*2),
            point[1] % (array.shape[1] - margin*2))

def map_slice(upper_left, array, margin = 1):
    x0, y0 = map_point(upper_left, array, margin)
    x1, y1 = (array.shape[0] - margin*2,
              array.shape[1] - margin*2)
    return array[x0:x1, y0:y1]
    