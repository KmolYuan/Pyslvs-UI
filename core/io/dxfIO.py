# -*- coding: utf-8 -*-

"""DXF output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from dxfwrite import DXFEngine as dxf
from .elements import v_to_slvs

def dxfSketch(VPointList, VLinkList, fileName):
    """Using DXF write to create sketch."""
    edges = v_to_slvs(VPointList, VLinkList)
    mechanism = dxf.drawing(fileName)
    for vpoint in VPointList:
        mechanism.add(dxf.point((vpoint.cx, vpoint.cy)))
    for p1, p2 in edges:
        vp1 = VPointList[p1]
        vp2 = VPointList[p2]
        mechanism.add(dxf.line((vp1.cx, vp1.cy), (vp2.cx, vp2.cy)))
    mechanism.save()
