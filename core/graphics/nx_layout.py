# -*- coding: utf-8 -*-

"""Painting function of NetworkX."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Dict,
    Tuple,
    Union,
    Optional,
)
from networkx import (
    Graph as nx_Graph,
    spring_layout,
)
from core.QtModules import (
    Qt,
    QImage,
    QSize,
    QPainter,
    QBrush,
    QPen,
    QPointF,
    QColor,
    QIcon,
    QPixmap,
    QFont,
)
from core.libs import Graph, external_loop_layout
from .color import color_qt, color_num
from .canvas import convex_hull, edges_view

Pos = Dict[int, Tuple[float, float]]

engines: Tuple[str, ...] = (
    "external loop",
    "spring",
)

_font = QFont("Monospace")
_font.setBold(True)
_font.setStyleHint(QFont.TypeWriter)


def _reversed_graph(graph: Graph) -> Graph:
    """Edges will become nodes."""
    edges = []
    for i, edge1 in edges_view(graph):
        for j, edge2 in edges_view(graph):
            if i == j:
                continue
            if set(edge1) & set(edge2):
                edges.append((i, j))
    return Graph(edges)


def engine_picker(g: Graph, engine: Union[str, Pos], node_mode: bool) -> Union[str, Pos]:
    """Generate a position dict."""
    if type(engine) != str:
        return engine

    if engine == "spring":
        if not node_mode:
            g = _reversed_graph(g)
        layout: Pos = spring_layout(nx_Graph(g.edges), scale=100)
    elif engine == "external loop":
        layout: Pos = external_loop_layout(g, node_mode, scale=100)
    else:
        raise ValueError(f"engine {engine} is not exist")

    inf = float('inf')
    x_max = -inf
    x_min = inf
    y_max = -inf
    y_min = inf
    for x, y in layout.values():
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
    x_cen = (x_max + x_min) / 2
    y_cen = (y_max + y_min) / 2
    pos: Pos = {node: (
        round(float(x), 4) - x_cen,
        round(float(y), 4) - y_cen
    ) for node, (x, y) in layout.items()}
    return pos


def to_graph(
    g: Graph,
    width: int,
    engine: Union[str, Pos],
    node_mode: bool,
    show_label: bool,
    *,
    except_node: Optional[int] = None
) -> QIcon:
    """Draw a generalized chain graph."""
    pos: Pos = engine_picker(g, engine, node_mode)
    width_bound = -float('inf')
    for x, y in pos.values():
        if abs(x) > width_bound:
            width_bound = x
        if abs(y) > width_bound:
            width_bound = y
    width_bound *= 2.5
    image = QImage(
        QSize(int(width_bound), int(width_bound)),
        QImage.Format_ARGB32_Premultiplied
    )
    image.fill(Qt.transparent)
    painter = QPainter(image)
    painter.translate(image.width() / 2, image.height() / 2)
    pen = QPen()
    r = width_bound / 50
    pen.setWidth(int(r))
    painter.setPen(pen)
    _font.setPixelSize(r * 6)
    painter.setFont(_font)

    # Draw edges.
    if node_mode:
        for l1, l2 in g.edges:
            if except_node in {l1, l2}:
                pen.setColor(Qt.gray)
            else:
                pen.setColor(Qt.black)
            painter.setPen(pen)

            painter.drawLine(
                QPointF(pos[l1][0], -pos[l1][1]),
                QPointF(pos[l2][0], -pos[l2][1])
            )
    else:
        painter.setBrush(QBrush(QColor(226, 219, 190, 150)))
        for link in g.nodes:
            if link == except_node:
                pen.setColor(Qt.gray)
            else:
                pen.setColor(Qt.black)
            painter.setPen(pen)

            painter.drawPolygon(*convex_hull([
                (pos[n][0], -pos[n][1])
                for n, edge in edges_view(g) if link in edge
            ], as_qpoint=True))

    # Draw nodes.
    for k, (x, y) in pos.items():
        if node_mode:
            color = color_num(len(list(g.neighbors(k))) - 1)
            if k == except_node:
                color.setAlpha(150)
        else:
            if except_node in dict(edges_view(g))[k]:
                color = color_qt('Green')
            else:
                color = color_qt('Blue')
        pen.setColor(color)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))
        point = QPointF(x, -y)
        painter.drawEllipse(point, r, r)
        if show_label:
            pen.setColor(Qt.darkMagenta)
            painter.setPen(pen)
            painter.drawText(point, str(k))
    painter.end()
    icon = QIcon(QPixmap.fromImage(image).scaledToWidth(width))
    return icon
