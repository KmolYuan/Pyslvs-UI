# -*- coding: utf-8 -*-

"""Solvespace format output as frame sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, List, Callable
from core.libs import VPoint
from .write import (
    shift16,
    param_val,
    request_line,
    entity_plane,
    entity_normal_2d,
    entity_relative_point,
    entity_line,
    constraint_point,
    constraint_fix,
    constraint_distence,
    constraint_comment,
    header_group,
    header_param,
    header_request,
    header_entity,
    save_slvs,
)


def slvs_frame(
    vpoints: List[VPoint],
    v_to_slvs: Callable[[], Tuple[int, int]],
    file_name: str
):
    """Generate frame sketch, ignore all points that was no any connection."""
    edges = tuple(v_to_slvs())
    
    #File headers of default framework.
    script_param = header_param()
    script_request = header_request()
    script_entity = header_entity()
    script_constraint = []
    
    #The number of same points.
    point_num = [[] for i in range(len(vpoints))]
    
    #The number of same lines.
    line_num = [[] for i in range(len(edges))]
    
    #Add "Param"
    param_num = 0x40000
    for i, edge in enumerate(edges):
        param_num += 0x10
        for p in edge:
            script_param.append(param_val(param_num, vpoints[p].cx))
            param_num += 1
            script_param.append(param_val(param_num, vpoints[p].cy))
            param_num += 2
        param_num = shift16(param_num)
    
    #Add "Request"
    request_num = 0x4
    for i in range(len(edges)):
        script_request.append(request_line(request_num))
        request_num += 1
    
    #Add "Entity"
    entity_num = 0x40000
    for i, edge in enumerate(edges):
        script_entity.append(entity_line(entity_num))
        for p in edge:
            entity_num += 1
            point_num[p].append(entity_num)
            script_entity.append(entity_relative_point(entity_num, vpoints[p].cx, vpoints[p].cy))
            line_num[i].append(entity_num)
        entity_num = shift16(entity_num)
    script_entity.append('\n\n'.join([
        entity_plane(0x80020000, 0x80020002, 0x80020001),
        entity_normal_2d(0x80020001, 0x80020002),
        entity_relative_point(0x80020002, 2012, 1)
    ]))
    
    #Add "Constraint"
    constraint_num = 0x1
    #Same point constraint
    for p in point_num:
        for p_ in p[1:]:
            script_constraint.append(constraint_point(constraint_num, p[0], p_))
            constraint_num += 1
    #Position constraint
    for i, vpoint in enumerate(vpoints):
        if "ground" in vpoint.links and point_num[i]:
            script_constraint.append(constraint_fix(constraint_num, point_num[i][0], vpoint.cx, vpoint.cy))
            constraint_num += 2
    #Distance constraint
    for i, (n1, n2) in enumerate(line_num):
        p1, p2 = edges[i]
        script_constraint.append(constraint_distence(constraint_num, n1, n2, vpoints[p1].distance(vpoints[p2])))
        constraint_num += 1
    #Comment constraint
    for i, vpoint in enumerate(vpoints):
        script_constraint.append(constraint_comment(constraint_num, "Point{}".format(i), vpoint.cx, vpoint.cy))
        constraint_num += 1
    
    #Write file
    save_slvs(
        file_name,
        header_group(),
        script_param,
        script_request,
        script_entity,
        script_constraint
    )
