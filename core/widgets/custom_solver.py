# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"


from typing import (
    List,
    Tuple,
)
from networkx import Graph
from core.graphics import edges_view
from core.libs import (
    slvsProcess,
    SlvsException,
    vpoints_configure,
    VPoint,
)

def resolve(self):
    """Resolve: Use Solvespace lib."""
    inputs = list(self.InputsWidget.getInputsVariables())
    try:
        result, DOF = slvsProcess(
            self.EntitiesPoint.dataTuple(),
            self.EntitiesLink.dataTuple(),
            inputs if not self.FreeMoveMode.isChecked() else ()
        )
    except SlvsException as e:
        if self.showConsoleError.isChecked():
            print(e)
        self.ConflictGuide.setToolTip(str(e))
        self.ConflictGuide.setStatusTip("Error: {}".format(e))
        self.ConflictGuide.setVisible(True)
        self.DOFview.setVisible(False)
    else:
        self.EntitiesPoint.updateCurrentPosition(result)
        self.DOF = DOF
        self.DOFview.setText("{} ({})".format(self.DOF, len(inputs)))
        self.ConflictGuide.setVisible(False)
        self.DOFview.setVisible(True)
    self.reloadCanvas()

def getGraph(self) -> List[Tuple[int, int]]:
    """Return edges data for NetworkX graph class.

    + VLinks will become graph nodes.
    """
    joint_data = self.EntitiesPoint.dataTuple()
    link_data = self.EntitiesLink.dataTuple()
    G = Graph()
    # links name for RP joint.
    k = len(link_data)
    used_point = set()
    for i, vlink in enumerate(link_data):
        for p in vlink.points:
            if p in used_point:
                continue
            for m, vlink_ in enumerate(link_data):
                if not ((i != m) and (p in vlink_.points)):
                    continue
                if joint_data[p].type != 2:
                    G.add_edge(i, m)
                    continue
                G.add_edge(i, k)
                G.add_edge(k, m)
                k += 1
            used_point.add(p)
    return [edge for n, edge in edges_view(G)]

def getTriangle(self, vpoints: Tuple[VPoint]) -> List[Tuple[str]]:
    """Update triangle expression here.

    Special function for VPoints.
    """
    exprs = vpoints_configure(
        vpoints,
        tuple(self.InputsWidget.inputPair())
    )
    self.Entities_Expr.setExpr(exprs)
    return exprs

def rightInput(self) -> bool:
    """Is input same as DOF?"""
    inputs = (self.InputsWidget.inputCount() != 0) and (self.DOF == 0)
    if not inputs:
        self.Entities_Expr.clear()
    return inputs

def pathInterval(self) -> float:
    """Wrapper use to get path interval."""
    return self.InputsWidget.record_interval.value()

def reloadCanvas(self):
    """Update main canvas data, without resolving."""
    self.MainCanvas.updateFigure(
        self.EntitiesPoint.dataTuple(),
        self.EntitiesLink.dataTuple(),
        self.InputsWidget.currentPath()
    )
