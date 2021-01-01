# -*- coding: utf-8 -*-

"""Solvespace format output as linkage sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, List, Tuple, Iterator
from math import radians, sin, cos, atan2
from pyslvs import VPoint, Coord
from pyslvs_ui.graphics import convex_hull
from .write import SlvsWriter2

_Coord = Tuple[float, float]
_CoordsPair = Tuple[Coord, Coord]


def _by_frame() -> Iterator[int]:
    """Number code of frame."""
    yield 0
    yield 1
    k = 2
    while True:
        for code in (0, 1):
            yield code
            yield k
        k += 1


def _by_boundary(length: int) -> Iterator[int]:
    """Number code of boundary."""
    k = 0
    while True:
        yield k
        k += 1
        k %= length
        yield k


def boundary_loop(
    boundary: Sequence[_Coord],
    radius: float
) -> List[_CoordsPair]:
    """Create boundary edges by pairs of coordinates."""
    boundary_tmp = []
    for i in range(len(boundary)):
        p1 = Coord(*boundary[i])
        p2 = Coord(*boundary[i + 1 if i + 1 < len(boundary) else 0])
        alpha = atan2(p2.y - p1.y, p2.x - p1.x) - radians(90)
        offset_x = radius * cos(alpha)
        offset_y = radius * sin(alpha)
        boundary_tmp.append((
            Coord(p1.x + offset_x, p1.y + offset_y),
            Coord(p2.x + offset_x, p2.y + offset_y),
        ))
    return boundary_tmp


def slvs2_part(vpoints: List[VPoint], radius: float, file_name: str) -> None:
    """Generate a linkage sketch by specified radius."""
    # Translate
    min_x = min(vpoint.cx for vpoint in vpoints)
    min_y = min(vpoint.cy for vpoint in vpoints)
    centers = [(vpoint.cx - min_x, vpoint.cy - min_y) for vpoint in vpoints]
    # Synchronous the point coordinates after using convex hull
    centers_ch = convex_hull(centers)
    _boundary = centers_ch.copy()
    for x, y in centers:
        if (x, y) not in centers_ch:
            centers_ch.append((x, y))
    centers = centers_ch
    del vpoints, min_x, min_y

    # Frame (p1, p2, p3) -> ((p1, p2), (p3, p1), (p3, p2))
    frame: List[_CoordsPair] = [(
        Coord(centers[-2][0], centers[-2][1]),
        Coord(centers[-1][0], centers[-1][1]),
    )]
    for x, y in centers[2:]:
        frame.append((frame[0][0], Coord(x, y)))
        frame.append((frame[0][1], Coord(x, y)))

    # Boundary
    boundary = boundary_loop(_boundary, radius)
    del _boundary

    # Writer object
    writer = SlvsWriter2()
    writer.script_group.pop()
    writer.group_normal(0x3, "boundary")

    # Add "Param"
    def add_param(edges: Sequence[_CoordsPair]) -> None:
        """Add param by pair of coordinates."""
        for edge in edges:
            writer.param_num += 0x10
            for coord in edge:
                writer.param_val(writer.param_num, coord.x)
                writer.param_num += 1
                writer.param_val(writer.param_num, coord.y)
                writer.param_num += 2
            writer.param_shift16()

    def arc_coords(
        index: int,
        _cx: float,
        _cy: float
    ) -> Iterator[_Coord]:
        yield from (
            (_cx, _cy),
            (boundary[index - 1][1].x, boundary[index - 1][1].y),
            (boundary[index][0].x, boundary[index][0].y),
        )

    add_param(frame)
    add_param(boundary)
    # Circles
    for x, y in centers:
        writer.param_num += 0x10
        writer.param_val(writer.param_num, x)
        writer.param_num += 1
        writer.param_val(writer.param_num, y)
        # Shift to 0x40
        writer.param_num += 0x2f
        writer.param_val(writer.param_num, radius / 2)
        writer.param_shift16()
    # Arc
    for i in range(len(boundary)):
        cx, cy = centers[i]
        writer.param_num += 0x10
        for x, y in arc_coords(i, cx, cy):
            writer.param_val(writer.param_num, x)
            writer.param_num += 1
            writer.param_val(writer.param_num, y)
            writer.param_num += 2
        writer.param_shift16()

    # Group 2:
    point_count = len(centers)
    # The number of same points
    point_num: List[List[int]] = [[] for _ in range(point_count)]
    # The number of same lines
    line_num: List[List[int]] = [[] for _ in range(len(frame))]

    def segment_processing(edges: Sequence[_CoordsPair], *,
                           is_frame: bool = True) -> None:
        """Add edges to work plane. (No any constraint.)"""
        # Add "Request"
        for _ in range(len(edges)):
            writer.request_line(writer.request_num)
            writer.request_num += 1

        # Add "Entity"
        p_counter = _by_frame() if is_frame else _by_boundary(len(point_num))
        for index, edge in enumerate(edges):
            writer.entity_line(writer.entity_num)
            for j, coord in enumerate(edge):
                writer.entity_num += 1
                point_num[next(p_counter)].append(writer.entity_num)
                writer.entity_point_2d(writer.entity_num, coord.x, coord.y)
                line_num[index].append(writer.entity_num)
            writer.entity_shift16()

    segment_processing(frame, is_frame=True)
    center_num = [nums[0] for nums in point_num]
    # Add "Constraint"
    # Same point constraint
    for p in point_num:
        for p_ in p[1:]:
            writer.constraint_point(writer.constraint_num, p[0], p_)
            writer.constraint_num += 1
    for i, (n1, n2) in enumerate(line_num):
        p1, p2 = frame[i]
        writer.constraint_distance(writer.constraint_num, n1, n2,
                                   p1.distance(p2))
        writer.constraint_num += 1
    # Add "Constraint" of position
    for i, c in enumerate(frame[0]):
        writer.constraint_grounded(writer.constraint_num, point_num[i][0], c.x, c.y)
        if i == 1:
            writer.script_constraint.pop()
            writer.constraint_num += 1
        else:
            writer.constraint_num += 2

    # Group 3:
    writer.set_group(0x3)

    # The number of same points
    point_num = [[] for _ in range(len(boundary))]
    # The number of same lines
    line_num = [[] for _ in range(len(boundary))]
    segment_processing(boundary)
    # The number of circles
    circles = []

    def add_circle(index: int, _x: float, _y: float) -> None:
        """Add circle"""
        # Add "Request"
        writer.request_circle(writer.request_num)
        writer.request_num += 1
        # Add "Entity"
        writer.entity_circle(writer.entity_num)
        circles.append(writer.entity_num)
        writer.entity_num += 1
        writer.entity_point_2d(writer.entity_num, _x, _y)
        num = writer.entity_num
        # Shift to 0x20
        writer.entity_num += 0x1f
        writer.entity_normal_2d(writer.entity_num, num)
        # Shift to 0x40
        writer.entity_num += 0x20
        writer.entity_distance(writer.entity_num, radius / 2)
        writer.entity_shift16()
        # Add "Constraint" for centers
        writer.constraint_point(writer.constraint_num, num, center_num[index])
        writer.constraint_num += 1
        # Add "Constraint" for diameter
        if index == 0:
            writer.constraint_diameter(writer.constraint_num, circles[-1],
                                       radius)
        else:
            writer.constraint_equal_radius(writer.constraint_num, circles[-1],
                                           circles[0])
        writer.constraint_num += 1

    def add_arc(index: int, _cx: float, _cy: float) -> None:
        """Add arc"""
        # Add "Request"
        writer.request_arc(writer.request_num)
        writer.request_num += 1
        # Add "Entity"
        writer.entity_arc(writer.entity_num)
        circles.append(writer.entity_num)
        p3 = []
        for ax, ay in arc_coords(index, _cx, _cy):
            writer.entity_num += 1
            writer.entity_point_2d(writer.entity_num, ax, ay)
            p3.append(writer.entity_num)
        writer.entity_num += 0x3d
        writer.entity_normal_2d(writer.entity_num, p3[0])
        writer.entity_shift16()
        # Add "Constraint" for three points
        num1 = point_num[index][0]
        num2 = point_num[index][1]
        if num1 % 16 < num2 % 16:
            num1, num2 = num2, num1
        for j, num in enumerate([center_num[index], num1, num2]):
            writer.constraint_point(writer.constraint_num, p3[j], num)
            writer.constraint_num += 1
        # Add "Constraint" for diameter
        if index == 0:
            writer.constraint_diameter(writer.constraint_num, circles[-1],
                                       radius * 2)
        else:
            writer.constraint_equal_radius(writer.constraint_num, circles[-1],
                                           circles[0])
        writer.constraint_num += 1
        # Add "Constraint" for become tangent line
        for j, num in enumerate((num1 - num1 % 16, num2 - num2 % 16)):
            writer.constraint_arc_line_tangent(
                writer.constraint_num,
                circles[-1],
                num,
                reverse=(j == 1)
            )
            writer.constraint_num += 1

    for i, (x, y) in enumerate(centers):
        add_circle(i, x, y)
    circles.clear()
    for i in range(len(boundary)):
        x, y = centers[i]
        add_arc(i, x, y)
    # Write file
    writer.save(file_name)
