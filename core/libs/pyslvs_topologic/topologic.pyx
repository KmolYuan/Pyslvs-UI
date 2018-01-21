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

from itertools import (
    combinations,
    product
)
import sys
import numpy as np
cimport numpy as np
from time import time
from cpython cimport bool

#NetworkX-like graph class.
cdef class Graph(object):
    cdef public object edges, nodes, adj
    
    def __cinit__(self, object edges):
        #edges
        self.edges = tuple(edges)
        #nodes
        cdef object nodes = []
        for p1, p2 in self.edges:
            if p1 not in nodes:
                nodes.append(p1)
            if p2 not in nodes:
                nodes.append(p2)
        self.nodes = tuple(nodes)
        #adj
        cdef int n
        self.adj = {n:self.neighbors(n) for n in self.nodes}
    
    cpdef object neighbors(self, int n):
        cdef object neighbors = []
        cdef int l1, l2
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
    
    cpdef object degree(self):
        return [(n, len(neighbors)) for n, neighbors in self.adj.items()]
    
    cpdef int number_of_edges(self, int u, int v):
        if v in self.adj[u]:
            return 1
        return 0
    
    def __len__(self):
        return len(self.nodes)

#Declared GMState.
cdef class GMState

#GraphMatcher and GMState class from NetworkX.
#Copyright (C) 2007-2009 by the NetworkX maintainers
#All rights reserved.
#BSD license.
#
#This work was originally coded by Christopher Ellison
#as part of the Computational Mechanics Python (CMPy) project.
#James P. Crutchfield, principal investigator.
#Complexity Sciences Center and Physics Department, UC Davis.
cdef class GraphMatcher(object):
    cdef public Graph G1, G2
    cdef object G1_nodes, G2_nodes, mapping
    cdef public object core_1, core_2, inout_1, inout_2
    cdef GMState state
    
    def __cinit__(self, Graph G1, Graph G2):
        self.G1 = G1
        self.G2 = G2
        self.G1_nodes = set(G1.nodes)
        self.G2_nodes = set(G2.nodes)
        
        # Set recursion limit.
        cdef int old_recursion_limit = sys.getrecursionlimit()
        cdef int expected_max_recursion_level = len(self.G2)
        if old_recursion_limit < 1.5 * expected_max_recursion_level:
            # Give some breathing room.
            sys.setrecursionlimit(int(1.5 * expected_max_recursion_level))
        
        # Initialize state
        self.initialize()
    
    #Reinitializes the state of the algorithm.
    cdef void initialize(self):
        # core_1[n] contains the index of the node paired with n, which is m,
        #           provided n is in the mapping.
        # core_2[m] contains the index of the node paired with m, which is n,
        #           provided m is in the mapping.
        self.core_1 = {}
        self.core_2 = {}
        
        # See the paper for definitions of M_x and T_x^{y}
        # inout_1[n]  is non-zero if n is in M_1 or in T_1^{inout}
        # inout_2[m]  is non-zero if m is in M_2 or in T_2^{inout}
        #
        # The value stored is the depth of the SSR tree when the node became
        # part of the corresponding set.
        self.inout_1 = {}
        self.inout_2 = {}
        # Practically, these sets simply store the nodes in the subgraph.
        
        self.state = GMState(self)
        
        # Provide a convienient way to access the isomorphism mapping.
        self.mapping = self.core_1.copy()
    
    #Generator candidate_pairs_iter()
    def candidate_pairs_iter(self):
        """Iterator over candidate pairs of nodes in G1 and G2."""
        cdef int node
        # All computations are done using the current state!
        cdef object G1_nodes = self.G1_nodes
        cdef object G2_nodes = self.G2_nodes
        # First we compute the inout-terminal sets.
        cdef object T1_inout = [node for node in G1_nodes if (node in self.inout_1) and (node not in self.core_1)]
        cdef object T2_inout = [node for node in G2_nodes if (node in self.inout_2) and (node not in self.core_2)]
        # If T1_inout and T2_inout are both nonempty.
        # P(s) = T1_inout x {min T2_inout}
        if T1_inout and T2_inout:
            for node in T1_inout:
                yield node, min(T2_inout)
        else:
            # If T1_inout and T2_inout were both empty....
            # P(s) = (N_1 - M_1) x {min (N_2 - M_2)}
            ##if not (T1_inout or T2_inout):
            # as suggested by  [2], incorrect
            # as inferred from [1], correct
            # First we determine the candidate node for G2
            for node in self.G1.nodes:
                if node not in self.core_1:
                    yield node, min(G2_nodes - set(self.core_2))
        # For all other cases, we don't have any candidate pairs.
    
    #Returns True if G1 and G2 are isomorphic graphs.
    cpdef bool is_isomorphic(self):
        # Let's do two very quick checks!
        # QUESTION: Should we call faster_graph_could_be_isomorphic(G1,G2)?
        # For now, I just copy the code.
        
        # Check global properties
        if len(self.G1)!=len(self.G2):
            return False
        
        # Check local properties
        if sorted([d for n, d in self.G1.degree()]) != sorted([d for n, d in self.G2.degree()]):
            return False
        try:
            next(self.isomorphisms_iter())
            return True
        except StopIteration:
            return False
    
    #Generator isomorphisms_iter()
    #Generator over isomorphisms between G1 and G2.
    def isomorphisms_iter(self):
        # Declare that we are looking for a graph-graph isomorphism.
        self.initialize()
        for mapping in self.match():
            yield mapping
    
    #Generator match()
    #Extends the isomorphism mapping.
    def match(self):
        cdef int G1_node, G2_node
        cdef GMState newstate
        cdef object mapping
        if len(self.core_1) == len(self.G2):
            # Save the final mapping, otherwise garbage collection deletes it.
            self.mapping = self.core_1.copy()
            # The mapping is complete.
            yield self.mapping
        else:
            for G1_node, G2_node in self.candidate_pairs_iter():
                if self.syntactic_feasibility(G1_node, G2_node):
                    # Recursive call, adding the feasible state.
                    newstate = self.state.__class__(self, G1_node, G2_node)
                    for mapping in self.match():
                        yield mapping
                    # restore data structures
                    newstate.restore()
    
    #Returns True if adding (G1_node, G2_node) is syntactically feasible.
    cdef bool syntactic_feasibility(self, int G1_node, int G2_node):
        # The VF2 algorithm was designed to work with graphs having, at most,
        # one edge connecting any two nodes.  This is not the case when
        # dealing with an MultiGraphs.
        #
        # Basically, when we test the look-ahead rules R_neighbor, we will
        # make sure that the number of edges are checked. We also add
        # a R_self check to verify that the number of selfloops is acceptable.
        #
        # Users might be comparing Graph instances with MultiGraph instances.
        # So the generic GraphMatcher class must work with MultiGraphs.
        # Care must be taken since the value in the innermost dictionary is a
        # singlet for Graph instances.  For MultiGraphs, the value in the
        # innermost dictionary is a list.
        
        ### Test at each step to get a return value as soon as possible.
        
        ### Look ahead 0
        # R_self
        # The number of selfloops for G1_node must equal the number of
        # self-loops for G2_node. Without this check, we would fail on
        # R_neighbor at the next recursion level. But it is good to prune the
        # search tree now.
        if self.G1.number_of_edges(G1_node, G1_node)!=self.G2.number_of_edges(G2_node, G2_node):
            return False
        # R_neighbor
        # For each neighbor n' of n in the partial mapping, the corresponding
        # node m' is a neighbor of m, and vice versa. Also, the number of
        # edges must be equal.
        cdef object neighbor
        for neighbor in self.G1.neighbors(G1_node):
            if neighbor in self.core_1:
                if not (self.core_1[neighbor] in self.G2.neighbors(G2_node)):
                    return False
                elif self.G1.number_of_edges(neighbor, G1_node)!=self.G2.number_of_edges(self.core_1[neighbor], G2_node):
                    return False
        for neighbor in self.G2.neighbors(G2_node):
            if neighbor in self.core_2:
                if not (self.core_2[neighbor] in self.G1.neighbors(G1_node)):
                    return False
                elif self.G1.number_of_edges(self.core_2[neighbor], G1_node) != self.G2.number_of_edges(neighbor, G2_node):
                    return False
        
        ### Look ahead 1
        # R_terminout
        # The number of neighbors of n that are in T_1^{inout} is equal to the
        # number of neighbors of m that are in T_2^{inout}, and vice versa.
        cdef int num1 = 0
        for neighbor in self.G1.neighbors(G1_node):
            if (neighbor in self.inout_1) and (neighbor not in self.core_1):
                num1 += 1
        cdef int num2 = 0
        for neighbor in self.G2.neighbors(G2_node):
            if (neighbor in self.inout_2) and (neighbor not in self.core_2):
                num2 += 1
        if not (num1 == num2):
            return False
        
        ### Look ahead 2
        # R_new
        # The number of neighbors of n that are neither in the core_1 nor
        # T_1^{inout} is equal to the number of neighbors of m
        # that are neither in core_2 nor T_2^{inout}.
        num1 = 0
        for neighbor in self.G1.neighbors(G1_node):
            if neighbor not in self.inout_1:
                num1 += 1
        num2 = 0
        for neighbor in self.G2.neighbors(G2_node):
            if neighbor not in self.inout_2:
                num2 += 1
        if not (num1 == num2):
            return False
        
        # Otherwise, this node pair is syntactically feasible!
        return True

