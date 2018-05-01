# -*- coding: utf-8 -*-

"""Compile the Cython libraries of Pyslvs."""

from distutils.core import setup
import os

from Cython.Build import cythonize
import numpy


os.environ['CFLAGS'] = '-O3 -Wno-cpp'

setup(
    ext_modules = cythonize(
        '*.pyx',
        compiler_directives = {'boundscheck': True}
    ),
    include_dirs = [numpy.get_include()],
)
