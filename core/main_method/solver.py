# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"


from traceback import format_exc
from typing import (
    Tuple,
    List,
    Set,
    Dict,
    Union,
    Optional,
)
from networkx import Graph
from core.QtModules import pyqtSlot, QAbcMeta
from core.graphics import edges_view
from core.libs import (
    slvs_solve,
    vpoints_configure,
    VPoint,
    data_collecting,
    expr_solving,
    vpoint_dof,
    bfgs_vpoint_solving,
)
from .entities import EntitiesMethodInterface


class SolverMethodInterface(EntitiesMethodInterface, metaclass=QAbcMeta):
    
    """Interface class for solver methods."""
    
    def __init__(self):
        super(SolverMethodInterface, self).__init__()
        self.DOF = 0
    
    def solve(self):
        """Resolve coordinates and preview path."""
        self.resolve()
        self.MainCanvas.updatePreviewPath()
    
    @pyqtSlot()
    def resolve(self):
        """Resolve: Using three libraries to solve the system.
        
        + Pyslvs
        + Python-Solvespace
        + Sketch Solve
        """
        vpoints = self.EntitiesPoint.dataTuple()
        solve_kernel = self.planarsolver_option.currentIndex()
        try:
            if solve_kernel == 0:
                result = expr_solving(
                    self.getTriangle(),
                    {n: f'P{n}' for n in range(len(vpoints))},
                    vpoints,
                    tuple(v[-1] for v in self.InputsWidget.inputPair())
                )
            elif solve_kernel == 1:
                result, _ = slvs_solve(
                    vpoints,
                    tuple(self.InputsWidget.inputPair())
                    if not self.freemode_button.isChecked() else ()
                )
            elif solve_kernel == 2:
                result = bfgs_vpoint_solving(
                    vpoints,
                    tuple(self.InputsWidget.inputPair())
                )
            else:
                raise RuntimeError("Incorrect kernel.")
        except RuntimeError as error:
            # Error: Show warning without update data.
            if self.consoleerror_option.isChecked():
                print(format_exc())
            error_text = f"Error: {error}"
            self.ConflictGuide.setToolTip(error_text)
            self.ConflictGuide.setStatusTip(error_text)
            self.ConflictGuide.setVisible(True)
            self.DOFview.setVisible(False)
        else:
            # Done: Update coordinate data.
            self.EntitiesPoint.updateCurrentPosition(result)
            self.DOF = vpoint_dof(vpoints)
            self.DOFview.setText(f"{self.DOF} ({self.InputsWidget.inputCount()})")
            self.ConflictGuide.setVisible(False)
            self.DOFview.setVisible(True)
        self.reloadCanvas()
    
    def previewpath(
        self,
        auto_preview: List[List[Tuple[float, float]]],
        slider_auto_preview: Dict[int, List[Tuple[float, float]]],
        vpoints: Tuple[VPoint]
    ):
        """Resolve auto preview path."""
        if not self.rightInput():
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
            if vpoints[i].type in {VPoint.P, VPoint.RP}:
                slider_auto_preview[i] = []
        
        bases = []
        drivers = []
        angles_o = []
        for b, d, a in self.InputsWidget.inputPair():
            bases.append(b)
            drivers.append(d)
            angles_o.append(a)
        
        i_count = self.InputsWidget.inputCount()
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
                        if self.freemode_button.isChecked():
                            inputs = ()
                        else:
                            inputs = tuple((bases[i], drivers[i], angles[i]) for i in range(i_count))
                        result, _ = slvs_solve(vpoints, inputs)
                    elif solve_kernel == 2:
                        result = bfgs_vpoint_solving(
                            vpoints,
                            tuple((bases[i], drivers[i], angles[i]) for i in range(i_count))
                        )
                    else:
                        raise RuntimeError("Incorrect kernel.")
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
                        if vpoints[i].type == VPoint.R:
                            auto_preview[i].append(result[i])
                            vpoints[i].move(result[i])
                        elif vpoints[i].type in {VPoint.P, VPoint.RP}:
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
        vpoints = self.EntitiesPoint.dataTuple()
        vlinks = self.EntitiesLink.dataTuple()
        graph = Graph()
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
                    if vpoints[p].type != VPoint.RP:
                        graph.add_edge(i, m)
                        continue
                    graph.add_edge(i, k)
                    graph.add_edge(k, m)
                    k += 1
                used_point.add(p)
        return [edge for n, edge in edges_view(graph)]
    
    def getCollection(self) -> Dict[str, Union[
        Dict[str, None],  # Driver
        Dict[str, None],  # Follower
        Dict[str, List[Tuple[float, float]]],  # Target
        str,  # Link_expr
        str,  # Expression
        Tuple[Tuple[int, int]],  # Graph
        Dict[int, Tuple[float, float]],  # pos
        Dict[str, int],  # cus
        Dict[int, int]  # same
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
        vpoints = self.EntitiesPoint.dataTuple()
        for vpoint in vpoints:
            if vpoint.type in {VPoint.P, VPoint.RP}:
                raise ValueError("Not support for prismatic joint yet.")
        vlinks = self.EntitiesLink.dataTuple()
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
        del count, not_cus
        
        drivers = {mapping[b] for b, d, a in self.InputsWidget.inputPair()}
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
            'constraints': [],
            'pos': pos,
            'cus': cus,
            'same': same,
        }
    
    def getTriangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> List[Tuple[str]]:
        """Update triangle expression here.
    
        Special function for VPoints.
        """
        if vpoints is None:
            vpoints = self.EntitiesPoint.dataTuple()
        status = {}
        exprs = vpoints_configure(
            vpoints,
            tuple((b, d) for b, d, a in self.InputsWidget.inputPair()),
            status
        )
        data_dict, _ = data_collecting(
            exprs,
            {n: f'P{n}' for n in range(len(vpoints))},
            vpoints
        )
        self.EntitiesExpr.setExpr(
            exprs,
            data_dict,
            tuple(p for p, s in status.items() if not s)
        )
        return exprs
    
    def rightInput(self) -> bool:
        """Is input same as DOF?"""
        inputs = self.InputsWidget.inputCount() == self.DOF
        if not inputs:
            self.EntitiesExpr.clear()
        return inputs
    
    def reloadCanvas(self):
        """Update main canvas data, without resolving."""
        self.MainCanvas.updateFigure(
            self.EntitiesPoint.dataTuple(),
            self.EntitiesLink.dataTuple(),
            self.getTriangle(),
            self.InputsWidget.currentPath()
        )
