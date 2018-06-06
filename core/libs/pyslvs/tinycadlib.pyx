# -*- coding: utf-8 -*-
#cython: language_level=3

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    Sequence,
    Dict,
    Union,
)
from cpython cimport bool
from libc.math cimport (
    sqrt,
    sin,
    cos,
    atan2,
    hypot,
)
import numpy as np
cimport numpy as np


cdef double nan = float('nan')


cdef inline double distance(double x1, double y1, double x2, double y2):
    """Distance of two cartesian coordinates."""
    return hypot(x2 - x1, y2 - y1)


cdef class VPoint:
    
    """Symbol of joints."""
    
    def __cinit__(self,
        links: str,
        type_int: int,
        angle: double,
        color_str: str,
        x: double,
        y: double,
        color_func: object = None
    ):
        cdef list tmp_list = []
        cdef str name
        links = links.replace(" ", '')
        for name in links.split(','):
            if not name:
                continue
            tmp_list.append(name)
        self.links = tuple(tmp_list)
        self.type = type_int
        self.typeSTR = ('R', 'P', 'RP')[type_int]
        self.angle = angle
        self.colorSTR = color_str
        if color_func:
            self.color = color_func(color_str)
        self.x = x
        self.y = y
        self.c = np.ndarray(2, dtype=np.object)
        if (self.type == 1) or (self.type == 2):
            """Slider current coordinates.
            
            + [0]: Current node on slot.
            + [1]: Pin.
            """
            self.c[0] = (self.x, self.y)
            self.c[1] = (self.x, self.y)
        else:
            self.c[0] = (self.x, self.y)
    
    @property
    def cx(self):
        """X value of frist current coordinate."""
        return self.c[0][0]
    
    @property
    def cy(self):
        """Y value of frist current coordinate."""
        return self.c[0][1]
    
    cpdef void move(self, tuple c1, tuple c2 = None):
        """Change coordinates of this point."""
        self.c[0] = c1
        if self.type != 0:
            self.c[1] = c2 if c2 else c1
    
    cpdef void rotate(self, double angle):
        """Change the angle of slider slot by degrees."""
        self.angle = angle % 180
    
    cpdef double distance(self, VPoint p):
        """Distance between two VPoint."""
        return distance(self.x, self.y, p.x, p.y)
    
    cpdef double slopeAngle(self, VPoint p, int num1 = 2, int num2 = 2):
        """Angle between horizontal line and two point.
        
        num1: me.
        num2: other side.
        [0]: base (slot) link.
        [1]: pin link.
        """
        cdef double x1, y1, x2, y2
        if num1 > 1:
            x2, y2 = self.x, self.y
        else:
            x2, y2 = self.c[num2]
        if num2 > 1:
            x1, y1 = p.x, p.y
        else:
            x1, y1 = p.c[num2]
        return np.rad2deg(atan2(y1 - y2, x1 - x2))
    
    cpdef bool grounded(self):
        """Return True if the joint is connect with the ground."""
        return 'ground' in self.links
    
    @property
    def expr(self):
        """Expression."""
        return "J[{}, color[{}], P[{}], L[{}]]".format(
            "{}, A[{}]".format(self.typeSTR, self.angle)
            if self.typeSTR != 'R' else 'R',
            self.colorSTR,
            "{}, {}".format(self.x, self.y),
            ", ".join(l for l in self.links)
        )
    
    def __getitem__(self, i: int) -> float:
        """Get coordinate like this:
        
        x, y = VPoint(10, 20)
        """
        if self.type == 0:
            return self.c[0][i]
        else:
            return self.c[1][i]
    
    def __repr__(self):
        """Use to generate script."""
        return "VPoint({p.links}, {p.type}, {p.angle}, {p.c})".format(p=self)


cdef class VLink:
    
    """Symbol of linkages."""
    
    cdef readonly str name, colorSTR
    cdef readonly object color
    cdef readonly tuple points
    
    def __cinit__(self,
        str name,
        str color_str,
        tuple points,
        object color_func = None
    ):
        self.name = name
        self.colorSTR = color_str
        if color_func:
            self.color = color_func(color_str)
        self.points = points
    
    def __contains__(self, point: int):
        """Check if point number is in the link."""
        return point in self.points
    
    def __repr__(self):
        """Use to generate script."""
        return "VLink('{l.name}', {l.points}, colorQt)".format(l=self)


cdef class Coordinate:
    
    """A class to store the coordinate."""
    
    def __cinit__(self, double x, double y):
        self.x = x
        self.y = y
    
    cpdef double distance(self, Coordinate p):
        """Distance."""
        return distance(self.x, self.y, p.x, p.y)
    
    def isnan(self):
        """Test this coordinate is a error-occured answer."""
        return np.isnan(self.x)
    
    def __repr__(self):
        """Debug printing."""
        return "Coordinate({p.x:.02f}, {p.y:.02f})".format(p=self)


