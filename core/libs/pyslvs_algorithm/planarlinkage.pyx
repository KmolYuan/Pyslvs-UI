# -*- coding: utf-8 -*-
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
    
    def __cinit__(self, object mechanismParams):
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
        Exp:
            {'relate': 'PLAP', 'target': 'B', 'params': ['A', 'L0', 'a0', 'D']},
            {'relate': 'PLLP', 'target': 'C', 'params': ['B', 'L1', 'L2', 'D']}, ...
        Expression: PLAP[A,L0,a0,D](B);PLLP[B,L1,L2,D](C);PLLP[B,L3,L4,C](E)
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
    
    cdef object get_data_dict(self, object v):
        cdef str name, L
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
        return tmp_dict
    
    cdef object from_formula(self, object expression_dict, object data_dict):
        cdef str fun = expression_dict["relate"]
        cdef object params = tuple(data_dict[p] for p in expression_dict["params"])
        if fun=='PLAP':
            return Coordinate(*PLAP(*params))
        if fun=='PLLP':
            return Coordinate(*PLLP(*params))
        if fun=='PLPP':
            return Coordinate(*PLPP(*params))
    
    cdef double run(self, object v):
        """
        v: a list of parameter [Ax, Ay, Dx, Dy, ...]
        target: a list of target [(1,5), (2,5), (3,5)]
        POINT: length of target
        VARS: linkage variables
        """
        # all variable
        cdef object test_dict = self.get_data_dict(v)
        # calculate the target point, and sum all error.
        cdef object path = []
        #Large fitness
        cdef double FAILURE = 9487
        #My fitness
        cdef double fitness = 0
        cdef int i
        for i in range(self.POINTS):
            #a0: random angle to generate target point.
            #match to path points.
            test_dict['a0'] = np.deg2rad(v[self.VARS+i])
            for e in self.Exp:
                #PLLP(test_dict['B'], test_dict['L1'], test_dict['L2'], test_dict['D'])
                target_coordinate = self.from_formula(e, test_dict)
                if target_coordinate.isnan():
                    return FAILURE
                if not legal_triangle(target_coordinate, test_dict[e["params"][0]], test_dict[e["params"][-1]]):
                    return FAILURE
                test_dict[e["target"]] = target_coordinate
            path.append(test_dict[self.targetPoint])
            fitness += path[i].distance(self.target[i])
        #constraint
        cdef str name
        for constraint in self.constraint:
            if not legal_crank(*[test_dict[name] for name in constraint]):
                return FAILURE
        #swap
        for i in range(self.POINTS):
            for j in range(self.POINTS):
                if path[j].distance(self.target[i])<path[i].distance(self.target[i]):
                    path[i], path[j] = path[j], path[i]
        return fitness
    
    cpdef object get_coordinates(self, object v):
        cdef object e
        cdef object final_dict = self.get_data_dict(v)
        final_dict['a0'] = np.deg2rad(v[self.VARS])
        for e in self.Exp:
            final_dict[e["target"]] = self.from_formula(e, final_dict)
        for k, v in final_dict.items():
            if type(v)==Coordinate:
                final_dict[k] = (v.x, v.y)
        return final_dict
    
    def __call__(self, object v):
        return self.run(v)
