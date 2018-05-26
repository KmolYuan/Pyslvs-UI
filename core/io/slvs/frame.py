# -*- coding: utf-8 -*-

"""Solvespace format output as frame sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence, Callable
from core.libs import VPoint
from .write import (
    shift16,
    group_origin,
    group_normal,
    param,
    request_line,
    entity_plane,
    entity_point,
    entity_normal_w,
    entity_normal_h,
    entity_normal_xyz,
    entity_relative_point,
    entity_line,
    constraint_point,
    constraint_fix,
    constraint_distence,
    constraint_comment,
)


def slvs_output(
    VPoints: Sequence[VPoint],
    v_to_slvs: Callable[[], Tuple[int, int]],
    file_name: str
):
    edges = tuple(v_to_slvs())
    script_param = ['\n\n'.join([
        '\n\n'.join("Param.h.v.={:08x}\nAddParam".format(0x10010+n) for n in range(3)),
        "Param.h.v.={:08x}\nParam.val={:.020f}\nAddParam".format(0x10020, 1),
        '\n\n'.join("Param.h.v.={:08x}\nAddParam".format(0x10020+n) for n in range(1, 4)),
        '\n\n'.join("Param.h.v.={:08x}\nAddParam".format(0x20010+n) for n in range(3)),
        '\n\n'.join("Param.h.v.={:08x}\nParam.val={:.020f}\nAddParam".format(0x20020+n, 0.5) for n in range(4)),
        '\n\n'.join("Param.h.v.={:08x}\nAddParam".format(0x30010+n) for n in range(3)),
        '\n\n'.join("Param.h.v.={:08x}\nParam.val={:.020f}\nAddParam".format(0x30020+n, 0.5 if n==0 else -0.5) for n in range(4))
    ])]
    script_request = ['\n\n'.join(
        ("Request.h.v={:08x}\n".format(n) +
        "Request.type=100\n" +
        "Request.group.v=00000001\n" +
        "Request.construction=0\n" +
        "AddRequest") for n in range(1, 4)
    )]
    script_entity = ['\n\n'.join([
        entity_plane(0x10000, 0x10001, 0x10020),
        entity_point(0x10001),
        entity_normal_w(0x10020, 0x10001),
        entity_plane(0x20000, 0x20001, 0x20020),
        entity_point(0x20001),
        entity_normal_xyz(0x20020, 0x20001),
        entity_plane(0x30000, 0x30001, 0x30020),
        entity_point(0x30001),
        entity_normal_xyz(0x30020, 0x30001, reversed=True)
    ])]
    #The number of same points.
    point_num = [[] for i in range(len(VPoints))]
    #The number of same lines.
    line_num = [[] for i in range(len(edges))]
    #Add "Param"
    param_num = 0x40000
    for i, edge in enumerate(edges):
        param_num += 0x10
        for p in edge:
            script_param.append(param(param_num, VPoints[p].cx))
            param_num += 1
            script_param.append(param(param_num, VPoints[p].cy))
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
            script_entity.append(entity_relative_point(entity_num, VPoints[p].cx, VPoints[p].cy))
            line_num[i].append(entity_num)
        entity_num = shift16(entity_num)
    script_entity.append('\n\n'.join([
        entity_plane(0x80020000, 0x80020002, 0x80020001),
        entity_normal_h(0x80020001, 0x80020002),
        entity_relative_point(0x80020002, 2012, 1)
    ]))
    #Add "Constraint"
    script_constraint = []
    constraint_num = 0x1
    #Same point constraint
    for p in point_num:
        for p_ in p[1:]:
            script_constraint.append(constraint_point(constraint_num, p[0], p_))
            constraint_num += 1
    #Position constraint
    for i, vpoint in enumerate(VPoints):
        if "ground" in vpoint.links and point_num[i]:
            script_constraint.append(constraint_fix(constraint_num, point_num[i][0], vpoint.cx, vpoint.cy))
            constraint_num += 2
    #Distance constraint
    for i, (n1, n2) in enumerate(line_num):
        p1, p2 = edges[i]
        script_constraint.append(constraint_distence(constraint_num, n1, n2, VPoints[p1].distance(VPoints[p2])))
        constraint_num += 1
    #Comment constraint
    for i, vpoint in enumerate(VPoints):
        script_constraint.append(constraint_comment(constraint_num, "Point{}".format(i), vpoint.cx, vpoint.cy))
        constraint_num += 1
    #Write file
    with open(file_name, 'w', encoding="iso-8859-15") as f:
        f.write('\n\n'.join('\n\n'.join(script) for script in [
            ['\n\n'.join([
                "±²³SolveSpaceREVa\n",
                group_origin(1, "#references"),
                group_normal(2, "sketch-in-plane"),
                group_normal(3, "comments"),
            ])],
            script_param,
            script_request,
            script_entity,
            script_constraint
        ]) + '\n\n')
