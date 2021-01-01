# -*- coding: utf-8 -*-

"""Solvespace format output as frame sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence, Iterable, Callable, List
from pyslvs import VPoint
from .write import SlvsWriter2


def slvs2_frame(
    vpoints: Sequence[VPoint],
    v_to_slvs: Callable[[], Iterable[Tuple[int, int]]],
    file_name: str
):
    """Generate frame sketch, ignore all points that was no any connection."""
    edges = tuple(v_to_slvs())

    # Writer object
    writer = SlvsWriter2()

    # Add "Param"
    for i, edge in enumerate(edges):
        writer.param_num += 0x10
        for p in edge:
            writer.param_val(writer.param_num, vpoints[p].cx)
            writer.param_num += 1
            writer.param_val(writer.param_num, vpoints[p].cy)
            writer.param_num += 2
        writer.param_shift16()

    # Add "Request"
    for _ in range(len(edges)):
        writer.request_line(writer.request_num)
        writer.request_num += 1

    # The number of same points
    point_num: List[List[int]] = [[] for _ in range(len(vpoints))]
    # The number of same lines
    line_num: List[List[int]] = [[] for _ in range(len(edges))]

    # Add "Entity"
    for i, edge in enumerate(edges):
        writer.entity_line(writer.entity_num)
        for p in edge:
            writer.entity_num += 1
            point_num[p].append(writer.entity_num)
            writer.entity_point_2d(writer.entity_num, vpoints[p].cx, vpoints[p].cy)
            line_num[i].append(writer.entity_num)
        writer.entity_shift16()

    # Add "Constraint
    # Same point constraint
    for ps in point_num:
        for p in ps[1:]:
            writer.constraint_point(writer.constraint_num, ps[0], p)
            writer.constraint_num += 1
    # Position constraint
    for i, vpoint in enumerate(vpoints):
        if "ground" in vpoint.links and point_num[i]:
            writer.constraint_grounded(writer.constraint_num, point_num[i][0], vpoint.cx, vpoint.cy)
            writer.constraint_num += 2
    # Distance constraint
    for i, (n1, n2) in enumerate(line_num):
        p1, p2 = edges[i]
        writer.constraint_distance(writer.constraint_num, n1, n2, vpoints[p1].distance(vpoints[p2]))
        writer.constraint_num += 1
    # Comment constraint
    for i, vpoint in enumerate(vpoints):
        writer.constraint_comment(writer.constraint_num, f"Point{i}", vpoint.cx, vpoint.cy)
        writer.constraint_num += 1

    # Write file
    writer.save(file_name)
