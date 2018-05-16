# -*- coding: utf-8 -*-

"""'pyslvs' module contains

+ Algorithm libraries to do triangular formula and dimentional synthesis.
+ Number synthesis and type synthesis libraries.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .tinycadlib import (
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
