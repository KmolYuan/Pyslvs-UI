# -*- coding: utf-8 -*-

"""Solvespace format output function.

This module are use a workplane and two groups for sketching and placing comments.
But the number codes can decide by functions.
The number code is all hexadecimal.

Here is the type codes of Solvespace (from "sketch.h"):

class EntityBase {
public:
    enum class Type : uint32_t {
        POINT_IN_3D            =  2000,
        POINT_IN_2D            =  2001,
        POINT_N_TRANS          =  2010,
        POINT_N_ROT_TRANS      =  2011,
        POINT_N_COPY           =  2012,
        POINT_N_ROT_AA         =  2013,

        NORMAL_IN_3D           =  3000,
        NORMAL_IN_2D           =  3001,
        NORMAL_N_COPY          =  3010,
        NORMAL_N_ROT           =  3011,
        NORMAL_N_ROT_AA        =  3012,

        DISTANCE               =  4000,
        DISTANCE_N_COPY        =  4001,

        FACE_NORMAL_PT         =  5000,
        FACE_XPROD             =  5001,
        FACE_N_ROT_TRANS       =  5002,
        FACE_N_TRANS           =  5003,
        FACE_N_ROT_AA          =  5004,

        WORKPLANE              = 10000,
        LINE_SEGMENT           = 11000,
        CUBIC                  = 12000,
        CUBIC_PERIODIC         = 12001,
        CIRCLE                 = 13000,
        ARC_OF_CIRCLE          = 14000,
        TTF_TEXT               = 15000,
        IMAGE                  = 16000
    };
}

class ConstraintBase {
public:
    enum class Type : uint32_t {
        POINTS_COINCIDENT      =  20,
        PT_PT_DISTANCE         =  30,
        PT_PLANE_DISTANCE      =  31,
        PT_LINE_DISTANCE       =  32,
        PT_FACE_DISTANCE       =  33,
        PROJ_PT_DISTANCE       =  34,
        PT_IN_PLANE            =  41,
        PT_ON_LINE             =  42,
        PT_ON_FACE             =  43,
        EQUAL_LENGTH_LINES     =  50,
        LENGTH_RATIO           =  51,
        EQ_LEN_PT_LINE_D       =  52,
        EQ_PT_LN_DISTANCES     =  53,
        EQUAL_ANGLE            =  54,
        EQUAL_LINE_ARC_LEN     =  55,
        LENGTH_DIFFERENCE      =  56,
        SYMMETRIC              =  60,
        SYMMETRIC_HORIZ        =  61,
        SYMMETRIC_VERT         =  62,
        SYMMETRIC_LINE         =  63,
        AT_MIDPOINT            =  70,
        HORIZONTAL             =  80,
        VERTICAL               =  81,
        DIAMETER               =  90,
        PT_ON_CIRCLE           = 100,
        SAME_ORIENTATION       = 110,
        ANGLE                  = 120,
        PARALLEL               = 121,
        PERPENDICULAR          = 122,
        ARC_LINE_TANGENT       = 123,
        CUBIC_LINE_TANGENT     = 124,
        CURVE_CURVE_TANGENT    = 125,
        EQUAL_RADIUS           = 130,
        WHERE_DRAGGED          = 200,

        COMMENT                = 1000
    };
}
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List

_group = 0x2
_comment_group = 0x3
_workplane = 0x80020000


def shift16(num: int) -> int:
    """Left shift with 16 bit.
    
    Usage:
    >>> a = 0x20009
    >>> hex(shift16(a))
    '0x30000'
    """
    ten = 1 << 16
    return num + ten - (num % ten)


def set_group(num: int):
    """Set the group number."""
    global _group
    _group = num


def set_comment_group(num: int):
    """Set the comment group number."""
    global _comment_group
    _comment_group = num


def set_workplane(num: int):
    """Set main workplane."""
    global _workplane
    _workplane = num


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
        "Group.activeWorkplane.v={:08x}".format(_workplane),
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
        "Group.remap={\n}",
        "AddGroup",
    ])


def param(num: int) -> str:
    """A no value parameter."""
    return '\n'.join([
        "Param.h.v.={:08x}".format(num),
        "AddParam",
    ])


def param_val(num: int, val: float) -> str:
    """A value parameter."""
    return '\n'.join([
        "Param.h.v.={:08x}".format(num),
        "Param.val={:.20f}".format(val),
        "AddParam",
    ])


def request(num: int, type: int) -> str:
    """A request for an entity."""
    return '\n'.join([
        "Request.h.v={:08x}".format(num),
        "Request.type={}".format(type),
        "Request.workplane.v={:08x}".format(_workplane),
        "Request.group.v={:08x}".format(_group),
        "Request.construction=0",
        "AddRequest",
    ])


def request_workplane(num: int) -> str:
    """Workplane request."""
    return '\n'.join([
        "Request.h.v={:08x}".format(num),
        "Request.type={}".format(100),
        "Request.group.v={:08x}".format(0x1),
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


def entity_plane(num: int, origin: int, normal: int) -> str:
    """A workplane."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(10000),
        "Entity.construction=0",
        "Entity.point[0].v={:08x}".format(origin),
        "Entity.normal.v={:08x}".format(normal),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_point(num: int) -> str:
    """A independent point."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(2000),
        "Entity.construction=0",
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_normal(num: int, p: int, type: int) -> str:
    """A 3D normal."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(type),
        "Entity.construction=0",
        "Entity.point[0].v={:08x}".format(p),
        "Entity.actNormal.w={:.020f}".format(1),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_normal_3d(num: int, p: int) -> str:
    """A 3D normal."""
    return entity_normal(num, p, 3000)


