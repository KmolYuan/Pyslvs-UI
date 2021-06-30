# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, Tuple, List, Sequence, Set, Dict, Union, Optional, Any
from math import radians, cos, sin
from abc import ABC, abstractmethod
from traceback import format_exc
from qtpy.QtCore import Slot
from pyslvs import (
    edges_view,
    graph2vpoints,
    t_config,
    get_vlinks,
    VJoint,
    VPoint,
    VLink,
    expr_solving,
    vpoint_dof,
    SolverSystem,
    EStack,
)
from pyslvs.graph import Graph
from pyslvs_ui.info import logger, HAS_SLVS, Kernel
from .entities import EntitiesMethodInterface

if HAS_SLVS:
    from python_solvespace import ResultFlag, Entity, SolverSystem as PySolver
_Coord = Tuple[float, float]
_Inputs = Dict[Tuple[int, int], float]


def _offset(p: VPoint) -> _Coord:
    """Make offset coordinate."""
    x = p.c[1, 0]
    y = p.c[1, 1]
    if p.has_offset() and p.true_offset() <= 0.1:
        if p.offset() > 0:
            x += 0.1
            y += 0.1
        else:
            x -= 0.1
            y -= 0.1
    return x, y


def _slvs_solve(
    vpoints: Sequence[VPoint],
    inputs: Dict[Tuple[int, int], float]
) -> Tuple[List[Union[_Coord, Tuple[_Coord, _Coord]]], int]:
    """Use element module to convert into Solvespace expression."""
    if not vpoints:
        return [], 0
    # VLinks with strings
    vlinks = {}
    for vlink in get_vlinks(vpoints):
        vlinks[vlink.name] = vlink
    # Solvespace kernel
    sys = PySolver()
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
            x = vpoint.c[0, 0]
            y = vpoint.c[0, 1]
            point = sys.add_point_2d(x, y, wp)
            sys.dragged(point, wp)
            points.append(point)
            continue
        if vpoint.grounded():
            x = vpoint.c[0, 0]
            y = vpoint.c[0, 1]
            if vpoint.type in {VJoint.P, VJoint.RP}:
                sliders[i] = len(slider_bases)
                # Base point (slot) is fixed
                point = sys.add_point_2d(x, y, wp)
                sys.dragged(point, wp)
                slider_bases.append(point)
                # Slot point (slot) is movable
                x += cos(vpoint.angle)
                y += sin(vpoint.angle)
                slider_slots.append(sys.add_point_2d(x, y, wp))
                # Pin is movable
                x, y = _offset(vpoint)
                points.append(sys.add_point_2d(x, y, wp))
            else:
                point = sys.add_point_2d(x, y, wp)
                sys.dragged(point, wp)
                points.append(point)
            continue
        x = vpoint.c[0, 0]
        y = vpoint.c[0, 1]
        point = sys.add_point_2d(x, y, wp)
        if vpoint.type in {VJoint.P, VJoint.RP}:
            sliders[i] = len(slider_bases)
            # Base point (slot) is movable
            slider_bases.append(point)
            # Slot point (slot) is movable
            x += cos(vpoint.angle)
            y += sin(vpoint.angle)
            slider_slots.append(sys.add_point_2d(x, y, wp))
            if vpoint.pin_grounded():
                # Pin is fixed
                x = vpoint.c[1, 0]
                y = vpoint.c[1, 1]
                point = sys.add_point_2d(x, y, wp)
                sys.dragged(point, wp)
                points.append(point)
            else:
                # Pin is movable
                x, y = _offset(vpoint)
                points.append(sys.add_point_2d(x, y, wp))
            continue
        # Point is movable
        points.append(point)

    def pick_slider(i1: int, i2: int) -> Tuple[Entity, Entity, float]:
        n1 = vpoints[i1]
        n2 = vpoints[i2]
        if n1.is_slot_link(vlink.name):
            e1 = slider_bases[sliders[i1]]
        else:
            e1 = points[i1]
        if n2.is_slot_link(vlink.name):
            e2 = slider_bases[sliders[i2]]
        else:
            e2 = points[i2]
        return e1, e2, n1.distance(n2)

    for vlink in vlinks.values():
        if len(vlink.points) < 2:
            continue
        if vlink.name == VLink.FRAME:
            continue
        a = vlink.points[0]
        b = vlink.points[1]
        p1, p2, d = pick_slider(a, b)
        sys.distance(p1, p2, d, wp)
        for c in vlink.points[2:]:
            for d in (a, b):
                p1, p2, x = pick_slider(c, d)
                sys.distance(p1, p2, x, wp)

    def get_friend(group: VLink, base: int) -> Optional[Tuple[VPoint, Entity]]:
        """Get friend for slider."""
        # A base link friend
        index = group.points[0]
        if index == base:
            if len(group.points) < 2:
                # If no any friend
                return None
            index = group.points[1]
        vp = vpoints[index]
        if vp.is_slot_link(group.name):
            # c is a slider, and it is be connected with slot link.
            return vp, slider_bases[sliders[index]]
        else:
            # c is a R joint or it is not connected with slot link
            return vp, points[index]

    for a, b in sliders.items():
        # Base point
        vp1 = vpoints[a]
        p1 = points[a]
        # Base slot
        slider_slot = sys.add_line_2d(slider_bases[b], slider_slots[b], wp)
        if vp1.grounded():
            # Slot is grounded
            sys.angle(hv, slider_slot, vp1.angle, wp)
            sys.coincident(p1, slider_slot, wp)
            if vp1.has_offset():
                p2 = slider_bases[b]
                if vp1.offset():
                    sys.distance(p2, p1, vp1.offset(), wp)
                else:
                    sys.coincident(p2, p1, wp)
        else:
            # Slider between links
            for name in vp1.links[:1]:
                vlink = vlinks[name]
                ret = get_friend(vlink, a)
                if ret is None:
                    continue
                vp2, p2 = ret
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
                ret = get_friend(vlink, a)
                if ret is None:
                    continue
                vp2, p2 = ret
                sys.angle(
                    slider_slot,
                    sys.add_line_2d(p1, p2, wp),
                    vp1.slope_angle(vp2) - vp1.angle,
                    wp
                )
    for (b, d), angle in inputs.items():
        # The constraints of drive shaft
        # Simulate the input variables to the mechanism
        # The 'base points' are shaft center
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
        result_list: List[Union[_Coord, Tuple[_Coord, _Coord]]] = []
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
    raise ValueError(f"{error}: {sys.failures()}\n{sys.constraints()}")


