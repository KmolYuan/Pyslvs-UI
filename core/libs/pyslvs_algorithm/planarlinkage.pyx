# -*- coding: utf-8 -*-
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

#Large fitness
cdef double FAILURE = 9487

cdef str get_from_parenthesis(str s, str front, str back):
    return s[s.find(front)+1:s.find(back)]

cdef str get_front_of_parenthesis(str s, str front):
    return s[:s.find(front)]

#This class used to verified kinematics of the linkage mechanism.
cdef class build_planar(object):
    cdef int POINTS, VARS
    cdef object constraint, Link, upper, lower, Driver, Follower, Driver_list, Follower_list, targetPoint
    cdef str Expression_str
    cdef np.ndarray Exp, target
    
    def __cinit__(self, object mechanismParams):
        '''
        mechanismParams = {
            'Target',
            'Driver',
            'Follower',
            'Target',
            'constraint',
            'Expression',
            'IMax', 'LMax', 'FMax', 'AMax',
            'IMin', 'LMin', 'FMin', 'AMin'
        }
        '''
        cdef object value
        cdef int l
        cdef object check_tuple = tuple(len(value) for value in mechanismParams['Target'].values())
        if not all([l==check_tuple[0] for l in check_tuple]):
            raise ValueError("Target path should be in the same size.")
        #counting how many action to satisfied require point
        self.POINTS = check_tuple[0]
        #driving point, string
        self.Driver = mechanismParams['Driver']
        #folower point, string
        self.Follower = mechanismParams['Follower']
        #target point name
        #[Coordinate(x0, y0), Coordinate(x1, y1), Coordinate(x2, y2), ...]
        cdef double x, y
        self.targetPoint = tuple(mechanismParams['Target'])
        self.target = np.ndarray((len(mechanismParams['Target']),), dtype=np.object)
        cdef int i
        for i, value in enumerate(mechanismParams['Target'].values()):
            self.target[i] = tuple(Coordinate(x, y) for x, y in value)
        
        #constraint
        self.constraint = mechanismParams['constraint']
        
        #Expression ['A', 'B', 'C', 'D', 'E', 'L0', 'L1', 'L2', 'L3', 'L4', 'a0']
        self.Expression_str = mechanismParams['Expression']
        cdef object ExpressionL = mechanismParams['Expression'].split(';')
        
        '''
        Link: L0, L1, L2, L3, ...
        Driver_list: The name of the point in "self.Driver".
        Follower_list: The name of the point in "self.Follower".
        Exp:
            {'relate': 'PLAP', 'target': 'B', 'params': ['A', 'L0', 'a0', 'D']},
            {'relate': 'PLLP', 'target': 'C', 'params': ['B', 'L1', 'L2', 'D']}, ...
        Expression: PLAP[A,L0,a0,D](B);PLLP[B,L1,L2,D](C);PLLP[B,L3,L4,C](E)
        '''
        cdef str expr, params
        self.Link = []
        self.Driver_list = []
        self.Follower_list = []
        self.Exp = np.ndarray((len(ExpressionL),), dtype=np.object)
        for i, expr in enumerate(ExpressionL):
            params = get_from_parenthesis(expr, '[', ']')
            self.Exp[i] = (
                #[0]: relate
                get_front_of_parenthesis(expr, '['),
                #[1]: target
                get_from_parenthesis(expr, '(', ')'),
                #[2]: params
                params.split(',')
            )
            for p in params.split(','):
                if ('L' in p) and ('L' != p):
                    self.Link.append(p)
                if (p in self.Driver) and (p not in self.Driver_list):
                    self.Driver_list.append(p)
                if (p in self.Follower) and (p not in self.Follower_list):
                    self.Follower_list.append(p)
        #The number of all variables (chromsome).
        self.VARS = 2*len(self.Driver_list) + 2*len(self.Follower_list) + len(self.Link)
        
        #upper
        cdef str name
        self.upper = []
        for name in self.Driver_list:
            for i in [0, 1]:
                self.upper.append(self.Driver[name][i] + self.Driver[name][2]/2)
        for name in self.Follower_list:
            for i in [0, 1]:
                self.upper.append(self.Follower[name][i] + self.Follower[name][2]/2)
        for name in ['IMax', 'LMax', 'FMax'] + ['LMax']*(len(self.Link)-3):
            self.upper.append(mechanismParams[name])
        self.upper += [mechanismParams['AMax']]*self.POINTS
        
        #lower
        self.lower = []
        for name in self.Driver_list:
            for i in [0, 1]:
                self.lower.append(self.Driver[name][i] - self.Driver[name][2]/2)
        for name in self.Follower_list:
            for i in [0, 1]:
                self.lower.append(self.Follower[name][i] - self.Follower[name][2]/2)
        for name in ['IMin', 'LMin', 'FMin'] + ['LMin']*(len(self.Link)-3):
            self.lower.append(mechanismParams[name])
        self.lower += [mechanismParams['AMin']]*self.POINTS
    
    cpdef object get_upper(self):
        return self.upper[:]
    
    cpdef object get_lower(self):
        return self.lower[:]
    
    cpdef int get_nParm(self):
        return self.VARS + self.POINTS
    
    cpdef object get_Link(self):
        return self.Link
    
    cpdef str get_Expression(self):
        return self.Expression_str
    
    cdef object get_data_dict(self, object v):
        cdef str name, L
        cdef object tmp_dict = dict()
        cdef int vi = 0
        #driving
        for name in self.Driver_list:
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
    
    cdef np.ndarray get_path_array(self):
        cdef np.ndarray path = np.ndarray((len(self.targetPoint),), dtype=np.object)
        cdef int i
        for i in range(len(self.targetPoint)):
            path[i] = []
        return path
    
    cdef object from_formula(self, object expression_dict, object data_dict):
        cdef str fun = expression_dict[0]
        cdef object params = tuple(data_dict[p] for p in expression_dict[2])
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
        cdef np.ndarray path = self.get_path_array()
        # calculate the target point, and sum all error.
        #My fitness
        cdef double fitness = 0
        cdef int i, j, k
        cdef str name
        cdef object e
        for i in range(self.POINTS):
            #a0: random angle to generate target point.
            #match to path points.
            test_dict['a0'] = np.deg2rad(v[self.VARS+i])
            for e in self.Exp:
                #PLLP(test_dict['B'], test_dict['L1'], test_dict['L2'], test_dict['D'])
                target_coordinate = self.from_formula(e, test_dict)
                if target_coordinate.isnan():
                    return FAILURE
                #params
                if not legal_triangle(target_coordinate, test_dict[e[2][0]], test_dict[e[2][-1]]):
                    return FAILURE
                #target
                test_dict[e[1]] = target_coordinate
            for i, name in enumerate(self.targetPoint):
                path[i].append(test_dict[name])
        #constraint
        for constraint in self.constraint:
            if not legal_crank(*[test_dict[name] for name in constraint]):
                return FAILURE
        #swap
        for k in range(len(self.targetPoint)):
            for i in range(self.POINTS):
                for j in range(self.POINTS):
                    if path[k][j].distance(self.target[k][i])<path[k][i].distance(self.target[k][i]):
                        path[k][i], path[k][j] = path[k][j], path[k][i]
        #sum the fitness
        for k in range(len(self.targetPoint)):
            for i in range(self.POINTS):
                fitness += path[k][i].distance(self.target[k][i])
        return fitness
    
    cpdef object get_coordinates(self, object v):
        cdef str k
        cdef object e, value
        cdef object final_dict = self.get_data_dict(v)
        final_dict['a0'] = np.deg2rad(v[self.VARS])
        for e in self.Exp:
            #target
            final_dict[e[1]] = self.from_formula(e, final_dict)
        for k, value in final_dict.items():
            if type(value)==Coordinate:
                final_dict[k] = (value.x, value.y)
        return final_dict
    
    def __call__(self, object v):
        return self.run(v)
