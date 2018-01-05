# -*- coding: utf-8 -*-
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

from itertools import (
    combinations,
    product
)
import numpy as np
cimport numpy as np
from cpython cimport bool

#NetworkX-like graph class.
cdef class Graph(object):
    cdef public object edges
    cdef public object nodes
    cdef public object adj
    
    def __cinit__(self, object edges):
        self.edges = tuple(edges)
        cdef object nodes = []
        for p1, p2 in self.edges:
            if p1 not in nodes:
                nodes.append(p1)
            elif p2 not in nodes:
                nodes.append(p2)
        self.nodes = tuple(nodes)
        self.adj = self.setAdj()
    
    cdef object setAdj(self):
        cdef object adj = {}
        cdef object neighbors = []
        cdef int n
        for n in self.nodes:
            adj[n] = self.neighbors(n)
        return adj
    
    cdef object count(self, object adj, object edges):
        cdef object tmp_adj = []
        cdef int l1, l2
        for l1, l2 in edges:
            tmp_adj.append(sorted((len(adj[l1]), len(adj[l2]))))
        return sorted(tmp_adj)
    
    cpdef object neighbors(self, int n):
        cdef object neighbors = []
        for l1, l2 in self.edges:
            if n==l1:
                neighbors.append(l2)
            if n==l2:
                neighbors.append(l1)
        return tuple(neighbors)
    
    cpdef bool has_triangles(self):
        cdef int i, n1, n2
        cdef object neighbors1, neighbors2
        for neighbors1 in self.adj.values():
            for n1, n2 in combinations(neighbors1, 2):
                for n, neighbors2 in self.adj.items():
                    if n1==n and (n2 in neighbors2):
                        return True
                    if n2==n and (n1 in neighbors2):
                        return True
        return False
    
    cpdef bool is_connected(self):
        cdef int index = 0
        cdef object nodes = [self.nodes[index]]
        while index < len(nodes):
            for neighbor in self.adj[nodes[index]]:
                if neighbor not in nodes:
                    nodes.append(neighbor)
            index += 1
        return len(nodes)==len(self.nodes)
    
    cpdef bool is_isomorphic(self, object G):
        return self.count(self.adj, self.edges)==self.count(G.adj, G.edges)

cdef object compose(object G, object H):
    cdef object tmp_edges = list(G.edges)
    for l1, l2 in H.edges:
        if ((l1, l2) in tmp_edges) or ((l2, l1) in tmp_edges):
            continue
        tmp_edges.append((l1, l2))
    return Graph(tmp_edges)

cdef bool test(object G, object answer):
    if not G.is_connected():
        #is not connected
        return True
    cdef object H
    for H in answer:
        if G.is_isomorphic(H):
            #is isomorphic
            return True
    return False

cdef object emptyFunc(str j, int i):
    return None

cdef bool returnFalse():
    return False

cdef object connection_get(int i, object connection):
    cdef object c
    return [c for c in connection if (i in c)]

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
    #connection = [(1, 2), (1, 3), ..., (2, 3), (2, 4), ...]
    cdef object connection = tuple(combinations(range(sum(link_num)), 2))
    #ALL results.
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
                if len(G.neighbors(n))>links[n]:
                    error = True
                    break
            if error:
                continue
            if degenerate and G.has_triangles():
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
        if test(G, answer):
            continue
        answer.append(G)
    return answer
