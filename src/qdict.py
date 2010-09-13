#!/usr/bin/env python

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

class qdict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._quality = {}
        self._source = {}
    def __setitem__(self, key, value):
        key, quality, source = key, 0.0, None
        if isinstance(key, tuple):
            s = key
            if len(s) > 0:
                key = s[0]
            if len(s) > 1:
                quality = s[1]
            if len(s) > 2:
                source = s[2]
        if key not in self or quality >= self._quality[key]:
            dict.__setitem__(self, key, value)
            self._quality[key] = quality
            self._source[key] = source
    def update(self, other):
        if hasattr(other, '_quality'):
            if hasattr(other, '_source'):
                for key in other:
                    self[key, other._quality[key], other._source[key]] = other[key]
            else:
                for key in other:
                    self[key, other._quality[key]] = other[key]
        else:
            dict.update(self, other)
    def source(self, key):
        return self._source[key]