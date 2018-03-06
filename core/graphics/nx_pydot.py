# -*- coding: utf-8 -*-

"""Painting function of NetworkX."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QImage,
    QSize,
    Qt,
    QPainter,
    QBrush,
    QPen,
    QPointF,
    QColor,
    QIcon,
    QPixmap,
)
from .color import colorQt, colorNum
from .canvas import convex_hull, edges_view
from networkx import (
    Graph,
    nx_pydot,
    shell_layout,
    circular_layout,
    spring_layout,
    spectral_layout,
    random_layout
)
from typing import Dict, Tuple
inf = float('inf')

_nx_engine = (
    "circular",
    "shell",
    "spring",
    "spectral",
    "random",
)
_graphviz_engine = (
    "dot",
    "neato",
    "fdp",
    "twopi",
    "circo",
)

EngineList = []
for engine in _nx_engine:
    EngineList.append("NetworkX - {}".format(engine))
for engine in _graphviz_engine:
    EngineList.append("Graphviz - {}".format(engine))

class EngineError(Exception):
    pass

def engine_picker(G: Graph, engine: str, node_mode: bool =False):
    """Generate a position dict."""
    if not node_mode:
        G_ = Graph()
        nodes = {i:edge for i, edge in edges_view(G)}
        for i, (l1, l2) in nodes.items():
            for j, edge in nodes.items():
                if i==j:
                    continue
                if (l1 in edge) or (l2 in edge):
                    G_.add_edge(i, j)
        H = G_
    else:
        H = G
    if type(engine) != str:
        return engine
    if engine=="random":
        E = {k:(x*200, y*200) for k, (x, y) in random_layout(H).items()}
    elif engine=="shell":
        E = shell_layout(H, scale=100)
    elif engine=="circular":
        E = circular_layout(H, scale=100)
    elif engine=="spring":
        E = spring_layout(H, scale=100)
    elif engine=="spectral":
        E = spectral_layout(H, scale=100)
    else:
        try:
            E = nx_pydot.graphviz_layout(H, prog=engine)
        except:
            raise EngineError("No Graphviz")
    x_max = -inf
    x_min = inf
    y_max = -inf
    y_min = inf
    for x, y in E.values():
        x = round(float(x), 4)
        y = round(float(y), 4)
        if x > x_max:
            x_max = x
        if x < x_min:
            x_min = x
        if y > y_max:
            y_max = y
        if y < y_min:
            y_min = y
    x_cen = (x_max + x_min)/2
    y_cen = (y_max + y_min)/2
    pos = {node: (
        round(float(x), 4) - x_cen,
        round(float(y), 4) - y_cen
    ) for node, (x, y) in E.items()}
    return pos

def graph(
    G: Graph,
    width: int,
    engine: [str, Dict[int, Tuple[float, float]]],
    node_mode: bool =False,
    except_node: int =None
) -> QIcon:
    """Draw a linkage graph."""
    try:
        pos = engine_picker(G, engine, node_mode)
    except EngineError as e:
        raise e
    width_ = -inf
    for x, y in pos.values():
        if abs(x) > width_:
            width_ = x
        if abs(y) > width_:
            width_ = y
    width_ *= 2 * 1.2
    image = QImage(QSize(width_, width_), QImage.Format_ARGB32_Premultiplied)
    image.fill(Qt.transparent)
    painter = QPainter(image)
    painter.translate(image.width()/2, image.height()/2)
    pen = QPen()
    r = width_ / 50
    pen.setWidth(r)
    painter.setPen(pen)
    if node_mode:
        for l1, l2 in G.edges:
            painter.drawLine(
                QPointF(pos[l1][0], -pos[l1][1]),
                QPointF(pos[l2][0], -pos[l2][1])
            )
    else:
        painter.setBrush(QBrush(QColor(226, 219, 190, 150)))
        for link in G.nodes:
            if link==except_node:
                continue
            #Distance sorted function from canvas
            painter.drawPolygon(*convex_hull([
                (pos[n][0], -pos[n][1])
                for n, edge in edges_view(G) if link in edge
            ]))
    for k, (x, y) in pos.items():
        if node_mode:
            color = colorNum(len(list(G.neighbors(k)))-1)
        else:
            if except_node in tuple(G.edges)[k]:
                color = colorQt('Green')
            else:
                color = colorQt('Blue')
        pen.setColor(color)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QPointF(x, -y), r, r)
    painter.end()
    icon = QIcon(QPixmap.fromImage(image).scaledToWidth(width))
    return icon
