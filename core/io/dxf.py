# -*- coding: utf-8 -*-

"""DXF output function.

+ Frame
+ Boundary
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence, Callable
import ezdxf
from core.libs import VPoint


def dxf_frame(
    vpoints: Sequence[VPoint],
    v_to_slvs: Callable[[], Tuple[int, int]],
    file_name: str
):
    """Create frame sketch only."""
    dwg = ezdxf.new('AC1015')
    msp = dwg.modelspace()
    for vpoint in vpoints:
        msp.add_point((vpoint.cx, vpoint.cy))
    for p1, p2 in v_to_slvs():
        vp1 = vpoints[p1]
        vp2 = vpoints[p2]
        msp.add_line((vp1.cx, vp1.cy), (vp2.cx, vp2.cy))
    dwg.saveas(file_name)

def dxf_boundary(
    vpoints: Sequence[VPoint],
    file_name: str
):
    """TODO: Create parts sketch in same file."""
