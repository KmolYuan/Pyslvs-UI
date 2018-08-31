# -*- coding: utf-8 -*-

"""Solvespace format output as linkage sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Sequence,
    List,
    Tuple,
    Iterator,
)
from math import (
    radians,
    sin,
    cos,
    atan2,
)
from core.libs import VPoint, Coordinate
from core.graphics import convex_hull
from .write import SlvsWriter


def boundaryloop(
    boundary: Sequence[Tuple[float, float]],
    radius: float
) -> List[Tuple[Coordinate, Coordinate]]:
    """Create boundary edges by pairs of coordinates."""
    boundary_tmp = []
    for i in range(len(boundary)):
        p1 = Coordinate(*boundary[i])
        p2 = Coordinate(*boundary[i + 1 if (i + 1) < len(boundary) else 0])
        alpha = atan2(p2.y - p1.y, p2.x - p1.x) - radians(90)
        offset_x = radius * cos(alpha)
        offset_y = radius * sin(alpha)
        boundary_tmp.append((
            Coordinate(p1.x + offset_x, p1.y + offset_y),
            Coordinate(p2.x + offset_x, p2.y + offset_y),
        ))
    return boundary_tmp


def slvs_part(vpoints: List[VPoint], radius: float, file_name: str):
    """Generate a linkage sketch by specified radius."""
    # Translate
    min_x = min(vpoint.cx for vpoint in vpoints)
    min_y = min(vpoint.cy for vpoint in vpoints)
    centers = [(vpoint.cx - min_x, vpoint.cy - min_y) for vpoint in vpoints]
    # Synchronous the point coordinates after using convex hull.
    centers_ch = convex_hull(centers)
    boundary = centers_ch.copy()
    for c in centers:
        if c not in centers_ch:
            centers_ch.append(c)
    centers = centers_ch
    del vpoints, min_x, min_y
    
    # Frame (p1, p2, p3) -> ((p1, p2), (p3, p1), (p3, p2))
    frame = [tuple(Coordinate(*c) for c in centers[:2])]
    for c in centers[2:]:
        frame.append((frame[0][0], Coordinate(*c)))
        frame.append((frame[0][1], Coordinate(*c)))
    
    # Boundary
    boundary = boundaryloop(boundary, radius)
    
    # Writer object.
    writer = SlvsWriter()
    writer.script_group.pop()
    writer.group_normal(0x3, "boundary")
    
    # Add "Param".
    def addParam(edges: Tuple[Tuple[Coordinate, Coordinate]]):
        """Add param by pair of coordinates."""
        for edge in edges:
            writer.param_num += 0x10
            for p in edge:
                writer.param_val(writer.param_num, p.x)
                writer.param_num += 1
                writer.param_val(writer.param_num, p.y)
                writer.param_num += 2
            writer.param_shift16()
    
    def arc_coords(
        i: int,
        cx: float,
        cy: float
    ) -> Iterator[Tuple[float, float]]:
        for x, y in (
            (cx, cy),
            (boundary[i-1][1].x, boundary[i-1][1].y),
            (boundary[i][0].x, boundary[i][0].y),
        ):
            yield x, y
    
    addParam(frame)
    addParam(boundary)
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
    # The number of same points.
    point_num = [[] for i in range(point_count)]
    # The number of same lines.
    line_num = [[] for i in range(len(frame))]
    
    def segment_processing(edges: Tuple[Tuple[Coordinate, Coordinate]]):
        """Add edges to workplane. (No any constraint.)"""
        # Add "Request".
        for i in range(len(edges)):
            writer.request_line(writer.request_num)
            writer.request_num += 1
        
        def edges_is_frame() -> Iterator[int]:
            """Number code of frame."""
            yield 0
            yield 1
            k = 2
            while True:
                for i in (0, 1):
                    yield i
                    yield k
                k += 1
        
        def edges_is_boundary() -> Iterator[int]:
            """Number code of boundary."""
            k = 0
            while True:
                yield k
                k += 1
                k %= len(point_num)
                yield k
        
        # Add "Entity".
        if edges is frame:
            p_count = edges_is_frame()
        else:
            p_count = edges_is_boundary()
        del edges_is_boundary, edges_is_frame
        for i, edge in enumerate(edges):
            writer.entity_line(writer.entity_num)
            for j, c in enumerate(edge):
                writer.entity_num += 1
                point_num[next(p_count)].append(writer.entity_num)
                writer.entity_point_2d(writer.entity_num, c.x, c.y)
                line_num[i].append(writer.entity_num)
            writer.entity_shift16()
    
    segment_processing(frame)
    
    center_num = [nums[0] for nums in point_num]
    
    # Add "Constraint".
    # Same point constraint.
    for p in point_num:
        for p_ in p[1:]:
            writer.constraint_point(writer.constraint_num, p[0], p_)
            writer.constraint_num += 1
    for i, (n1, n2) in enumerate(line_num):
        p1, p2 = frame[i]
        writer.constraint_distance(writer.constraint_num, n1, n2, p1.distance(p2))
        writer.constraint_num += 1
    # Add "Constraint" of position.
    for i in range(2):
        c = frame[0][i]
        writer.constraint_fix(writer.constraint_num, point_num[i][0], c.x, c.y)
        if i == 1:
            writer.script_constraint.pop()
            writer.constraint_num += 1
        else:
            writer.constraint_num += 2
    
    # Group 3:
    writer.set_group(0x3)
    
    # The number of same points.
    point_num = [[] for i in range(len(boundary))]
    # The number of same lines.
    line_num = [[] for i in range(len(boundary))]
    # The number of circles.
    circles = []
    
    segment_processing(boundary)
    
    def addCircle(i: int, x: float, y: float):
        """Add circle"""
        # Add "Request"
        writer.request_circle(writer.request_num)
        writer.request_num += 1
        # Add "Entity"
        writer.entity_circle(writer.entity_num)
        circles.append(writer.entity_num)
        writer.entity_num += 1
        writer.entity_point_2d(writer.entity_num, x, y)
        p = writer.entity_num
        # Shift to 0x20
        writer.entity_num += 0x1f
        writer.entity_normal_2d(writer.entity_num, p)
        # Shift to 0x40
        writer.entity_num += 0x20
        writer.entity_distance(writer.entity_num, radius / 2)
        writer.entity_shift16()
        # Add "Constraint" for centers.
        writer.constraint_point(writer.constraint_num, p, center_num[i])
        writer.constraint_num += 1
        # Add "Constraint" for diameter.
        if i == 0:
            writer.constraint_diameter(writer.constraint_num, circles[-1], radius)
        else:
            writer.constraint_equal_radius(writer.constraint_num, circles[-1], circles[0])
        writer.constraint_num += 1
    
    def addArc(i: int, cx: float, cy: float):
        """Add arc"""
        # Add "Request"
        writer.request_arc(writer.request_num)
        writer.request_num += 1
        # Add "Entity"
        writer.entity_arc(writer.entity_num)
        circles.append(writer.entity_num)
        p3 = []
        for x, y in arc_coords(i, cx, cy):
            writer.entity_num += 1
            writer.entity_point_2d(writer.entity_num, x, y)
            p3.append(writer.entity_num)
        writer.entity_num += 0x3d
        writer.entity_normal_2d(writer.entity_num, p3[0])
        writer.entity_shift16()
        # Add "Constraint" for three points.
        num1, num2 = point_num[i]
        if (num1 % 16) < (num2 % 16):
            num1, num2 = num2, num1
        for j, num in enumerate((
            center_num[i],
            num1,
            num2,
        )):
            writer.constraint_point(writer.constraint_num, p3[j], num)
            writer.constraint_num += 1
        # Add "Constraint" for diameter.
        if i == 0:
            writer.constraint_diameter(writer.constraint_num, circles[-1], radius * 2)
        else:
            writer.constraint_equal_radius(writer.constraint_num, circles[-1], circles[0])
        writer.constraint_num += 1
        # Add "Constraint" for become tangent line.
        for i, num in enumerate((num1 - num1 % 16, num2 - num2 % 16)):
            r = i == 1
            writer.constraint_arc_line_tangent(writer.constraint_num, circles[-1], num, reversed=r)
            writer.constraint_num += 1
    
    for i, (x, y) in enumerate(centers):
        addCircle(i, x, y)
    circles.clear()
    for i in range(len(boundary)):
        x, y = centers[i]
        addArc(i, x, y)
    
    # Write file.
    writer.save(file_name)
