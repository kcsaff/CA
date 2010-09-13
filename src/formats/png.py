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


def write(file, world, view):
    f = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    #First try to save PNG data (charts with palettes)
    _write_charts(f, world, view)
    _write_meta(f, world, view)
    f.close()

def read(file):
    return _reader().read(filename)
