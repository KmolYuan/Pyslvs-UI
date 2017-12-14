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
    triangles,
    is_connected,
    is_isomorphic
)
from itertools import (
    combinations,
    product
)
from collections import Counter
from typing import Iterable

class TestError(Exception):
    pass

def testG(G, answer, degenerate):
    if degenerate:
        if not all(n==0 for n in triangles(G).values()):
            raise TestError("has triangle")
    if not is_connected(G):
        raise TestError("is not connected")
    for G_ in answer:
        if is_isomorphic(G, G_):
            raise TestError("is isomorphic")

#TODO: The function must be accelerated.
#Linkage Topological Component
def topo(iter: Iterable[int,], degenerate: bool =True, setjobFunc=lambda j, i:None, stopFunc=lambda: False):
    links = Counter()
    for i in range(sum(iter)):
        name = i
        joint_count = 0
        for j, t in enumerate(iter):
            if i < t:
                joint_count = j+2
                break
            i -= t
        links[name] = joint_count
    connection = list(combinations(range(sum(iter)), 2))
    connection_get = lambda i, limit=(): (c for c in connection if (i in c) and all(l not in c for l in limit))
    edges_combinations = set()
    for link, count in links.items():
        match = set(combinations(connection_get(link), count))
        m = set()
        prod = list(product(edges_combinations, match))
        setjobFunc("Match link #{}".format(link), len(prod))
        for p1, p2 in prod:
            if stopFunc():
                return
            combin = tuple(set(p1)|set(p2))
            error = False
            for link, count in links.items():
                if sum((link in c) for c in combin)>count:
                    error = True
                    break
            if error:
                continue
            m.add(combin)
        if not edges_combinations:
            edges_combinations = match
        else:
            edges_combinations = m
    setjobFunc("Verify the graphs...", len(edges_combinations))
    answer = []
    for edges in edges_combinations:
        if stopFunc():
            return
        G = Graph()
        G.add_edges_from(edges)
        try:
            testG(G, answer, degenerate)
        except TestError:
            continue
        answer.append(G)
    return answer

if __name__=='__main__':
    print("Topologic test")
    answer = topo([4, 2])
    #Show tree
    for G in answer:
        print(G.edges)
        print('-'*7)
    print("Answer count: {}".format(len(answer)))
