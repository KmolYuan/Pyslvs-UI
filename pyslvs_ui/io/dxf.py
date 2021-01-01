# -*- coding: utf-8 -*-

"""DXF output function.

+ Frame
+ Boundary
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence, Iterable, Callable, Dict, List
from math import degrees, atan2
import ezdxf
from ezdxf.lldxf.const import versions_supported_by_new, acad_release
from pyslvs import VPoint, VLink
from pyslvs_ui.graphics import convex_hull
from .slvs import boundary_loop

# A list of support versions with "ezdxf" module.
DXF_VERSIONS = versions_supported_by_new
DXF_VERSIONS_MAP = acad_release


def dxf_frame(
    vpoints: Sequence[VPoint],
    v_to_slvs: Callable[[], Iterable[Tuple[int, int]]],
    version: str,
    file_name: str
):
    """Create frame sketch only."""
    dwg = ezdxf.new(version)
    msp = dwg.modelspace()

    for p1, p2 in v_to_slvs():
        vp1 = vpoints[p1]
        vp2 = vpoints[p2]
        msp.add_line((vp1.cx, vp1.cy), (vp2.cx, vp2.cy))

    dwg.saveas(file_name)


def dxf_boundary(
    vpoints: Sequence[VPoint],
    radius: float,
    interval: float,
    version: str,
    file_name: str
):
    """Create parts sketch in same file."""
    vlinks: Dict[str, List[int]] = {}
    for i, vpoint in enumerate(vpoints):
        for link in vpoint.links:
            if link in vlinks:
                vlinks[link].append(i)
            else:
                vlinks[link] = [i]

    dwg = ezdxf.new(version)
    msp = dwg.modelspace()

    # _Interval: Offset with x axis.
    interval += radius * 2
    x_max = -interval

    # Draw link boundaries
    for name in sorted(
        vlinks,
        key=lambda n: min(vpoints[p].cx for p in vlinks[n])
    ):
        if name == VLink.FRAME:
            continue
        # Draw joint holes
        x_min = min(vpoints[p].cx for p in vlinks[name])

        centers = [(
            x_max + interval + (vpoints[p].cx - x_min),
            vpoints[p].cy
        ) for p in vlinks[name]]

        for coord in centers:
            msp.add_circle(coord, radius / 2)

        x_max = max(coord[0] for coord in centers)
        # Sort the centers
        centers_ch = convex_hull(centers)
        boundary = centers_ch.copy()
        for c in centers:
            if c not in centers_ch:
                centers_ch.append(c)
        centers = centers_ch

        # Draw boundary edges
        boundary = boundary_loop(boundary, radius)
        for c1, c2 in boundary:
            msp.add_line((c1.x, c1.y), (c2.x, c2.y))

        # Draw fillets
        for i in range(len(boundary)):
            x, y = centers[i]
            c1 = boundary[i - 1][1]
            c2 = boundary[i][0]
            msp.add_arc(
                centers[i],
                radius,
                degrees(atan2(c1.y - y, c1.x - x)),
                degrees(atan2(c2.y - y, c2.x - x))
            )

    dwg.saveas(file_name)
