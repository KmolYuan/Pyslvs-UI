# -*- coding: utf-8 -*-

"""Solvespace format output as linkage sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Tuple
from math import (
    radians,
    sin,
    cos,
    atan2,
)
from core.libs import VPoint, Coordinate
from core.graphics import convex_hull
from .write import SlvsWriter


def slvs_part(vpoints: List[VPoint], radius: float, file_name: str):
    """Generate a linkage sketch by specified radius."""
    #Translate
    min_x = min(vpoint.cx for vpoint in vpoints)
    min_y = min(vpoint.cy for vpoint in vpoints)
    centers = [(vpoint.cx - min_x, vpoint.cy - min_y) for vpoint in vpoints]
    del vpoints, min_x, min_y
    
    #Frame (p1, p2, p3) -> ((p1, p2), (p3, p1), (p3, p2))
    if len(centers) > 2:
        frame = [tuple(centers[:2])]
        for c in centers[2:]:
            frame.append((c, centers[0]))
            frame.append((c, centers[1]))
    else:
        frame = [tuple(centers)]
    
    #Boundary
    boundary = convex_hull(centers)
    boundary_tmp = []
    for i in range(len(boundary)):
        p1 = Coordinate(boundary[i])
        p2 = Coordinate(boundary[i + 1 if (i + 1) < len(boundary) else 0])
        alpha = atan2(p2.y - p1.y, p2.x - p1.x) - radians(90)
        offset_x = radius * cos(alpha)
        offset_y = radius * sin(alpha)
        boundary_tmp.append((
            (p1.x + offset_x, p1.y + offset_y),
            (p2.x + offset_x, p2.y + offset_y)
        ))
    boundary = boundary_tmp
    
    #Writer object
    writer = SlvsWriter()
    writer.script_group.pop()
    writer.group_normal(0x3, "boundary")
    
    #Add "Param"
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
    
    addParam(frame)
    addParam(boundary)
    
    #Group 2:
    
    #The number of same points.
    point_num = [[] for i in range(len(frame)*2)]
    #The number of same lines.
    line_num = [[] for i in range(len(frame))]
    
    def segment_processing(edges: Tuple[Tuple[Coordinate, Coordinate]]):
        """TODO: Add edges to workplane."""
        #Add "Request"
        for i in range(len(edges)):
            writer.request_line(writer.request_num)
            writer.request_num += 1
        
        #Add "Entity"
        for i, edge in enumerate(edges):
            writer.entity_line(writer.entity_num)
            for j, c in enumerate(edge):
                writer.entity_num += 1
                point_num[j].append(writer.entity_num)
                writer.entity_point_2d(writer.entity_num, c.x, c.y)
                line_num[i].append(writer.entity_num)
            writer.entity_shift16()
        
        #Add "Constraint"
        for p in point_num:
            for p_ in p[1:]:
                writer.constraint_point(writer.constraint_num, p[0], p_)
                writer.constraint_num += 1
        for i, (n1, n2) in enumerate(line_num):
            p1, p2 = edges[i]
            writer.constraint_distence(writer.constraint_num, n1, n2, p1.distance(p2))
            writer.constraint_num += 1
    
    segment_processing(frame)
    
    #Group 3:
    writer.set_group(0x3)
    
    #The number of same points.
    point_num = [[] for i in range(len(boundary)*2)]
    #The number of same lines.
    line_num = [[] for i in range(len(boundary))]
    
    segment_processing(boundary)
    
    #Write file
    writer.save_slvs(file_name)
