# -*- coding: utf-8 -*-

"""Python-Solvespace wrapper for 2D CAD function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple
from .slvs import (
    #System base
    System,
    groupNum,
    Slvs_MakeQuaternion,
    #Entities & Constraint
    Point3d,
    Workplane,
    Normal3d,
    Point2d,
    LineSegment2d,
    Constraint,
)


def create2DSystem(num: int) -> Tuple[System, Workplane, LineSegment2d]:
    """Create CAD system."""
    sys = System(num + 12)
    sys.default_group = groupNum(1)
    origin = Point3d(
        sys.add_param(0.),
        sys.add_param(0.),
        sys.add_param(0.)
    )
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    wp1 = Workplane(origin, Normal3d(
        sys.add_param(qw),
        sys.add_param(qx),
        sys.add_param(qy),
        sys.add_param(qz)
    ))
    origin2d = Point2d(
        wp1,
        sys.add_param(0.),
        sys.add_param(0.)
    )
    Constraint.dragged(wp1, origin2d)
    hp = Point2d(
        wp1,
        sys.add_param(10.),
        sys.add_param(0.)
    )
    Constraint.dragged(wp1, hp)
    vp = Point2d(
        wp1,
        sys.add_param(10.),
        sys.add_param(0.)
    )
    Constraint.dragged(wp1, vp)
    #Name 'ground' is a horizontal line through (0, 0) and (10, 0).
    h_line = LineSegment2d(wp1, origin2d, hp)
    sys.default_group = groupNum(2)
    return sys, wp1, h_line