cdef class GMState(object):
    cdef GraphMatcher GM
    cdef int G1_node, G2_node, depth
    
    def __cinit__(self, GraphMatcher GM, int G1_node=-1, int G2_node=-1):
        """Initializes GMState object.
        
        Pass in the GraphMatcher to which this GMState belongs and the
        new node pair that will be added to the GraphMatcher's current
        isomorphism mapping.
        """
        self.GM = GM
        
        # Initialize the last stored node pair.
        self.G1_node = -1
        self.G2_node = -1
        self.depth = len(GM.core_1)
        
        if G1_node==-1 or G2_node==-1:
            # Then we reset the class variables
            GM.core_1 = {}
            GM.core_2 = {}
            GM.inout_1 = {}
            GM.inout_2 = {}
        cdef object new_nodes
        cdef object neighbor
        cdef int node
        # Watch out! G1_node == 0 should evaluate to True.
        if G1_node!=-1 and G2_node!=-1:
            # Add the node pair to the isomorphism mapping.
            GM.core_1[G1_node] = G2_node
            GM.core_2[G2_node] = G1_node
            
            # Store the node that was added last.
            self.G1_node = G1_node
            self.G2_node = G2_node
            
            # Now we must update the other two vectors.
            # We will add only if it is not in there already!
            self.depth = len(GM.core_1)
            
            # First we add the new nodes...
            if G1_node not in GM.inout_1:
                GM.inout_1[G1_node] = self.depth
            if G2_node not in GM.inout_2:
                    GM.inout_2[G2_node] = self.depth
            
            # Now we add every other node...
            
            # Updates for T_1^{inout}
            new_nodes = set([])
            for node in GM.core_1:
                new_nodes.update([neighbor for neighbor in GM.G1.neighbors(node) if neighbor not in GM.core_1])
            for node in new_nodes:
                if node not in GM.inout_1:
                    GM.inout_1[node] = self.depth
            
            # Updates for T_2^{inout}
            new_nodes = set([])
            for node in GM.core_2:
                new_nodes.update([neighbor for neighbor in GM.G2.neighbors(node) if neighbor not in GM.core_2])
            for node in new_nodes:
                if node not in GM.inout_2:
                    GM.inout_2[node] = self.depth
    
    cpdef void restore(self):
        """Deletes the GMState object and restores the class variables."""
        # First we remove the node that was added from the core vectors.
        # Watch out! G1_node == 0 should evaluate to True.
        if self.G1_node!=-1 and self.G2_node!=-1:
            del self.GM.core_1[self.G1_node]
            del self.GM.core_2[self.G2_node]
        
        # Now we revert the other two vectors.
        # Thus, we delete all entries which have this depth level.
        cdef object vector
        cdef int node
        for vector in (self.GM.inout_1, self.GM.inout_2):
            for node in list(vector):
                if vector[node] == self.depth:
                    del vector[node]

