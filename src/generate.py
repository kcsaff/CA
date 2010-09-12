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

import os.path, sys, imp
import shlex, subprocess

def __doc_string_for_c(string):
    if string:
        return string.replace('\n', '\\n"\n"')
    else:
        return 'No documentation provided.'

def __define_function(modname, name, doc, definition):
    
    fun_def = """
    /*****     FUNCTION: {modname}.{name}     *****/
    /*Documentation for {modname}.{name}: */
    PyDoc_STRVAR({modname}_{name}_doc, "{doc}");
    
    /*Definition for {modname}.{name}: */
    static PyObject *{modname}_{name}(PyObject *self, PyObject *args)
    {{
    {definition}
    }}    
    """.format(modname=modname,
               name=name,
               doc=__doc_string_for_c(doc),
               definition=definition)
    
    fun_dec = """
    /*Declaration for {modname}.{name}: */
    {{"{name}", 
    {modname}_{name}, 
    METH_VARARGS,
    {modname}_{name}_doc
    }},
    """.format(modname=modname,
               name=name)
    
    return fun_def, fun_dec

def __define_module(name, doc, fun_defs, fun_decs):
    
    mod_def = """
#include "Python.h"
#include <stdlib.h>
#include "numpy/arrayobject.h"

/******* Definition for module "{name}" *******/

static PyObject *ErrorObject;

{fun_defs}

/* Function declarations. */

static PyMethodDef {name}_methods[] = {{
{fun_decs}
    {{NULL, NULL}} /* sentinel */
}};

/* Module {name} documentation */
PyDoc_STRVAR(module_doc, "{doc}");

/* Module {name} initialization */
PyMODINIT_FUNC
init{name}(void)
{{
    PyObject *m;

    /* Create the module and add the functions */
    m = Py_InitModule3("{name}", {name}_methods, module_doc);
    if (m == NULL)
        return;

    /* Use numpy arrays. */
    import_array();
}}
    """.format(name=name,
               doc=__doc_string_for_c(doc),
               fun_defs='\n'.join(fun_defs),
               fun_decs='\n'.join(fun_decs))
    
    return mod_def
    
def __create_c(module_name,
                module_doc,
                function_list, #list of tuples: (name, doc, definition)
                ):
    fun_defs = []
    fun_decs = []
    for fun in function_list:
        fun_def, fun_dec = __define_function(module_name, *fun)
        fun_defs.append(fun_def)
        fun_decs.append(fun_dec)
    mod_def = __define_module(module_name,
                              module_doc,
                              fun_defs,
                              fun_decs)
    
    return mod_def

def __c_filename(module_name):
    return '%smodule.c' % module_name

def __save_c(path, #path to directory to save c file under.
             module_name,
             module_doc,
             function_list):
    filename = os.path.join(path, __c_filename(module_name))
    f = file(filename, 'w')
    f.write(__create_c(module_name,
                       module_doc,
                       function_list))
    f.close()
    
def __create_setup(path, module_name):
    result = """
from distutils.core import setup, Extension
#raw_input()
try:
    setup (name = 'Ex',
           version = '0.1',
           description = 'Yes',
           ext_modules = [Extension('{module_name}', sources=['{filename}'])],
           include_dirs = ['C:/Python26/Lib/site-packages/numpy/core/include']) 
except Exception as e:
    print 'Oh no!'
    #raw_input()
#raw_input()
    """.format(module_name=module_name,
               filename=os.path.join(path, __c_filename(module_name)).replace('\\', '\\\\'))
    return result
    
def __save_setup(path,#path to directory to save files under.
                 module_name
                 ):
    filename = os.path.join(path, 'setup.py')
    f = file(filename, 'w')
    f.write(__create_setup(path, module_name))
    f.close()

def __build_inplace(path, outpath=None):
    outpath = outpath or path
    python = sys.executable
    setup = os.path.join(path, 'setup.py')
    output = file(os.path.join(path, 'log.txt'), 'w')
    the_call = '{python} {setup} build_ext --inplace'.format(python=python,
                                                             setup=setup)
    the_call = the_call.replace('\\', '/') #hack for windows, shlex removes backslashes
    print the_call
    args = shlex.split(the_call)
    print args
    result = subprocess.Popen(args, 
                              stdout=output, 
                              stderr=subprocess.STDOUT,
                              cwd=outpath).communicate()
    return result

def __generate_from_c(path,
                        module_name, 
                        module_doc,
                        function_list, #list of tuples: (name, doc, definition)
                        ):
    temp_path = os.path.join(path, 'build')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    __save_c(temp_path,
             module_name,
             module_doc,
             function_list,
             )
    __save_setup(temp_path,
                 module_name,
                 )
    __build_inplace(temp_path, path)

class __to_generate(object):
    def __init__(self,
                 name, 
                 docstring,
                 definition, 
                 signature = None):
        self.name = name
        self.docstring = docstring
        self.definition = definition
        self.signature = signature

    def unwrap(self):
        return (self.name,
                self.docstring,
                self.definition)

def c(fun):
    return __to_generate(fun.__name__,
                         fun.__doc__,
                         fun())
    
def auto_generate(source_name):
    #source is expected to be a module name, __name__
    source = sys.modules[source_name]
    module_name = '_c'
    module_doc = source.__doc__

    function_list = []
    if 'functions' in source.__dict__:
        function_list = source.functions
    for value in source.__dict__.values():
        if isinstance(value, __to_generate):
            function_list.append(value.unwrap())
            
    path = os.path.dirname(source.__file__)
    
    try:
        _, found_module, _ = imp.find_module(module_name, [path])
        if os.path.getmtime(found_module) < os.path.getmtime(source.__file__):
            os.remove(found_module)
            found_module = None
    except ImportError:
        found_module = None
        
    if not found_module:
        __generate_from_c(path,
                          module_name,
                          module_doc,
                          function_list,
                          )

    module = __import__(module_name, source.__dict__)
    for fun in function_list:
        setattr(source, fun[0], getattr(module, fun[0]))
    #setattr(source, module_name, __import__(module_name, source.__dict__))
    