class SolverMethodInterface(EntitiesMethodInterface, ABC):
    """Abstract class for solver methods."""

    @abstractmethod
    def __init__(self):
        super(SolverMethodInterface, self).__init__()
        self.__dof = 0

    def get_back_position(self) -> None:
        """Make current position back."""
        self.entities_point.get_back_position()
        for vpoint in self.vpoint_list:
            vpoint.move((vpoint.x, vpoint.y))

    def solve(self) -> None:
        """Resolve coordinates and preview path."""
        self.resolve()
        self.main_canvas.update_preview_path()

    @Slot()
    def resolve(self) -> None:
        """Resolve: Using three libraries to solve the system.

        + Pyslvs
        + Python-Solvespace
        + Sketch Solve
        """
        for b, d, a in self.inputs_widget.input_pairs():
            if b == d:
                self.vpoint_list[b].set_offset(a)
        solve_kernel = self.prefer.planar_solver_option
        input_pair = {(b, d): a for b, d, a in self.inputs_widget.input_pairs()}
        try:
            if solve_kernel == Kernel.PYSLVS:
                result = expr_solving(
                    self.get_triangle(),
                    self.vpoint_list,
                    input_pair
                )
            elif solve_kernel == Kernel.SOLVESPACE:
                result, _ = _slvs_solve(
                    self.vpoint_list,
                    input_pair if not self.free_move_btn.isChecked() else {}
                )
            elif solve_kernel == Kernel.SKETCH_SOLVE:
                result = SolverSystem(self.vpoint_list, input_pair).solve()
            else:
                raise ValueError("incorrect kernel")
        except ValueError as error:
            # Error: Show warning without update data.
            if self.prefer.console_error_option:
                logger.warn(format_exc())
            error_text = f"Error: {error}"
            self.conflict.setToolTip(error_text)
            self.conflict.setStatusTip(error_text)
            self.conflict.setVisible(True)
            self.dof_view.setVisible(False)
        else:
            self.entities_point.update_current_position(result)
            for i, c in enumerate(result):
                if isinstance(c[0], float):
                    self.vpoint_list[i].move(c)
                else:
                    c1, c2 = c
                    self.vpoint_list[i].move(c1, c2)
            self.__dof = vpoint_dof(self.vpoint_list)
            self.dof_view.setText(
                f"{self.__dof} ({self.inputs_widget.input_count()})")
            self.conflict.setVisible(False)
            self.dof_view.setVisible(True)
        self.reload_canvas()

    def preview_path(
        self,
        auto_preview: List[List[Tuple[float, float]]],
        slider_auto_preview: Dict[int, List[Tuple[float, float]]],
        vpoints: Sequence[VPoint]
    ):
        """Resolve auto preview path."""
        auto_preview.clear()
        slider_auto_preview.clear()
        if not self.right_input():
            return
        vpoints = tuple(vpoint.copy() for vpoint in vpoints)
        solve_kernel = self.prefer.path_preview_option
        if solve_kernel == Kernel.SAME_AS_SOLVING:
            solve_kernel = self.prefer.planar_solver_option
        interval = self.inputs_widget.interval()
        # path: [[p]: ((x0, y0), (x1, y1), (x2, y2), ...), ...]
        for i, vpoint in enumerate(vpoints):
            auto_preview.append([])
            if vpoint.type in {VJoint.P, VJoint.RP}:
                slider_auto_preview[i] = []
        input_pair = {(b, d): a for b, d, a in self.inputs_widget.input_pairs()}
        # Cumulative angle
        angles_cum = dict.fromkeys(input_pair, 0.)
        nan = float('nan')
        for dp in input_pair:
            for interval in (interval, -interval):
                while 0 <= angles_cum[dp] <= 360:
                    try:
                        if solve_kernel == Kernel.PYSLVS:
                            result = expr_solving(
                                self.get_triangle(vpoints),
                                vpoints,
                                input_pair
                            )
                        elif solve_kernel == Kernel.SOLVESPACE:
                            result, _ = _slvs_solve(
                                vpoints,
                                {}
                                if self.free_move_btn.isChecked() else
                                input_pair
                            )
                        elif solve_kernel == Kernel.SKETCH_SOLVE:
                            result = SolverSystem(vpoints, input_pair).solve()
                        else:
                            raise ValueError("incorrect kernel")
                    except ValueError:
                        # Update with error sign
                        for i in range(len(vpoints)):
                            auto_preview[i].append((nan, nan))
                        # Back to last feasible solution
                        input_pair[dp] -= interval
                        break
                    # Update with result
                    for i, vpoint in enumerate(vpoints):
                        if vpoint.type == VJoint.R:
                            auto_preview[i].append(cast(_Coord, result[i]))
                            vpoint.move(cast(_Coord, result[i]))
                        elif vpoint.type in {VJoint.P, VJoint.RP}:
                            slot, pin = cast(Tuple[_Coord, _Coord], result[i])
                            # Pin path
                            auto_preview[i].append(pin)
                            # Slot path
                            slider_auto_preview[i].append(slot)
                            vpoint.move(slot, pin)
                    angles_cum[dp] += abs(interval)
                    input_pair[dp] += interval
                    input_pair[dp] %= 360
        for path in auto_preview:
            path[:] = path[:-1]

    def get_graph(self) -> Tuple[
        Graph,
        List[int],
        List[Tuple[int, int]],
        Dict[int, Tuple[float, float]],
        Dict[int, int],
        Dict[int, int]
    ]:
        """Generalization Algorithm

        Return edges data, grounded list, variable list and multiple joints.
        VLinks will become graph vertices.
        """
        link_names = [vlink.name for vlink in self.vlink_list]
        input_pair = set()
        for b, d, _ in self.inputs_widget.input_pairs():
            input_pair.update({b, d})
        # links name for RP joint
        k = len(self.vlink_list)
        graph = Graph([])
        grounded_list = []
        pos = {}
        same = {}
        used_point: Set[int] = set()
        mapping = {}
        # Link names will change to index number
        for i, vlink in enumerate(self.vlink_list):
            for p in vlink.points:
                if p in used_point:
                    continue
                vpoint = self.vpoint_list[p]
                base_num = len(graph.edges)
                mapping[p] = base_num
                pos[base_num] = (vpoint.x, vpoint.y)
                for link_name in vpoint.links:
                    if vlink.name == link_name:
                        continue
                    m = link_names.index(link_name)
                    grounded = VLink.FRAME in {vlink.name, link_name}
                    ref_num = len(graph.edges)
                    if ref_num != base_num:
                        pos[ref_num] = (vpoint.x, vpoint.y)
                    if vpoint.type == VJoint.RP:
                        graph.add_edge(i, k)
                        if grounded:
                            grounded_list.append(len(graph.edges))
                        graph.add_edge(k, m)
                        k += 1
                    else:
                        if ref_num != base_num:
                            same[ref_num] = base_num
                        graph.add_edge(i, m)
                    if grounded and ref_num not in same:
                        grounded_list.append(ref_num)
                used_point.add(p)
        counter = len(graph.edges)
        cus = {}
        for vpoint in self.vpoint_list:
            if len(vpoint.links) == 1:
                cus[counter] = link_names.index(vpoint.links[0])
                counter += 1
        return (
            graph,
            grounded_list,
            [(mapping[b], mapping[d])
             for b, d, _ in self.inputs_widget.input_pairs()],
            pos,
            cus,
            same,
        )

    def get_configure(self) -> Dict[str, Any]:
        """Return collection data.

        + Expression
        + input
        + Graph
        + Placement
        + Target
        + cus
        + same
        """
        for vpoint in self.vpoint_list:
            if vpoint.type in {VJoint.P, VJoint.RP}:
                raise ValueError("not support for prismatic joint yet")
        graph, grounded_list, input_list, pos, cus, same = self.get_graph()
        links: List[Set[int]] = [set() for _ in range(len(graph.vertices))]
        for joint, pair in edges_view(graph):
            for node in pair:
                links[node].add(joint)
        placement = set(grounded_list)
        for row, link in enumerate(links):
            if placement == link - set(same):
                grounded = row
                break
        else:
            raise ValueError("no grounded link")
        vpoints = graph2vpoints(graph, pos, cus, same, grounded)
        return {
            'expression': self.get_expression(vpoints),
            'input': input_list,
            'graph': graph.edges,
            'placement': {p: None for p in grounded_list},
            'target': {p: None for p in cus},
            'cus': cus,
            'same': same,
        }

    def get_triangle(
        self,
        vpoints: Optional[Sequence[VPoint]] = None
    ) -> EStack:
        """Update triangle expression here.

        Special function for VPoints.
        """
        if vpoints is None:
            vpoints = self.vpoint_list
        status: Dict[int, bool] = {}
        exprs = t_config(
            vpoints,
            [(b, d) for b, d, _ in self.inputs_widget.input_pairs()],
            status
        )
        self.entities_expr.set_expr(exprs, tuple(p for p, s in status.items()
                                                 if not s))
        return exprs

    def right_input(self) -> bool:
        """Is input same as DOF?"""
        inputs = self.inputs_widget.input_count() == self.__dof
        if not inputs:
            self.entities_expr.clear()
        return inputs

    def reload_canvas(self) -> None:
        """Update main canvas data, without resolving."""
        paths, slider_paths = self.inputs_widget.current_path()
        self.main_canvas.update_canvas(
            self.get_triangle().as_list(),
            paths,
            slider_paths
        )

    def dof(self) -> int:
        """Return DOF."""
        return self.__dof
