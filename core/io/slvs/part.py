# -*- coding: utf-8 -*-

"""Solvespace format output as linkage sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List
from math import (
    radians,
    sin,
    cos,
    atan2,
)
from core.libs import VPoint
from core.graphics import convex_hull
from .write import SlvsWriter


def slvs_part(vpoints: List[VPoint], radius: float, file_name: str):
    """TODO: Generate a linkage sketch by specified radius."""
    #Translate
    min_x = min(vpoint.cx for vpoint in vpoints)
    min_y = min(vpoint.cy for vpoint in vpoints)
    centers = [(vpoint.cx - min_x, vpoint.cy - min_y) for vpoint in vpoints]
    del vpoints
    
    #Boundary
    boundary = convex_hull(centers)
    boundary_tmp = []
    for i in range(len(boundary)):
        p1 = boundary[i]
        p2 = boundary[i + 1 if (i + 1) < len(boundary) else 0]
        alpha = atan2(p2[1] - p1[1], p2[0] - p1[0]) - radians(90)
        offset_x = radius * cos(alpha)
        offset_y = radius * sin(alpha)
        boundary_tmp.append((p1[0] + offset_x, p1[1] + offset_y))
        boundary_tmp.append((p2[0] + offset_x, p2[1] + offset_y))
    boundary = boundary_tmp
    print(boundary)
    
    #Writer object
    writer = SlvsWriter()
    
    #Write file
    writer.save_slvs(file_name)
