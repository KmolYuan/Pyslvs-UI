# -*- coding: utf-8 -*-

"""Solvespace format output function.

This module are use a workplane and two groups for sketching and placing
comments.
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
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List


def _shift16(num: int) -> int:
    """Left shift with 16 bit.

    Usage:
    >>> hex(_shift16(0x20009))
    0x30000
    """
    ten = 1 << 16
    return num + ten - (num % ten)


class SlvsWriter2:
    """Use to save data with solvespace file format."""
    script_param: List[str]
    script_request: List[str]
    script_entity: List[str]
    script_constraint: List[str]

    def __init__(
        self,
        *,
        group: int = 0x2,
        comment_group: int = 0x3,
        workplane: int = 0x80020000
    ):
        """Initialize the settings and collections."""
        self.__group = group
        self.__comment_group = comment_group
        self.__workplane = workplane

        self.script_group = ["±²³SolveSpaceREVa\n"]
        self.group_origin(0x1)
        self.group_normal(0x2, "sketch-in-plane")
        self.group_normal(0x3, "comments")

        self.param_num = 0x40000
        self.script_param = []
        for n in range(3):
            self.param(0x10010 + n)
        self.param_val(0x10020, 1)
        for n in range(1, 4):
            self.param(0x10020 + n)
        for n in range(3):
            self.param(0x20010 + n)
        for n in range(4):
            self.param_val(0x20020 + n, 0.5)
        for n in range(3):
            self.param(0x30010 + n)
        for n in range(4):
            self.param_val(0x30020 + n, 0.5 if (n == 0) else -0.5)

        self.request_num = 0x4
        self.script_request = []
        for n in range(1, 4):
            self.request_workplane(n)

        self.entity_num = 0x40000
        self.script_entity = []
        self.entity_plane(0x10000, 0x10001, 0x10020)
        self.entity_point(0x10001)
        self.entity_normal_3d(0x10020, 0x10001)
        self.entity_plane(0x20000, 0x20001, 0x20020)
        self.entity_point(0x20001)
        self.entity_normal_3d_wxyz(0x20020, 0x20001)
        self.entity_plane(0x30000, 0x30001, 0x30020)
        self.entity_point(0x30001)
        self.entity_normal_3d_wxyz(0x30020, 0x30001, reverse=True)

        self.constraint_num = 0x1
        self.script_constraint = []

    def set_group(self, num: int) -> None:
        """Set the group number."""
        self.__group = num

    def set_comment_group(self, num: int) -> None:
        """Set the comment group number."""
        self.__comment_group = num

    def set_workplane(self, num: int) -> None:
        """Set main workplane."""
        self.__workplane = num

    def param_shift16(self) -> None:
        """Shift param counting."""
        self.param_num = _shift16(self.param_num)

    def entity_shift16(self) -> None:
        """Shift entity counting."""
        self.entity_num = _shift16(self.entity_num)

    def group_origin(self, num: int = 1, name: str = "#references") -> None:
        """First group called "#references"."""
        self.script_group.append('\n'.join([
            f"Group.h.v={num:08x}",
            f"Group.type={5000}",
            f"Group.name={name}",
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
        ]))

    def group_normal(self, num: int, name: str) -> None:
        """A normal group."""
        self.script_group.append('\n'.join([
            f"Group.h.v={num:08x}",
            f"Group.type={5001}",
            "Group.order=1",
            f"Group.name={name}",
            f"Group.activeWorkplane.v={self.__workplane:08x}",
            "Group.color=ff000000",
            "Group.subtype=6000",
            "Group.skipFirst=0",
            f"Group.predef.q.w={1:.020f}",
            f"Group.predef.origin.v={(1 << 16) + 1:08x}",
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
        ]))

    def param(self, num: int) -> None:
        """A no value parameter."""
        self.script_param.append('\n'.join((
            f"Param.h.v.={num:08x}",
            "AddParam",
        )))

    def param_val(self, num: int, val: float) -> None:
        """A value parameter."""
        self.script_param.append('\n'.join([
            f"Param.h.v.={num:08x}",
            f"Param.val={val:.20f}",
            "AddParam",
        ]))

    def request(self, num: int, type_i: int) -> None:
        """A request for an entity."""
        self.script_request.append('\n'.join([
            f"Request.h.v={num:08x}",
            f"Request.type={type_i}",
            f"Request.workplane.v={self.__workplane:08x}",
            f"Request.group.v={self.__group:08x}",
            "Request.construction=0",
            "AddRequest",
        ]))

    def request_workplane(self, num: int) -> None:
        """Workplane request."""
        self.script_request.append('\n'.join([
            f"Request.h.v={num:08x}",
            f"Request.type={100}",
            f"Request.group.v={1:08x}",
            "Request.construction=0",
            "AddRequest",
        ]))

    def request_line(self, num: int) -> None:
        """Line segment request."""
        self.request(num, 200)

    def request_arc(self, num: int) -> None:
        """Arc request."""
        self.request(num, 500)

    def request_circle(self, num: int) -> None:
        """Circle request."""
        self.request(num, 400)

    def entity_plane(self, num: int, origin: int, normal: int) -> None:
        """A workplane."""
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={10000}",
            "Entity.construction=0",
            f"Entity.point[0].v={origin:08x}",
            f"Entity.normal.v={normal:08x}",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_point(self, num: int) -> None:
        """A independent point."""
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={2000}",
            "Entity.construction=0",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_normal(self, num: int, p: int, type_i: int) -> None:
        """A 3D normal."""
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={type_i}",
            "Entity.construction=0",
            f"Entity.point[0].v={p:08x}",
            f"Entity.actNormal.w={1:.020f}",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_normal_3d(self, num: int, p: int) -> None:
        """A 3D normal."""
        self.entity_normal(num, p, 3000)

    def entity_normal_3d_wxyz(self, num: int, p: int, *,
                              reverse: bool = False) -> None:
        """A 3D normal from quaternion."""
        unit = -0.5 if reverse else 0.5
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={3000}",
            "Entity.construction=0",
            f"Entity.point[0].v={p:08x}",
            f"Entity.actNormal.w={0.5:.020f}",
            f"Entity.actNormal.vx={unit:.020f}",
            f"Entity.actNormal.vy={unit:.020f}",
            f"Entity.actNormal.vz={unit:.020f}",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_normal_2d(self, num: int, p: int) -> None:
        """A 2D normal."""
        unit = 1
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={3001}",
            "Entity.construction=0",
            f"Entity.point[0].v={p:08x}",
            f"Entity.workplane.v={self.__workplane:08x}",
            f"Entity.actNormal.w={unit:.020f}",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_normal_copy(self, num: int, p: int) -> None:
        """A copied normal."""
        self.entity_normal(num, p, 3010)

    def __2d_point_line(self, t: int, num: int, p1: str, p2: str) -> None:
        """Used for 2D point and line creation."""
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={t}",
            "Entity.construction=0",
            f"Entity.workplane.v={self.__workplane:08x}",
            p1, p2,
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_point_2d(self, num: int, x: float, y: float) -> None:
        """A point related with the entity."""
        self.__2d_point_line(2001, num,
                             f"Entity.actPoint.x={x:.20f}",
                             f"Entity.actPoint.y={y:.20f}")

    def entity_line(self, num: int) -> None:
        """A line segment."""
        self.__2d_point_line(11000, num,
                             f"Entity.point[0].v={num + 1:08x}",
                             f"Entity.point[1].v={num + 2:08x}")

    def entity_arc(self, num: int) -> None:
        """An arc."""
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={14000}",
            "Entity.construction=0",
            f"Entity.point[0].v={num + 1:08x}",
            f"Entity.point[1].v={num + 2:08x}",
            f"Entity.point[2].v={num + 3:08x}",
            f"Entity.normal.v={num + 0x20:08x}",
            f"Entity.workplane.v={self.__workplane:08x}",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_circle(self, num: int) -> None:
        """A circle."""
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={13000}",
            "Entity.construction=0",
            f"Entity.point[0].v={num + 1:08x}",
            f"Entity.normal.v={num + 0x20:08x}",
            f"Entity.distance.v={num + 0x40:08x}",
            f"Entity.workplane.v={self.__workplane:08x}",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def entity_distance(self, num: int, val: float) -> None:
        """A distance entity."""
        self.script_entity.append('\n'.join([
            f"Entity.h.v={num:08x}",
            f"Entity.type={4000}",
            "Entity.construction=0",
            f"Entity.workplane.v={self.__workplane:08x}",
            f"Entity.actDistance={val:.20f}",
            "Entity.actVisible=1",
            "AddEntity",
        ]))

    def __cons_point_radius(self, t: int, num: int, e1: str, e2: str) -> None:
        """Used for point / radius equally constrain creation."""
        self.script_constraint.append('\n'.join([
            f"Constraint.h.v={num:08x}",
            f"Constraint.type={t}",
            f"Constraint.group.v={self.__group:08x}",
            f"Constraint.workplane.v={self.__workplane:08x}",
            e1, e2,
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            "AddConstraint",
        ]))

    def constraint_point(self, num: int, p1: int, p2: int) -> None:
        """Constraint two points as same one."""
        self.__cons_point_radius(20, num,
                                 f"Constraint.ptA.v={p1:08x}",
                                 f"Constraint.ptB.v={p2:08x}")

    def constraint_equal_radius(self, num: int, e1: int, e2: int) -> None:
        """Constraint two arcs or circles are be the same radius."""
        self.__cons_point_radius(130, num,
                                 f"Constraint.entityA.v={e1:08x}",
                                 f"Constraint.entityB.v={e2:08x}")

    def constraint_grounded(
        self,
        num: int,
        p0: int,
        x: float,
        y: float,
        *,
        offset: int = 10
    ):
        """Constraint two distance between two workplane."""

        def constraint_fix_hv(n: int, phv: int, val: float) -> None:
            """Constraint a distance from a point to a plane."""
            self.script_constraint.append('\n'.join([
                f"Constraint.h.v={n:08x}",
                f"Constraint.type={31}",
                f"Constraint.group.v={self.__group:08x}",
                f"Constraint.workplane.v={self.__workplane:08x}",
                f"Constraint.valA={val:.20f}",
                f"Constraint.ptA.v={p0:08x}",
                f"Constraint.entityA.v={phv:08x}",
                "Constraint.other=0",
                "Constraint.other2=0",
                "Constraint.reference=0",
                f"Constraint.disp.offset.x={offset:.20f}",
                f"Constraint.disp.offset.y={offset:.20f}",
                "AddConstraint",
            ]))

        constraint_fix_hv(num, 0x30000, y)
        constraint_fix_hv(num + 1, 0x20000, x)

    def __cons_val(self, t: int, num: int, a: int, b: int, val: float, *,
                   offset: float = 10) -> None:
        """Used for valued constrain creation."""
        self.script_constraint.append('\n'.join([
            f"Constraint.h.v={num:08x}",
            f"Constraint.type={t}",
            f"Constraint.group.v={self.__group:08x}",
            f"Constraint.workplane.v={self.__workplane:08x}",
            f"Constraint.valA={val:.20f}",
            f"Constraint.ptA.v={a:08x}",
            f"Constraint.ptB.v={b:08x}",
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            f"Constraint.disp.offset.x={offset:.20f}",
            f"Constraint.disp.offset.y={offset:.20f}",
            "AddConstraint",
        ]))

    def constraint_distance(self, num: int, p1: int, p2: int, length: float, *,
                            offset: float = 10):
        """Constraint the distance of line segment."""
        self.__cons_val(30, num, p1, p2, length, offset=offset)

    def constraint_angle(self, num: int, l1: int, l2: int, angle: float, *,
                         offset: float = 10):
        """Constraint the angle between two line segments."""
        self.__cons_val(120, num, l1, l2, angle, offset=offset)

    def constraint_diameter(
        self,
        num: int,
        e1: int,
        val: float,
        *,
        offset: float = -1
    ):
        """Constraint the diameter of a circle."""
        if offset < 0:
            offset = val / 2
        self.script_constraint.append('\n'.join([
            f"Constraint.h.v={num:08x}",
            f"Constraint.type={90}",
            f"Constraint.group.v={self.__group:08x}",
            f"Constraint.workplane.v={self.__workplane:08x}",
            f"Constraint.valA={val:.20f}",
            f"Constraint.entityA.v={e1:08x}",
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            f"Constraint.disp.offset.x={offset:.20f}",
            f"Constraint.disp.offset.y={offset:.20f}",
            "AddConstraint",
        ]))

    def constraint_arc_line_tangent(
        self,
        num: int,
        e1: int,
        e2: int,
        *,
        reverse: bool = False
    ):
        """Constraint an arc is tangent with a line."""
        self.script_constraint.append('\n'.join([
            f"Constraint.h.v={num:08x}",
            f"Constraint.type={123}",
            f"Constraint.group.v={self.__group:08x}",
            f"Constraint.workplane.v={self.__workplane:08x}",
            f"Constraint.entityA.v={e1:08x}",
            f"Constraint.entityB.v={e2:08x}",
            f"Constraint.other={1 if reverse else 0}",
            "Constraint.other2=0",
            "Constraint.reference=0",
            "AddConstraint",
        ]))

    def constraint_comment(
        self,
        num: int,
        comment: str,
        x: float,
        y: float,
        *,
        offset: int = 5
    ):
        """Comment in group."""
        self.script_constraint.append('\n'.join([
            f"Constraint.h.v={num:08x}",
            f"Constraint.type={1000}",
            f"Constraint.group.v={self.__comment_group:08x}",
            f"Constraint.workplane.v={self.__workplane:08x}",
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            f"Constraint.comment={comment}",
            f"Constraint.disp.offset.x={x + offset:.20f}",
            f"Constraint.disp.offset.y={y + offset:.20f}",
            "AddConstraint",
        ]))

    def save(self, file_name: str) -> None:
        """Save the file."""
        self.entity_plane(0x80020000, 0x80020002, 0x80020001)
        self.entity_normal_copy(0x80020001, 0x80020002)
        self.entity_point_2d(0x80020002, 2012, 1)
        with open(file_name, 'w+', encoding="iso-8859-15") as f:
            f.write('\n\n'.join('\n\n'.join(script) for script in [
                self.script_group,
                self.script_param,
                self.script_request,
                self.script_entity,
                self.script_constraint,
            ]) + '\n\n')
