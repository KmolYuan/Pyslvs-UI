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

from math import pi, sin, cos
from anytree import LevelOrderIter
from anytree.search import findall

#Return a function that can calculate coordinates by diameter.
def regular_polygons(sides: int, vertice_based: bool =False):
    angle_unit = 2*pi/sides
    angle_init = pi if vertice_based else (pi - angle_unit/2)
    
    def func(d: float):
        dots = []
        for i in range(sides):
            a = (angle_init + i*angle_unit)%360
            dots.append((round(d/2*cos(a), 4), round(d/2*sin(a), 4)))
        return dots
    
    return func

def circulation_allocation(root):
    deepest_node = list(LevelOrderIter(root))[-1]
    step_1 = deepest_node.path
    clone = findall(root, filter_=lambda n: n.name==deepest_node.name.replace('[', '').replace(']', ''))[0]
    step_2 = clone.path
    extern = len(step_1)-1 + len(step_2)-1
    return extern

if __name__=='__main__':
    #foo = regular_polygons(7)
    #print(foo(10))
    from topologic import topo, show_tree
    answer = topo([4, 2])
    for root, joints in answer:
        print(show_tree(root))
        print(circulation_allocation(root))
        print('-'*7)
