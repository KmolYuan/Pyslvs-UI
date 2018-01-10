# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang [pyslvs@gmail.com]

"""
"lib" module contains C++ and Cython libraries.
"""

from .pyslvs_algorithm.rga import Genetic
from .pyslvs_algorithm.firefly import Firefly
from .pyslvs_algorithm.de import DiffertialEvolution
from .pyslvs_algorithm import tinycadlib
from .pyslvs_algorithm.planarlinkage import build_planar
from .pyslvs_topologic.number import NumberSynthesis
from .pyslvs_topologic.topologic import topo
from .python_solvespace.slvs import (
    System, groupNum, Slvs_MakeQuaternion,
    Point3d, Workplane, Normal3d, Point2d, LineSegment2d, Constraint,
    SLVS_RESULT_OKAY, SLVS_RESULT_INCONSISTENT, SLVS_RESULT_DIDNT_CONVERGE, SLVS_RESULT_TOO_MANY_UNKNOWNS
)

__all__ = [
    'Genetic',
    'Firefly',
    'DiffertialEvolution',
    'tinycadlib',
    'build_planar',
    'NumberSynthesis',
    'topo',
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
