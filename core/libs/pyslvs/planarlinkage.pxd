# -*- coding: utf-8 -*-
#cython: language_level=3

"""Algorithm type defination."""

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

import numpy as np
cimport numpy as np
from tinycadlib cimport Coordinate


cdef enum limit:
    maxGen,
    minFit,
    maxTime


cdef class Chromosome:
    cdef public int n
    cdef public double f
    cdef public np.ndarray v
    
    cdef double distance(self, Chromosome)
    cpdef void assign(self, Chromosome)


cdef class Planar:
    cdef int POINTS, VARS
    cdef list constraint, Link, driver_list, follower_list
    cdef dict Driver, Follower
    cdef np.ndarray target_names, exprs, target, upper, lower
    
    cdef inline np.ndarray get_upper(self):
        return self.upper
    
    cdef inline np.ndarray get_lower(self):
        return self.lower
    
    cdef inline int get_nParm(self):
        return len(self.upper)
    
    cdef dict get_data_dict(self, np.ndarray)
    cdef np.ndarray get_path_array(self)
    cdef Coordinate from_formula(self, tuple, dict)
    cdef double run(self, np.ndarray v) except *
    cpdef dict get_coordinates(self, np.ndarray)
