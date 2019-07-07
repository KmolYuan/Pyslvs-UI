# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Sequence,
    Set,
    Dict,
    Optional,
    Any,
)
from abc import ABC, abstractmethod
from traceback import format_exc
from core.QtModules import Slot
from core.info import logger
from core.libs import (
    slvs_solve,
    edges_view,
    graph2vpoints,
    vpoints_configure,
    VJoint,
    VPoint,
    data_collecting,
    expr_solving,
    vpoint_dof,
    vpoint_solving,
    ExpressionStack,
    Graph,
)
from .entities import EntitiesMethodInterface


class SolverMethodInterface(EntitiesMethodInterface, ABC):

    """Abstract class for solver methods."""

    @abstractmethod
    def __init__(self):
        super(SolverMethodInterface, self).__init__()
        self.dof = 0

    def solve(self):
        """Resolve coordinates and preview path."""
        self.resolve()
        self.main_canvas.update_preview_path()

    @Slot()
    def resolve(self):
        """Resolve: Using three libraries to solve the system.

        + Pyslvs
        + Python-Solvespace
        + Sketch Solve
        """
        for b, d, a in self.inputs_widget.input_pairs():
            if b == d:
                self.vpoint_list[b].set_offset(a)

        solve_kernel = self.planar_solver_option.currentIndex()
        try:
            if solve_kernel == 0:
                result = expr_solving(
                    self.get_triangle(),
                    {n: f'P{n}' for n in range(len(self.vpoint_list))},
                    self.vpoint_list,
                    tuple(a for b, d, a in self.inputs_widget.input_pairs() if b != d)
                )
            elif solve_kernel == 1:
                result, _ = slvs_solve(
                    self.vpoint_list,
                    {(b, d): a for b, d, a in self.inputs_widget.input_pairs()}
                    if not self.free_move_button.isChecked() else ()
                )
            elif solve_kernel == 2:
                result = vpoint_solving(
                    self.vpoint_list,
                    {(b, d): a for b, d, a in self.inputs_widget.input_pairs()}
                )
            else:
                raise ValueError("incorrect kernel")
        except ValueError as error:
            # Error: Show warning without update data.
            if self.console_error_option.isChecked():
                logger.warn(format_exc())
            error_text = f"Error: {error}"
            self.conflict.setToolTip(error_text)
            self.conflict.setStatusTip(error_text)
            self.conflict.setVisible(True)
            self.DOFview.setVisible(False)
        else:
            self.entities_point.update_current_position(result)
            for i, c in enumerate(result):
                if type(c[0]) is float:
                    self.vpoint_list[i].move(c)
                else:
                    c1, c2 = c
                    self.vpoint_list[i].move(c1, c2)
            self.dof = vpoint_dof(self.vpoint_list)
            self.DOFview.setText(f"{self.dof} ({self.inputs_widget.input_count()})")
            self.conflict.setVisible(False)
            self.DOFview.setVisible(True)
        self.reload_canvas()

    def preview_path(
        self,
        auto_preview: List[List[Tuple[float, float]]],
        slider_auto_preview: Dict[int, List[Tuple[float, float]]],
        vpoints: Sequence[VPoint]
    ):
        """Resolve auto preview path."""
        if not self.right_input():
            auto_preview.clear()
            slider_auto_preview.clear()
            return

        vpoints = tuple(vpoint.copy() for vpoint in vpoints)
        vpoint_count = len(vpoints)

        solve_kernel = self.path_preview_option.currentIndex()
        if solve_kernel == self.path_preview_option.count() - 1:
            solve_kernel = self.planar_solver_option.currentIndex()
        interval_o = self.inputs_widget.interval()

        # path: [[p]: ((x0, y0), (x1, y1), (x2, y2), ...), ...]
        auto_preview.clear()
        slider_auto_preview.clear()
        for i in range(vpoint_count):
            auto_preview.append([])
            if vpoints[i].type in {VJoint.P, VJoint.RP}:
                slider_auto_preview[i] = []

        bases = []
        drivers = []
        angles_o = []
        for b, d, a in self.inputs_widget.input_pairs():
            bases.append(b)
            drivers.append(d)
            angles_o.append(a)

        i_count = self.inputs_widget.input_count()
        # Cumulative angle
        angles_cum = [0.] * i_count

        nan = float('nan')
        for interval in (interval_o, -interval_o):
            # Driver pointer
            dp = 0
            angles = angles_o.copy()
            while dp < i_count:
                try:
                    if solve_kernel == 0:
                        result = expr_solving(
                            self.get_triangle(vpoints),
                            {n: f'P{n}' for n in range(vpoint_count)},
                            vpoints,
                            angles
                        )
                    elif solve_kernel == 1:
                        if self.free_move_button.isChecked():
                            inputs = {}
                        else:
                            inputs = {(bases[i], drivers[i]): angles[i] for i in range(i_count)}
                        result, _ = slvs_solve(vpoints, inputs)
                    elif solve_kernel == 2:
                        result = vpoint_solving(
                            vpoints,
                            {(bases[i], drivers[i]): angles[i] for i in range(i_count)}
                        )
                    else:
                        raise ValueError("incorrect kernel")
                except ValueError:
                    # Update with error sign.
                    for i in range(vpoint_count):
                        auto_preview[i].append((nan, nan))
                    # Back to last feasible solution.
                    angles[dp] -= interval
                    dp += 1
                else:
                    # Update with result.
                    for i in range(vpoint_count):
                        if vpoints[i].type == VJoint.R:
                            auto_preview[i].append(result[i])
                            vpoints[i].move(result[i])
                        elif vpoints[i].type in {VJoint.P, VJoint.RP}:
                            slot, pin = result[i]
                            # Pin path
                            auto_preview[i].append(pin)
                            # Slot path
                            slider_auto_preview[i].append(slot)
                            vpoints[i].move(slot, pin)
                    angles[dp] += interval
                    angles[dp] %= 360
                    angles_cum[dp] += abs(interval)
                    if angles_cum[dp] > 360:
                        angles[dp] -= interval
                        dp += 1

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
        VLinks will become graph nodes.
        """
        link_names = [vlink.name for vlink in self.vlink_list]
        input_pair = set()
        for b, d, _ in self.inputs_widget.input_pairs():
            input_pair.update({b, d})

        # links name for RP joint.
        k = len(self.vlink_list)

        graph = Graph([])
        grounded_list = []
        pos = {}
        same = {}
        used_point = set()
        mapping = {}
        # Link names will change to index number.
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
                    grounded = 'ground' in {vlink.name, link_name}
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
            [(mapping[b], mapping[d]) for b, d, _ in self.inputs_widget.input_pairs()],
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

        links: List[Set[int]] = [set() for _ in range(len(graph.nodes))]
        for joint, link in edges_view(graph):
            for node in link:
                links[node].add(joint)

        placement = set(grounded_list)
        for row, link in enumerate(links):
            if placement == link - set(same):
                grounded = row
                break
        else:
            raise ValueError("no grounded link")

        vpoint_exprs = [
            vpoint.expr()
            for vpoint in graph2vpoints(graph, pos, cus, same, grounded)
        ]

        return {
            'Expression': "M[" + ", ".join(vpoint_exprs) + "]",
            'input': input_list,
            'Graph': graph.edges,
            'Placement': {p: None for p in grounded_list},
            'Target': {p: None for p in cus},
            'cus': cus,
            'same': same,
        }

    def get_triangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> ExpressionStack:
        """Update triangle expression here.

        Special function for VPoints.
        """
        if vpoints is None:
            vpoints = self.vpoint_list
        status = {}
        exprs = vpoints_configure(
            vpoints,
            [(b, d) for b, d, _ in self.inputs_widget.input_pairs()],
            status
        )
        data_dict, _ = data_collecting(
            exprs,
            {n: f'P{n}' for n in range(len(vpoints))},
            vpoints
        )
        self.entities_expr.set_expr(
            exprs,
            data_dict,
            tuple(p for p, s in status.items() if not s)
        )
        return exprs

    def right_input(self) -> bool:
        """Is input same as DOF?"""
        inputs = self.inputs_widget.input_count() == self.dof
        if not inputs:
            self.entities_expr.clear()
        return inputs

    def reload_canvas(self):
        """Update main canvas data, without resolving."""
        self.main_canvas.update_figure(
            self.get_triangle().as_list(),
            self.inputs_widget.current_path()
        )

    def dof(self) -> int:
        """Return DOF."""
        return self.dof
