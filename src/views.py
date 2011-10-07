# Copyright (C) 2010 by Kevin Saff

# This file is part of the CA scanner.

# The CA scanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The CA scanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the CA scanner.  If not, see <http://www.gnu.org/licenses/>.

import generate
import numpy
import simple

class View(simple.typed_object):
    center = (0,0)
    zoom = 1
    speed = 60
    def __init__(self, **kwargs):
        simple.typed_object.__init__(self, 'view', **kwargs)
    def __call__(self, chart):
        return self.colorize(chart, self.palette)

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

def _to_rgb(color):
    red = (color & 0xFF0000) >> 16
    green = (color & 0x00FF00) >> 8
    blue = (color & 0x0000FF) >> 0
    return (red, green, blue)

def _from_rgb(color):
    return (color[0] << 16) | (color[1] << 8) | (color[2] << 0)

class palette(object):
    default = (0, 0xFFFFFF, 0xFF0000, 0, 0xCC9900)
    
    cga = (0x000000, 0x0000AA, 0x00AA00, 0x00AAAA,
           0xAA0000, 0xAA00AA, 0xAA5500, 0xAAAAAA,
           0x555555, 0x5555FF, 0x55FF55, 0x55FFFF,
           0xFF5555, 0xFF55FF, 0xFFFF55, 0xFFFFFF)

    grays = _gradient(256, 0x000000, 0xFFFFFF)

    @staticmethod
    def to_rgb(palette):
        return [_to_rgb(color) for color in palette]

    @staticmethod
    def from_rgb(palette):
        return [_from_rgb(color) for color in palette]
    
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
    
def _colorize_default(chart, palette):
    return numpy.take(palette, chart.data)
    
def _colorize_gradient(chart, palette):
    mean = numpy.mean(chart.data)
    std = numpy.std(chart.data)
    #top = numpy.max(chart.data)
    #bot = numpy.min(chart.data)
    top = mean + std * 2
    bot = mean - std * 2
    data = (chart.data - bot) * 255.9 / (top - bot)
    data = numpy.cast[numpy.int16](data)
#    data = numpy.cast[numpy.uint8](chart.data)
    return numpy.take(palette, data, mode='clip')
    
def _colorize_specular(chart, palette):
    data = chart.data
    data = data[1:,1:] - data[:-1,:-1]
    
    mean = numpy.mean(data[1:-1,1:-1])
    std = numpy.std(data[1:-1,1:-1])
    #top = numpy.max(chart.data)
    #bot = numpy.min(chart.data)
    top = mean + std * 2
    bot = mean - std * 2
    data = (data - bot) * 255.9 / (top - bot)
    data = numpy.cast[numpy.int16](data)
#    data = numpy.cast[numpy.uint8](chart.data)
    return numpy.take(palette, data, mode='clip')

def _colorize_rivers(chart, palette=None):
#    data = numpy.cast[numpy.uint8](chart.data)
#    data = numpy.cast[numpy.uint32](data)
#    return (data[:,:,0] << 8) + (data[:,:,1])
    wtop = numpy.max(chart.data[1:-1,1:-1,1])
    wbot = numpy.min(chart.data[1:-1,1:-1,1])
    wdata = (chart.data[1:-1,1:-1,1] - wbot) * 255.9 / (wtop - wbot)
    vtop = numpy.max(chart.data[1:-1,1:-1,0])
    vbot = numpy.min(chart.data[1:-1,1:-1,0])
    vdata = (chart.data[1:-1,1:-1,0] - vbot) * 255.9 / (vtop - vbot)
    #return numpy.cast[numpy.uint8](vdata)
    return (numpy.cast[numpy.uint16](vdata)) << 8 + numpy.cast[numpy.uint8](wdata)
#    print top, bot
#    top = numpy.max(data)
#    bot = numpy.min(data)
#    print top, bot
#    print palette
#    data = numpy.cast[numpy.uint8](chart.data)
    return numpy.take(palette, data, mode='clip')

def default():
    result = View(palette=palette.default,
                  colorize=_colorize_default)
    return result

def water():
    result = View(palette=palette.grays,
                  colorize=_colorize_specular)
    return result

def rivers():
    result = View(palette=palette.grays,
                  colorize=_colorize_rivers)
    return result
     
