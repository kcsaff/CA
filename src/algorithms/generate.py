
import os.path, sys
import shlex, subprocess

def __doc_string_for_c(string):
    return string.replace('\n', '\\n\n')

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
    
def __create_setup(module_name):
    result = """
from distutils.core import setup, Extension

setup (name = 'Ex',
       version = '0.1',
       description = 'Yes',
       ext_modules = [Extension('{module_name}', '{filename}')],
       include_dirs = ['C:/Python26/Lib/site-packages/numpy/core/include']) 
    """.format(module_name=module_name,
               filename=__c_filename(module_name))
    return result
    
def __save_setup(path,#path to directory to save files under.
                 module_name
                 ):
    filename = os.path.join(path, 'setup.py')
    f = file(filename, 'w')
    f.write(__create_setup(module_name))
    f.close()

def __build_inplace(path):
    python = os.path.join(sys.exec_prefix, 'python')
    setup = os.path.join(path, 'setup.py')
    the_call = '{python} {setup} build_ext --inplace'.format(python=python,
                                                             setup=setup)
    result = subprocess.Popen(shlex.split(the_call))
    return result

def generate_from_c(path,
                        module_name, 
                        module_doc,
                        function_list, #list of tuples: (name, doc, definition)
                        ):
    temp_path = os.path.join(path, 'temp')
    __save_c(temp_path,
             module_name,
             module_doc,
             function_list,
             )
    __save_setup(temp_path,
                 module_name,
                 )
    
    