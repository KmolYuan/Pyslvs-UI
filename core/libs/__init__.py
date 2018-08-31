# -*- coding: utf-8 -*-

"""'lib' module contains C++ and Cython libraries."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .pyslvs import (
    __version__,
    Genetic,
    Firefly,
    DiffertialEvolution,
    Coordinate,
    PLAP,
    PLLP,
    PLPP,
    PXY,
    expr_solving,
    data_collecting,
    VPoint,
    VLink,
    bfgs_vpoint_solving,
    Planar,
    number_synthesis,
    topo,
    Graph,
    vpoints_configure,
    vpoint_dof,
    colorNames,
    colorRGB,
    parse_params,
    parse_vpoints,
    PMKSLexer,
    example_list,
)
from .solvespace_translate import slvs_solve

__all__ = [
    '__version__',
    'kernel_list',
    'Genetic',
    'Firefly',
    'DiffertialEvolution',
    'Coordinate',
    'PLAP',
    'PLLP',
    'PLPP',
    'PXY',
    'expr_solving',
    'data_collecting',
    'VPoint',
    'VLink',
    'bfgs_vpoint_solving',
    'Planar',
    'number_synthesis',
    'topo',
    'Graph',
    'vpoints_configure',
    'vpoint_dof',
    'colorNames',
    'colorRGB',
    'parse_params',
    'parse_vpoints',
    'PMKSLexer',
    'example_list',
    'slvs_solve',
]


kernel_list = ("Pyslvs", "Python-Solvespace", "Sketch Solve")
