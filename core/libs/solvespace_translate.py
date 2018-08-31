# -*- coding: utf-8 -*-

"""This module contains the Python-Solvespace simulation functions."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, List
from math import radians, cos, sin
from .pyslvs import VPoint
from .python_solvespace import (
    # Entities & Constraint
    Point3d,
    Workplane,
    Normal3d,
    Point2d,
    LineSegment2d,
    Constraint,
    # Result flags
    SLVS_RESULT_OKAY,
    SLVS_RESULT_INCONSISTENT,
    SLVS_RESULT_DIDNT_CONVERGE,
    SLVS_RESULT_TOO_MANY_UNKNOWNS,
    # System base
    System,
    groupNum,
    Slvs_MakeQuaternion,
)


def _2d_system(num: int) -> Tuple[System, Workplane, LineSegment2d]:
    """Create 2D CAD system."""
    sys = System(num + 13)
    sys.default_group = groupNum(1)
    origin = Point3d(sys.add_param(0.), sys.add_param(0.), sys.add_param(0.))
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    wp1 = Workplane(origin, Normal3d(
        sys.add_param(qw),
        sys.add_param(qx),
        sys.add_param(qy),
        sys.add_param(qz)
    ))
    origin2d = Point2d(wp1, sys.add_param(0.), sys.add_param(0.))
    Constraint.dragged(wp1, origin2d)
    hp = Point2d(wp1, sys.add_param(10.), sys.add_param(0.))
    Constraint.dragged(wp1, hp)
    vp = Point2d(wp1, sys.add_param(10.), sys.add_param(0.))
    Constraint.dragged(wp1, vp)
    # Name 'ground' is a horizontal line through (0, 0) and (10, 0).
    h_line = LineSegment2d(wp1, origin2d, hp)
    sys.default_group = groupNum(2)
    return sys, wp1, h_line


def _pos(p: Point2d) -> Tuple[float, float]:
    """Get position of a Point2d instance."""
    return (p.u().value, p.v().value)


def slvs_solve(
    vpoints: Tuple[VPoint],
    constraints: Tuple[Tuple[int, int, float]]
) -> Tuple[List[Tuple[float, float]], int]:
    """Use element module to convert into solvespace expression."""
    if not vpoints:
        return [], 0
    
    # Define VLinks here.
    vlinks = {}
    for i, vpoint in enumerate(vpoints):
        for vlink in vpoint.links:
            if vlink == 'ground':
                continue
            if vlink in vlinks:
                if i not in vlinks[vlink]:
                    vlinks[vlink].append(i)
            else:
                vlinks[vlink] = [i]
    
    # Limitation of Solvespacce kernel sys.
    point_count = 0
    slider_count = 0
    for vpoint in vpoints:
        point_count += 1
        if vpoint.type in {1, 2}:
            slider_count += 1
    
    sys, wp1, h_line = _2d_system(point_count * 2 + slider_count * 2 + len(constraints) * 2)
    
    solved_points = []
    slider_points = {}
    slot_points = {}
    for i, vpoint in enumerate(vpoints):
        if vpoint.type == 0:
            # Has only one coordinate.
            x = sys.add_param(vpoint.cx)
            y = sys.add_param(vpoint.cy)
            solved_points.append(Point2d(wp1, x, y))
        elif vpoint.type in {1, 2}:
            # Has two coordinates.
            bx = sys.add_param(vpoint.c[0][0])
            by = sys.add_param(vpoint.c[0][1])
            angle = radians(vpoint.angle)
            sx = sys.add_param(vpoint.c[0][0] + cos(angle))
            sy = sys.add_param(vpoint.c[0][1] + sin(angle))
            x = sys.add_param(vpoint.c[1][0])
            y = sys.add_param(vpoint.c[1][1])
            slider_points[i] = Point2d(wp1, bx, by)
            slot_points[i] = Point2d(wp1, sx, sy)
            solved_points.append(Point2d(wp1, x, y))
        if vpoint.grounded():
            Constraint.dragged(wp1, solved_points[i])
        elif vpoint.pin_grounded():
            Constraint.dragged(wp1, slider_points[i])
    
    # Link constraints.
    for vlink in vlinks:
        if len(vlinks[vlink]) < 2:
            continue
        a = vlinks[vlink][0]
        b = vlinks[vlink][1]
        distance = vpoints[a].distance(vpoints[b])
        if vpoints[a].is_slot_link(vlink):
            p1 = slider_points[a]
        else:
            p1 = solved_points[a]
        if vpoints[b].is_slot_link(vlink):
            p2 = slider_points[b]
        else:
            p2 = solved_points[b]
        if distance:
            Constraint.distance(distance, wp1, p1, p2)
        else:
            Constraint.on(wp1, p1, p2)
        for c in vlinks[vlink][2:]:
            for d in (a, b):
                distance = vpoints[c].distance(vpoints[d])
                if vpoints[c].is_slot_link(vlink):
                    p1 = slider_points[c]
                else:
                    p1 = solved_points[c]
                if vpoints[d].is_slot_link(vlink):
                    p2 = slider_points[d]
                else:
                    p2 = solved_points[d]
                if distance:
                    Constraint.distance(distance, wp1, p1, p2)
                else:
                    Constraint.on(wp1, p1, p2)
    
    # Slider constraints.
    for i, pb in slider_points.items():
        vpoint = vpoints[i]
        slider_slot = LineSegment2d(wp1, pb, slot_points[i])
        if vpoint.grounded():
            # Slot is grounded.
            if vpoint.angle in {0., 180.}:
                Constraint.parallel(wp1, h_line, slider_slot)
            else:
                Constraint.angle(wp1, radians(vpoint.angle), h_line, slider_slot)
            if vpoint.has_offset():
                Constraint.distance(vpoint.offset(), wp1, pb, solved_points[i])
        else:
            # Slider between links.
            for vlink in vpoint.links[:1]:
                f1 = vlinks[vlink][0]
                if f1 == i:
                    if len(vlinks[vlink]) < 2:
                        # If no any friend.
                        continue
                    f1 = vlinks[vlink][1]
                if vpoints[f1].is_slot_link(vlink):
                    helper = LineSegment2d(wp1, pb, slider_points[f1])
                else:
                    helper = LineSegment2d(wp1, pb, solved_points[f1])
                angle = vpoint.slope_angle(vpoints[f1]) - vpoint.angle
                if angle in {0., 180.}:
                    Constraint.parallel(wp1, slider_slot, helper)
                else:
                    Constraint.angle(wp1, radians(angle), slider_slot, helper)
                if vpoint.has_offset():
                    Constraint.distance(vpoint.offset(), wp1, pb, solved_points[i])
        # P joint.
        if vpoint.type == 1:
            for vlink in vpoint.links[1:]:
                f1 = vlinks[vlink][0]
                if f1 == a:
                    if len(vlinks[vlink]) < 2:
                        # If no any friend.
                        continue
                    f1 = vlinks[vlink][1]
                if vpoints[f1].is_slot_link(vlink):
                    helper = LineSegment2d(wp1, solved_points[i], slider_points[f1])
                else:
                    helper = LineSegment2d(wp1, solved_points[i], solved_points[f1])
                angle = vpoint.slope_angle(vpoints[f1]) - vpoint.angle
                if angle in {0., 180.}:
                    Constraint.parallel(wp1, slider_slot, helper)
                else:
                    Constraint.angle(wp1, radians(angle), slider_slot, helper)
    
    for p0, p1, angle in constraints:
        """The constraints of drive shaft.
        
        Simulate the input variables to the mechanism.
        The 'base points' are shaft center.
        """
        if vpoints[p0].type == 0:
            p_base = solved_points[p0]
        else:
            p_base = slider_points[p0]
        
        x = sys.add_param(round(vpoints[p0].cx + 10 * cos(radians(angle)), 8))
        y = sys.add_param(round(vpoints[p0].cy + 10 * sin(radians(angle)), 8))
        p_hand = Point2d(wp1, x, y)
        Constraint.dragged(wp1, p_hand)
        # The virtual link that dragged by "hand".
        leader = LineSegment2d(wp1, p_base, p_hand)
        # Make another virtual link that should follow "hand".
        if vpoints[p1].type == 0:
            p_drive = solved_points[p1]
        else:
            p_drive = slider_points[p1]
        link = LineSegment2d(wp1, p_base, p_drive)
        Constraint.angle(wp1, .5, link, leader)
    
    # Solve
    result_flag = sys.solve()
    if result_flag == SLVS_RESULT_OKAY:
        resultList = []
        for i, vpoint in enumerate(vpoints):
            p = solved_points[i]
            if vpoint.type == 0:
                resultList.append(_pos(p))
            else:
                resultList.append((_pos(slider_points[i]), _pos(p)))
        return resultList, sys.dof
    elif result_flag == SLVS_RESULT_INCONSISTENT:
        error = "Inconsistent."
    elif result_flag == SLVS_RESULT_DIDNT_CONVERGE:
        error = "Did not converge."
    elif result_flag == SLVS_RESULT_TOO_MANY_UNKNOWNS:
        error = "Too many unknowns."
    raise Exception(error)
