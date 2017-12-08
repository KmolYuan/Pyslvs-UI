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

from networkx import (
    Graph,
    is_isomorphic,
    find_cycle
)
from itertools import permutations
from typing import Iterable

as_expression = lambda G: tuple("L[{}, {}]".format(l1, l2) for l1, l2 in G.edges)

class TestError(Exception):
    pass

def testG(G_base, answer):
    G = Graph(G_base)
    for G_ in answer:
        if is_isomorphic(G, G_):
            raise TestError()
    while G:
        c = find_cycle(G)
        if len(c)==3:
            print(c)
            raise TestError()
        G.remove_edges_from(c)

#Linkage Topological Component
def topo(iter: Iterable[int,]):
    link_type = []
    for i, num in enumerate(iter):
        i += 2
        for j in range(num):
            link_type.append(i)
    answer = []
    for all_link in [list(e) for e in set(permutations(link_type))]:
        edges = []
        #Matching
        for i in range(len(all_link)):
            j = i
            while all_link[i]:
                j += 1
                if all_link[j%len(all_link)] and ({i, j} not in edges):
                    all_link[i] -= 1
                    edges.append({i, j})
        G = Graph()
        G.add_edges_from(edges)
        try:
            testG(G, answer)
        except TestError:
            continue
        answer.append(G)
    return answer

if __name__=='__main__':
    print("Topologic test")
    answer = topo([4, 2])
    #Show tree
    for G in answer:
        print(as_expression(G))
        print('-'*7)
    print("Answer count: {}".format(len(answer)))