cpdef tuple PLAP(
    Coordinate A,
    double L0,
    double a0,
    Coordinate B = None,
    bool inverse = False
):
    """Point on circle by angle."""
    cdef double a1 = atan2(B.y - A.y, B.x - A.x) if B else 0
    if inverse:
        return (A.x + L0*cos(a1 - a0), A.y + L0*sin(a1 - a0))
    else:
        return (A.x + L0*cos(a1 + a0), A.y + L0*sin(a1 + a0))


cpdef tuple PLLP(
    Coordinate A,
    double L0,
    double L1,
    Coordinate B,
    bool inverse = False
):
    """Two intersection points of two circles."""
    cdef double dx = B.x - A.x
    cdef double dy = B.y - A.y
    cdef double d = A.distance(B)
    
    #No solutions, the circles are separate.
    if d > L0 + L1:
        return (nan, nan)
    
    #No solutions because one circle is contained within the other.
    if d < abs(L0 - L1):
        return (nan, nan)
    
    #Circles are coincident and there are an infinite number of solutions.
    if (d == 0) and (L0 == L1):
        return (nan, nan)
    cdef double a = (L0*L0 - L1*L1 + d*d)/(2*d)
    cdef double h = sqrt(L0*L0 - a*a)
    cdef double xm = A.x + a*dx/d
    cdef double ym = A.y + a*dy/d
    
    if inverse:
        return (xm + h*dy/d, ym - h*dx/d)
    else:
        return (xm - h*dy/d, ym + h*dx/d)


cpdef tuple PLPP(
    Coordinate A,
    double L0,
    Coordinate B,
    Coordinate C,
    bool inverse = False
):
    """Two intersection points of a line and a circle."""
    cdef double line_mag = B.distance(C)
    cdef double dx = C.x - B.x
    cdef double dy = C.y - B.y
    cdef double u = ((A.x - B.x)*dx + (A.y - B.y)*dy) / (line_mag*line_mag)
    cdef Coordinate I = Coordinate(B.x + u*dx, B.y + u*dy)
    
    #Test distance between point A and intersection.
    cdef double d = A.distance(I)
    if d > L0:
        #No intersection.
        return (nan, nan)
    elif d == L0:
        #One intersection point.
        return (I.x, I.y)
    
    #Two intersection points.
    d = sqrt(L0*L0 - d*d) / line_mag
    if inverse:
        return (I.x - dx*d, I.y - dy*d)
    else:
        return (I.x + dx*d, I.y + dy*d)


cpdef tuple PXY(Coordinate A, double x, double y):
    """Using relative cartesian coordinate to get solution."""
    return (A.x + x, A.y + y)


cdef inline bool legal_crank(Coordinate A, Coordinate B, Coordinate C, Coordinate D):
    """
    verify the fourbar is satisfied the Gruebler's Equation, s + g <= p + q
        C - D
        |   |
        A   B
    """
    cdef double driver = A.distance(C)
    cdef double follower = B.distance(D)
    cdef double ground = A.distance(B)
    cdef double connector = C.distance(D)
    return (
        (driver + connector <= ground + follower) or
        (driver + ground <= connector + follower)
    )


cdef inline str strbetween(str s, str front, str back):
    """Get the string that is inside of parenthesis."""
    return s[s.find(front)+1:s.find(back)]

cdef inline str strbefore(str s, str front):
    """Get the string that is front of parenthesis."""
    return s[:s.find(front)]


cpdef void expr_parser(str exprs, dict data_dict):
    """Use to generate path data.
    
    exprs: "PLAP[P0,L0,a0,P1](P2);PLLP[P2,L1,L2,P1](P3);..."
    data_dict: {'a0':0., 'L1':10., 'A':(30., 40.), ...}
    """
    #Remove all the spaces in the expression.
    exprs = exprs.replace(" ", '')
    cdef str expr, f, name
    cdef list params
    cdef object p
    cdef list args
    for expr in exprs.split(';'):
        #If the mechanism has no any solution.
        if not expr:
            return
        f = strbefore(expr, '[')
        params = strbetween(expr, '[', ']').split(',')
        target = strbetween(expr, '(', ')')
        args = []
        for name in params:
            if name == 'T':
                p = True
            elif name == 'F':
                p = False
            else:
                p = data_dict[name]
            if type(p) == tuple:
                args.append(Coordinate(*p))
            else:
                args.append(p)
        if f == 'PLAP':
            data_dict[target] = PLAP(*args)
        elif f == 'PLLP':
            data_dict[target] = PLLP(*args)
        elif f == 'PLPP':
            data_dict[target] = PLPP(*args)
        elif f == 'PXY':
            data_dict[target] = PXY(*args)
    """'data_dict' has been updated."""


