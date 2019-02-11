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
    edges_view,
)
from .entities import EntitiesMethodInterface


class SolverMethodInterface(EntitiesMethodInterface, ABC):

    """Abstract class for solver methods."""

    @abstractmethod
    def __init__(self):
        super(SolverMethodInterface, self).__init__()
        self.DOF = 0

    def solve(self):
        """Resolve coordinates and preview path."""
        self.resolve()
        self.MainCanvas.update_preview_path()

    @Slot()
    def resolve(self):
        """Resolve: Using three libraries to solve the system.

        + Pyslvs
        + Python-Solvespace
        + Sketch Solve
        """
        vpoints = self.EntitiesPoint.data_tuple()
        solve_kernel = self.planarsolver_option.currentIndex()

        for b, d, a in self.InputsWidget.input_pairs():
            if b == d:
                vpoints[b].set_offset(a)

        try:
            if solve_kernel == 0:
                result = expr_solving(
                    self.get_triangle(),
                    {n: f'P{n}' for n in range(len(vpoints))},
                    vpoints,
                    tuple(a for b, d, a in self.InputsWidget.input_pairs() if b != d)
                )
            elif solve_kernel == 1:
                result, _ = slvs_solve(
                    vpoints,
                    tuple(self.InputsWidget.input_pairs())
                    if not self.free_move_button.isChecked() else ()
                )
            elif solve_kernel == 2:
                result = vpoint_solving(
                    vpoints,
                    {(b, d): a for b, d, a in self.InputsWidget.input_pairs()}
                )
            else:
                raise ValueError("incorrect kernel")
        except ValueError as error:
            # Error: Show warning without update data.
            if self.consoleerror_option.isChecked():
                print(format_exc())
            error_text = f"Error: {error}"
            self.conflict.setToolTip(error_text)
            self.conflict.setStatusTip(error_text)
            self.conflict.setVisible(True)
            self.DOFview.setVisible(False)
        else:
            # Done: Update coordinate data.
            self.EntitiesPoint.update_current_position(result)
            self.DOF = vpoint_dof(vpoints)
            self.DOFview.setText(f"{self.DOF} ({self.InputsWidget.input_count()})")
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

        solve_kernel = self.pathpreview_option.currentIndex()
        if solve_kernel == self.pathpreview_option.count() - 1:
            solve_kernel = self.planarsolver_option.currentIndex()
        interval_o = self.InputsWidget.interval()

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
        for b, d, a in self.InputsWidget.input_pairs():
            bases.append(b)
            drivers.append(d)
            angles_o.append(a)

        i_count = self.InputsWidget.input_count()
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

    def get_graph(self) -> List[Tuple[int, int]]:
        """Return edges data for NetworkX graph class.

        + VLinks will become graph nodes.
        """
        vpoints = self.EntitiesPoint.data_tuple()
        vlinks = self.EntitiesLink.data_tuple()
        graph = Graph([])
        # links name for RP joint.
        k = len(vlinks)
        used_point = set()
        # Link names will change to index number.
        for i, vlink in enumerate(vlinks):
            for p in vlink.points:
                if p in used_point:
                    continue
                for m, vlink_ in enumerate(vlinks):
                    if (i == m) or (p not in vlink_.points):
                        continue
                    if vpoints[p].type != VJoint.RP:
                        graph.add_edge(i, m)
                        continue
                    graph.add_edge(i, k)
                    graph.add_edge(k, m)
                    k += 1
                used_point.add(p)
        return [edge for n, edge in edges_view(graph)]

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
        vlinks: Iterator[VLink] = self.EntitiesLink.data()
        link_names = [vlink.name for vlink in vlinks]
        graph = tuple(self.get_graph())

        count = len(graph)
        vpoint_exprs = []
        grounded_list = []
        same = {}
        cus = {}
        for i, vpoint in enumerate(self.EntitiesPoint.data()):
            if vpoint.type in {VJoint.P, VJoint.RP}:
                raise ValueError("not support for prismatic joint yet")

            i += len(same)
            link_count = len(vpoint.links)
            if link_count > 2:
                for j in range(1, link_count - 1):
                    same[i + j] = i
            elif link_count == 1:
                cus[count] = link_names.index(vpoint.links[0])
                count += 1

            vpoint_exprs.append(vpoint.expr)
            if 'ground' in vpoint.links:
                grounded_list.append(i - len(same))

        vpoint_exprs = ", ".join(vpoint_exprs)

        params = {
            'Expression': f"M[{vpoint_exprs}]",
            'input': [(b, d) for b, d, _ in self.InputsWidget.input_pairs()],
            'Graph': graph,
            'Placement': {p: None for p in grounded_list},
            'Target': {p: None for p in cus},
            'cus': cus,
            'same': same,  # TODO: Still incorrect here.
        }
        print(params)
        return params

    def get_triangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> List[Tuple[str, ...]]:
        """Update triangle expression here.

        Special function for VPoints.
        """
        if vpoints is None:
            vpoints = self.EntitiesPoint.data_tuple()
        status = {}
        exprs = vpoints_configure(
            vpoints,
            [(b, d) for b, d, _ in self.InputsWidget.input_pairs()],
            status
        )
        data_dict, _ = data_collecting(
            exprs,
            {n: f'P{n}' for n in range(len(vpoints))},
            vpoints
        )
        self.EntitiesExpr.set_expr(
            exprs,
            data_dict,
            tuple(p for p, s in status.items() if not s)
        )
        return exprs

    def right_input(self) -> bool:
        """Is input same as DOF?"""
        inputs = self.InputsWidget.input_count() == self.DOF
        if not inputs:
            self.EntitiesExpr.clear()
        return inputs

    def reload_canvas(self):
        """Update main canvas data, without resolving."""
        self.MainCanvas.update_figure(
            self.EntitiesPoint.data_tuple(),
            self.EntitiesLink.data_tuple(),
            self.get_triangle(),
            self.InputsWidget.current_path()
        )

    def dof(self) -> int:
        """Return DOF."""
        return self.DOF
