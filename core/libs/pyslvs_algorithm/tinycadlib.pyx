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
    atan2
)
import numpy as np
cimport numpy as np
from cpython cimport bool

nan = float("nan")

cdef class Coordinate:
    
    """A class to store the coordinate."""
    
    cdef public double x, y
    
    def __cinit__(self, double x, double y):
        self.x = x
        self.y = y
    
    cpdef double distance(self, Coordinate obj):
        cdef double x = self.x - obj.x
        cdef double y = self.y - obj.y
        return sqrt(x*x + y*y)
    
    cpdef bool isnan(self):
        return isnan(self.x) or isnan(self.y)

cpdef tuple PLAP(Coordinate A, double L0, double a0, Coordinate B, bool inverse=False):
    """Point on circle by angle."""
    cdef double b0 = atan2((B.y - A.y), (B.x - A.x))
    if inverse:
        return (A.x + L0*sin(b0 - a0), A.y + L0*cos(b0 - a0))
    else:
        return (A.x + L0*sin(b0 + a0), A.y + L0*cos(b0 + a0))

cpdef tuple PLLP(Coordinate A, double L0, double R0, Coordinate B, bool inverse=False):
    """Two intersection points of two circles."""
    cdef double dx = B.x - A.x
    cdef double dy = B.y - A.y
    cdef double d = A.distance(B)
    #No solutions, the circles are separate.
    if d > L0 + R0:
        return (nan, nan)
    #No solutions because one circle is contained within the other.
    if d < abs(L0 - R0):
        return (nan, nan)
    #Circles are coincident and there are an infinite number of solutions.
    if d==0 and L0==R0:
        return (nan, nan)
    cdef double a = (L0*L0 - R0*R0 + d*d)/(2*d)
    cdef double h = sqrt(L0*L0 - a*a)
    cdef double xm = A.x + a*dx/d
    cdef double ym = A.y + a*dy/d
    if inverse:
        return (xm + h*dy/d, ym - h*dx/d)
    else:
        return (xm - h*dy/d, ym + h*dx/d)

cpdef tuple PLPP(Coordinate A, double L0, Coordinate B, Coordinate C, bool inverse=False):
    cdef double x1 = A.x
    cdef double y1 = A.y
    cdef double x2 = B.x
    cdef double y2 = B.y
    cdef double x3 = C.x
    cdef double y3 = C.y
    if inverse:
        return (
            ((x2-x3)*(x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (y2 - y3)*sqrt(L0**2*x2**2 - 2*L0**2*x2*x3 + L0**2*y2**2 - 2*L0**2*y2*y3 + L0**2*x3**2 + L0**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2)) - (x2*y3 - y2*x3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))/((y2 - y3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)),
            (x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (y2 - y3)*sqrt(L0**2*x2**2 - 2*L0**2*x2*x3 + L0**2*y2**2 - 2*L0**2*y2*y3 + L0**2*x3**2 + L0**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2))/(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)
        )
    else:
        return (
            ((x2-x3)*(x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (-y2 + y3)*sqrt(L0**2*x2**2 - 2*L0**2*x2*x3 + L0**2*y2**2 - 2*L0**2*y2*y3 + L0**2*x3**2 + L0**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2)) - (x2*y3 - y2*x3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))/((y2 - y3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)),
            (x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (-y2 + y3)*sqrt(L0**2*x2**2 - 2*L0**2*x2*x3 + L0**2*y2**2 - 2*L0**2*y2*y3 + L0**2*x3**2 + L0**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2))/(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)
        )

cpdef bool legal_triangle(Coordinate A, Coordinate B, Coordinate C):
    #L0, L1, L2 is triangle
    cdef double L0 = A.distance(B)
    cdef double L1 = B.distance(C)
    cdef double L2 = A.distance(C)
    return L1+L2 > L0 and L0+L2 > L1 and L0+L1 > L2

cpdef bool legal_crank(Coordinate A, Coordinate B, Coordinate C, Coordinate D):
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

cdef str get_from_parenthesis(str s, str front, str back):
    """Get the string that is inside of parenthesis."""
    return s[s.find(front)+1:s.find(back)]

