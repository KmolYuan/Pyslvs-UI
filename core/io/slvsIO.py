# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.libs import VPoint, VLink
from typing import Tuple, Sequence, Callable

script_group = ['''\
±²³SolveSpaceREVa


Group.h.v=00000001
Group.type=5000
Group.name=#references
Group.color=ff000000
Group.skipFirst=0
Group.predef.swapUV=0
Group.predef.negateU=0
Group.predef.negateV=0
Group.visible=1
Group.suppress=0
Group.relaxConstraints=0
Group.allowRedundant=0
Group.allDimsReference=0
Group.scale=1.00000000000000000000
Group.remap={
}
AddGroup

Group.h.v=00000002
Group.type=5001
Group.order=1
Group.name=sketch-in-plane
Group.activeWorkplane.v=80020000
Group.color=ff000000
Group.subtype=6000
Group.skipFirst=0
Group.predef.q.w=1.00000000000000000000
Group.predef.origin.v=00010001
Group.predef.swapUV=0
Group.predef.negateU=0
Group.predef.negateV=0
Group.visible=1
Group.suppress=0
Group.relaxConstraints=0
Group.allowRedundant=0
Group.allDimsReference=0
Group.scale=1.00000000000000000000
Group.remap={
}
AddGroup''']

entity_plane = lambda n, p, v, : '\n'.join([
    "Entity.h.v={:08x}".format(n),
    "Entity.type={}".format(10000),
    "Entity.construction={}".format(0),
    "Entity.point[0].v={:08x}".format(p),
    "Entity.normal.v={:08x}".format(v),
    "Entity.actVisible=1",
    "AddEntity"
])

entity_point = lambda n, t=2000, con=0: '\n'.join([
    "Entity.h.v={:08x}".format(n),
    "Entity.type={}".format(t),
    "Entity.construction={}".format(con),
    "Entity.actVisible=1",
    "AddEntity"
])

entity_normal_w = lambda n, p, t=3000: '\n'.join([
    "Entity.h.v={:08x}".format(n),
    "Entity.type={}".format(t),
    "Entity.construction={}".format(0),
    "Entity.point[0].v={:08x}".format(p),
    "Entity.actNormal.w={:.020f}".format(1),
    "Entity.actVisible=1",
    "AddEntity"
])

entity_normal_xyz = lambda n, p, reversed=False: '\n'.join([
    "Entity.h.v={:08x}".format(n),
    "Entity.type={}".format(3000),
    "Entity.construction={}".format(0),
    "Entity.point[0].v={:08x}".format(p),
    "Entity.actNormal.w={:.020f}".format(0.5),
    "Entity.actNormal.vx={:.020f}".format(-0.5 if reversed else 0.5),
    "Entity.actNormal.vy={:.020f}".format(-0.5 if reversed else 0.5),
    "Entity.actNormal.vz={:.020f}".format(-0.5 if reversed else 0.5),
    "Entity.actVisible=1",
    "AddEntity"
])

