# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Dict,
    Iterator,
    Optional,
    Any,
)
from abc import ABC, abstractmethod
from traceback import format_exc
from core.QtModules import Slot
from core.libs import (
    slvs_solve,
    vpoints_configure,
    VJoint,
    VPoint,
    VLink,
    data_collecting,
    expr_solving,
    vpoint_dof,
    vpoint_solving,
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
        vpoints = self.entities_point.data_tuple()
        solve_kernel = self.planar_solver_option.currentIndex()

        for b, d, a in self.inputs_widget.input_pairs():
            if b == d:
                vpoints[b].set_offset(a)

        try:
            if solve_kernel == 0:
                result = expr_solving(
                    self.get_triangle(),
                    {n: f'P{n}' for n in range(len(vpoints))},
                    vpoints,
                    tuple(a for b, d, a in self.inputs_widget.input_pairs() if b != d)
                )
            elif solve_kernel == 1:
                result, _ = slvs_solve(
                    vpoints,
                    tuple(self.inputs_widget.input_pairs())
                    if not self.free_move_button.isChecked() else ()
                )
            elif solve_kernel == 2:
                result = vpoint_solving(
                    vpoints,
                    {(b, d): a for b, d, a in self.inputs_widget.input_pairs()}
                )
            else:
                raise ValueError("incorrect kernel")
        except ValueError as error:
            # Error: Show warning without update data.
            if self.console_error_option.isChecked():
                print(format_exc())
            error_text = f"Error: {error}"
            self.conflict.setToolTip(error_text)
            self.conflict.setStatusTip(error_text)
            self.conflict.setVisible(True)
            self.DOFview.setVisible(False)
        else:
            # Done: Update coordinate data.
            self.entities_point.update_current_position(result)
            self.dof = vpoint_dof(vpoints)
            self.DOFview.setText(f"{self.dof} ({self.inputs_widget.input_count()})")
            self.conflict.setVisible(False)
            self.DOFview.setVisible(True)
        self.reload_canvas()

    def preview_path(
        self,
        auto_preview: List[List[Tuple[float, float]]],
        slider_auto_preview: Dict[int, List[Tuple[float, float]]],
        vpoints: Tuple[VPoint, ...]
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
                            inputs = ()
                        else:
                            inputs = tuple((bases[i], drivers[i], angles[i]) for i in range(i_count))
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
                            # Pin path
                            auto_preview[i].append(result[i][1])
                            # Slot path
                            slider_auto_preview[i].append(result[i][0])
                            vpoints[i].move(result[i][0], result[i][1])
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
        Dict[int, int],
        Dict[int, int]
    ]:
        """Return edges data, grounded list, variable list and multiple joints.

        VLinks will become graph nodes.
        """
        vpoints: Tuple[VPoint, ...] = self.entities_point.data_tuple()
        vlinks: Tuple[VLink, ...] = self.entities_link.data_tuple()
        link_names = [vlink.name for vlink in vlinks]
        input_pair = set()
        for b, d, _ in self.inputs_widget.input_pairs():
            input_pair.update({b, d})

        # links name for RP joint.
        k = len(vlinks)

        graph = Graph([])
        grounded_list = []
        same = {}
        used_point = set()
        mapping = {}
        # Link names will change to index number.
        for i, vlink in enumerate(vlinks):
            for p in vlink.points:
                if p in used_point:
                    continue

                vpoint = vpoints[p]
                base_num = len(graph.edges)
                mapping[p] = base_num

                for link_name in vpoint.links:
                    if vlink.name == link_name:
                        continue

                    m = link_names.index(link_name)
                    ref_num = len(graph.edges)

                    if vpoint.type == VJoint.RP:
                        graph.add_edge(i, k)
                        grounded_list.append(len(graph.edges))
                        graph.add_edge(k, m)
                        k += 1
                    else:
                        if ref_num != base_num:
                            same[ref_num] = base_num
                        graph.add_edge(i, m)

                    if 'ground' in {vlink.name, link_name}:
                        if ref_num not in same:
                            grounded_list.append(ref_num)

                used_point.add(p)

        input_list = [
            (mapping[b], mapping[d])
            for b, d, _ in self.inputs_widget.input_pairs()
        ]

        counter = len(graph.edges)
        cus = {}
        for vpoint in vpoints:
            if len(vpoint.links) == 1:
                cus[counter] = link_names.index(vpoint.links[0])
                counter += 1

        return graph, grounded_list, input_list, cus, same

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
        graph, grounded_list, input_list, cus, same = self.get_graph()

        vpoint_exprs = []
        for i, vpoint in enumerate(self.entities_point.data()):
            if vpoint.type in {VJoint.P, VJoint.RP}:
                raise ValueError("not support for prismatic joint yet")

            vpoint_exprs.append(vpoint.expr())

        return {
            'Expression': "M[" + ", ".join(vpoint_exprs) + "]",
            'input': input_list,
            'Graph': graph.edges,
            'Placement': {p: None for p in grounded_list},
            'Target': {p: None for p in cus},
            'cus': cus,
            'same': same,
        }

    def get_triangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> List[Tuple[str, ...]]:
        """Update triangle expression here.

        Special function for VPoints.
        """
        if vpoints is None:
            vpoints = self.entities_point.data_tuple()
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
            self.entities_point.data_tuple(),
            self.entities_link.data_tuple(),
            self.get_triangle(),
            self.inputs_widget.current_path()
        )

    def dof(self) -> int:
        """Return DOF."""
        return self.dof