cdef str get_front_of_parenthesis(str s, str front):
    """Get the string that is front of parenthesis."""
    return s[:s.find(front)]

cpdef void expr_parser(str exprs, dict data_dict):
    '''Use to generate path data.
    
    exprs: "PLAP[A,a0,L1,B](C);PLLP[C,L1,L2,B](D);..."
        or "PLAP[P0,L0,a0,P1](P2);PLLP[P2,L1,L2,P1](P3);..."
    data_dict: {'a0':0., 'L1':10., 'A':(30., 40.), ...}
    '''
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
            p = data_dict[name]
            if type(p)==tuple or type(p)==list:
                args.append(Coordinate(*p))
            else:
                args.append(p)
        if f=='PLAP':
            data_dict[target] = PLAP(*args)
        elif f=='PLLP':
            data_dict[target] = PLLP(*args)
        elif f=='PLPP':
            data_dict[target] = PLPP(*args)
    """'data_dict' has been updated."""

cdef double distance(tuple c1, tuple c2):
    """Calculate the distance between two tuple coordinates."""
    cdef double x = c1[0] - c2[0]
    cdef double y = c1[1] - c2[1]
    return sqrt(x*x + y*y)

cdef void rotate(
    int input_angle,
    str expr_str,
    dict data_dict,
    dict mapping_r,
    list path,
    bool reverse=False
):
    """Add path coordinates.
    
    + Rotate the input joints.
    + Collect the coordinates of all joints.
    """
    cdef str param = 'a{}'.format(input_angle)
    cdef double a
    if not reverse:
        for a in range(0, 361, 5):
            data_dict[param] = np.deg2rad(a)
            expr_parser(expr_str, data_dict)
            rotate_collect(data_dict, mapping_r, path)
    else:
        for a in range(360, -1, -5):
            data_dict[param] = np.deg2rad(a)
            expr_parser(expr_str, data_dict)
            rotate_collect(data_dict, mapping_r, path)

cdef void rotate_collect(dict data_dict, dict mapping_r, list path):
    """Collecting."""
    cdef str m
    cdef int n
    for m, n in mapping_r.items():
        path[n].append(data_dict[m])

cpdef list expr_path(list exprs, dict mapping, list pos):
    """Auto preview function.
    
    exprs: [('PLAP', 'P0', 'L0', 'a0', 'P1', 'P2'), ...]
    mapping: {0: 'P0', 1: 'P2', 2: 'P3', 3: 'P4', ...}
    pos: [(x0, y0), (x1, y1), (x2, y2), ...]
    """
    
    cdef int n
    cdef str m
    cdef dict mapping_r = {m: n for n, m in mapping.items()}
    cdef set targets = set()
    cdef tuple expr
    cdef int dof = 0
    cdef dict data_dict = {}
    
    for expr in exprs:
        #Link 1: expr[2]
        data_dict[expr[2]] = distance(pos[mapping_r[expr[1]]], pos[mapping_r[expr[-1]]])
        if expr[0] == 'PLAP':
            #Inputs
            dof += 1
        else:
            #Link 2: expr[3]
            data_dict[expr[3]] = distance(pos[mapping_r[expr[4]]], pos[mapping_r[expr[-1]]])
        #Targets
        targets.add(expr[-1])
    
    cdef int i
    cdef tuple c
    for i, c in enumerate(pos):
        if mapping[i] not in targets:
            data_dict[mapping[i]] = c
    
    cdef double a = 0
    for i in range(dof):
        data_dict['a{}'.format(i)] = a
    
    cdef str expr_str = ';'.join(["{}[{},{},{},{}]({})".format(*expr) for expr in exprs])
    cdef list path = [[] for i in range(len(mapping))]
    
    #For each input joint.
    for i in range(dof):
        rotate(i, expr_str, data_dict, mapping_r, path)
    if dof > 1:
        #Rotate back.
        for i in range(dof):
            rotate(i, expr_str, data_dict, mapping_r, path, True)
    """
    return_path: [[each_joints]: [(x0, y0), (x1, y1), (x2, y2), ...], ...]
    """
    for i in range(len(path)):
        if len(set(path[i])) <= 1:
            path[i] = ()
        else:
            path[i] = tuple(path[i])
    return path
