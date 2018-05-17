# -*- coding: utf-8 -*-

"""DXF output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from dxfwrite import DXFEngine as dxf
from typing import Tuple, Sequence, Callable
from core.libs import VPoint


def dxfSketch(
    VPointList: Sequence[VPoint],
    v_to_slvs: Callable[[], Tuple[int, int]],
    file_name: str
):
    """Using DXF write to create sketch."""
    mechanism = dxf.drawing(file_name)
    for vpoint in VPointList:
        mechanism.add(dxf.point((vpoint.cx, vpoint.cy)))
    for p1, p2 in v_to_slvs():
        vp1 = VPointList[p1]
        vp2 = VPointList[p2]
        mechanism.add(dxf.line((vp1.cx, vp1.cy), (vp2.cx, vp2.cy)))
    mechanism.save()
