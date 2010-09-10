from distutils.core import setup, Extension

module1 = Extension('xx',
                    sources = ['xxmodule.c'])

setup (name = 'Ex',
       version = '0.1',
       description = 'Yes',
       ext_modules = [module1],
       include_dirs = ['C:/Python26/Lib/site-packages/numpy/core/include']) 

import shutil

try:
    os.remove('xx.pyd')
except:
    pass
shutil.copy('build/lib.win32-2.6/xx.pyd', 'xx.pyd')
