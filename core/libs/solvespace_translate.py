# -*- coding: utf-8 -*-

"""This module contains the Python-Solvespace simulation functions."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Sequence,
    Dict,
    Union,
)
from math import radians, cos, sin
from pyslvs import (
    get_vlinks,
    VJoint,
    VPoint,
    VLink,
)
from python_solvespace import ResultFlag, Entity, SolverSystem

_Coord = Tuple[float, float]


def slvs_solve(
    vpoints: Sequence[VPoint],
    inputs: Dict[Tuple[int, int], float]
) -> Tuple[List[Union[_Coord, Tuple[_Coord, _Coord]]], int]:
    """Use element module to convert into solvespace expression."""
    if not vpoints:
        return [], 0

    vlinks: Dict[str, VLink] = {vlink.name: vlink for vlink in get_vlinks(vpoints)}

    # Solvespace kernel
    sys = SolverSystem()
    sys.set_group(1)
    wp = sys.create_2d_base()
    origin_2d = sys.add_point_2d(0., 0., wp)
    sys.dragged(origin_2d, wp)
    origin_2d_p = sys.add_point_2d(10., 0., wp)
    sys.dragged(origin_2d_p, wp)
    hv = sys.add_line_2d(origin_2d, origin_2d_p, wp)
    sys.set_group(2)

    points: List[Entity] = []
    sliders: Dict[int, int] = {}
    slider_bases: List[Entity] = []
    slider_slots: List[Entity] = []

    for i, vpoint in enumerate(vpoints):
        if vpoint.no_link():
            x, y = vpoint.c[0]  # type: float
            point = sys.add_point_2d(x, y, wp)
            sys.dragged(point, wp)
            points.append(point)
            continue

        if vpoint.grounded():
            x, y = vpoint.c[0]
            if vpoint.type in {VJoint.P, VJoint.RP}:
                sliders[i] = len(slider_bases)
                # Base point (slot) is fixed.
                point = sys.add_point_2d(x, y, wp)
                sys.dragged(point, wp)
                slider_bases.append(point)
                # Slot point (slot) is movable.
                x += cos(vpoint.angle)
                y += sin(vpoint.angle)
                slider_slots.append(sys.add_point_2d(x, y, wp))
                # Pin is movable.
                x, y = vpoint.c[1]
                if vpoint.has_offset() and vpoint.true_offset() <= 0.1:
                    if vpoint.offset() > 0:
                        x += 0.1
                        y += 0.1
                    else:
                        x -= 0.1
                        y -= 0.1
                points.append(sys.add_point_2d(x, y, wp))
            else:
                point = sys.add_point_2d(x, y, wp)
                sys.dragged(point, wp)
                points.append(point)
            continue

        x, y = vpoint.c[0]
        point = sys.add_point_2d(x, y, wp)
        if vpoint.type in {VJoint.P, VJoint.RP}:
            sliders[i] = len(slider_bases)
            # Base point (slot) is movable.
            slider_bases.append(point)
            # Slot point (slot) is movable.
            x += cos(vpoint.angle)
            y += sin(vpoint.angle)
            slider_slots.append(sys.add_point_2d(x, y, wp))
            if vpoint.pin_grounded():
                # Pin is fixed.
                x, y = vpoint.c[1]
                point = sys.add_point_2d(x, y, wp)
                sys.dragged(point, wp)
                points.append(point)
            else:
                # Pin is movable.
                x, y = vpoint.c[1]
                if vpoint.has_offset() and vpoint.true_offset() <= 0.1:
                    if vpoint.offset() > 0:
                        x += 0.1
                        y += 0.1
                    else:
                        x -= 0.1
                        y -= 0.1
                points.append(sys.add_point_2d(x, y, wp))
            continue

        # Point is movable.
        points.append(point)

    for vlink in vlinks.values():
        if len(vlink.points) < 2:
            continue
        if vlink.name == 'ground':
            continue

        a = vlink.points[0]
        b = vlink.points[1]
        vp1 = vpoints[a]
        vp2 = vpoints[b]
        if vp1.is_slot_link(vlink.name):
            p1 = slider_bases[sliders[a]]
        else:
            p1 = points[a]
        if vp2.is_slot_link(vlink.name):
            p2 = slider_bases[sliders[b]]
        else:
            p2 = points[b]
        sys.distance(p1, p2, vp1.distance(vp2), wp)

        for c in vlink.points[2:]:  # type: int
            for d in (a, b):
                vp1 = vpoints[c]
                vp2 = vpoints[d]
                if vp1.is_slot_link(vlink.name):
                    p1 = slider_bases[sliders[c]]
                else:
                    p1 = points[c]
                if vp2.is_slot_link(vlink.name):
                    p2 = slider_bases[sliders[d]]
                else:
                    p2 = points[d]
                sys.distance(p1, p2, vp1.distance(vp2), wp)

    for a, b in sliders.items():
        # Base point
        vp1 = vpoints[a]
        p1 = points[a]
        # Base slot
        slider_slot = sys.add_line_2d(slider_bases[b], slider_slots[b], wp)
        if vp1.grounded():
            # Slot is grounded.
            sys.angle(hv, slider_slot, vp1.angle, wp)
            sys.coincident(p1, slider_slot, wp)
            if vp1.has_offset():
                p2 = slider_bases[b]
                if vp1.offset():
                    sys.distance(p2, p1, vp1.offset(), wp)
                else:
                    sys.coincident(p2, p1, wp)
        else:
            # Slider between links.
            for name in vp1.links[:1]:  # type: str
                vlink = vlinks[name]
                # A base link friend.
                c = vlink.points[0]
                if c == a:
                    if len(vlink.points) < 2:
                        # If no any friend.
                        continue
                    c = vlink.points[1]

                vp2 = vpoints[c]
                if vp2.is_slot_link(vlink.name):
                    # c is a slider, and it is be connected with slot link.
                    p2 = slider_bases[sliders[c]]
                else:
                    # c is a R joint or it is not connected with slot link.
                    p2 = points[c]
                sys.angle(
                    slider_slot,
                    sys.add_line_2d(slider_bases[b], p2, wp),
                    vp1.slope_angle(vp2) - vp1.angle,
                    wp
                )
                sys.coincident(p1, slider_slot, wp)

                if vp1.has_offset():
                    p2 = slider_bases[b]
                    if vp1.offset():
                        sys.distance(p2, p1, vp1.offset(), wp)
                    else:
                        sys.coincident(p2, p1, wp)

            if vp1.type != VJoint.P:
                continue

            for name in vp1.links[1:]:
                vlink = vlinks[name]
                # A base link friend.
                c = vlink.points[0]
                if c == a:
                    if len(vlink.points) < 2:
                        # If no any friend.
                        continue
                    c = vlink.points[1]

                vp2 = vpoints[c]
                if vp2.is_slot_link(vlink.name):
                    # c is a slider, and it is be connected with slot link.
                    p2 = slider_bases[sliders[c]]
                else:
                    # c is a R joint or it is not connected with slot link.
                    p2 = points[c]
                sys.angle(
                    slider_slot,
                    sys.add_line_2d(p1, p2, wp),
                    vp1.slope_angle(vp2) - vp1.angle,
                    wp
                )

    for (b, d), angle in inputs.items():
        # The constraints of drive shaft.
        # Simulate the input variables to the mechanism.
        # The 'base points' are shaft center.
        if b == d:
            continue

        vp1 = vpoints[b]
        if vp1.type == VJoint.R:
            p1 = points[b]
        else:
            p1 = slider_bases[sliders[b]]

        angle = radians(angle)
        p2 = sys.add_point_2d(vp1.cx + cos(angle), vp1.cy + sin(angle), wp)
        sys.dragged(p2, wp)
        # The virtual link that dragged by "hand".
        leader = sys.add_line_2d(p1, p2, wp)
        # Make another virtual link that should follow "hand".
        vp2 = vpoints[d]
        if vp2.type == VJoint.R:
            p2 = points[d]
        else:
            p2 = slider_bases[sliders[d]]
        link = sys.add_line_2d(p1, p2, wp)
        sys.angle(link, leader, 0.5, wp)

    # Solve
    result_flag = sys.solve()
    if result_flag == ResultFlag.OKAY:
        result_list = []
        for i, vpoint in enumerate(vpoints):
            p1 = points[i]
            x1, y1 = sys.params(p1.params)
            if vpoint.type == VJoint.R:
                result_list.append((x1, y1))
            else:
                p2 = slider_bases[sliders[i]]
                x2, y2 = sys.params(p2.params)
                result_list.append(((x2, y2), (x1, y1)))
        return result_list, sys.dof()

    if result_flag == ResultFlag.INCONSISTENT:
        error = "inconsistent"
    elif result_flag == ResultFlag.DIDNT_CONVERGE:
        error = "didn't converge"
    else:
        error = "too many unknowns"
    error += f": {sys.faileds()}\n{sys.constraints()}"
    raise ValueError(error)
