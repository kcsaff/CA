from cascading_object import cascading_object

class View(cascading_object):
    pass

def _mix(amount, color0, color1):
    result = 0
    for component in (0xFF0000, 0x00FF00, 0x0000FF):
        part0 = color0 & component
        part1 = color1 & component
        mixed_part = int(round(part0 * (1.0 - amount) + part1 * amount)) & component
        result |= mixed_part
    return result

def _gradient(size, color0, color1):
    if size == 1:
        return [color0]
    
    return [_mix(i / (size - 1.0), color0, color1) 
            for i in range(size)]

def _mcell_few(size):
    return [0] + _gradient(size - 1, 0xFFFF00, 0xFF0000)

def _mcell_many():
    #Stolen from MCell's MJPalette.java
    Palette = [0] * 64
    Palette[ 0] = 0;
    Palette[ 1] = 16776960;
    Palette[ 2] = 16767744;
    Palette[ 3] = 16758528;
    Palette[ 4] = 16749312;
    Palette[ 5] = 16740096;
    Palette[ 6] = 16730880;
    Palette[ 7] = 16721664;
    Palette[ 8] = 16711680;
    Palette[ 9] = 15728640;
    Palette[10] = 14745600;
    Palette[11] = 13762560;
    Palette[12] = 12779520;
    Palette[13] = 11796480;
    Palette[14] = 10813440;
    Palette[15] = 9830400;
    Palette[16] = 8388608;
    Palette[17] = 8060928;
    Palette[18] = 7733248;
    Palette[19] = 7405568;
    Palette[20] = 7077888;
    Palette[21] = 6750208;
    Palette[22] = 6422528;
    Palette[23] = 6094848;
    Palette[24] = 5308416;
    Palette[25] = 4660992;
    Palette[26] = 4013568;
    Palette[27] = 3366144;
    Palette[28] = 2718720;
    Palette[29] = 2071296;
    Palette[30] = 1423872;
    Palette[31] = 776448;
    Palette[32] = 65280;
    Palette[33] = 65311;
    Palette[34] = 65342;
    Palette[35] = 65373;
    Palette[36] = 65404;
    Palette[37] = 65435;
    Palette[38] = 65466;
    Palette[39] = 65497;
    Palette[40] = 65535;
    Palette[41] = 57599;
    Palette[42] = 49663;
    Palette[43] = 41727;
    Palette[44] = 33791;
    Palette[45] = 25855;
    Palette[46] = 17919;
    Palette[47] = 9983;
    Palette[48] = 255;
    Palette[49] = 1376490;
    Palette[50] = 2752725;
    Palette[51] = 4128960;
    Palette[52] = 5505195;
    Palette[53] = 6881430;
    Palette[54] = 8388736;
    Palette[55] = 9180536;
    Palette[56] = 9972336;
    Palette[57] = 10764136;
    Palette[58] = 11555936;
    Palette[59] = 12347736;
    Palette[60] = 13139536;
    Palette[61] = 13931336;
    Palette[62] = 14723136;
    Palette[63] = 15514936;
    Palette *= 4
    Palette[64] = Palette[66] 
    Palette[128] = Palette[66]
    Palette[192] = Palette[66]
    return Palette

class palette(object):
    default = (0, 0xFFFFFF, 0xFF0000, 0, 0xCC9900)
    
    cga = (0x000000, 0x0000AA, 0x00AA00, 0x00AAAA,
           0xAA0000, 0xAA00AA, 0xAA5500, 0xAAAAAA,
           0x555555, 0x5555FF, 0x55FF55, 0x55FFFF,
           0xFF5555, 0xFF55FF, 0xFFFF55, 0xFFFFFF)

    grays = _gradient(256, 0x000000, 0xFFFFFF)
    
    @staticmethod
    def mcell(states = (0,1)):
        if len(states) <= 16:
            palette = _mcell_few(len(states))
        else:
            palette = _mcell_many()
        #Map palette to the states we're going to use.
        result = [0] * (max(states) + 1)
        for i, state in enumerate(states):
            result[state] = palette[i]
        return result

def default():
    result = View(source='default')
    result.center = (0,0)
    result.zoom = 1
    result.palette = palette.default
    result.speed = 60
    return result

def water():
    result = View(source='water')
    result.center = (0,0)
    result.zoom = 1
    result.palette = palette.grays
    result.speed = 60
    return result
     
