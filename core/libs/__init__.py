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
    expr_parser,
    expr_solving,
    expr_path,
    VPoint,
    VLink,
    Planar,
    NumberSynthesis,
    topo,
    Graph,
    vpoints_configure,
    dof,
    colorNames,
    colorRGB,
    parse_params,
    parse_vpoints,
    PMKSLexer,
)
from .python_solvespace import create2DSystem, slvsProcess

__all__ = [
    '__version__',
    'Genetic',
    'Firefly',
    'DiffertialEvolution',
    'Coordinate',
    'PLAP',
    'PLLP',
    'PLPP',
    'PXY',
    'expr_parser',
    'expr_solving',
    'expr_path',
    'VPoint',
    'VLink',
    'Planar',
    'NumberSynthesis',
    'topo',
    'Graph',
    'vpoints_configure',
    'dof',
    'colorNames',
    'colorRGB',
    'parse_params',
    'parse_vpoints',
    'PMKSLexer',
    'create2DSystem',
    'slvsProcess',
]
