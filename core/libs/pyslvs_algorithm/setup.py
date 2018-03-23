from distutils.core import setup
import distutils.sysconfig
from Cython.Build import cythonize
import numpy

cfg_vars = distutils.sysconfig.get_config_vars()
for key, value in cfg_vars.items():
    if type(value) == str:
        cfg_vars[key] = value.replace("-Wstrict-prototypes", "")

setup(
    ext_modules=cythonize(
        '*.pyx',
        compiler_directives={'boundscheck':True}
    ),
    include_dirs=[numpy.get_include()]
)
