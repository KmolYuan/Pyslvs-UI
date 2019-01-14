# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""
from PyQt5.QtCore import QPoint

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Set,
    Dict,
    Union,
    Optional,
)
from abc import abstractmethod
from traceback import format_exc
from core.QtModules import pyqtSlot, QAbcMeta
from core.libs import (
    slvs_solve,
    vpoints_configure,
    VJoint,
    VPoint,
    data_collecting,
    expr_solving,
    vpoint_dof,
    vpoint_solving,
    Graph,
    edges_view,
)
from .entities import EntitiesMethodInterface


class SolverMethodInterface(EntitiesMethodInterface, metaclass=QAbcMeta):

    """Abstract class for solver methods."""

    def __init__(self):
        super(SolverMethodInterface, self).__init__()
        self.DOF = 0

    def solve(self):
        """Resolve coordinates and preview path."""
        self.resolve()
        self.MainCanvas.update_preview_path()

    @pyqtSlot()
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
                    self.getTriangle(),
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
                raise RuntimeError("incorrect kernel")
        except RuntimeError as error:
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

    def previewpath(
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
                            self.getTriangle(vpoints),
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
                        raise RuntimeError("incorrect kernel")
                except RuntimeError:
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

    def getGraph(self) -> List[Tuple[int, int]]:
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
                    if not ((i != m) and (p in vlink_.points)):
                        continue
                    if vpoints[p].type != VJoint.RP:
                        graph.add_edge(i, m)
                        continue
                    graph.add_edge(i, k)
                    graph.add_edge(k, m)
                    k += 1
                used_point.add(p)
        return [edge for n, edge in edges_view(graph)]

    def get_collection(self) -> Dict[str, Union[
        Dict[str, None],
        Dict[str, List[Tuple[float, float]]],
        str,
        Tuple[Tuple[int, int], ...],
        Dict[int, Tuple[float, float]],
        Dict[str, int]
    ]]:
        """Return collection data.

        + Driver
        + Follower
        + Target
        + Link_expr
        + Expression
        x constraint

        + Graph
        + pos
        + cus
        + same
        """
        vpoints = self.EntitiesPoint.data_tuple()
        for vpoint in vpoints:
            if vpoint.type in {VJoint.P, VJoint.RP}:
                raise ValueError("not support for prismatic joint yet")
        vlinks = self.EntitiesLink.data_tuple()
        link_names = [vlink.name for vlink in vlinks]
        graph = tuple(self.getGraph())

        def find(joint: Set[int]) -> int:
            """Find the vpoint that is match from joint.
            Even that is a multi joint.
            """
            for order, links in enumerate(graph):
                if joint <= set(links):
                    return order

        pos = {}
        same = {}
        mapping = {}
        not_cus = set()

        def has_link(order: int) -> Tuple[bool, Optional[int]]:
            for key, value in mapping.items():
                if order == value:
                    return True, key
            return False, None

        for i, vpoint in enumerate(vpoints):
            if len(vpoint.links) < 2:
                continue
            j = find({link_names.index(link) for link in vpoint.links})
            # Set position.
            pos[j] = vpoint.c[0]
            ok, index = has_link(j)
            if ok:
                same[i] = index
            else:
                mapping[i] = j
            not_cus.add(i)

        count = len(graph)
        cus = {}
        for i, vpoint in enumerate(vpoints):
            if (i in not_cus) or (not vpoint.links):
                continue
            mapping[i] = count
            pos[count] = vpoint.c[0]
            cus[f'P{count}'] = link_names.index(vpoint.links[0])
            count += 1

        drivers = {mapping[b] for b, d, a in self.InputsWidget.input_pairs()}
        followers = {
            mapping[i] for i, vpoint in enumerate(vpoints)
            if ('ground' in vpoint.links) and (i not in drivers)
        }

        def map_str(s: str) -> str:
            """Replace as mapped index."""
            if not s.replace('P', '').isdigit():
                return s
            node = int(s.replace('P', ''))
            return f"P{mapping[node]}"

        expr_list = []
        for exprs in self.getTriangle():
            params = ','.join(map_str(i) for i in exprs[1:-1])
            expr_list.append(f'{exprs[0]}[{params}]({map_str(exprs[-1])})')

        link_expr_list = []
        for vlink in vlinks:
            points_text = ','.join(f'P{mapping[p]}' for p in vlink.points)
            link_expr_list.append(f'[{points_text}]')

        return {
            'Driver': {f'P{p}': None for p in drivers},
            'Follower': {f'P{p}': None for p in followers},
            'Target': {p: None for p in cus},
            'Link_expr': ';'.join(link_expr_list),
            'Expression': ';'.join(expr_list),
            'Graph': graph,
            'pos': pos,
            'cus': cus,
            'same': same,
        }

    def getTriangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> List[Tuple[str]]:
        """Update triangle expression here.

        Special function for VPoints.
        """
        if vpoints is None:
            vpoints = self.EntitiesPoint.data_tuple()
        status = {}
        exprs = vpoints_configure(
            vpoints,
            tuple((b, d) for b, d, a in self.InputsWidget.input_pairs()),
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
            self.getTriangle(),
            self.InputsWidget.current_path()
        )

    @abstractmethod
    def command_reload(self, index: int) -> None:
        ...

    @abstractmethod
    def add_target_point(self) -> None:
        ...

    @abstractmethod
    def set_mouse_pos(self, x: float, y: float) -> None:
        ...

    @abstractmethod
    def commit(self, is_branch: bool = False) -> None:
        ...

    @abstractmethod
    def commit_branch(self) -> None:
        ...

    @abstractmethod
    def enable_mechanism_actions(self) -> None:
        ...

    @abstractmethod
    def copy_coord(self) -> None:
        ...

    @abstractmethod
    def copy_points_table(self) -> None:
        ...

    @abstractmethod
    def copy_links_table(self) -> None:
        ...

    @abstractmethod
    def canvas_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def link_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def customize_zoom(self) -> None:
        ...

    @abstractmethod
    def reset_options(self) -> None:
        ...
