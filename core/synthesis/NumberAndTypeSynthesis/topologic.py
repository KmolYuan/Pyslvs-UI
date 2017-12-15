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
    compose,
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

def testT(G, degenerate):
    if degenerate:
        if not all(n==0 for n in triangles(G).values()):
            raise TestError("has triangle")

def testG(G, answer):
    if not is_connected(G):
        raise TestError("is not connected")
    for G_ in answer:
        if is_isomorphic(G, G_):
            raise TestError("is isomorphic")

#TODO: The function must be accelerated.
#Linkage Topological Component
def topo(iter: Iterable[int,], degenerate: bool, setjobFunc=lambda j, i:None, stopFunc=lambda: False):
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
    edges_combinations = []
    for link, count in links.items():
        match = [Graph(m) for m in combinations(connection_get(link), count)]
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
            if error:
                continue
            if degenerate and not all(n==0 for n in triangles(G).values()):
                continue
            match_.append(G)
        if not edges_combinations:
            edges_combinations = match
        else:
            edges_combinations = match_
    setjobFunc("Verify the graphs...", len(edges_combinations))
    answer = []
    for G in edges_combinations:
        if stopFunc():
            return
        try:
            testG(G, answer)
        except TestError:
            continue
        answer.append(G)
    return answer

if __name__=='__main__':
    print("Topologic test")
    answer = topo([4, 2], degenerate=True)
    #Show tree
    for G in answer:
        print(G.edges)
        print('-'*7)
    print("Answer count: {}".format(len(answer)))
