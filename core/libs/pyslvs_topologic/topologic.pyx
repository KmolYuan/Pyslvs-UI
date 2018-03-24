# -*- coding: utf-8 -*-

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from itertools import combinations, product
import sys
import numpy as np
cimport numpy as np
from time import time
from cpython cimport bool

cdef class Graph(object):
    
    """NetworkX-like graph class."""
    
    cdef tuple nodes
    cdef dict adj
    cdef public tuple edges
    
    def __cinit__(self, object edges):
        #edges
        """edges: ((l1, l2), ...)"""
        self.edges = tuple(edges)
        #nodes
        cdef list nodes = []
        for p1, p2 in self.edges:
            if p1 not in nodes:
                nodes.append(p1)
            if p2 not in nodes:
                nodes.append(p2)
        self.nodes = tuple(nodes)
        #adj
        cdef int n
        self.adj = {n: self.neighbors(n) for n in self.nodes}
    
    cdef tuple neighbors(self, int n):
        """Neighbors except the node."""
        cdef list neighbors = []
        cdef int l1, l2
        for l1, l2 in self.edges:
            if n==l1:
                neighbors.append(l2)
            if n==l2:
                neighbors.append(l1)
        return tuple(neighbors)
    
    cpdef Graph compose(self, Graph H):
        return Graph(set(self.edges) | set(H.edges))
    
    cpdef bool out_of_limit(self, np.ndarray limit):
        cdef int n
        for n in self.adj:
            if len(self.adj[n]) > limit[n]:
                return True
        return False
    
    cpdef bool has_triangles(self):
        cdef int n1, n2
        cdef tuple neighbors
        for neighbors in self.adj.values():
            for n1 in neighbors:
                for n2 in neighbors:
                    if n1 == n2:
                        continue
                    if n1 in self.adj[n2]:
                        return True
        return False
    
    cpdef bool is_connected(self):
        cdef int index = 0
        cdef list nodes = [self.nodes[index]]
        while index < len(nodes):
            for neighbor in self.adj[nodes[index]]:
                if neighbor not in nodes:
                    nodes.append(neighbor)
            index += 1
        return len(nodes) == len(self.nodes)
    
    cpdef bool is_isomorphic(self, Graph H):
        cdef GraphMatcher GM_GH = GraphMatcher(self, H)
        return GM_GH.is_isomorphic()
    
    cpdef list links(self):
        return sorted([len(neighbors) for neighbors in self.adj.values()])
    
    cpdef int number_of_edges(self, int u, int v):
        if v in self.adj[u]:
            return 1
        return 0

