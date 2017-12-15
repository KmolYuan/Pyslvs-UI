# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from ...QtModules import *
from ...graphics.color import colorQt, colorNum
from networkx import (
    Graph,
    nx_pydot,
    shell_layout,
    circular_layout,
    spring_layout,
    spectral_layout,
    random_layout
)
from typing import Tuple

def v_to_edges(jointData: Tuple['VPoint'], linkData: Tuple['VLink']):
    G = Graph()
    #Links name for RP joint.
    k = len(linkData)
    used_point = []
    for i, vlink in enumerate(linkData):
        for p in vlink.points:
            if p in used_point:
                continue
            match = [m for m, vlink_ in enumerate(linkData) if i!=m and (p in vlink_.points)]
            for m in match:
                if jointData[p].type==2:
                    G.add_edge(i, k)
                    G.add_edge(k, m)
                    k += 1
                else:
                    G.add_edge(i, m)
            used_point.append(p)
    return str(list(G.edges))

EngineList = [
    "Graphviz - dot",
    "Graphviz - neato",
    "Graphviz - fdp",
    "Graphviz - twopi",
    "Graphviz - circo",
    "NetworkX - shell",
    "NetworkX - circular",
    "NetworkX - spring",
    "NetworkX - spectral",
    "NetworkX - random"
]

class EngineError(Exception):
    pass

def engine_picker(G: Graph, engine: str):
    if engine=="random":
        E = {k:(x*200, y*200) for k, (x, y) in random_layout(G).items()}
    elif engine=="shell":
        E = shell_layout(G, scale=100)
    elif engine=="circular":
        E = circular_layout(G, scale=100)
    elif engine=="spring":
        E = spring_layout(G, scale=100)
    elif engine=="spectral":
        E = spectral_layout(G, scale=100)
    else:
        try:
            E = nx_pydot.graphviz_layout(G, prog=engine)
        except:
            raise EngineError("No Graphviz")
    pos = {k:(round(float(x), 4), round(float(y), 4)) for k, (x, y) in E.items()}
    x_cen = (max(x for x, y in pos.values())+min(x for x, y in pos.values()))/2
    y_cen = (max(y for x, y in pos.values())+min(y for x, y in pos.values()))/2
    return {k:(x-x_cen, y-y_cen) for k, (x, y) in pos.items()}

def graph(G: Graph, width: int, engine: str, node_mode: bool):
    if not node_mode:
        G_ = Graph()
        nodes = {i:edge for i, edge in enumerate(G.edges)}
        for i, (l1, l2) in nodes.items():
            for j, edge in nodes.items():
                if i==j:
                    continue
                if (l1 in edge) or (l2 in edge):
                    G_.add_edge(i, j)
    try:
        if node_mode:
            pos = engine_picker(G, engine)
        else:
            pos = engine_picker(G_, engine)
    except EngineError as e:
        raise e
    width_ = max(max(x for x, y in pos.values()), max(y for x, y in pos.values()))*2*1.2
    image = QImage(QSize(width_, width_), QImage.Format_ARGB32_Premultiplied)
    image.fill(Qt.transparent)
    painter = QPainter(image)
    painter.translate(image.width()/2, image.height()/2)
    pen = QPen()
    r = width_ / 33.78744
    pen.setWidth(r)
    painter.setPen(pen)
    if node_mode:
        for l1, l2 in G.edges:
            painter.drawLine(QPointF(*pos[l1]), QPointF(*pos[l2]))
    else:
        painter.setBrush(QBrush(QColor(226, 219, 190, 150)))
        for l in G.nodes:
            painter.drawPolygon(*[QPointF(*pos[n]) for n, edge in nodes.items() if l in edge])
    for k, (x, y) in pos.items():
        if node_mode:
            color = colorNum(len(list(G.neighbors(k)))-1)
        else:
            color = colorQt('Blue')
        pen.setColor(color)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QPointF(x, y), r, r)
    painter.end()
    return QIcon(QPixmap.fromImage(image).scaledToWidth(width))
