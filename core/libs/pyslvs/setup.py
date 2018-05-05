# -*- coding: utf-8 -*-

"""Compile the Cython libraries of Pyslvs."""

from distutils.core import setup, Extension
import os

from Cython.Distutils import build_ext
import numpy


sources = [
    source for source in os.listdir(".")
    if source.split('.')[-1] == 'pyx'
]
extra_compile_args = [
    #Compiler optimize.
    '-O3',
    #Disable NumPy warning only on Linux.
    '-Wno-cpp',
    #Windows format warning.
    '-Wno-format',
]

setup(
    ext_modules = [
        Extension(
            source.split('.')[0],
            sources = [source],
            extra_compile_args = extra_compile_args,
        )
        for source in sources
    ],
    cmdclass = {'build_ext': build_ext},
    include_dirs = [numpy.get_include()],
)
