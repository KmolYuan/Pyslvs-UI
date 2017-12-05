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
from itertools import permutations
from typing import Tuple

def show_tree(node, noname=False):
    if noname:
        string = '\n'.join("{}{}".format(pre, n.limit) for pre, fill, n in RenderTree(node))
    else:
        string = '\n'.join("{}{}({})".format(pre, n.name, n.limit) for pre, fill, n in RenderTree(node))
    return string

#Linkage Topological Component
def make_link(iter: Tuple[int,]):
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
            nodes = list(get_no_done())
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
        if findall(links[0], filter_=lambda n: len([c.name for c in n.children])!=len(set(c.name for c in n.children))):
            continue
        answer.append(links[0])
    return answer

if __name__=='__main__':
    print("Topologic test")
    answer = make_link([5, 4])
    #Show tree
    for root in answer:
        print(show_tree(root))
        print('-'*7)
    print("Answer count: {}".format(len(answer)))