cdef inline double tuple_distance(tuple c1, tuple c2):
    """Calculate the distance between two tuple coordinates."""
    return distance(c1[0], c1[1], c2[0], c2[1])


cdef inline void rotate_collect(dict data_dict, dict mapping, list path):
    """Collecting."""
    cdef int n
    cdef str m
    for n, m in mapping.items():
        path[n].append(data_dict[m])


cdef inline void rotate(
    int input_angle,
    str expr_str,
    dict data_dict,
    dict mapping,
    list path,
    double interval,
    bool reverse=False
):
    """Add path coordinates.
    
    + Rotate the input joints.
    + Collect the coordinates of all joints.
    """
    cdef str param = 'a{}'.format(input_angle)
    cdef double a = 0
    if reverse:
        a = 360
        interval = -interval
    cdef dict copy_dict
    while 0 <= a <= 360:
        data_dict[param] = np.deg2rad(a)
        copy_dict = data_dict.copy()
        expr_parser(expr_str, copy_dict)
        rotate_collect(copy_dict, mapping, path)
        a += interval


cdef inline list return_path(
    str expr_str,
    dict data_dict,
    dict mapping,
    int dof,
    double interval
):
    """Return as paths."""
    cdef int i
    cdef list path = [[] for i in range(len(mapping))]
    #For each input joint.
    for i in range(dof):
        rotate(i, expr_str, data_dict, mapping, path, interval)
    if dof > 1:
        #Rotate back.
        for i in range(dof):
            rotate(i, expr_str, data_dict, mapping, path, interval, True)
    """
    return_path: [[each_joints]: [(x0, y0), (x1, y1), (x2, y2), ...], ...]
    """
    for i in range(len(path)):
        if len(set(path[i])) <= 1:
            path[i] = ()
        else:
            path[i] = tuple(path[i])
    return path


cdef inline str expr_join(object exprs):
    """Use to append a list of symbols into a string."""
    return ';'.join([
        "{}[{}]({})".format(expr[0], ','.join(expr[1:-1]), expr[-1])
        for expr in exprs
    ])


cdef inline int base_friend(int node, object vpoints):
    cdef int i
    cdef VPoint vpoint
    for i, vpoint in enumerate(vpoints):
        if not vpoints[node].links:
            continue
        if vpoints[node].links[0] in vpoint.links:
            return i


def data_collecting(
    exprs: Sequence[Tuple[str]],
    mapping: Dict[int, str],
    vpoints: Sequence[VPoint]
) -> Tuple[Dict[str, Union[Tuple[float, float], float]], int]:
    """Python wrapper of c version function."""
    return data_collecting_c(exprs, mapping, vpoints)


