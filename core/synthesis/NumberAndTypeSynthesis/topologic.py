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

from anytree import Node, RenderTree
from anytree.search import findall
from collections import Counter
from itertools import permutations
from typing import Tuple

show_tree = lambda root: '\n'.join("{}{}({})".format(pre, n.name, n.limit) for pre, fill, n in RenderTree(root))
show_joint = lambda root: Counter([tuple(sorted(([n.parent.limit] if n.parent else [])+[int(c.limit) for c in n.children])) for n in findall(root, filter_=lambda n: '[' not in n.name)])

#Linkage Topological Component
def topo(iter: Tuple[int,]):
    link_type = []
    for i, num in enumerate(iter):
        i += 2
        for j in range(num):
            link_type.append(i)
    answer = []
    for all_link in list(set(permutations(link_type))):
        all_link = [Node("L{}".format(i), limit=v) for i, v in enumerate(all_link)]
        links = []
        #Root
        links.append(all_link.pop(0))
        #First connect.
        while all_link:
            #Let all of links to connect.
            link = all_link.pop(0)
            if (len(links[-1].children) + bool(links[-1].parent))==links[-1].limit:
                links.append(links[-1].children[0])
            link.parent = links[-1]
        #Decided the remaining connection.
        get_no_done = lambda: findall(links[0], filter_=lambda n: '[' not in n.name and (len(n.children) + bool(links[-1].parent)) < n.limit)
        error = False
        while get_no_done():
            nodes = get_no_done()
            try:
                l_1, l_2 = nodes[0], nodes[1]
            except (ValueError, IndexError):
                error = True
                break
            else:
                Node("[{}]".format(l_1.name), limit=str(l_1.limit), parent=l_2)
                Node("[{}]".format(l_2.name), limit=str(l_2.limit), parent=l_1)
        if error:
            continue
        joints = show_joint(links[0])
        if joints in [a[1] for a in answer]:
            continue
        if findall(links[0], filter_=lambda n: len(n.children)!=len(set(c.name.replace('[', '').replace(']', '') for c in n.children))):
            continue
        answer.append((links[0], joints))
    return answer

if __name__=='__main__':
    print("Topologic test")
    answer = topo([4, 2])
    #Show tree
    for root, joints in answer:
        print(show_tree(root))
        print('-'*7)
    print("Answer count: {}".format(len(answer)))
