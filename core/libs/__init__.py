# -*- coding: utf-8 -*-

"""'lib' module contains C++ and Cython libraries."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .pyslvs_algorithm import (
    Genetic,
    Firefly,
    DiffertialEvolution,
    Coordinate,
    PLAP,
    PLLP,
    PLPP,
    expr_parser,
    expr_solving,
    expr_path,
    VPoint,
    VLink,
    build_planar,
)
from .pyslvs_topologic import (
    NumberSynthesis,
    topo,
    Graph,
    graph_configure,
    vpoints_configure,
)
#Solvespace API.
from .python_solvespace.slvs import (
    System,
    groupNum,
    Slvs_MakeQuaternion,
    Point3d,
    Workplane,
    Normal3d,
    Point2d,
    LineSegment2d,
    Constraint,
    SLVS_RESULT_OKAY,
    SLVS_RESULT_INCONSISTENT,
    SLVS_RESULT_DIDNT_CONVERGE,
    SLVS_RESULT_TOO_MANY_UNKNOWNS,
)

__all__ = [
    'Genetic',
    'Firefly',
    'DiffertialEvolution',
    'Coordinate',
    'PLAP',
    'PLLP',
    'PLPP',
    'expr_parser',
    'expr_solving',
    'expr_path',
    'VPoint',
    'VLink',
    'build_planar',
    'NumberSynthesis',
    'topo',
    'Graph',
    'graph_configure',
    'vpoints_configure',
    'System',
    'groupNum',
    'Slvs_MakeQuaternion',
    'Point3d',
    'Workplane',
    'Normal3d',
    'Point2d',
    'LineSegment2d',
    'Constraint',
    'SLVS_RESULT_OKAY',
    'SLVS_RESULT_INCONSISTENT',
    'SLVS_RESULT_DIDNT_CONVERGE',
    'SLVS_RESULT_TOO_MANY_UNKNOWNS',
]