cdef class GraphMatcher(object):
    
    """GraphMatcher and GMState class from NetworkX.
    Copyright (C) 2007-2009 by the NetworkX maintainers
    All rights reserved.
    BSD license.
    
    This work was originally coded by Christopher Ellison
    as part of the Computational Mechanics Python (CMPy) project.
    James P. Crutchfield, principal investigator.
    Complexity Sciences Center and Physics Department, UC Davis.
    """
    
    cdef Graph G1, G2
    cdef set G1_nodes, G2_nodes
    cdef dict core_1, core_2, inout_1, inout_2, mapping
    cdef GMState state
    
    def __cinit__(self, Graph G1, Graph G2):
        self.G1 = G1
        self.G2 = G2
        self.G1_nodes = set(G1.nodes)
        self.G2_nodes = set(G2.nodes)
        
        # Set recursion limit.
        cdef int old_recursion_limit = sys.getrecursionlimit()
        cdef int expected_max_recursion_level = len(self.G2.nodes)
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
        # First we compute the inout-terminal sets.
        cdef set s1 = set(self.inout_1) - set(self.core_1)
        cdef set s2 = set(self.inout_2) - set(self.core_2)
        cdef list T1_inout = [node for node in self.G1_nodes if (node in s1)]
        cdef list T2_inout = [node for node in self.G2_nodes if (node in s2)]
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
                    yield node, min(self.G2_nodes - set(self.core_2))
        # For all other cases, we don't have any candidate pairs.
    
    #Returns True if G1 and G2 are isomorphic graphs.
    cpdef bool is_isomorphic(self):
        # Let's do two very quick checks!
        # QUESTION: Should we call faster_graph_could_be_isomorphic(G1,G2)?
        # For now, I just copy the code.
        
        # Check global properties
        if len(self.G1.nodes) != len(self.G2.nodes):
            return False
        
        # Check local properties
        if self.G1.links() != self.G2.links():
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
        cdef dict mapping
        for mapping in self.match():
            yield mapping
    
    #Generator match()
    #Extends the isomorphism mapping.
    def match(self):
        cdef int G1_node, G2_node
        cdef GMState newstate
        cdef dict mapping
        if len(self.core_1) == len(self.G2.nodes):
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
        if self.G1.number_of_edges(G1_node, G1_node) != self.G2.number_of_edges(G2_node, G2_node):
            return False
        # R_neighbor
        # For each neighbor n' of n in the partial mapping, the corresponding
        # node m' is a neighbor of m, and vice versa. Also, the number of
        # edges must be equal.
        cdef int neighbor
        for neighbor in self.G1.adj[G1_node]:
            if neighbor in self.core_1:
                if not (self.core_1[neighbor] in self.G2.adj[G2_node]):
                    return False
                elif self.G1.number_of_edges(neighbor, G1_node) != self.G2.number_of_edges(self.core_1[neighbor], G2_node):
                    return False
        for neighbor in self.G2.adj[G2_node]:
            if neighbor in self.core_2:
                if not (self.core_2[neighbor] in self.G1.adj[G1_node]):
                    return False
                elif self.G1.number_of_edges(self.core_2[neighbor], G1_node) != self.G2.number_of_edges(neighbor, G2_node):
                    return False
        
        ### Look ahead 1
        # R_terminout
        # The number of neighbors of n that are in T_1^{inout} is equal to the
        # number of neighbors of m that are in T_2^{inout}, and vice versa.
        cdef int num1 = 0
        for neighbor in self.G1.adj[G1_node]:
            if (neighbor in self.inout_1) and (neighbor not in self.core_1):
                num1 += 1
        cdef int num2 = 0
        for neighbor in self.G2.adj[G2_node]:
            if (neighbor in self.inout_2) and (neighbor not in self.core_2):
                num2 += 1
        if num1 != num2:
            return False
        
        ### Look ahead 2
        # R_new
        # The number of neighbors of n that are neither in the core_1 nor
        # T_1^{inout} is equal to the number of neighbors of m
        # that are neither in core_2 nor T_2^{inout}.
        num1 = 0
        for neighbor in self.G1.adj[G1_node]:
            if neighbor not in self.inout_1:
                num1 += 1
        num2 = 0
        for neighbor in self.G2.adj[G2_node]:
            if neighbor not in self.inout_2:
                num2 += 1
        return num1 == num2

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
        cdef set new_nodes
        cdef int node, neighbor
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
                new_nodes.update([neighbor for neighbor in GM.G1.adj[node] if neighbor not in GM.core_1])
            for node in new_nodes:
                if node not in GM.inout_1:
                    GM.inout_1[node] = self.depth
            
            # Updates for T_2^{inout}
            new_nodes = set([])
            for node in GM.core_2:
                new_nodes.update([neighbor for neighbor in GM.G2.adj[node] if neighbor not in GM.core_2])
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
        cdef dict vector
        cdef int node
        for vector in (self.GM.inout_1, self.GM.inout_2):
            for node in list(vector):
                if vector[node] == self.depth:
                    del vector[node]

cdef bool verify(Graph G, list answer):
    if not G.is_connected():
        #is not connected
        return True
    cdef Graph H
    for H in answer:
        if G.is_isomorphic(H):
            return True
    return False

cdef list connection_get(int i, tuple connection):
    cdef tuple c
    return [c for c in connection if (i in c)]

#Linkage Topological Component
cpdef topo(
    object link_num,
    bool degenerate=True,
    object setjobFunc=None,
    object stopFunc=None
):
    """
    link_num = [L2, L3, L4, ...]
    links = [
        [number_code]: joint_number,
        ...
    ]
    """
    
    cdef double t0 = time()
    cdef int joint_count = sum(link_num)
    cdef np.ndarray links = np.zeros((joint_count,), dtype=np.int32)
    cdef int i, j, t, name, link_joint_count
    for i in range(joint_count):
        name = i
        link_joint_count = 0
        for j, t in enumerate(link_num):
            if i < t:
                link_joint_count = j+2
                break
            i -= t
        links[name] = link_joint_count
    
    #connection = [(1, 2), (1, 3), ..., (2, 3), (2, 4), ...]
    cdef tuple connection = tuple(combinations(range(joint_count), 2))
    #ALL results.
    cdef list edges_combinations = []
    cdef int link, count, n
    cdef list match, matched
    cdef tuple m
    cdef Graph G, H
    cdef GraphMatcher GM_GH
    for link, count in enumerate(links):
        match = [Graph(m) for m in combinations(connection_get(link, connection), count)]
        if not edges_combinations:
            edges_combinations = match
            continue
        if setjobFunc:
            setjobFunc(
                "Match link #{} / {}".format(link, len(links)-1),
                len(edges_combinations)*len(match)
            )
        matched = []
        for G, H in product(edges_combinations, match):
            if stopFunc and stopFunc():
                return None, time()-t0
            G = G.compose(H)
            #Out of limit.
            if G.out_of_limit(links):
                continue
            #Has triangles.
            if degenerate and G.has_triangles():
                continue
            matched.append(G)
        edges_combinations = matched
    
    if setjobFunc:
        setjobFunc("Verify the graphs...", len(edges_combinations))
    cdef list answer = []
    for G in edges_combinations:
        if stopFunc and stopFunc():
            return answer, time()-t0
        if verify(G, answer):
            continue
        answer.append(G)
    return answer, time()-t0
