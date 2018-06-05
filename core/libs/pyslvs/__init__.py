# -*- coding: utf-8 -*-

"""Kernel of Pyslvs.

This kernel can work without GUI.

Modules:
+ Solver:
    + parser
    + tinycadlib
    + triangulation
+ Dimensional synthesis:
    + planarlinkage
    + rga
    + firefly
    + de
+ Number synthesis:
    + number
+ Topologic synthesis:
    + topologic

Dependents:
+ lark-parser
+ pygments (optional: provide highlighting)
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"
__version__ = (18, 6, 0, 'dev')

from .tinycadlib import (
    Coordinate,
    PLAP,
    PLLP,
    PLPP,
    PXY,
    expr_parser,
    expr_solving,
    expr_path,
    data_collecting,
    VPoint,
    VLink,
)
from .planarlinkage import Planar
from .rga import Genetic
from .firefly import Firefly
from .de import DiffertialEvolution
from .number import NumberSynthesis
from .topologic import topo, Graph
from .triangulation import vpoints_configure, dof
from .parser import (
    colorNames,
    colorRGB,
    parse_params,
    parse_vpoints,
    HAS_PYGMENTS,
)
if HAS_PYGMENTS:
    try:
        from .parser import PMKSLexer
    except ImportError:
        raise ImportError("no module name 'Pygment'")

__all__ = [
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
    'data_collecting',
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
]
