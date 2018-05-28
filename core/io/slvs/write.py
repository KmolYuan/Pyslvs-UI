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


def _shift16(num: int) -> int:
    """Left shift with 16 bit.
    
    Usage:
    >>> a = 0x20009
    >>> hex(_shift16(a))
    '0x30000'
    """
    ten = 1 << 16
    return num + ten - (num % ten)


class SlvsWriter:
    
    """Use to save data with solvespace file format."""
    
    def __init__(self, *,
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
        self.entity_normal_3d_wxyz(0x30020, 0x30001, reversed=True)
        
        self.constraint_num = 0x1
        self.script_constraint = []
    
    def set_group(self, num: int):
        """Set the group number."""
        self.__group = num
    
    def set_comment_group(self, num: int):
        """Set the comment group number."""
        self.__comment_group = num
    
    def set_workplane(self, num: int):
        """Set main workplane."""
        self.__workplane = num
    
    def param_shift16(self):
        """Shift param counting."""
        self.param_num = _shift16(self.param_num)
    
    def entity_shift16(self):
        """Shift entity counting."""
        self.entity_num = _shift16(self.entity_num)
    
    def save_slvs(self, file_name: str):
        """Save the file."""
        self.entity_plane(0x80020000, 0x80020002, 0x80020001)
        self.entity_normal_copy(0x80020001, 0x80020002)
        self.entity_point_2d(0x80020002, 2012, 1)
        with open(file_name, 'w', encoding="iso-8859-15") as f:
            f.write('\n\n'.join('\n\n'.join(script) for script in [
                self.script_group,
                self.script_param,
                self.script_request,
                self.script_entity,
                self.script_constraint,
            ]) + '\n\n')
    
    def group_origin(self, num: int = 1, name: str = "#references"):
        """First group called "#references"."""
        self.script_group.append('\n'.join([
            "Group.h.v={:08x}".format(num),
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
        ]))
    
    def group_normal(self, num: int, name: str):
        """A normal group."""
        self.script_group.append('\n'.join([
            "Group.h.v={:08x}".format(num),
            "Group.type={}".format(5001),
            "Group.order=1",
            "Group.name={}".format(name),
            "Group.activeWorkplane.v={:08x}".format(self.__workplane),
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
        ]))
    
    def param(self, num: int) -> str:
        """A no value parameter."""
        self.script_param.append('\n'.join([
            "Param.h.v.={:08x}".format(num),
            "AddParam",
        ]))
    
    def param_val(self, num: int, val: float):
        """A value parameter."""
        self.script_param.append('\n'.join([
            "Param.h.v.={:08x}".format(num),
            "Param.val={:.20f}".format(val),
            "AddParam",
        ]))
    
    def request(self, num: int, type: int):
        """A request for an entity."""
        self.script_request.append('\n'.join([
            "Request.h.v={:08x}".format(num),
            "Request.type={}".format(type),
            "Request.workplane.v={:08x}".format(self.__workplane),
            "Request.group.v={:08x}".format(self.__group),
            "Request.construction=0",
            "AddRequest",
        ]))
    
    def request_workplane(self, num: int):
        """Workplane request."""
        self.script_request.append('\n'.join([
            "Request.h.v={:08x}".format(num),
            "Request.type={}".format(100),
            "Request.group.v={:08x}".format(0x1),
            "Request.construction=0",
            "AddRequest",
        ]))
    
    def request_line(self, num: int):
        """Line segment request."""
        self.request(num, 200)
    
    def request_arc(self, num: int):
        """Arc request."""
        self.request(num, 500)
    
    def request_circle(self, num: int):
        """Circle request."""
        self.request(num, 400)
    
    def entity_plane(self, num: int, origin: int, normal: int):
        """A workplane."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(10000),
            "Entity.construction=0",
            "Entity.point[0].v={:08x}".format(origin),
            "Entity.normal.v={:08x}".format(normal),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_point(self, num: int):
        """A independent point."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(2000),
            "Entity.construction=0",
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_normal(self, num: int, p: int, type: int):
        """A 3D normal."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(type),
            "Entity.construction=0",
            "Entity.point[0].v={:08x}".format(p),
            "Entity.actNormal.w={:.020f}".format(1),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_normal_3d(self, num: int, p: int):
        """A 3D normal."""
        self.entity_normal(num, p, 3000)
    
    def entity_normal_3d_wxyz(self, num: int, p: int, *, reversed: bool = False):
        """A 3D normal from quaternion."""
        unit = 0.5
        self.script_entity.append('\n'.join([
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
        ]))
    
    def entity_normal_2d(self, num: int, p: int):
        """A 2D normal."""
        unit = 1
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(3001),
            "Entity.construction=0",
            "Entity.point[0].v={:08x}".format(p),
            "Entity.workplane.v={:08x}".format(self.__workplane),
            "Entity.actNormal.w={:.020f}".format(unit),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_normal_copy(self, num: int, p: int):
        """A copied normal."""
        self.entity_normal(num, p, 3010)
    
    def entity_point_2d(self, num: int, x: float, y: float):
        """A point related with the entity."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(2001),
            "Entity.construction=0",
            "Entity.workplane.v={:08x}".format(self.__workplane),
            "Entity.actPoint.x={:.20f}".format(x),
            "Entity.actPoint.y={:.20f}".format(y),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_line(self, num: int):
        """A line segment."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(11000),
            "Entity.construction=0",
            "Entity.point[0].v={:08x}".format(num + 1),
            "Entity.point[1].v={:08x}".format(num + 2),
            "Entity.workplane.v={:08x}".format(self.__workplane),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_arc(self, num: int):
        """An arc."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(14000),
            "Entity.construction=0",
            "Entity.point[0].v={:08x}".format(num + 1),
            "Entity.point[1].v={:08x}".format(num + 2),
            "Entity.point[2].v={:08x}".format(num + 3),
            "Entity.normal.v={:08x}".format(num + 0x20),
            "Entity.workplane.v={:08x}".format(self.__workplane),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_circle(self, num: int):
        """A circle."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(13000),
            "Entity.construction=0",
            "Entity.point[0].v={:08x}".format(num + 1),
            "Entity.normal.v={:08x}".format(num + 0x20),
            "Entity.distance.v={:08x}".format(num + 0x40),
            "Entity.workplane.v={:08x}".format(self.__workplane),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def entity_distance(self, num: int, val: float):
        """A distance entity."""
        self.script_entity.append('\n'.join([
            "Entity.h.v={:08x}".format(num),
            "Entity.type={}".format(4000),
            "Entity.construction=0",
            "Entity.workplane.v={:08x}".format(self.__workplane),
            "Entity.actDistance={:.20f}".format(val),
            "Entity.actVisible=1",
            "AddEntity",
        ]))
    
    def constraint_point(self, num: int, p1: int, p2: int):
        """Constraint two points as same one."""
        self.script_constraint.append('\n'.join([
            "Constraint.h.v={:08x}".format(num),
            "Constraint.type={}".format(20),
            "Constraint.group.v={:08x}".format(self.__group),
            "Constraint.workplane.v={:08x}".format(self.__workplane),
            "Constraint.ptA.v={:08x}".format(p1),
            "Constraint.ptB.v={:08x}".format(p2),
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            "AddConstraint",
        ]))

    def constraint_fix(self,
        num: int,
        p0: int,
        x: float,
        y: float,
        *,
        offset: int = 10
    ):
        """Constraint two distance between two workplane."""
        
        def constraint_fix_hv(num: int, phv: int, val: float):
            """Constraint a distance from a point to a plane."""
            self.script_constraint.append('\n'.join([
                "Constraint.h.v={:08x}".format(num),
                "Constraint.type={}".format(31),
                "Constraint.group.v={:08x}".format(self.__group),
                "Constraint.workplane.v={:08x}".format(self.__workplane),
                "Constraint.valA={:.20f}".format(val),
                "Constraint.ptA.v={:08x}".format(p0),
                "Constraint.entityA.v={:08x}".format(phv),
                "Constraint.other=0",
                "Constraint.other2=0",
                "Constraint.reference=0",
                "Constraint.disp.offset.x={:.20f}".format(offset),
                "Constraint.disp.offset.y={:.20f}".format(offset),
                "AddConstraint",
            ]))
        
        constraint_fix_hv(num, 0x30000, y)
        constraint_fix_hv(num + 1, 0x20000, x)
    
    def constraint_distence(self,
        num: int,
        p1: int,
        p2: int,
        leng: float,
        *,
        offset: int = 10
    ):
        """Constraint the distance of line segment."""
        self.script_constraint.append('\n'.join([
            "Constraint.h.v={:08x}".format(num),
            "Constraint.type={}".format(30),
            "Constraint.group.v={:08x}".format(self.__group),
            "Constraint.workplane.v={:08x}".format(self.__workplane),
            "Constraint.valA={:.20f}".format(leng),
            "Constraint.ptA.v={:08x}".format(p1),
            "Constraint.ptB.v={:08x}".format(p2),
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            "Constraint.disp.offset.x={:.20f}".format(offset),
            "Constraint.disp.offset.y={:.20f}".format(offset),
            "AddConstraint",
        ]))
    
    def constraint_angle(self,
        num: int,
        l1: int,
        l2: int,
        angle: float,
        *,
        offset: int = 10
    ):
        """Constraint the angle between two line segments."""
        self.script_constraint.append('\n'.join([
            "Constraint.h.v={:08x}".format(num),
            "Constraint.type={}".format(120),
            "Constraint.group.v={:08x}".format(self.__group),
            "Constraint.workplane.v={:08x}".format(self.__workplane),
            "Constraint.valA={:.20f}".format(angle),
            "Constraint.ptA.v={:08x}".format(l1),
            "Constraint.ptB.v={:08x}".format(l2),
            "Constraint.other=1",
            "Constraint.other2=0",
            "Constraint.reference=0",
            "Constraint.disp.offset.x={:.20f}".format(offset),
            "Constraint.disp.offset.y={:.20f}".format(offset),
            "AddConstraint",
        ]))
    
    def constraint_arc_line_tangent(self,
        num: int,
        e1: int,
        e2: int,
        *,
        reversed: bool = False
    ):
        """Constraint an arc is tangent with a line."""
        self.script_constraint.append('\n'.join([
            "Constraint.h.v={:08x}".format(num),
            "Constraint.type={}".format(123),
            "Constraint.group.v={:08x}".format(self.__group),
            "Constraint.workplane.v={:08x}".format(self.__workplane),
            "Constraint.entityA.v={:08x}".format(e1),
            "Constraint.entityB.v={:08x}".format(e2),
            "Constraint.other={}".format(1 if reversed else 0),
            "Constraint.other2=0",
            "Constraint.reference=0",
            "AddConstraint",
        ]))
    
    def constraint_equal_radius(self, num: int, e1: int, e2: int):
        """Constraint two arcs or circles are be the same radius."""
        self.script_constraint.append('\n'.join([
            "Constraint.h.v={:08x}".format(num),
            "Constraint.type={}".format(130),
            "Constraint.group.v={:08x}".format(self.__group),
            "Constraint.workplane.v={:08x}".format(self.__workplane),
            "Constraint.entityA.v={:08x}".format(e1),
            "Constraint.entityB.v={:08x}".format(e2),
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            "AddConstraint",
        ]))
    
    def constraint_comment(self,
        num: int,
        comment: str,
        x: float,
        y: float,
        *,
        offset: int = 5
    ):
        """Comment in group."""
        self.script_constraint.append('\n'.join([
            "Constraint.h.v={:08x}".format(num),
            "Constraint.type={}".format(1000),
            "Constraint.group.v={:08x}".format(self.__comment_group),
            "Constraint.workplane.v={:08x}".format(self.__workplane),
            "Constraint.other=0",
            "Constraint.other2=0",
            "Constraint.reference=0",
            "Constraint.comment={}".format(comment),
            "Constraint.disp.offset.x={:.20f}".format(x + offset),
            "Constraint.disp.offset.y={:.20f}".format(y + offset),
            "AddConstraint",
        ]))
