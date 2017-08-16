# -*- coding: utf-8 -*-
from libc.math cimport isnan
import tinycadlib
from tinycadlib import legal_crank, legal_triangle, DEGREE, Coordinate, DEGREE
import numpy as np
cimport numpy as np

cdef class build_planar(object):
    cdef int POINTS, count, _tmp, VARS
    cdef object formula, ExpressionL, ExpressionNameL, coord, constraint
    cdef object Exp, Link
    cdef str Driving, Follower, targetPoint, Link_str, ExpressionName_str, Expression_str
    cdef np.ndarray target
    
    def __cinit__ (self, object mechanismParams):
        self.VARS = mechanismParams['VARS']
        # split string to list
        self.Link_str = mechanismParams['Link']
        self.Link = mechanismParams['Link'].split(',')
        #target point
        self.targetPoint = mechanismParams['Target']
        # counting how many action to satisfied require point
        self.POINTS = len(mechanismParams['targetPath'])
        # driving point, string
        self.Driving = mechanismParams['Driving']
        # folower point, string
        self.Follower = mechanismParams['Follower']
        #constraint
        self.constraint = mechanismParams['constraint']
        # use tuple data, create a list of coordinate object
        self.target = np.ndarray((self.POINTS,),dtype=np.object)
        for i, coord in enumerate(mechanismParams['targetPath']):
            self.target[i] = Coordinate(coord[0], coord[1])
            #[Coordinate(x0, y0), Coordinate(x0, y0), Coordinate(x0, y0), ...]
        # formulaction dictionary Link
        self.formula = dict()
        for f in mechanismParams['formula']:
            self.formula[f] = getattr(tinycadlib, f)
            #{'PLAP': PLAP(), 'PLLP': PLLP()}
        
        # Expression A, L0, a0, D, B, B, L1, L2, D, C, B, L3, L4, C, E
        # split Expression to list
        self.Expression_str = mechanismParams['Expression']
        ExpressionL = mechanismParams['Expression'].split(',')
        
        # ExpressionName PLAP, PLLP, PLLP
        # split ExpressionName to list
        self.ExpressionName_str = mechanismParams['ExpressionName']
        ExpressionNameL = mechanismParams['ExpressionName'].split(',')
        
        # combine ExpressionName and Expression, to set Expression List
        # counter,
        # PLLP -> A,L1,L2,D,B  the B will be equation target
        # the reset will be parameter of PLLP
        count = 0
        self.Exp = []
        for ExpressN in ExpressionNameL:
            _tmp = count+len(ExpressN)
            relate = ExpressN
            params = ExpressionL[count:_tmp]
            target = ExpressionL[_tmp]
            count = _tmp+1
            self.Exp.append({"relate":relate, 'target':target, 'params':params})
            #{'relate': 'PLAP', 'target': 'B', 'params': ['A', 'L0', 'a0', 'D']}
            #{'relate': 'PLLP', 'target': 'C', 'params': ['B', 'L1', 'L2', 'D']}
    
    def get_Driving(self):
        return self.Driving
    def get_Follower(self):
        return self.Follower
    def get_Target(self):
        return self.targetPoint
    def get_Link(self):
        return self.Link_str
    def get_ExpressionName(self):
        return self.ExpressionName_str
    def get_Expression(self):
        return self.Expression_str
    
    def __call__(self, object v):
        """
        target: a list of target [(1,5), (2,5), (3,5)]
        POINT: length of target
        VARS: linkage variables
        """
        cdef object tmp_dict, path, e
        cdef int index, i
        cdef double x
        cdef double y
        cdef double sum
        #Large fitness
        cdef int FAILURE = 1987
        # all variable
        tmp_dict = dict()
        index = 0
        # driving
        tmp_dict[self.Driving] = Coordinate(v[index], v[index+1])
        # follower
        tmp_dict[self.Follower] = Coordinate(v[index+2], v[index+3])
        index += 4
        # links
        for i, L in enumerate(self.Link):
            tmp_dict[L] = v[index+i]
        path = []
        fourbar_ground = tmp_dict[self.Driving].distance(tmp_dict[self.Follower])
        for constraint in self.constraint:
            if not legal_crank(tmp_dict[constraint['driver']], tmp_dict[constraint['follower']], tmp_dict[constraint['connect']], fourbar_ground):
                return FAILURE
        # calculate the target point, and sum all error.
        sum = 0
        for i in range(self.POINTS):
            #a0: random angle to generate target point.
            #match to path points.
            tmp_dict['a0'] = v[self.VARS+i]*DEGREE
            for e in self.Exp:
                #self.formula['PLLP'](tmp_dict['B'], tmp_dict['L1'], tmp_dict['L2'], tmp_dict['D'])
                x, y = self.formula[e["relate"]](*[tmp_dict[p] for p in e["params"]])
                if isnan(x) or isnan(y):
                    return FAILURE
                target_coordinate = Coordinate(x, y)
                if not legal_triangle(target_coordinate, tmp_dict[e["params"][0]], tmp_dict[e["params"][-1]]):
                    return FAILURE
                tmp_dict[e["target"]] = target_coordinate
            path.append(tmp_dict[self.targetPoint])
            sum += path[i].distance(self.target[i])
        # swap
        for i in range(self.POINTS):
            for j in range(self.POINTS):
                if path[j].distance(self.target[i])<path[i].distance(self.target[i]):
                    path[i], path[j] = path[j], path[i]
        if isnan(sum):
            return FAILURE
        return sum
