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

class typed_object(object):
    def __init__(self, type, **kwargs):
        self.type = type
        self.kwargs = kwargs
        
    def __getattr__(self, attr):
        return self.kwargs.get(attr)
    
    def format_args(self):
        args = ["'%s'" % self.type]
        args.extend(['%s=%s' % (key, repr(value)) 
                     for key, value in self.kwargs.items()])
        return ', '.join(args)
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           self.format_args())
        