cdef object compose(Graph G, Graph H):
    cdef object tmp_edges = list(G.edges)
    cdef int l1, l2
    for l1, l2 in H.edges:
        if ((l1, l2) in tmp_edges) or ((l2, l1) in tmp_edges):
            continue
        tmp_edges.append((l1, l2))
    return Graph(tmp_edges)

cdef bool test(Graph G, object answer):
    if not G.is_connected():
        #is not connected
        return True
    cdef Graph H
    cdef GraphMatcher GM_GH
    for H in answer:
        GM_GH = GraphMatcher(G, H)
        if GM_GH.is_isomorphic():
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
    cdef double t0 = time()
    cdef np.ndarray links = np.zeros((sum(link_num),), dtype=np.int8)
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
    cdef object match, match_
    cdef Graph G, H
    cdef bool error
    for link, count in enumerate(links):
        match = [Graph(m) for m in combinations(connection_get(link, connection), count)]
        if not edges_combinations:
            edges_combinations = match
            continue
        match_ = []
        setjobFunc("Match link #{} / {}".format(link, len(links)-1), len(edges_combinations)*len(match))
        for G, H in product(edges_combinations, match):
            if stopFunc():
                return None, time()-t0
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
        edges_combinations = match_
    setjobFunc("Verify the graphs...", len(edges_combinations))
    cdef object answer = []
    for G in edges_combinations:
        if stopFunc():
            return None, time()-t0
        if test(G, answer):
            continue
        answer.append(G)
    return answer, time()-t0
