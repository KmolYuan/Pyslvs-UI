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
from ezdxf.lldxf.const import (
    versions_supported_by_new,
    acad_release,
)
from core.libs import VPoint
from .slvs import boundaryloop


#A list of support versions with "ezdxf" module.
DXF_VERSIONS = versions_supported_by_new
DXF_VERSIONS_MAP = acad_release


def dxf_frame(
    vpoints: Sequence[VPoint],
    v_to_slvs: Callable[[], Tuple[int, int]],
    version: str,
    file_name: str
):
    """Create frame sketch only."""
    dwg = ezdxf.new(version)
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
    version: str,
    file_name: str
):
    """Create parts sketch in same file."""
    vlinks = {}
    for i, vpoint in enumerate(vpoints):
        for link in vpoint.links:
            if link in vlinks:
                vlinks[link].append(i)
            else:
                vlinks[link] = [i]
    
    dwg = ezdxf.new(version)
    msp = dwg.modelspace()
    
    for link_name in sorted(vlinks, key=lambda name: len(vlinks[name])):
        #TODO: Draw linkage boundaries.
        pass
    
    dwg.saveas(file_name)
