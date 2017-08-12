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
from ..kernel.python_solvespace.slvs import (System, Slvs_MakeQuaternion,
    Point3d, Workplane, Normal3d, Point2d, LineSegment2d, Constraint,
    SLVS_RESULT_OKAY, SLVS_RESULT_INCONSISTENT, SLVS_RESULT_DIDNT_CONVERGE, SLVS_RESULT_TOO_MANY_UNKNOWNS)

def slvsProcess(Point=False, Line=False, Chain=False, Shaft=False, Slider=False, Rod=False,
        currentShaft=0, currentAngle=False, hasWarning=True):
    pathTrackProcess = not(Point is False) and not currentAngle is False
    staticProcess = not(Point is False) and currentAngle is False
    Sys = System(len(Point)*2+len(Shaft)*2+9)
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
    Point0 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point0)
    Slvs_Points = [Point0]
    for e in Point[1:]:
        x = Sys.add_param(e.cx)
        y = Sys.add_param(e.cy)
        p = Point2d(Workplane1, x, y)
        if e.fix:
            Constraint.dragged(Workplane1, p)
        Slvs_Points.append(p)
    for e in Chain:
        Constraint.distance(e.p1p2, Workplane1, Slvs_Points[e.p1], Slvs_Points[e.p2])
        Constraint.distance(e.p2p3, Workplane1, Slvs_Points[e.p2], Slvs_Points[e.p3])
        Constraint.distance(e.p1p3, Workplane1, Slvs_Points[e.p1], Slvs_Points[e.p3])
    for e in Line:
        Constraint.distance(e.len, Workplane1, Slvs_Points[e.start], Slvs_Points[e.end])
    for e in Slider:
        Constraint.on(Workplane1, Slvs_Points[e.cen], LineSegment2d(Workplane1, Slvs_Points[e.start], Slvs_Points[e.end]))
    for e in Rod:
        Constraint.on(Workplane1, Slvs_Points[e.cen], LineSegment2d(Workplane1, Slvs_Points[e.start], Slvs_Points[e.end]))
        Constraint.distance(e.pos, Workplane1, Slvs_Points[e.start], Slvs_Points[e.cen])
    def setShaft(e, angle):
        lines = [e.cen==l.start and e.ref==l.end or e.cen==l.end and e.ref==l.start for l in Line]
        if True in lines:
            d0 = Line[lines.index(True)].len
        else:
            d0 = ((Point[e.cen].cx-Point[e.ref].cx)**2+(Point[e.cen].cy-Point[e.ref].cy)**2)**(1/2)
        mx = round(d0*cos(angle*pi/180)+Point[e.cen].cx, 8)
        my = round(d0*sin(angle*pi/180)+Point[e.cen].cy, 8)
        x = Sys.add_param(mx if mx!=0 else 0.)
        y = Sys.add_param(my if my!=0 else 0.)
        moving = Point2d(Workplane1, x, y)
        Constraint.dragged(Workplane1, moving)
        Line0 = LineSegment2d(Workplane1, Slvs_Points[e.cen], moving)
        Constraint.angle(Workplane1, .5, LineSegment2d(Workplane1, Slvs_Points[e.cen], Slvs_Points[e.ref]), Line0)
    if pathTrackProcess:
        setShaft(Shaft[currentShaft], currentAngle)
    elif staticProcess:
        for e in Shaft:
            setShaft(e, e.demo)
    result = Sys.solve()
    if result==SLVS_RESULT_OKAY:
        resultList = [{'x':0., 'y':0.}]
        for i in range(2, len(Point)*2, 2):
            resultList.append({'x':round(float(Sys.get_param(i+7).val), 4), 'y':round(float(Sys.get_param(i+8).val), 4)})
        if pathTrackProcess:
            return resultList
        elif staticProcess:
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
        if pathTrackProcess:
            return [{'x':False, 'y':False} for i in range(len(Point))]
        elif staticProcess:
            return list(), resultSTR
