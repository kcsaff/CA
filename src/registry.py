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

import os, os.path, sys, imp

import logging

REG_DIR = 'reg'
REG_EXT = '_r.txt'

logger = logging.getLogger('registry')

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
    

def _register_file(filename):
    print filename
    name = os.path.basename(filename).split('.')[0]
    path = os.path.dirname(filename)
    args = imp.find_module(name, [path])
    module = imp.load_module(name, *args)
#    reg_name = os.path.join(os.path.dirname(filename),
#                            REG_DIR,
#                            path + REG_EXT)
#    if (os.path.exists(reg_name) and 
#            not os.path.getmtime(reg_name) < os.path.getmtime(filename)):
#        _load_registry(reg_name)
#    else:
#        _create_registry(filename, reg_name)

def _register_dir(path):
    print path
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
        except None:
            logger.warn('Unable to register purported module "%s"', name)
            filename = None
        if filename:
            _register_file(filename)



def auto_register(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)
    _register_dir(path)

def register(name, obj, quality = 1.0, filename=None):
    _registry[name] = obj

    
