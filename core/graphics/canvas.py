# -*- coding: utf-8 -*-

"""All color options in Pyslvs."""

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
    Any,
    Union,
)
from abc import abstractmethod
from dataclasses import dataclass
from math import (
    radians,
    sin,
    cos,
    atan2,
    hypot,
    isnan,
)
from functools import reduce
from pyslvs import (
    VPoint,
    Graph,
    edges_view,
    parse_pos,
)
from core.QtModules import (
    Slot,
    Qt,
    QABCMeta,
    QPointF,
    QRectF,
    QPolygonF,
    QSizeF,
    QWidget,
    QSizePolicy,
    QPainter,
    QBrush,
    QPen,
    QColor,
    QFont,
    QPainterPath,
    QImage,
)
from .color import (
    color_num,
    color_qt,
    target_path_style,
)

_Coord = Tuple[float, float]


def convex_hull(
    points: List[_Coord],
    *,
    as_qpoint: bool = False
) -> Union[List[_Coord], List[QPointF]]:
    """Returns points on convex hull in counterclockwise order
    according to Graham's scan algorithm.
    """
    def cmp(a: float, b: float) -> int:
        return (a > b) - (a < b)

    def turn(p: _Coord, q: _Coord, r: _Coord) -> int:
        px, py = p
        qx, qy = q
        rx, ry = r
        return cmp((qx - px) * (ry - py) - (rx - px) * (qy - py), 0)

    def keep_left(hull: List[_Coord], r: _Coord) -> List[_Coord]:
        while len(hull) > 1 and turn(hull[-2], hull[-1], r) != 1:
            hull.pop()
        if not hull or hull[-1] != r:
            hull.append(r)
        return hull

    points.sort()
    lower = reduce(keep_left, points, [])
    upper = reduce(keep_left, reversed(points), [])
    lower.extend(upper[i] for i in range(1, len(upper) - 1))

    result = []
    for x, y in lower:
        if as_qpoint:
            result.append(QPointF(x, y))
        else:
            result.append((x, y))
    return result


@dataclass(repr=False, eq=False)
class _PathOption:

    """Path option class.

    Attributes:

    + Preview path data
    + Path data
    + Display mode:
        + Show mode parameter.
        + The path will be the curve, otherwise using the points.
    """

    path: Tuple[Tuple[_Coord, ...], ...] = ()
    show: int = -1
    curve: bool = True