cdef inline tuple data_collecting_c(object exprs, dict mapping, object vpoints_):
    """Input data:
    
    + exprs: [('PLAP', 'P0', 'L0', 'a0', 'P1', 'P2'), ...]
    + mapping: {0: 'P0', 1: 'P2', 2: 'P3', 3: 'P4', ...}
        + Specify linkage length: mapping['L0'] = 20.0
    + vpoints_: [VPoint0, VPoint1, VPoint2, ...]
    + pos: [(x0, y0), (x1, y1), (x2, y2), ...]
    
    vpoints will make a copy that we don't want to modified itself.
    """
    cdef list vpoints = list(vpoints_)
    
    """First, we create a "VLinks" that can help us to
    find a releationship just like adjacency matrix.
    """
    cdef int node
    cdef str link
    cdef VPoint vpoint
    cdef dict vlinks = {}
    for node, vpoint in enumerate(vpoints):
        for link in vpoint.links:
            #Add as vlink.
            if link not in vlinks:
                vlinks[link] = {node}
            else:
                vlinks[link].add(node)
    
    """Replace the P joints and their friends with RP joint.
    
    DOF must be same after properties changed.
    """
    cdef int base
    cdef str link_
    cdef VPoint vpoint_
    cdef set links
    for base in range(len(vpoints)):
        vpoint = vpoints[base]
        if vpoint.type != 1:
            continue
        for link in vpoint.links[1:]:
            links = set()
            for node in vlinks[link]:
                vpoint_ = vpoints[node]
                if (node == base) or (vpoint_.type != 0):
                    continue
                links.update(vpoint_.links)
                vpoints[node] = VPoint(
                    ",".join([vpoint.links[0]] + [
                        link_ for link_ in vpoint_.links
                        if (link_ not in vpoint.links)
                    ]),
                    2,
                    vpoint.angle,
                    vpoint_.colorSTR,
                    vpoint_.cx,
                    vpoint_.cy
                )
    
    cdef k, v
    #Reverse mapping, exclude specified linkage length.
    cdef dict mapping_r = {
        v: k
        for k, v in mapping.items() if (type(k) == int)
    }
    
    cdef list pos = []
    for vpoint in vpoints:
        if vpoint.type == 0:
            pos.append(vpoint.c[0])
        else:
            pos.append(vpoint.c[1])
    
    cdef int i, bf
    cdef double angle
    #Add slider slot virtual coordinates.
    for i, vpoint in enumerate(vpoints):
        #PLPP dependents.
        if vpoint.type != 2:
            continue
        bf = base_friend(i, vpoints)
        angle = np.deg2rad(
            vpoint.angle -
            vpoint.slopeAngle(vpoints[bf], 1, 0) +
            vpoint.slopeAngle(vpoints[bf], 0, 0)
        )
        pos.append((vpoint.c[1][0] + cos(angle), vpoint.c[1][1] + sin(angle)))
        mapping_r['S{}'.format(i)] = len(pos) - 1
    
    cdef int dof = 0
    cdef tuple expr
    cdef dict data_dict = {}
    cdef set targets = set()
    
    """Add data to 'data_dict'.
    
    + Add 'L' (link) parameters.
    + Counting DOF and targets.
    """
    cdef int target
    for expr in exprs:
        node = mapping_r[expr[1]]
        target = mapping_r[expr[-1]]
        if expr[0] == 'PLAP':
            #Link 1: expr[2]
            if expr[2] in mapping:
                data_dict[expr[2]] = mapping[expr[2]]
            else:
                data_dict[expr[2]] = tuple_distance(pos[node], pos[target])
            #Inputs
            dof += 1
        elif expr[0] == 'PLLP':
            #Link 1: expr[2]
            if expr[2] in mapping:
                data_dict[expr[2]] = mapping[expr[2]]
            else:
                data_dict[expr[2]] = tuple_distance(pos[node], pos[target])
            #Link 2: expr[3]
            if expr[3] in mapping:
                data_dict[expr[3]] = mapping[expr[3]]
            else:
                data_dict[expr[3]] = tuple_distance(pos[mapping_r[expr[4]]], pos[target])
        elif expr[0] == 'PLPP':
            #Link 1: expr[2]
            if expr[2] in mapping:
                data_dict[expr[2]] = mapping[expr[2]]
            else:
                data_dict[expr[2]] = tuple_distance(pos[node], pos[target])
            #PLPP[P1, L0, P2, S2](P2)
            #So we should get P2 first.
            data_dict[expr[3]] = pos[mapping_r[expr[3]]]
        elif expr[0] == 'PXY':
            #X: expr[2]
            if expr[2] in mapping:
                data_dict[expr[2]] = mapping[expr[2]]
            else:
                data_dict[expr[2]] = pos[target][0] - pos[node][0]
            #Y: expr[3]
            if expr[3] in mapping:
                data_dict[expr[3]] = mapping[expr[3]]
            else:
                data_dict[expr[3]] = pos[target][1] - pos[node][1]
        #Targets
        targets.add(expr[-1])
    
    for i in range(len(vpoints)):
        if mapping[i] not in targets:
            data_dict[mapping[i]] = pos[i]
    
    return data_dict, dof


cpdef list expr_path(
    object exprs,
    dict mapping,
    object vpoints,
    double interval
):
    """Auto preview function."""
    cdef dict data_dict
    cdef int dof
    data_dict, dof = data_collecting_c(exprs, mapping, vpoints)
    
    #Angles.
    cdef double a = 0
    cdef int i
    for i in range(dof):
        data_dict['a{}'.format(i)] = a
    
    return return_path(expr_join(exprs), data_dict, mapping, dof, interval)


cpdef list expr_solving(
    object exprs,
    dict mapping,
    object vpoints,
    object angles
):
    """Solving function."""
    cdef dict data_dict
    data_dict, _ = data_collecting_c(exprs, mapping, vpoints)
    
    #Angles.
    cdef double a
    cdef int i
    for i, a in enumerate(angles):
        data_dict['a{}'.format(i)] = np.deg2rad(a)
    
    expr_parser(expr_join(exprs), data_dict)
    
    cdef list solved_points = []
    for i in range(len(vpoints)):
        if np.isnan(data_dict[mapping[i]][0]):
            raise Exception("Result contains failure: Point{}".format(i))
        if vpoints[i].type == 0:
            solved_points.append(data_dict[mapping[i]])
        else:
            solved_points.append((vpoints[i].c[0], data_dict[mapping[i]]))
    
    return solved_points
