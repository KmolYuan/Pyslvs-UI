# -*- coding: utf-8 -*-

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from libc.math cimport (
    sqrt,
    isnan,
    sin,
    cos,
    atan2,
    hypot,
)
import numpy as np
cimport numpy as np
from cpython cimport bool

cdef double nan = float('nan')

cdef inline double distance(double x1, double y1, double x2, double y2):
    return hypot(x2 - x1, y2 - y1)

cdef class VPoint:
    
    """Symbol of joints."""
    
    cdef readonly tuple links, c
    cdef readonly int type
    cdef readonly object color
    cdef readonly str colorSTR, typeSTR
    cdef readonly double x, y, angle
    
    def __cinit__(self,
        str links,
        int type_int,
        double angle,
        str color_str,
        double x,
        double y,
        object color_func=None
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
        cdef int i
        if (self.type == 1) or (self.type == 2):
            self.c = tuple((self.x, self.y) for i in range(len(self.links)))
        else:
            self.c = ((self.x, self.y),)
    
    @property
    def cx(self):
        """X value of frist current coordinate."""
        return self.c[0][0]
    
    @property
    def cy(self):
        """Y value of frist current coordinate."""
        return self.c[0][1]
    
    def move(self, *coordinates):
        """Change coordinates of this point."""
        self.c = tuple(coordinates)
    
    cpdef double distance(self, VPoint p):
        """Distance."""
        return distance(self.x, self.y, p.x, p.y)
    
    cpdef double slopeAngle(self, VPoint p, int num1=-1, int num2=-1):
        """Angle between horizontal line and two point.
        
        num1: me.
        num2: other side.
        """
        cdef double y1
        cdef double x1
        cdef double y2
        cdef double x2
        if num1 == -1:
            y2 = self.y
            x2 = self.x
        else:
            y2 = self.c[num2][1]
            x2 = self.c[num2][0]
        if num2 == -1:
            y1 = p.y
            x1 = p.x
        else:
            y1 = p.c[num2][1]
            x1 = p.c[num2][0]
        return np.rad2deg(atan2(y1 - y2, x1 - x2))
    
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
    
    def __richcmp__(VPoint p1, VPoint p2, int op):
        """Equal comparison.
        
        op == 2: __eq__
        op == 3: __ne__
        """
        if (op != 2) and (op != 3):
            raise TypeError("Only allow to compare two VPoints.")
        return (p1.x == p2.x) and (p1.y == p2.y) and (op == 2)
    
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
        object color_func=None
    ):
        self.name = name
        self.colorSTR = color_str
        if color_func:
            self.color = color_func(color_str)
        self.points = points
    
    def __contains__(self, int point):
        """Check if point number is in the link."""
        return point in self.points
    
    def __repr__(self):
        """Use to generate script."""
        return "VLink('{l.name}', {l.points}, colorQt)".format(l=self)

cdef class Coordinate:
    
    """A class to store the coordinate."""
    
    cdef readonly double x, y
    
    def __cinit__(self, double x, double y):
        self.x = x
        self.y = y
    
    cpdef double distance(self, Coordinate p):
        """Distance."""
        return distance(self.x, self.y, p.x, p.y)
    
    cpdef bool isnan(self):
        """Test this coordinate is a error-occured answer."""
        return isnan(self.x)
    
    def __repr__(self):
        """Debug printing."""
        return "Coordinate({p.x}, {p.y})".format(p=self)

