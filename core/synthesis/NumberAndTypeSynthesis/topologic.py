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
    is_isomorphic
)
from itertools import (
    combinations,
    product
)
from collections import Counter
from typing import Iterable

as_expression = lambda G: tuple("L[L{}, L{}]".format(l1, l2) for l1, l2 in G.edges)

class TestError(Exception):
    pass

def testG(G, answer):
    for G_ in answer:
        if is_isomorphic(G, G_):
            raise TestError("is isomorphic")

#Linkage Topological Component
def topo(iter: Iterable[int,]):
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
        for p1, p2 in product(edges_combinations, match):
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
    answer = []
    for edges in edges_combinations:
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
