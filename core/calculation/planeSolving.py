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

from typing import List, Tuple
from math import cos, sin
from ..kernel.python_solvespace.slvs import (
    #System base
    System, groupNum, Slvs_MakeQuaternion,
    #Entities
    Point3d, Workplane, Normal3d, Point2d, LineSegment2d, Constraint,
    #Results
    SLVS_RESULT_OKAY, SLVS_RESULT_INCONSISTENT, SLVS_RESULT_DIDNT_CONVERGE, SLVS_RESULT_TOO_MANY_UNKNOWNS
)

def slvsProcess(
    Point: Tuple['VPoint'] =False,
    Link: Tuple['VLink'] =False,
    currentShaft: List[Tuple[int, float]] =(),
    hasWarning: bool =True
):
    pointCount = len(Point)
    sliderCount = sum([len(p.links)-1 for p in Point if p.type==1 or p.type==2])
    Sys = System(pointCount*2+sliderCount+15)
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
    p7 = Sys.add_param(0.)
    p8 = Sys.add_param(0.)
    Origin2D = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Origin2D)
    p9 = Sys.add_param(10.)
    p10 = Sys.add_param(0.)
    hp = Point2d(Workplane1, p9, p10)
    Constraint.dragged(Workplane1, hp)
    ground = LineSegment2d(Workplane1, Origin2D, hp)
    Sys.default_group = groupNum(2)
    Slvs_Points = []
    #Append all points first.
    for vpoint in Point:
        #This is the point recorded in the table.
        x = Sys.add_param(vpoint.cx)
        y = Sys.add_param(vpoint.cy)
        if vpoint.type==0:
            #Has only one pointer
            Slvs_Points.append(Point2d(Workplane1, x, y))
        elif vpoint.type==1 or vpoint.type==2:
            #Has one more pointer
            Slvs_Points.append(tuple(Point2d(Workplane1, x, y) for i in range(len(vpoint.links))))
    #Topology of PMKS points.
    LinkIndex = [vlink.name for vlink in Link]
    for i, vpoint in enumerate(Point):
        #P and RP Joint: If the point has a sliding degree of freedom.
        if vpoint.type==1 or vpoint.type==2:
            p_base = Slvs_Points[i][0]
            if vpoint.type==1:
                pass
        else:
            p_base = Slvs_Points[i]
        #Link to other points on the same link.
        for linkOrder, linkName in enumerate(vpoint.links):
            #If the joint is a slider, defined its base.
            if vpoint.type==1 or vpoint.type==2:
                p_base = Slvs_Points[i][linkOrder]
            else:
                p_base = Slvs_Points[i]
            #If this link is on the ground.
            if linkName=='ground':
                Constraint.dragged(Workplane1, p_base)
                continue
            relate = Link[LinkIndex.index(linkName)].points
            relateOrder = relate.index(i)
            if relateOrder==0:
                continue
            #Connect function:
            def ConnectTo(index):
                n = relate[index]
                p = Point[n]
                d = p.distance(vpoint)
                if p.type==1 or p.type==2:
                    p_contact = Slvs_Points[n][p.links.index(linkName)]
                else:
                    p_contact = Slvs_Points[n]
                Constraint.distance(d, Workplane1, p_contact, p_base)
            #Connect first point of this link.
            ConnectTo(0)
            #Conect the previous point.
            if relateOrder!=1:
                ConnectTo(relateOrder-1)
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
    '''
    result = Sys.solve()
    if result==SLVS_RESULT_OKAY:
        resultList = []
        for p in Slvs_Points:
            if type(p)==Point2d:
                resultList.append((round(p.u().value, 4), round(p.v().value, 4)))
            else:
                resultList.append(tuple((round(c.u().value, 4), round(c.v().value, 4)) for c in p))
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
        return [], resultSTR
