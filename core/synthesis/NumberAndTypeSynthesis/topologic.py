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
from random import randint, sample
from typing import Tuple

def show_tree(node, noname=False):
    if noname:
        string = '\n'.join("{}{}".format(pre, n.limit) for pre, fill, n in RenderTree(node))
    else:
        string = '\n'.join("{}{}({})".format(pre, n.name, n.limit) for pre, fill, n in RenderTree(node))
    return string

#Linkage Topological Component
def make_link(iter: Tuple[int,]):
    all_link = []
    for i, num in enumerate(iter):
        i += 2
        for j in range(num):
            all_link.append(Node("L{}".format(len(all_link)), limit=i, space=i))
    link_old = []
    #Root
    link_old.append(all_link.pop(randint(0, len(all_link)-1)))
    #First connect.
    while all_link:
        #Let all of links to connect.
        link = all_link.pop(randint(0, len(all_link)-1))
        if len(link_old[-1].children)==link_old[-1].limit:
            link_old.append(link_old[-1].children[0])
        link.parent = link_old[-1]
    del all_link
    for node in link_old:
        node.space = node.limit - len(node.children)
    #Decided the remaining connection.
    get_no_done = lambda: findall(link_old[0], filter_=lambda n: len(n.children)<n.space)
    while get_no_done():
        nodes = list(get_no_done())
        try:
            l_1, l_2 = sample(nodes, 2)
        except ValueError:
            raise ValueError("Loop does not close.")
        else:
            l_1.space -= 1
            l_2.space -= 1
            Node(l_1.name, limit=l_1.limit, space=-1, parent=l_2)
            Node(l_2.name, limit=l_2.limit, space=-1, parent=l_1)
    return link_old[0]

if __name__=='__main__':
    print("Topologic test")
    root = None
    while not root:
        try:
            root = make_link([5, 4])
        except ValueError:
            continue
    #Show tree
    print(show_tree(root))
