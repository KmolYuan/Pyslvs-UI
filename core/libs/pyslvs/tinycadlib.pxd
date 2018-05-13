# -*- coding: utf-8 -*-
#cython: language_level=3

"""Header for sharing classes."""

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from cpython cimport bool
from numpy cimport ndarray


cdef class VPoint:
    cdef readonly tuple links
    cdef readonly ndarray c
    cdef readonly int type
    cdef readonly object color
    cdef readonly str colorSTR
    cdef str typeSTR
    cdef readonly double x, y, angle
    
    cpdef void move(self, tuple, tuple c2 = *)
    cpdef void rotate(self, double)
    cpdef double distance(self, VPoint)
    cpdef double slopeAngle(self, VPoint, int num1 = *, int num2 = *)
    cpdef bool grounded(self)


cdef class Coordinate:
    cdef readonly double x, y
    
    cpdef double distance(self, Coordinate)
    #cpdef bool isnan(self) # cause error??

cdef bool legal_crank(Coordinate, Coordinate, Coordinate, Coordinate)
cdef str strbetween(str, str, str)
cdef str strbefore(str, str)
