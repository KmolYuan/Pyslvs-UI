# -*- coding: utf-8 -*-
from libc.math cimport isnan
import tinycadlib
from tinycadlib import (
    PLAP,
    PLLP,
    PLPP,
    legal_crank,
    legal_triangle,
    Coordinate
)
import numpy as np
cimport numpy as np

cdef object formula = {
    'PLAP':PLAP,
    'PLLP':PLLP,
    'PLPP':PLPP
}

cdef str get_from_parenthesis(str s, str front, str back):
    return s[s.find(front)+1:s.find(back)]

cdef str get_front_of_parenthesis(str s, str front):
    return s[:s.find(front)]

#This class used to verified kinematics of the linkage mechanism.
cdef class build_planar(object):
    cdef int POINTS, VARS
    cdef object constraint, Link, upper, lower, Driving, Follower, Driving_list, Follower_list
    cdef str targetPoint, Expression_str
    cdef np.ndarray target, Exp
    
    def __cinit__ (self, object mechanismParams):
        '''
        mechanismParams = {
            'targetPath',
            'Target',
            'Driving',
            'Follower',
            'Target',
            'constraint',
            'Expression',
            'IMax', 'LMax', 'FMax', 'AMax',
            'IMin', 'LMin', 'FMin', 'AMin'
        }
        '''
        #counting how many action to satisfied require point
        self.POINTS = len(mechanismParams['targetPath'])
        #driving point, string
        self.Driving = mechanismParams['Driving']
        #folower point, string
        self.Follower = mechanismParams['Follower']
        #target point
        self.targetPoint = mechanismParams['Target']
        #constraint
        self.constraint = mechanismParams['constraint']
        
        #use tuple data, create a list of coordinate object
        #[Coordinate(x0, y0), Coordinate(x1, y1), Coordinate(x2, y2), ...]
        cdef int i
        self.target = np.ndarray((self.POINTS,), dtype=np.object)
        for i, (x, y) in enumerate(mechanismParams['targetPath']):
            self.target[i] = Coordinate(x, y)
        
        #Expression ['A', 'B', 'C', 'D', 'E', 'L0', 'L1', 'L2', 'L3', 'L4', 'a0']
        self.Expression_str = mechanismParams['Expression']
        cdef object ExpressionL = mechanismParams['Expression'].split(';')
        
        '''
        Link: L0, L1, L2, L3, ...
        Driving_list: The name of the point in "self.Driving".
        Follower_list: The name of the point in "self.Follower".
        Exp:        Tuple[Dict]
        Expression: PLAP[A,L0,a0,D](B);PLLP[B,L1,L2,D](C);PLLP[B,L3,L4,C](E)
        {'relate': 'PLAP', 'target': 'B', 'params': ['A', 'L0', 'a0', 'D']},
        {'relate': 'PLLP', 'target': 'C', 'params': ['B', 'L1', 'L2', 'D']}, ...
        '''
        cdef str expr, params, name
        self.Link = []
        self.Driving_list = []
        self.Follower_list = []
        self.Exp = np.ndarray((len(ExpressionL),), dtype=np.object)
        for i, expr in enumerate(ExpressionL):
            params = get_from_parenthesis(expr, '[', ']')
            self.Exp[i] = {
                'relate':get_front_of_parenthesis(expr, '['),
                'target':get_from_parenthesis(expr, '(', ')'),
                'params':params.split(',')
            }
            for p in params.split(','):
                if ('L' in p) and ('L' != p):
                    self.Link.append(p)
                if (p in self.Driving) and (p not in self.Driving_list):
                    self.Driving_list.append(p)
                if (p in self.Follower) and (p not in self.Follower_list):
                    self.Follower_list.append(p)
        #The number of all variables (chromsome).
        self.VARS = 2*len(self.Driving_list) + 2*len(self.Follower_list) + len(self.Link)
        
        #upper
        self.upper = []
        for name in self.Driving_list:
            for i in [0, 1]:
                self.upper.append(self.Driving[name][i] + self.Driving[name][2]/2)
        for name in self.Follower_list:
            for i in [0, 1]:
                self.upper.append(self.Follower[name][i] + self.Follower[name][2]/2)
        for name in ['IMax', 'LMax', 'FMax'] + ['LMax']*(len(self.Link)-3):
            self.upper.append(mechanismParams[name])
        self.upper += [mechanismParams['AMax']]*self.POINTS
        
        #lower
        self.lower = []
        for name in self.Driving_list:
            for i in [0, 1]:
                self.lower.append(self.Driving[name][i] - self.Driving[name][2]/2)
        for name in self.Follower_list:
            for i in [0, 1]:
                self.lower.append(self.Follower[name][i] - self.Follower[name][2]/2)
        for name in ['IMin', 'LMin', 'FMin'] + ['LMin']*(len(self.Link)-3):
            self.lower.append(mechanismParams[name])
        self.lower += [mechanismParams['AMin']]*self.POINTS
    
    cpdef object get_path(self):
        return [(c.x, c.y) for c in self.target]
    
    cpdef object get_upper(self):
        return self.upper[:]
    
    cpdef object get_lower(self):
        return self.lower[:]
    
    cpdef int get_nParm(self):
        return self.VARS + self.POINTS
    
    cpdef str get_Driving(self):
        return self.Driving
    
    cpdef str get_Follower(self):
        return self.Follower
    
    cpdef str get_Target(self):
        return self.targetPoint
    
    cpdef object get_Link(self):
        return self.Link
    
    cpdef str get_Expression(self):
        return self.Expression_str
    
    def __call__(self, object v):
        """
        v: a list of parameter [Ax, Ay, Dx, Dy, ...]
        target: a list of target [(1,5), (2,5), (3,5)]
        POINT: length of target
        VARS: linkage variables
        """
        cdef double x, y
        cdef str name, L
        #Large fitness
        cdef int FAILURE = 9487
        # all variable
        cdef object tmp_dict = dict()
        cdef int vi = 0
        #driving
        for name in self.Driving_list:
            tmp_dict[name] = Coordinate(v[vi], v[vi+1])
            vi += 2
        #follower
        for name in self.Follower_list:
            tmp_dict[name] = Coordinate(v[vi], v[vi+1])
            vi += 2
        #links
        for L in self.Link:
            tmp_dict[L] = v[vi]
            vi += 1
        # calculate the target point, and sum all error.
        cdef object path = []
        cdef double fitness = 0
        cdef int i
        for i in range(self.POINTS):
            #a0: random angle to generate target point.
            #match to path points.
            tmp_dict['a0'] = np.deg2rad(v[self.VARS+i])
            for e in self.Exp:
                #formula['PLLP'](tmp_dict['B'], tmp_dict['L1'], tmp_dict['L2'], tmp_dict['D'])
                x, y = formula[e["relate"]](*[tmp_dict[p] for p in e["params"]])
                if isnan(x) or isnan(y):
                    return FAILURE
                target_coordinate = Coordinate(x, y)
                if not legal_triangle(target_coordinate, tmp_dict[e["params"][0]], tmp_dict[e["params"][-1]]):
                    return FAILURE
                tmp_dict[e["target"]] = target_coordinate
            path.append(tmp_dict[self.targetPoint])
            fitness += path[i].distance(self.target[i])
        #constraint
        for constraint in self.constraint:
            if not legal_crank(*[tmp_dict[name] for name in constraint]):
                return FAILURE
        #swap
        for i in range(self.POINTS):
            for j in range(self.POINTS):
                if path[j].distance(self.target[i])<path[i].distance(self.target[i]):
                    path[i], path[j] = path[j], path[i]
        if isnan(fitness):
            return FAILURE
        return fitness
    
    cpdef object get_coordinates(self, object v):
        cdef int i
        cdef double x, y
        cdef str name, L, P
        cdef object e
        cdef object final_dict = dict()
        cdef int vi = 0
        #driving
        for name in self.Driving_list:
            final_dict[name] = Coordinate(v[vi], v[vi+1])
            vi += 2
        #follower
        for name in self.Follower_list:
            final_dict[name] = Coordinate(v[vi], v[vi+1])
            vi += 2
        #links
        for L in self.Link:
            final_dict[L] = v[vi]
            vi += 1
        final_dict['a0'] = np.deg2rad(v[self.VARS])
        for e in self.Exp:
            final_dict[e["target"]] = Coordinate(*formula[e["relate"]](*[final_dict[p] for p in e["params"]]))
        for k, v in final_dict.items():
            if type(v)==Coordinate:
                final_dict[k] = (v.x, v.y)
        return final_dict
