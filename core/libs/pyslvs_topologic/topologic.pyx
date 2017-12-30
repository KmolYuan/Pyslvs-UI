# -*- coding: utf-8 -*-
# cython: boundscheck=False
# cython: cdivision=True
# cython: wraparound=False

##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
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

from networkx import (
    Graph,
    compose,
    triangles,
    is_connected,
    is_isomorphic
)
from itertools import (
    combinations,
    product
)
import numpy as np
cimport numpy as np
from cpython cimport bool

cpdef bool testG(object G, object answer):
    if not is_connected(G):
        #is not connected
        return True
    cdef object G_
    for G_ in answer:
        if is_isomorphic(G, G_):
            #is isomorphic
            return True
    return False

cdef object emptyFunc(str j, int i):
    return None

cdef bool returnFalse():
    return False

cpdef object connection_get(int i, object connection):
    cdef object c
    return [c for c in connection if (i in c)]

#TODO: The function must be accelerated.
#Linkage Topological Component
cpdef topo(object link_num, bool degenerate=True, object setjobFunc=emptyFunc, object stopFunc=returnFalse):
    cdef np.ndarray links = np.ndarray((sum(link_num),), dtype=np.int)
    cdef int i, j, t, name, joint_count
    for i in range(sum(link_num)):
        name = i
        joint_count = 0
        for j, t in enumerate(link_num):
            if i < t:
                joint_count = j+2
                break
            i -= t
        links[name] = joint_count
    cdef object connection = list(combinations(range(sum(link_num)), 2))
    cdef object edges_combinations = []
    cdef int link, count, n
    cdef object match, match_, prod, G, H
    cdef bool error
    for link, count in enumerate(links):
        match = [Graph(m) for m in combinations(connection_get(link, connection), count)]
        match_ = []
        prod = list(product(edges_combinations, match))
        setjobFunc("Match link #{} / {}".format(link, len(links)-1), len(prod))
        for G, H in prod:
            if stopFunc():
                return
            G = compose(G, H)
            error = False
            for n in G.nodes:
                if len(list(G.neighbors(n)))>links[n]:
                    error = True
                    break
            if degenerate:
                for n in triangles(G).values():
                    if n!=0:
                        error = True
                        break
            if error:
                continue
            match_.append(G)
        if not edges_combinations:
            edges_combinations = match
        else:
            edges_combinations = match_
    setjobFunc("Verify the graphs...", len(edges_combinations))
    cdef object answer = []
    for G in edges_combinations:
        if stopFunc():
            return
        if testG(G, answer):
            continue
        answer.append(G)
    return answer
