# -*- coding: utf-8 -*-

"""'python_solvespace' module is a wrapper of
Python binding Solvespace solver libraries.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .slvs import (
    System, groupNum, Slvs_MakeQuaternion,
    Point3d, Workplane, Normal3d, Point2d, LineSegment2d, Constraint,
    SLVS_RESULT_OKAY, SLVS_RESULT_INCONSISTENT, SLVS_RESULT_DIDNT_CONVERGE, SLVS_RESULT_TOO_MANY_UNKNOWNS
)

__all__ = [
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
