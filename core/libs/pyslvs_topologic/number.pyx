# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from itertools import product

cdef int Max(int NL, int NJ):
    if NL <= NJ and NJ <= (2*NL - 3):
        return NJ - NL + 2
    if NL == NJ == 0:
        return -1
    if (2*NL - 3) <= NJ and NJ <= (NL*(NL - 1)/2):
        return NL - 1
    return -1

cpdef object NumberSynthesis(int NL, int NJ):
    cdef object result = []
    cdef int Mmax = Max(NL, NJ)
    if Mmax>1:
        Mmax = Max(NL, NJ)
    else:
        return "incorrect mechanism."
    cdef int i, p, s
    cdef object symbols, answer
    for symbols in product(range(NL + 1), repeat=(Mmax - 2)):
        NLMmax = NL - sum(symbols)
        if NLMmax < 0:
            continue
        answer = symbols + (NLMmax,)
        s = 0
        for i, p in enumerate(answer):
            s += (i+2)*p
        if s == 2*NJ:
            result.append(answer)
    return tuple(result)
