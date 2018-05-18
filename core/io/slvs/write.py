# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence, Callable
from core.libs import VPoint


def _group(n: int, name: str) -> str:
    return '\n'.join([
        "Group.h.v={:08x}".format(n),
        "Group.type=5001",
        "Group.order=1",
        "Group.name={}".format(name),
        "Group.activeWorkplane.v=80020000",
        "Group.color=ff000000",
        "Group.subtype=6000",
        "Group.skipFirst=0",
        "Group.predef.q.w={:.020f}".format(1),
        "Group.predef.origin.v={:08x}".format((1<<16) + 1),
        "Group.predef.swapUV=0",
        "Group.predef.negateU=0",
        "Group.predef.negateV=0",
        "Group.visible=1",
        "Group.suppress=0",
        "Group.relaxConstraints=0",
        "Group.allowRedundant=0",
        "Group.allDimsReference=0",
        "Group.scale={:.020f}".format(1),
        "Group.remap={\n}",
        "AddGroup",
    ])


_script_group = ["""\
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

""" + _group(2, "sketch-in-plane") + '\n\n' + _group(3, "comments")]


def _entity_plane(n: int, p: int, v: int) -> str:
    return '\n'.join([
        "Entity.h.v={:08x}".format(n),
        "Entity.type={}".format(10000),
        "Entity.construction={}".format(0),
        "Entity.point[0].v={:08x}".format(p),
        "Entity.normal.v={:08x}".format(v),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def _entity_point(n: int, t: int = 2000, con: int = 0) -> str:
    return '\n'.join([
        "Entity.h.v={:08x}".format(n),
        "Entity.type={}".format(t),
        "Entity.construction={}".format(con),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def _entity_normal_w(n: int, p: int, t: int = 3000) -> str:
    return '\n'.join([
        "Entity.h.v={:08x}".format(n),
        "Entity.type={}".format(t),
        "Entity.construction={}".format(0),
        "Entity.point[0].v={:08x}".format(p),
        "Entity.actNormal.w={:.020f}".format(1),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def _entity_normal_xyz(n: int, p: int, *, reversed: bool = False) -> str:
    return '\n'.join([
        "Entity.h.v={:08x}".format(n),
        "Entity.type={}".format(3000),
        "Entity.construction={}".format(0),
        "Entity.point[0].v={:08x}".format(p),
        "Entity.actNormal.w={:.020f}".format(0.5),
        "Entity.actNormal.vx={:.020f}".format(-0.5 if reversed else 0.5),
        "Entity.actNormal.vy={:.020f}".format(-0.5 if reversed else 0.5),
        "Entity.actNormal.vz={:.020f}".format(-0.5 if reversed else 0.5),
        "Entity.actVisible=1",
        "AddEntity",
    ])


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
        _entity_plane(0x10000, 0x10001, 0x10020),
        _entity_point(0x10001),
        _entity_normal_w(0x10020, 0x10001),
        _entity_plane(0x20000, 0x20001, 0x20020),
        _entity_point(0x20001),
        _entity_normal_xyz(0x20020, 0x20001),
        _entity_plane(0x30000, 0x30001, 0x30020),
        _entity_point(0x30001),
        _entity_normal_xyz(0x30020, 0x30001, reversed=True)
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
            script_param.append(_Param(param_num, VPoints[p].cx))
            param_num += 1
            script_param.append(_Param(param_num, VPoints[p].cy))
            param_num += 2
        param_num = _up(param_num)
    #Add "Request"
    request_num = 0x4
    for i in range(len(edges)):
        script_request.append(_Request(request_num))
        request_num += 1
    #Add "Entity"
    entity_num = 0x40000
    for i, edge in enumerate(edges):
        script_entity.append(_Entity_line(entity_num))
        for p in edge:
            entity_num += 1
            point_num[p].append(entity_num)
            script_entity.append(_Entity_point(entity_num, VPoints[p].cx, VPoints[p].cy))
            line_num[i].append(entity_num)
        entity_num = _up(entity_num)
    script_entity.append('\n\n'.join([
        _entity_plane(0x80020000, 0x80020002, 0x80020001),
        _entity_normal_w(0x80020001, 0x80020002, 3010),
        _entity_point(0x80020002, 2012, 1)
    ]))
    #Add "Constraint"
    script_constraint = []
    constraint_num = 0x1
    #Same point constraint
    for p in point_num:
        for p_ in p[1:]:
            script_constraint.append(_Constraint_point(constraint_num, p[0], p_))
            constraint_num += 1
    #Position constraint
    for i, vpoint in enumerate(VPoints):
        if "ground" in vpoint.links and point_num[i]:
            script_constraint.append(_Constraint_fix(constraint_num, point_num[i][0], vpoint.cx, vpoint.cy))
            constraint_num += 2
    #Distance constraint
    for i, (n1, n2) in enumerate(line_num):
        p1, p2 = edges[i]
        script_constraint.append(_Constraint_line(constraint_num, n1, n2, VPoints[p1].distance(VPoints[p2])))
        constraint_num += 1
    #Comment constraint
    for i, vpoint in enumerate(VPoints):
        script_constraint.append(_Constraint_comment(constraint_num, "Point{}".format(i), vpoint.cx, vpoint.cy))
        constraint_num += 1
    #Write file
    with open(file_name, 'w', encoding="iso-8859-15") as f:
        f.write('\n\n'.join('\n\n'.join(script) for script in [
            _script_group,
            script_param,
            script_request,
            script_entity,
            script_constraint
        ]) + '\n\n')


def _up(num: int) -> int:
    """Carry 16 bit."""
    ten = 1 << 16
    num += ten
    num -= num % ten
    return num


def _Param(num: int, val: float) -> str:
    return '\n'.join([
        "Param.h.v.={:08x}".format(num),
        "Param.val={:.20f}".format(val),
        "AddParam",
    ])


def _Request(num: int) -> str:
    return '\n'.join([
        "Request.h.v={:08x}".format(num),
        "Request.type=200",
        "Request.workplane.v=80020000",
        "Request.group.v=00000002",
        "Request.construction=0",
        "AddRequest",
    ])


def _Entity_line(num: int) -> str:
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(11000),
        "Entity.construction={}".format(0),
        "Entity.point[0].v={:08x}".format(num+1),
        "Entity.point[1].v={:08x}".format(num+2),
        "Entity.workplane.v=80020000",
        "Entity.actVisible=1",
        "AddEntity",
    ])


def _Entity_point(num: int, x: float, y: float) -> str:
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(2001),
        "Entity.construction={}".format(0),
        "Entity.workplane.v=80020000",
        "Entity.actPoint.x={:.20f}".format(x),
        "Entity.actPoint.y={:.20f}".format(y),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def _Constraint_point(num: int, p1: int, p2: int) -> str:
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
        "Constraint.type={}".format(20),
        "Constraint.group.v=00000002",
        "Constraint.workplane.v=80020000",
        "Constraint.ptA.v={:08x}".format(p1),
        "Constraint.ptB.v={:08x}".format(p2),
        "Constraint.other=0",
        "Constraint.other2=0",
        "Constraint.reference=0",
        "AddConstraint",
    ])


def _Constraint_fix(num: int, p0: int, x: float, y: float) -> str:
    
    def _Constraint_fix_hv(num: int, p0: int, phv: int, val: float) -> str:
        return '\n'.join([
            "Constraint.h.v={:08x}".format(num),
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
            "AddConstraint",
        ])
    
    return (
        _Constraint_fix_hv(num, p0, 0x30000, y) + '\n\n' +
        _Constraint_fix_hv(num+1, p0, 0x20000, x)
    )


def _Constraint_line(num: int, p1: int, p2: int, leng: float) -> str:
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
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
        "AddConstraint",
    ])


def _Constraint_angle(num: int, l1: int, l2: int, angle: float) -> str:
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
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
        "AddConstraint",
    ])


def _Constraint_comment(num: int, comment: str, x: float, y: float) -> str:
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
        "Constraint.type={}".format(1000),
        "Constraint.group.v=00000003",
        "Constraint.workplane.v=80020000",
        "Constraint.other=0",
        "Constraint.other2=0",
        "Constraint.reference=0",
        "Constraint.comment={}".format(comment),
        "Constraint.disp.offset.x={:.20f}".format(x),
        "Constraint.disp.offset.y={:.20f}".format(y),
        "AddConstraint",
    ])