def entity_normal_2d(num: int, p: int) -> str:
    """A 2D normal."""
    return entity_normal(num, p, 3010)


def entity_normal_xyz(num: int, p: int, *, reversed: bool = False) -> str:
    """A 3D normal from quaternion."""
    unit = 0.5
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(3000),
        "Entity.construction=0",
        "Entity.point[0].v={:08x}".format(p),
        "Entity.actNormal.w={:.020f}".format(unit),
        "Entity.actNormal.vx={:.020f}".format(-unit if reversed else unit),
        "Entity.actNormal.vy={:.020f}".format(-unit if reversed else unit),
        "Entity.actNormal.vz={:.020f}".format(-unit if reversed else unit),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_relative_point(num: int, x: float, y: float) -> str:
    """A point related with the entity."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(2001),
        "Entity.construction=0",
        "Entity.workplane.v={:08x}".format(_workplane),
        "Entity.actPoint.x={:.20f}".format(x),
        "Entity.actPoint.y={:.20f}".format(y),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_line(num: int) -> str:
    """A line segment."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(11000),
        "Entity.construction=0",
        "Entity.point[0].v={:08x}".format(num + 1),
        "Entity.point[1].v={:08x}".format(num + 2),
        "Entity.workplane.v={:08x}".format(_workplane),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_arc(num: int) -> str:
    """An arc."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(14000),
        "Entity.construction=0",
        "Entity.point[0].v={:08x}".format(num + 1),
        "Entity.point[1].v={:08x}".format(num + 2),
        "Entity.point[2].v={:08x}".format(num + 3),
        "Entity.normal.v={:08x}".format(num + 0x20),
        "Entity.workplane.v={:08x}".format(_workplane),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_circle(num: int) -> str:
    """A circle."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(13000),
        "Entity.construction=0",
        "Entity.point[0].v={:08x}".format(num + 1),
        "Entity.normal.v={:08x}".format(num + 0x20),
        "Entity.distance.v={:08x}".format(num + 0x40),
        "Entity.workplane.v={:08x}".format(_workplane),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def entity_distance(num: int, val: float) -> str:
    """A distance entity."""
    return '\n'.join([
        "Entity.h.v={:08x}".format(num),
        "Entity.type={}".format(4000),
        "Entity.construction=0",
        "Entity.workplane.v={:08x}".format(_workplane),
        "Entity.actDistance={:.20f}".format(val),
        "Entity.actVisible=1",
        "AddEntity",
    ])


