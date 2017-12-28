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

from dxfwrite import DXFEngine as dxf
from .elements import v_to_slvs

def dxfSketch(VPointList, VLinkList, fileName):
    edges = v_to_slvs(VPointList, VLinkList)
    mechanism = dxf.drawing(fileName)
    for vpoint in VPointList:
        mechanism.add(dxf.point((vpoint.cx, vpoint.cy)))
    for p1, p2 in edges:
        vp1 = VPointList[p1]
        vp2 = VPointList[p2]
        mechanism.add(dxf.line((vp1.cx, vp1.cy), (vp2.cx, vp2.cy)))
    mechanism.save()
