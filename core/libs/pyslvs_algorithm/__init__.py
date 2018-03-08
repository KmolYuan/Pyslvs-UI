# -*- coding: utf-8 -*-

"""'pyslvs_algorithm' module contains
algorithm libraries to do triangular formula and dimentional synthesis.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .rga import Genetic
from .firefly import Firefly
from .de import DiffertialEvolution
from .tinycadlib import expr_parser
from .planarlinkage import build_planar

__all__ = [
    'Genetic',
    'Firefly',
    'DiffertialEvolution',
    'expr_parser',
    'build_planar'
]
