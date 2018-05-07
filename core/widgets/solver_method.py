# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
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
        result, dof = slvsProcess(
            self.EntitiesPoint.dataTuple(),
            self.EntitiesLink.dataTuple(),
            inputs if not self.freemode_button.isChecked() else ()
        )
    except SlvsException as e:
        if self.consoleerror_option.isChecked():
            print(e)
        self.ConflictGuide.setToolTip(str(e))
        self.ConflictGuide.setStatusTip("Error: {}".format(e))
        self.ConflictGuide.setVisible(True)
        self.DOFview.setVisible(False)
    else:
        self.EntitiesPoint.updateCurrentPosition(result)
        self.DOF = dof
        self.DOFview.setText("{} ({})".format(self.DOF, len(inputs)))
        self.ConflictGuide.setVisible(False)
        self.DOFview.setVisible(True)
    self.reloadCanvas()


def getGraph(self) -> List[Tuple[int, int]]:
    """Return edges data for NetworkX graph class.

    + VLinks will become graph nodes.
    """
    vpoints = self.EntitiesPoint.dataTuple()
    vlinks = self.EntitiesLink.dataTuple()
    G = Graph()
    # links name for RP joint.
    k = len(vlinks)
    used_point = set()
    #Link names will change to index number.
    for i, vlink in enumerate(vlinks):
        for p in vlink.points:
            if p in used_point:
                continue
            for m, vlink_ in enumerate(vlinks):
                if not ((i != m) and (p in vlink_.points)):
                    continue
                if vpoints[p].type != 2:
                    G.add_edge(i, m)
                    continue
                G.add_edge(i, k)
                G.add_edge(k, m)
                k += 1
            used_point.add(p)
    return [edge for n, edge in edges_view(G)]


def getCollection(self) -> Dict[str, Union[
    Dict[str, None], #Driver
    Dict[str, None], #Follower
    Dict[str, List[Tuple[float, float]]], #Target
    str, #Link_Expression
    str, #Expression
    Tuple[Tuple[int, int]], #Graph
    Dict[int, Tuple[float, float]], #pos
    Dict[str, int], #cus
    Dict[int, int] #same
]]:
    """Return collection data.
    
    + Driver
    + Follower
    + Target
    + Link_Expression
    + Expression
    x constraint
    
    + Graph
    + pos
    + cus
    + same
    """
    vpoints = self.EntitiesPoint.dataTuple()
    for vpoint in vpoints:
        if vpoint.type != 0:
            raise ValueError("Not support for prismatic joint yet.")
    vlinks = self.EntitiesLink.dataTuple()
    link_names = [vlink.name for vlink in vlinks]
    graph = tuple(getGraph(self))
    
    def find(joint: Set[int]) -> int:
        """Find the vpoint that is match from joint.
        Even that is a multi joint.
        """
        for i, links in enumerate(graph):
            if joint <= set(links):
                return i
    
    pos = {}
    same = {}
    mapping = {}
    not_cus = set()
    
    def haslink(index: int) -> Tuple[bool, Optional[int]]:
        for key, value in mapping.items():
            if index == value:
                return True, key
        return False, None
    
    for i, vpoint in enumerate(vpoints):
        if len(vpoint.links) < 2:
            continue
        j = find({link_names.index(link) for link in vpoint.links})
        #Set position.
        pos[j] = vpoint.c[0]
        ok, index = haslink(j)
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
        cus['P{}'.format(count)] = link_names.index(vpoint.links[0])
        count += 1
    del count, not_cus
    
    drivers = {mapping[base] for base, drive in self.InputsWidget.inputPair()}
    followers = {
        mapping[i] for i, vpoint in enumerate(vpoints)
        if ('ground' in vpoint.links) and (i not in drivers)
    }
    
    def mapstr(s: str) -> str:
        """Replace as mapped index."""
        if not s.replace('P', '').isdigit():
            return s
        return 'P{}'.format(mapping[int(s.replace('P', ''))])
    
    expression = ';'.join('{}[{}]({})'.format(
        exprs[0],
        ','.join(mapstr(i) for i in exprs[1:-1]),
        mapstr(exprs[-1])
    ) for exprs in self.getTriangle())
    link_expression = ';'.join('[{}]'.format(','.join(
        'P{}'.format(mapping[p]) for p in vlink.points
    )) for vlink in vlinks)
    
    return {
        'Driver': {'P{}'.format(p): None for p in drivers},
        'Follower': {'P{}'.format(p): None for p in followers},
        'Target': {p: None for p in cus},
        'Link_Expression': link_expression,
        'Expression': expression,
        'Graph': graph,
        'constraint': [],
        'pos': pos,
        'cus': cus,
        'same': same,
    }


def getTriangle(self,
    vpoints: Optional[Tuple[VPoint]] = None
) -> List[Tuple[str]]:
    """Update triangle expression here.

    Special function for VPoints.
    """
    if vpoints is None:
        vpoints = self.EntitiesPoint.dataTuple()
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
