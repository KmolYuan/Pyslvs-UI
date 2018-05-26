# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"


def shift16(num: int) -> int:
    """Left shift with 16 bit."""
    ten = 1 << 16
    return num + ten - (num % ten)


def group_origin(n: int = 1, name: str = "#references") -> str:
    """First group called "#references"."""
    return '\n'.join([
        "Group.h.v={:08x}".format(n),
        "Group.type={}".format(5000),
        "Group.name={}".format(name),
        "Group.color=ff000000",
        "Group.skipFirst=0",
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


def group_normal(n: int, name: str) -> str:
    """A normal group."""
    return '\n'.join([
        "Group.h.v={:08x}".format(n),
        "Group.type={}".format(5001),
        "Group.order=1",
        "Group.name={}".format(name),
        "Group.activeWorkplane.v=80020000",
        "Group.color=ff000000",
        "Group.subtype=6000",
        "Group.skipFirst=0",
        "Group.predef.q.w={:.020f}".format(1),
        "Group.predef.origin.v={:08x}".format((1 << 16) + 1),
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


def param(num: int, val: float) -> str:
    """A parameter for point coordinate value."""
    return '\n'.join([
        "Param.h.v.={:08x}".format(num),
        "Param.val={:.20f}".format(val),
        "AddParam",
    ])


def request(num: int, type_num: int) -> str:
    """A request for an entity."""
    return '\n'.join([
        "Request.h.v={:08x}".format(num),
        "Request.type={}".format(type_num),
        "Request.workplane.v=80020000",
        "Request.group.v=00000002",
        "Request.construction=0",
        "AddRequest",
    ])


def request_line(num: int) -> str:
    """Line segment request."""
    return request(num, 200)


def request_arc(num: int) -> str:
    """Arc request."""
    return request(num, 500)


def request_circle(num: int) -> str:
    """Circle request."""
    return request(num, 400)


def entity_plane(num: int, p: int, v: int) -> str:
    """A workplane."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(10000),
        "Entity.construction={}".format(0),
        "Entity.point[0].v={:08x}".format(p),
        "Entity.normal.v={:08x}".format(v),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_point(num: int) -> str:
    """A independent point."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(2000),
        "Entity.construction={}".format(0),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_normal(num: int, p: int, type: int) -> str:
    """A 3D normal."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(type),
        "Entity.construction={}".format(0),
        "Entity.point[0].v={:08x}".format(p),
        "Entity.actNormal.w={:.020f}".format(1),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_normal_w(num: int, p: int) -> str:
    """A 3D normal."""
    return entity_normal(num, p, 3000)


def entity_normal_h(num: int, p: int) -> str:
    """A 3D normal."""
    return entity_normal(num, p, 3010)


def entity_normal_xyz(num: int, p: int, *, reversed: bool = False) -> str:
    """A 3D normal from quaternion."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
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


def entity_line(num: int) -> str:
    """A line segment."""
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


def entity_line_point(num: int, x: float, y: float) -> str:
    """A point on the line segment."""
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


def constraint_point(num: int, p1: int, p2: int) -> str:
    """Constraint two points as same one."""
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


def constraint_fix(
    num: int,
    p0: int,
    x: float,
    y: float,
    *,
    offset: int = 10
) -> str:
    """Constraint two distence of line segment."""
    
    def constraint_fix_hv(num: int, phv: int, val: float) -> str:
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
            "Constraint.disp.offset.x={:.20f}".format(offset),
            "Constraint.disp.offset.y={:.20f}".format(offset),
            "AddConstraint",
        ])
    
    return '\n\n'.join([
        constraint_fix_hv(num, 0x30000, y),
        constraint_fix_hv(num + 1, 0x20000, x)
    ])


def constraint_line(
    num: int,
    p1: int,
    p2: int,
    leng: float,
    *,
    offset: int = 10
) -> str:
    """Constraint the distence of line segment."""
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
        "Constraint.disp.offset.x={:.20f}".format(offset),
        "Constraint.disp.offset.y={:.20f}".format(offset),
        "AddConstraint",
    ])


def constraint_angle(
    num: int,
    l1: int,
    l2: int,
    angle: float,
    *,
    offset: int = 10
) -> str:
    """Constraint the angle between two line segments."""
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
        "Constraint.disp.offset.x={:.20f}".format(offset),
        "Constraint.disp.offset.y={:.20f}".format(offset),
        "AddConstraint",
    ])


def constraint_comment(
    num: int,
    comment: str,
    x: float,
    y: float,
    *,
    offset: int = 5
) -> str:
    """Comment in group."""
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
        "Constraint.type={}".format(1000),
        "Constraint.group.v=00000003",
        "Constraint.workplane.v=80020000",
        "Constraint.other=0",
        "Constraint.other2=0",
        "Constraint.reference=0",
        "Constraint.comment={}".format(comment),
        "Constraint.disp.offset.x={:.20f}".format(x + offset),
        "Constraint.disp.offset.y={:.20f}".format(y + offset),
        "AddConstraint",
    ])