def slvs2D(
    VPoints: Sequence[VPoint],
    VLinks: Sequence[VLink],
    v_to_slvs: Callable[[], Tuple[int, int]],
    fileName: str
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
        "Request.h.v={:08x}\nRequest.type=100\nRequest.group.v=00000001\nRequest.construction=0\nAddRequest".format(n) for n in range(1, 4)
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
        entity_normal_xyz(0x30020, 0x30001, True)
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
            script_param.append(Param(param_num, VPoints[p].cx))
            param_num += 1
            script_param.append(Param(param_num, VPoints[p].cy))
            param_num += 2
        param_num = up(param_num, 4)
    #Add "Request"
    request_num = 0x4
    for i in range(len(edges)):
        script_request.append(Request(request_num))
        request_num += 1
    #Add "Entity"
    entity_num = 0x40000
    for i, edge in enumerate(edges):
        script_entity.append(Entity_line(entity_num))
        for p in edge:
            entity_num += 1
            point_num[p].append(entity_num)
            script_entity.append(Entity_point(entity_num, VPoints[p].cx, VPoints[p].cy))
            line_num[i].append(entity_num)
        entity_num = up(entity_num, 4)
    script_entity.append('\n\n'.join([
        entity_plane(0x80020000, 0x80020002, 0x80020001),
        entity_normal_w(0x80020001, 0x80020002, 3010),
        entity_point(0x80020002, 2012, 1)
    ]))
    #Add "Constraint"
    script_constraint = []
    constraint_num = 0x1
    #Same point constraint
    for p in point_num:
        for p_ in p[1:]:
            script_constraint.append(Constraint_point(constraint_num, p[0], p_))
            constraint_num += 1
    #Position constraint
    for i, vpoint in enumerate(VPoints):
        if "ground" in vpoint.links and point_num[i]:
            script_constraint.append(Constraint_fix(constraint_num, point_num[i][0], vpoint.cx, vpoint.cy))
            constraint_num += 2
    #Distance constraint
    for i, (n1, n2) in enumerate(line_num):
        p1, p2 = edges[i]
        script_constraint.append(Constraint_line(constraint_num, n1, n2, VPoints[p1].distance(VPoints[p2])))
        constraint_num += 1
    #Comment constraint
    for i, vpoint in enumerate(VPoints):
        script_constraint.append(Constraint_comment(constraint_num, "Point{}".format(i), vpoint.cx, vpoint.cy))
        constraint_num += 1
    #Write file
    with open(fileName, 'w', encoding="iso-8859-15") as f:
        f.write('\n\n'.join('\n\n'.join(script) for script in [
            script_group,
            script_param,
            script_request,
            script_entity,
            script_constraint
        ]) + '\n\n')

def up(num, digit):
    ten = 0x10**digit
    num += ten
    num -= num%ten
    return num

Param = lambda num, val: '\n'.join([
    "Param.h.v.={:08x}".format(num),
    "Param.val={:.20f}".format(val),
    "AddParam"
])

Request = lambda num: '\n'.join([
    "Request.h.v={:08x}".format(num),
    "Request.type=200",
    "Request.workplane.v=80020000",
    "Request.group.v=00000002",
    "Request.construction=0",
    "AddRequest"
])

Entity_line = lambda num: '\n'.join([
    "Entity.h.v={:08x}".format(num),
    "Entity.type={}".format(11000),
    "Entity.construction={}".format(0),
    "Entity.point[0].v={:08x}".format(num+1),
    "Entity.point[1].v={:08x}".format(num+2),
    "Entity.workplane.v=80020000",
    "Entity.actVisible=1",
    "AddEntity"
])

Entity_point = lambda num, x, y: '\n'.join([
    "Entity.h.v={:08x}".format(num),
    "Entity.type={}".format(2001),
    "Entity.construction={}".format(0),
    "Entity.workplane.v=80020000",
    "Entity.actPoint.x={:.20f}".format(x),
    "Entity.actPoint.y={:.20f}".format(y),
    "Entity.actVisible=1",
    "AddEntity"
])

Constraint_point = lambda num, p1, p2: '\n'.join([
    "Constraint.h.v={0:08x}".format(num),
    "Constraint.type={}".format(20),
    "Constraint.group.v=00000002",
    "Constraint.workplane.v=80020000",
    "Constraint.ptA.v={:08x}".format(p1),
    "Constraint.ptB.v={:08x}".format(p2),
    "Constraint.other=0",
    "Constraint.other2=0",
    "Constraint.reference=0",
    "AddConstraint"
])

Constraint_fix = lambda num, p0, x, y: Constraint_fix_hv(num, p0, 0x30000, y) +'\n\n'+ Constraint_fix_hv(num+1, p0, 0x20000, x)

Constraint_fix_hv = lambda num, p0, phv, val: '\n'.join([
    "Constraint.h.v={0:08x}".format(num),
    "Constraint.type={}".format(31),
    "Constraint.group.v=00000002",
    "Constraint.workplane.v=80020000",
    "Constraint.valA={:.20f}".format(val),
    "Constraint.ptA.v={:08x}".format(p0),
    "Constraint.entityA.v={:08x}".format(phv),
    "Constraint.other=0",
    "Constraint.other2=0",
    "Constraint.reference=0",
    "Constraint.disp.offset.x={:.20f}".format(10),
    "Constraint.disp.offset.y={:.20f}".format(10),
    "AddConstraint"
])

Constraint_line = lambda num, p1, p2, leng: '\n'.join([
    "Constraint.h.v={0:08x}".format(num),
    "Constraint.type={}".format(30),
    "Constraint.group.v=00000002",
    "Constraint.workplane.v=80020000",
    "Constraint.valA={:.20f}".format(leng),
    "Constraint.ptA.v={:08x}".format(p1),
    "Constraint.ptB.v={:08x}".format(p2),
    "Constraint.other=0",
    "Constraint.other2=0",
    "Constraint.reference=0",
    "Constraint.disp.offset.x={:.20f}".format(10),
    "Constraint.disp.offset.y={:.20f}".format(10),
    "AddConstraint"
])

Constraint_angle = lambda num, l1, l2, angle: '\n'.join([
    "Constraint.h.v={0:08x}".format(num),
    "Constraint.type={}".format(120),
    "Constraint.group.v=00000002",
    "Constraint.workplane.v=80020000",
    "Constraint.valA={:.20f}".format(angle),
    "Constraint.ptA.v={:08x}".format(l1),
    "Constraint.ptB.v={:08x}".format(l2),
    "Constraint.other=1",
    "Constraint.other2=0",
    "Constraint.reference=0",
    "Constraint.disp.offset.x={:.20f}".format(10),
    "Constraint.disp.offset.y={:.20f}".format(10),
    "AddConstraint"
])

Constraint_comment = lambda num, comment, x, y: '\n'.join([
    "Constraint.h.v={:08x}".format(num),
    "Constraint.type={}".format(1000),
    "Constraint.group.v=00000002",
    "Constraint.workplane.v=80020000",
    "Constraint.other=0",
    "Constraint.other2=0",
    "Constraint.reference=0",
    "Constraint.comment={}".format(comment),
    "Constraint.disp.offset.x={:.20f}".format(x),
    "Constraint.disp.offset.y={:.20f}".format(y),
    "AddConstraint"
])