cpdef tuple PLAP(
    Coordinate A,
    double L0,
    double a0,
    Coordinate B=None,
    bool inverse=False
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
    bool inverse=False
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
    bool inverse=False
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
    d = sqrt(L0*L0 - d*d)
    dx *= d / line_mag
    dy *= d / line_mag
    if inverse:
        return (I.x - dx, I.y - dy)
    else:
        return (I.x + dx, I.y + dy)

cpdef inline bool legal_triangle(Coordinate A, Coordinate B, Coordinate C):
    #L0, L1, L2 is triangle
    cdef double L0 = A.distance(B)
    cdef double L1 = B.distance(C)
    cdef double L2 = A.distance(C)
    return (L1+L2 > L0) and (L0+L2 > L1) and (L0+L1 > L2)

cpdef inline bool legal_crank(Coordinate A, Coordinate B, Coordinate C, Coordinate D):
    '''
    verify the fourbar is satisfied the Gruebler's Equation, s + g <= p + q
        C - D
        |   |
        A   B
    '''
    cdef double driver = A.distance(C)
    cdef double follower = B.distance(D)
    cdef double ground = A.distance(B)
    cdef double connector = C.distance(D)
    return (
        (driver + connector <= ground + follower) or
        (driver + ground <= connector + follower)
    )

cdef inline str get_from_parenthesis(str s, str front, str back):
    """Get the string that is inside of parenthesis."""
    return s[s.find(front)+1:s.find(back)]

cdef inline str get_front_of_parenthesis(str s, str front):
    """Get the string that is front of parenthesis."""
    return s[:s.find(front)]

cpdef void expr_parser(str exprs, dict data_dict):
    '''Use to generate path data.
    
    exprs: "PLAP[P0,L0,a0,P1](P2);PLLP[P2,L1,L2,P1](P3);..."
    data_dict: {'a0':0., 'L1':10., 'A':(30., 40.), ...}
    '''
    #Remove all the spaces in the expression.
    exprs = exprs.replace(" ", '')
    cdef str expr, f, name
    cdef list params
    cdef object p
    cdef list args
    for expr in exprs.split(';'):
        f = get_front_of_parenthesis(expr, '[')
        params = get_from_parenthesis(expr, '[', ']').split(',')
        target = get_from_parenthesis(expr, '(', ')')
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
        if vpoints[node].links[0] in vpoint.links:
            return i

cdef tuple data_collecting(object exprs, dict mapping, object vpoints):
    """Input data:
    
    exprs: [('PLAP', 'P0', 'L0', 'a0', 'P1', 'P2'), ...]
    mapping: {0: 'P0', 1: 'P2', 2: 'P3', 3: 'P4', ...}
    vpoints: [VPoint0, VPoint1, VPoint2, ...]
    pos: [(x0, y0), (x1, y1), (x2, y2), ...]
    """
    cdef int i
    cdef str m
    cdef dict mapping_r = {m: i for i, m in mapping.items()}
    
    cdef VPoint vpoint
    cdef list pos = []
    for vpoint in vpoints:
        if vpoint.type == 0:
            pos.append((vpoint.cx, vpoint.cy))
        else:
            pos.append((vpoint.c[1][0], vpoint.c[1][1]))
    
    cdef int bf
    cdef double angle
    #Add slider coordinates.
    for i, vpoint in enumerate(vpoints):
        #PLPP dependents.
        if vpoint.type == 2:
            bf = base_friend(i, vpoints)
            angle = np.deg2rad(
                vpoint.angle +
                vpoint.slopeAngle(vpoints[bf], 1, 0) -
                vpoint.slopeAngle(vpoints[bf])
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
    for expr in exprs:
        #Link 1: expr[2]
        data_dict[expr[2]] = tuple_distance(
            pos[mapping_r[expr[1]]],
            pos[mapping_r[expr[-1]]]
        )
        if expr[0] == 'PLAP':
            #Inputs
            dof += 1
        elif expr[0] == 'PLLP':
            #Link 2: expr[3]
            data_dict[expr[3]] = tuple_distance(
                pos[mapping_r[expr[4]]],
                pos[mapping_r[expr[-1]]]
            )
        elif expr[0] == 'PLPP':
            #PLPP[P1, L0, P2, S2](P2)
            #So we should get P2 first.
            data_dict[expr[3]] = pos[mapping_r[expr[3]]]
        #Targets
        targets.add(expr[-1])
    
    for i in range(len(vpoints)):
        if mapping[i] not in targets:
            data_dict[mapping[i]] = pos[i]
    return data_dict, dof

cpdef list expr_path(object exprs, dict mapping, object vpoints, double interval):
    """Auto preview function."""
    cdef dict data_dict
    cdef int dof
    data_dict, dof = data_collecting(exprs, mapping, vpoints)
    
    #Angles.
    cdef double a = 0
    cdef int i
    for i in range(dof):
        data_dict['a{}'.format(i)] = a
    
    return return_path(expr_join(exprs), data_dict, mapping, dof, interval)

cpdef list expr_solving(object exprs, dict mapping, object vpoints, object angles):
    """Solving function."""
    cdef dict data_dict
    cdef int dof
    data_dict, dof = data_collecting(exprs, mapping, vpoints)
    
    #Angles.
    cdef double a
    cdef int i
    for i, a in enumerate(angles):
        data_dict['a{}'.format(i)] = np.deg2rad(a)
    
    expr_parser(expr_join(exprs), data_dict)
    
    cdef list solved_points = []
    for i in range(len(vpoints)):
        solved_points.append(data_dict[mapping[i]])
    
    return solved_points
