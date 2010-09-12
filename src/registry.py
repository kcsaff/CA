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

import os, os.path, sys, imp, sys

import logging

REG_DIR = 'reg'
REG_EXT = '_r.txt'

logger = logging.getLogger('registry')

class _type_registry(object):
    def __init__(self):
        self.functions = {}
        self.quality = {}
    def __call__(self, obj):
        return self.functions[obj.type](obj)
    def insert(self, type, quality, function):
        if type not in self.functions or quality > self.quality[type]:
            self.functions[type] = function
            self.quality[type] = quality

_registry = {}

#Modules may register various objects.  Registrations should indicate:
# accessible name(s),  (including namespaces as namespace.namespace.name).
# version
# effectiveness, ie speed if applicable.
# if an adaptor, what does it adapt?
# name of class or function

#r = {'names': [...],
#     'version': '1.4.5',
#     'access': (path, name, call),
     

def _load_registry(regpath):
    path = os.path.dirname(os.path.dirname(regpath))
    name = os.path.basename(regpath)[-len(REG_EXT):]
    
def _get_full_module_name(filename):
    name = os.path.basename(filename).split('.')[0]
    path = os.path.dirname(filename)
    while path and path != sys.path[0]:
        name = '.'.join((os.path.basename(path), name))
        path = os.path.dirname(path)
    return name

def _register_file(filename):
    name = os.path.basename(filename).split('.')[0]
    path = os.path.dirname(filename)
    fullname = _get_full_module_name(filename)
    parentname = fullname.rsplit('.', 1)[0]
    __import__(parentname)
    args = imp.find_module(name, [path])
    module = imp.load_module(fullname, *args)
#    reg_name = os.path.join(os.path.dirname(filename),
#                            REG_DIR,
#                            path + REG_EXT)
#    if (os.path.exists(reg_name) and 
#            not os.path.getmtime(reg_name) < os.path.getmtime(filename)):
#        _load_registry(reg_name)
#    else:
#        _create_registry(filename, reg_name)

def _register_dir(path):
    register_path = os.path.join(path, REG_DIR)
    if not os.path.exists(register_path):
        os.mkdir(register_path)
    
    names = set([name.split('.')[0] 
                 for name in os.listdir(path)
                 if os.path.isfile(os.path.join(path, name))
                 ])

    for name in names:
        if not name[0].isalpha():
            continue
        try:
            _, filename, _ = imp.find_module(name, [path])
        except ImportError:
            logger.warn('Unable to register purported module "%s" under path "%s"', 
                        name, path)
            filename = None
        if filename:
            _register_file(filename)



def auto_register(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)
    _register_dir(path)

def register(name, quality=1.0, type=None, *args, **kwargs):
    import inspect
    module = inspect.getmodule(inspect.stack()[1][0])

    def decorator(fun):
        if name not in _registry:
            _registry[name] = _type_registry()
        _registry[name].insert(type, quality, fun)
        return fun
    return decorator

class _get(object):
    def __getattr__(self, attr):
        return _registry[attr]

get = _get()