def constraint_point(num: int, p1: int, p2: int) -> str:
    """Constraint two points as same one."""
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
        "Constraint.type={}".format(20),
        "Constraint.group.v={:08x}".format(_group),
        "Constraint.workplane.v={:08x}".format(_workplane),
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
    """Constraint two distance between two workplane."""
    
    def constraint_fix_hv(num: int, phv: int, val: float) -> str:
        """Constraint a distance from a point to a plane."""
        return '\n'.join([
            "Constraint.h.v={:08x}".format(num),
            "Constraint.type={}".format(31),
            "Constraint.group.v={:08x}".format(_group),
            "Constraint.workplane.v={:08x}".format(_workplane),
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


def constraint_distence(
    num: int,
    p1: int,
    p2: int,
    leng: float,
    *,
    offset: int = 10
) -> str:
    """Constraint the distance of line segment."""
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
        "Constraint.type={}".format(30),
        "Constraint.group.v={:08x}".format(_group),
        "Constraint.workplane.v={:08x}".format(_workplane),
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
        "Constraint.group.v={:08x}".format(_group),
        "Constraint.workplane.v={:08x}".format(_workplane),
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


def constraint_arc_line_tangent(
    num: int,
    e1: int,
    e2: int,
    *,
    reversed: bool = False
) -> str:
    """Constraint an arc is tangent with a line."""
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
        "Constraint.type={}".format(123),
        "Constraint.group.v={:08x}".format(_comment_group),
        "Constraint.workplane.v={:08x}".format(_workplane),
        "Constraint.entityA.v={:08x}".format(e1),
        "Constraint.entityB.v={:08x}".format(e2),
        "Constraint.other={}".format(1 if reversed else 0),
        "Constraint.other2=0",
        "Constraint.reference=0",
        "AddConstraint",
    ])


def constraint_equal_radius(num: int, e1: int, e2: int) -> str:
    """Constraint two arcs or circles are be the same radius."""
    return '\n'.join([
        "Constraint.h.v={:08x}".format(num),
        "Constraint.type={}".format(130),
        "Constraint.group.v={:08x}".format(_comment_group),
        "Constraint.workplane.v={:08x}".format(_workplane),
        "Constraint.entityA.v={:08x}".format(e1),
        "Constraint.entityB.v={:08x}".format(e2),
        "Constraint.other=0",
        "Constraint.other2=0",
        "Constraint.reference=0",
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
        "Constraint.group.v={:08x}".format(_comment_group),
        "Constraint.workplane.v={:08x}".format(_workplane),
        "Constraint.other=0",
        "Constraint.other2=0",
        "Constraint.reference=0",
        "Constraint.comment={}".format(comment),
        "Constraint.disp.offset.x={:.20f}".format(x + offset),
        "Constraint.disp.offset.y={:.20f}".format(y + offset),
        "AddConstraint",
    ])


def first_line() -> str:
    """File first line."""
    return "±²³SolveSpaceREVa\n"


def header_group() -> List[str]:
    """Standard group settings."""
    return [
        first_line(),
        group_origin(1, "#references"),
        group_normal(2, "sketch-in-plane"),
        group_normal(3, "comments"),
    ]


def header_param() -> List[str]:
    """Standard param settings."""
    return [
        '\n\n'.join(param(0x10010 + n) for n in range(3)),
        param_val(0x10020, 1),
        '\n\n'.join(param(0x10020 + n) for n in range(1, 4)),
        '\n\n'.join(param(0x20010 + n) for n in range(3)),
        '\n\n'.join(param_val(0x20020 + n, 0.5) for n in range(4)),
        '\n\n'.join(param(0x30010 + n) for n in range(3)),
        '\n\n'.join(param_val(0x30020 + n, 0.5 if (n == 0) else -0.5) for n in range(4))
    ]


def header_request() -> List[str]:
    """Standard request settings."""
    return [request_workplane(n) for n in range(1, 4)]


def header_entity() -> List[str]:
    """Standard entity settings."""
    return [
        entity_plane(0x10000, 0x10001, 0x10020),
        entity_point(0x10001),
        entity_normal_3d(0x10020, 0x10001),
        entity_plane(0x20000, 0x20001, 0x20020),
        entity_point(0x20001),
        entity_normal_xyz(0x20020, 0x20001),
        entity_plane(0x30000, 0x30001, 0x30020),
        entity_point(0x30001),
        entity_normal_xyz(0x30020, 0x30001, reversed=True)
    ]


def save_slvs(
    file_name: str,
    script_group: List[str],
    script_param: List[str],
    script_request: List[str],
    script_entity: List[str],
    script_constraint: List[str]
):
    """Save the file."""
    with open(file_name, 'w', encoding="iso-8859-15") as f:
        f.write('\n\n'.join('\n\n'.join(script) for script in [
            script_group,
            script_param,
            script_request,
            script_entity,
            script_constraint,
        ]) + '\n\n')


def save_empty_slvs(file_name: str):
    """Save an empty file."""
    save_slvs(
        file_name,
        header_group(),
        header_param(),
        header_request(),
        header_entity(),
        []
    )
