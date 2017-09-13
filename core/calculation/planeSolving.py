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

from math import pi, cos, sin
from typing import List, Tuple
from ..kernel.python_solvespace.slvs import (
    System, groupNum, Slvs_MakeQuaternion,
    Point3d, Workplane, Normal3d, Point2d, LineSegment2d, Constraint,
    SLVS_RESULT_OKAY, SLVS_RESULT_INCONSISTENT, SLVS_RESULT_DIDNT_CONVERGE, SLVS_RESULT_TOO_MANY_UNKNOWNS)

def slvsProcess(
    Point: Tuple['VPoint'] =False,
    Link: Tuple['VLink'] =False,
    currentShaft: List[Tuple[int, float]] =(),
    hasWarning: bool =True
):
    Sys = System(len(Point)*2+2+9)
    Sys.default_group = groupNum(1)
    p0 = Sys.add_param(0.)
    p1 = Sys.add_param(0.)
    p2 = Sys.add_param(0.)
    Origin = Point3d(p0, p1, p2)
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = Sys.add_param(qw)
    p4 = Sys.add_param(qx)
    p5 = Sys.add_param(qy)
    p6 = Sys.add_param(qz)
    Workplane1 = Workplane(Origin, Normal3d(p3, p4, p5, p6))
    Sys.default_group = groupNum(2)
    Slvs_Points = []
    for vpoint in Point:
        x = Sys.add_param(vpoint.cx)
        y = Sys.add_param(vpoint.cy)
        p = Point2d(Workplane1, x, y)
        if 'ground' in vpoint.Links:
            Constraint.dragged(Workplane1, p)
        Slvs_Points.append(p)
    for vlink in Link[1:]:
        for i, p in enumerate(vlink.Points):
            if i==0:
                continue
            d = Point[vlink.Points[0]].distance(Point[p])
            Constraint.distance(d, Workplane1, Slvs_Points[vlink.Points[0]], Slvs_Points[p])
            if not i==1:
                d = Point[p-1].distance(Point[p])
                Constraint.distance(d, Workplane1, Slvs_Points[p-1], Slvs_Points[p])
    
    def setShaft(shaft, angle):
        '''
        shaft: int
        angle: float, int (degrees)
        '''
        mx = round(Point[shaft].cx+10*cos(angle*pi/180), 8)
        my = round(Point[shaft].cy+10*sin(angle*pi/180), 8)
        x = Sys.add_param(mx if mx!=0 else 0.)
        y = Sys.add_param(my if my!=0 else 0.)
        leader = Point2d(Workplane1, x, y)
        Constraint.dragged(Workplane1, leader)
        Line0 = LineSegment2d(Workplane1, Slvs_Points[shaft], leader)
        #Another point on specified link
        for i in range(len(Point[shaft].Links)):
            linkRef = list(set(Point[shaft].Links[i])-{i})[0]
            Constraint.angle(Workplane1, .5, LineSegment2d(Workplane1, Slvs_Points[shaft], Slvs_Points[linkRef]), Line0)
    
    for shaft in currentShaft:
        setShaft(*shaft)
    result = Sys.solve()
    if result==SLVS_RESULT_OKAY:
        resultList = []
        for i in range(0, len(Point)*2, 2):
            resultList.append((round(float(Sys.get_param(i+7).val), 4), round(float(Sys.get_param(i+8).val), 4)))
        return resultList, int(Sys.dof)
    else:
        if result==SLVS_RESULT_INCONSISTENT:
            if hasWarning:
                print("SLVS_RESULT_INCONSISTENT")
            resultSTR = "Inconsistent"
        elif result==SLVS_RESULT_DIDNT_CONVERGE:
            if hasWarning:
                print("SLVS_RESULT_DIDNT_CONVERGE")
            resultSTR = "Didn't Converge"
        elif result==SLVS_RESULT_TOO_MANY_UNKNOWNS:
            if hasWarning:
                print("SLVS_RESULT_TOO_MANY_UNKNOWNS")
            resultSTR = "Too Many Unknowns"
        return tuple(), resultSTR