class BaseCanvas(QWidget, metaclass=QABCMeta):

    """The subclass can draw a blank canvas more easier."""

    @abstractmethod
    def __init__(self, parent: QWidget):
        """Set the parameters for drawing."""
        super(BaseCanvas, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setFocusPolicy(Qt.StrongFocus)
        self.painter = QPainter()

        # Origin coordinate.
        self.ox = self.width() / 2
        self.oy = self.height() / 2
        # Canvas zoom rate.
        self.rate = 2.
        self.zoom = 2. * self.rate
        # Joint size.
        self.joint_size = 5
        # Canvas line width.
        self.link_width = 3
        self.path_width = 3
        # Font size.
        self.font_size = 15
        # Show point mark or dimension.
        self.show_point_mark = True
        self.show_dimension = True
        # Path track.
        self.path = _PathOption()
        # Path solving.
        self.ranges: Dict[str, QRectF] = {}
        self.target_path: Dict[str, Sequence[_Coord]] = {}
        self.show_target_path = False
        # Background
        self.background = QImage()
        self.background_opacity = 1.
        self.background_scale = 1
        self.background_offset = QPointF(0, 0)
        # Monochrome mode
        self.monochrome = False

    @abstractmethod
    def paintEvent(self, event):
        """Using a QPainter under 'self',
        so just change QPen or QBrush before painting.
        """
        self.painter.begin(self)
        self.painter.fillRect(event.rect(), QBrush(Qt.white))
        # Translation
        self.painter.translate(self.ox, self.oy)
        # Background
        if not self.background.isNull():
            rect = self.background.rect()
            self.painter.setOpacity(self.background_opacity)
            img_origin: QPointF = self.background_offset * self.zoom
            self.painter.drawImage(
                QRectF(img_origin, QSizeF(
                    rect.width() * self.background_scale * self.zoom,
                    rect.height() * self.background_scale * self.zoom
                )),
                self.background,
                QRectF(rect)
            )
            self.painter.setOpacity(1)
        # Show frame.
        pen = QPen(Qt.blue)
        pen.setWidth(1)
        self.painter.setPen(pen)
        self.painter.setFont(QFont("Arial", self.font_size))
        # Draw origin lines.
        pen.setColor(Qt.gray)
        self.painter.setPen(pen)
        x_l = -self.ox
        x_r = self.width() - self.ox
        self.painter.drawLine(QPointF(x_l, 0), QPointF(x_r, 0))
        y_t = self.height() - self.oy
        y_b = -self.oy
        self.painter.drawLine(QPointF(0, y_b), QPointF(0, y_t))

        def indexing(v):
            """Draw tick."""
            return int(v / self.zoom - v / self.zoom % 5)

        # Draw tick
        for x in range(indexing(x_l), indexing(x_r) + 1, 5):
            self.painter.drawLine(
                QPointF(x, 0) * self.zoom,
                QPointF(x * self.zoom, -10 if x % 10 == 0 else -5)
            )
        for y in range(indexing(y_b), indexing(y_t) + 1, 5):
            self.painter.drawLine(
                QPointF(0, y) * self.zoom,
                QPointF(10 if y % 10 == 0 else 5, y * self.zoom)
            )
        # Please to call the "end" method when ending paint event.

    def draw_point(
        self,
        i: int,
        cx,
        cy,
        fix: bool,
        color: Tuple[int, int, int]
    ):
        """Draw a joint."""
        pen = QPen(Qt.black if self.monochrome else QColor(*color))
        pen.setWidth(2)
        self.painter.setPen(pen)
        x = cx * self.zoom
        y = cy * -self.zoom
        if fix:
            bottom = y + 20
            width = 10
            # Draw a triangle below.
            self.painter.drawPolygon(
                QPointF(x, y),
                QPointF(x - width, bottom),
                QPointF(x + width, bottom)
            )
            r = self.joint_size * 2
        else:
            r = self.joint_size
        self.painter.drawEllipse(QPointF(x, y), r, r)

        if not self.show_point_mark:
            return
        pen.setColor(Qt.darkGray)
        pen.setWidth(2)
        self.painter.setPen(pen)
        text = f"[{i}]" if type(i) is str else f"[Point{i}]"
        if self.show_dimension:
            text += f":({cx:.02f}, {cy:.02f})"
        self.painter.drawText(QPointF(x, y) + QPointF(6, -6), text)

    def draw_slvs_ranges(self):
        """Draw solving range."""
        pen = QPen()
        pen.setWidth(5)
        for i, (tag, rect) in enumerate(self.ranges.items()):
            range_color = QColor(color_num(i + 1))
            range_color.setAlpha(30)
            self.painter.setBrush(range_color)
            range_color.setAlpha(255)
            pen.setColor(range_color)
            self.painter.setPen(pen)
            cx = rect.x() * self.zoom
            cy = rect.y() * -self.zoom
            if rect.width():
                self.painter.drawRect(QRectF(
                    QPointF(cx, cy),
                    QSizeF(rect.width(), rect.height()) * self.zoom
                ))
            else:
                self.painter.drawEllipse(QPointF(cx, cy), 3, 3)
            range_color.setAlpha(255)
            pen.setColor(range_color)
            self.painter.setPen(pen)
            self.painter.drawText(QPointF(cx, cy) + QPointF(6, -6), tag)
            self.painter.setBrush(Qt.NoBrush)

    def draw_target_path(self):
        """Draw solving path."""
        pen = QPen()
        pen.setWidth(self.path_width)
        for i, name in enumerate(sorted(self.target_path)):
            path = self.target_path[name]
            road, dot, brush = target_path_style(i)
            pen.setColor(road)
            self.painter.setPen(pen)
            self.painter.setBrush(brush)
            if len(path) == 1:
                x, y = path[0]
                p = QPointF(x, -y) * self.zoom
                self.painter.drawText(p + QPointF(6, -6), name)
                pen.setColor(dot)
                self.painter.setPen(pen)
                self.painter.drawEllipse(p, self.joint_size, self.joint_size)
            else:
                painter_path = QPainterPath()
                for j, (x, y) in enumerate(path):
                    p = QPointF(x, -y) * self.zoom
                    self.painter.drawEllipse(p, self.joint_size, self.joint_size)
                    if j == 0:
                        self.painter.drawText(p + QPointF(6, -6), name)
                        painter_path.moveTo(p)
                    else:
                        x2, y2 = path[j - 1]
                        self.__draw_arrow(x, -y, x2, -y2, zoom=True)
                        painter_path.lineTo(p)
                pen.setColor(road)
                self.painter.setPen(pen)
                self.painter.drawPath(painter_path)
                for x, y in path:
                    pen.setColor(dot)
                    self.painter.setPen(pen)
                    p = QPointF(x, -y) * self.zoom
                    self.painter.drawEllipse(p, self.joint_size, self.joint_size)
        self.painter.setBrush(Qt.NoBrush)

    def __draw_arrow(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        zoom: bool = False,
        text: str = ''
    ):
        """Front point -> Back point"""
        if zoom:
            x1 *= self.zoom
            y1 *= self.zoom
            x2 *= self.zoom
            y2 *= self.zoom
        a = atan2(y2 - y1, x2 - x1)
        x1 = (x1 + x2) / 2 - 7.5 * cos(a)
        y1 = (y1 + y2) / 2 - 7.5 * sin(a)
        first_point = QPointF(x1, y1)
        self.painter.drawLine(first_point, QPointF(
            x1 + 15 * cos(a + radians(20)),
            y1 + 15 * sin(a + radians(20))
        ))
        self.painter.drawLine(first_point, QPointF(
            x1 + 15 * cos(a - radians(20)),
            y1 + 15 * sin(a - radians(20))
        ))
        if not text:
            return
        # Font
        font = self.painter.font()
        font_copy = QFont(font)
        font.setBold(True)
        font.setPointSize(font.pointSize() + 8)
        self.painter.setFont(font)
        # Color
        pen = self.painter.pen()
        color = pen.color()
        pen.setColor(color.darker())
        self.painter.setPen(pen)
        self.painter.drawText(first_point, text)
        pen.setColor(color)
        self.painter.setPen(pen)
        self.painter.setFont(font_copy)

    def draw_curve(self, path: Sequence[_Coord]):
        """Draw path as curve."""
        if len(set(path)) <= 2:
            return
        painter_path = QPainterPath()
        error = False
        for i, (x, y) in enumerate(path):
            if isnan(x):
                error = True
                self.painter.drawPath(painter_path)
                painter_path = QPainterPath()
            else:
                x *= self.zoom
                y *= -self.zoom
                if i == 0:
                    painter_path.moveTo(x, y)
                    self.painter.drawEllipse(QPointF(x, y), self.joint_size, self.joint_size)
                    continue
                if error:
                    painter_path.moveTo(x, y)
                    error = False
                else:
                    painter_path.lineTo(x, y)
        self.painter.drawPath(painter_path)

    def draw_dot(self, path: Sequence[_Coord]):
        """Draw path as dots."""
        if len(set(path)) <= 2:
            return
        for x, y in path:
            if isnan(x):
                continue
            self.painter.drawPoint(QPointF(x, -y) * self.zoom)

    def solution_polygon(
        self,
        func: str,
        args: Sequence[str],
        target: str,
        pos: Sequence[VPoint]
    ) -> Tuple[List[QPointF], QColor]:
        """Get solution polygon."""
        if func == 'PLLP':
            color = QColor(121, 171, 252)
            params = [args[0], args[-1]]
        elif func == 'PLAP':
            color = QColor(249, 84, 216)
            params = [args[0]]
        else:
            if func == 'PLPP':
                color = QColor(94, 255, 185)
            else:
                # PXY
                color = QColor(249, 175, 27)
            params = [args[0]]
        params.append(target)
        tmp_list = []
        for name in params:
            try:
                index = int(name.replace('P', ''))
            except ValueError:
                continue
            else:
                vpoint = pos[index]
                tmp_list.append(QPointF(vpoint.cx, -vpoint.cy) * self.zoom)
        return tmp_list, color

    def draw_solution(
        self,
        func: str,
        args: Sequence[str],
        target: str,
        pos: Sequence[VPoint]
    ):
        """Draw the solution triangle."""
        points, color = self.solution_polygon(func, args, target, pos)
        color.setAlpha(150)
        pen = QPen(color)
        pen.setWidth(self.joint_size)
        self.painter.setPen(pen)

        def draw_arrow(index: int, text: str):
            """Draw arrow."""
            self.__draw_arrow(
                points[-1].x(),
                points[-1].y(),
                points[index].x(),
                points[index].y(),
                text=text
            )

        draw_arrow(0, args[1])
        if func == 'PLLP':
            draw_arrow(1, args[2])
        color.setAlpha(30)
        self.painter.setBrush(QBrush(color))
        self.painter.drawPolygon(QPolygonF(points))
        self.painter.setBrush(Qt.NoBrush)

    @Slot(bool)
    def set_monochrome_mode(self, monochrome: bool):
        self.monochrome = monochrome
        self.update()


class PreviewCanvas(BaseCanvas):

    """A preview canvas use to show structure diagram."""

    view_size = 240

    def __init__(self, parent: QWidget):
        """Input parameters and attributes.

        + Origin graph
        + Customize points: Dict[str, int]
        + Multiple joints: Dict[int, int]
        + Positions: Dict[int, Tuple[float, float]]
        + Joint status: Dict[int, bool]
        + Name dict: Dict['P0', 'A']
        """
        super(PreviewCanvas, self).__init__(parent)
        self.G = Graph([])
        self.cus: Dict[int, int] = {}
        self.same: Dict[int, int] = {}
        self.pos: Dict[int, _Coord] = {}
        self.status = {}

        # Additional attributes.
        self.grounded = -1
        self.driver: Set[int] = set()
        self.target: Set[int] = set()

        self.clear()

    def clear(self):
        """Clear the attributes."""
        self.G = Graph([])
        self.cus.clear()
        self.same.clear()
        self.pos.clear()
        self.status.clear()
        self.grounded = -1
        self.driver.clear()
        self.target.clear()
        self.update()

    def paintEvent(self, event):
        """Draw the structure."""
        width = self.width()
        height = self.height()
        if self.pos:
            x_right, x_left, y_top, y_bottom = self.__zoom_to_fit_limit()
            x_diff = x_left - x_right
            y_diff = y_top - y_bottom
            x_diff = x_diff if x_diff else 1
            y_diff = y_diff if y_diff else 1
            if width / x_diff < height / y_diff:
                factor = width / x_diff
            else:
                factor = height / y_diff
            self.zoom = factor * 0.75
            self.ox = width / 2 - (x_left + x_right) / 2 * self.zoom
            self.oy = height / 2 + (y_top + y_bottom) / 2 * self.zoom
        else:
            if width <= height:
                self.zoom = width / PreviewCanvas.view_size
            else:
                self.zoom = height / PreviewCanvas.view_size
            self.ox = width / 2
            self.oy = height / 2

        super(PreviewCanvas, self).paintEvent(event)

        pen = QPen()
        pen.setWidth(self.joint_size)
        self.painter.setPen(pen)
        if self.monochrome:
            color = QColor(Qt.darkGray)
        else:
            color = QColor(226, 219, 190)
        color.setAlpha(150)
        self.painter.setBrush(QBrush(color))

        # Links
        for link in self.G.nodes:
            if link == self.grounded:
                continue
            points = []
            # Points that is belong with the link.
            for num, edge in edges_view(self.G):
                if link in edge:
                    if num in self.same:
                        num = self.same[num]
                    x, y = self.pos[num]
                    points.append((x * self.zoom, y * -self.zoom))
            # Customize points.
            for name, link_ in self.cus.items():
                if link == link_:
                    x, y = self.pos[name]
                    points.append((x * self.zoom, y * -self.zoom))
            self.painter.drawPolygon(*convex_hull(points, as_qpoint=True))

        # Nodes
        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue
            x *= self.zoom
            y *= -self.zoom
            if self.monochrome:
                color = Qt.black
            elif node in self.driver:
                color = color_qt('Red')
            elif node in self.target:
                color = color_qt('Orange')
            elif self.get_status(node):
                color = color_qt('Green')
            else:
                color = color_qt('Blue')
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.setBrush(QBrush(color))
            self.painter.drawEllipse(QPointF(x, y), self.joint_size, self.joint_size)
            pen.setColor(Qt.black)
            self.painter.setPen(pen)

        # Text of node.
        pen.setColor(Qt.black)
        self.painter.setPen(pen)
        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue
            x *= self.zoom
            x += 2 * self.joint_size
            y *= -self.zoom
            y -= 2 * self.joint_size
            self.painter.drawText(QPointF(x, y), f'P{node}')

        self.painter.end()

    def __zoom_to_fit_limit(self) -> Tuple[float, float, float, float]:
        """Limitations of four side."""
        inf = float('inf')
        x_right = inf
        x_left = -inf
        y_top = -inf
        y_bottom = inf
        for x, y in self.pos.values():
            if x < x_right:
                x_right = x
            if x > x_left:
                x_left = x
            if y < y_bottom:
                y_bottom = y
            if y > y_top:
                y_top = y
        return x_right, x_left, y_top, y_bottom

    def set_graph(self, graph: Graph, pos: Dict[int, _Coord]):
        """Set the graph from NetworkX graph type."""
        self.G = graph
        self.pos = pos
        self.status = {k: False for k in pos}
        self.update()

    def set_grounded(self, link: int):
        """Set the grounded link number."""
        self.grounded = link
        for n, edge in edges_view(self.G):
            self.status[n] = self.grounded in edge
        for n, link in self.cus.items():
            self.status[n] = self.grounded == link
        self.update()

    def set_driver(self, input_list: List[Tuple[int, int]]):
        """Set driver nodes."""
        self.driver.clear()
        self.driver.update(pair[0] for pair in input_list)
        self.update()

    def set_target(self, nodes: Sequence[int]):
        """Set target nodes."""
        self.target.clear()
        self.target.update(nodes)
        self.update()

    def set_status(self, point: str, status: bool):
        """Set status node."""
        self.status[int(point.replace('P', ''))] = status
        self.update()

    def get_status(self, point: int) -> bool:
        """Get status. If multiple joints, return true."""
        return self.status[point] or (point in self.same)

    def from_profile(self, params: Dict[str, Any]):
        """Simple load by dict object."""
        # Customize points and multiple joints
        graph = Graph(params['Graph'])
        expression: str = params['Expression']
        pos_list = parse_pos(expression)
        self.cus: Dict[int, int] = params['cus']
        self.same: Dict[int, int] = params['same']
        for node, ref in sorted(self.same.items()):
            pos_list.insert(node, pos_list[ref])
        pos: Dict[int, _Coord] = dict(enumerate(pos_list))
        self.set_graph(graph, pos)

        # Grounded setting
        placement: Set[int] = set(params['Placement'])
        links: List[Set[int]] = [set() for _ in range(len(graph.nodes))]
        for joint, link in edges_view(graph):
            for node in link:
                links[node].add(joint)

        for row, link in enumerate(links):
            if placement == link - set(self.same):
                self.set_grounded(row)
                break

        # Driver setting
        input_list: List[Tuple[int, int]] = params['input']
        self.driver.clear()
        self.driver.update(pair[0] for pair in input_list)

        # Target setting
        target: Dict[int, Sequence[_Coord]] = params['Target']
        self.target.clear()
        self.target.update(target)

        self.update()

    def is_all_lock(self) -> bool:
        """Is all joint has solution."""
        for node, status in self.status.items():
            if not status and node not in self.same:
                return False
        return True

    def distance(self, n1: int, n2: int) -> float:
        """Return the distance of two point."""
        x1, y1 = self.pos[n1]
        x2, y2 = self.pos[n2]
        return hypot(x1 - x2, y1 - y2)
