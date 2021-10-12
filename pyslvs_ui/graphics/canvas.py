# -*- coding: utf-8 -*-

"""All color options in Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    TypeVar, Tuple, List, Sequence, Set, Dict, Mapping, Iterator, Any,
    Optional, ClassVar, overload,
)
from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from enum import auto, unique, IntEnum
from math import radians, sin, cos, atan2, hypot, isnan
from functools import reduce
from qtpy.QtCore import Slot, Qt, QPointF, QRectF, QSizeF, Signal, QLineF
from qtpy.QtWidgets import QWidget, QSizePolicy
from qtpy.QtGui import (
    QPolygonF, QPainter, QBrush, QPen, QColor, QFont,
    QPainterPath, QImage, QPaintEvent, QMouseEvent,
)
from pyslvs import VPoint, edges_view, parse_pos
from pyslvs.graph import Graph
from pyslvs_ui.qt_patch import QABCMeta
from .color import color_num, color_qt, target_path_style

_T = TypeVar('_T')
_Coord = Tuple[float, float]
LINK_COLOR = QColor(226, 219, 190)


@overload
def convex_hull(points: List[_Coord], *, as_qpoint: bool) -> List[QPointF]:
    pass


@overload
def convex_hull(points: List[_Coord]) -> List[_Coord]:
    pass


def convex_hull(points, *, as_qpoint=False):
    """Returns points on convex hull in counterclockwise order
    according to Graham's scan algorithm.
    """

    def cmp(a: float, b: float) -> int:
        return int(a > b) - int(a < b)

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
    return [(QPointF(x, y) if as_qpoint else (x, y)) for x, y in lower]


@dataclass(init=False, repr=False, eq=False)
class RangeDetector:
    """Range detection of points."""
    inf = float('inf')
    right = inf
    left = -inf
    top = -inf
    bottom = inf
    del inf

    def __call__(self, right: float, left: float,
                 top: float, bottom: float) -> None:
        """Set ranges from new point."""
        if right < self.right:
            self.right = right
        if left > self.left:
            self.left = left
        if top > self.top:
            self.top = top
        if bottom < self.bottom:
            self.bottom = bottom


@dataclass(init=False, repr=False, eq=False)
class _PathOption:
    """Path option class.

    Attributes:

    + Path data (-1: Hide, 0: Preview path data)
    + Show mode parameter.
    + The path will be the curve, otherwise using the points.
    """
    path: Sequence[Sequence[_Coord]] = ()
    slider_path: Mapping[int, Sequence[_Coord]] = field(default_factory=dict)
    show: int = -1
    curve: bool = True


@unique
class _TickMark(IntEnum):
    """The status of tick mark."""
    HIDE = auto()
    SHOW = auto()
    SHOW_NUM = auto()


class BaseCanvas(QWidget, metaclass=QABCMeta):
    """The subclass can draw a blank canvas more easier."""
    ranges: Dict[str, QRectF]
    target_path: Dict[int, Sequence[_Coord]]

    @abstractmethod
    def __init__(self, parent: QWidget):
        """Set the parameters for drawing."""
        super(BaseCanvas, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        self.painter = QPainter()
        # Origin coordinate
        self.ox = self.width() / 2
        self.oy = self.height() / 2
        # Canvas zoom rate
        self.zoom = 1.
        # Joint size
        self.joint_size = 5
        # Canvas line width
        self.link_width = 3
        self.path_width = 3
        # Font size
        self.font_size = 15
        # Show point mark or dimension
        self.show_ticks = _TickMark.SHOW
        self.show_point_mark = True
        self.show_dimension = True
        # Path track
        self.path = _PathOption()
        # Path solving
        self.ranges = {}
        self.target_path = {}
        self.show_target_path = False
        # Background
        self.background = QImage()
        self.background_opacity = 1.
        self.background_scale = 1.
        self.background_offset = QPointF(0, 0)
        # Monochrome mode
        self.monochrome = False
        # Grab mode
        self.__grab_mode = False

    def switch_grab(self) -> None:
        """Start grab mode."""
        self.__grab_mode = not self.__grab_mode

    @staticmethod
    def zoom_factor(
        width: int,
        height: int,
        x_right: float,
        x_left: float,
        y_top: float,
        y_bottom: float
    ) -> float:
        """Calculate the zoom factor."""
        x_diff = x_left - x_right
        y_diff = y_top - y_bottom
        x_diff = x_diff if x_diff else 1.
        y_diff = y_diff if y_diff else 1.
        if width / x_diff < height / y_diff:
            return width / x_diff
        else:
            return height / y_diff

    @abstractmethod
    def paintEvent(self, event: QPaintEvent) -> None:
        """Using a QPainter under 'self',
        so just change QPen or QBrush before painting.
        """
        if not self.__grab_mode:
            self.painter.begin(self)
            self.painter.fillRect(event.rect(), QBrush(Qt.white))
        # Translation
        self.painter.translate(self.ox, self.oy)
        # Background
        if not self.background.isNull():
            rect = self.background.rect()
            self.painter.setOpacity(self.background_opacity)
            self.painter.drawImage(QRectF(
                self.background_offset * self.zoom,
                QSizeF(rect.width(), rect.height())
                * self.background_scale * self.zoom
            ), self.background, QRectF(rect))
            self.painter.setOpacity(1)
        # Show frame
        pen = QPen(Qt.blue)
        pen.setWidth(1)
        self.painter.setPen(pen)
        self.painter.setFont(QFont("Arial", self.font_size))
        # Draw origin lines
        if self.show_ticks not in {_TickMark.SHOW, _TickMark.SHOW_NUM}:
            return
        pen.setColor(Qt.gray)
        self.painter.setPen(pen)
        x_l = -self.ox
        x_r = self.width() - self.ox
        self.painter.drawLine(QLineF(x_l, 0, x_r, 0))
        y_t = self.height() - self.oy
        y_b = -self.oy
        self.painter.drawLine(QLineF(0, y_b, 0, y_t))

        def indexing(v: float) -> int:
            """Draw tick."""
            return int(v / self.zoom - v / self.zoom % 5)

        # Draw tick
        for x in range(indexing(x_l), indexing(x_r) + 1, 5):
            if x == 0:
                continue
            is_ten = x % 10 == 0
            end = QPointF(x * self.zoom, -10 if is_ten else -5)
            self.painter.drawLine(QPointF(x, 0) * self.zoom, end)
            if self.show_ticks == _TickMark.SHOW_NUM and is_ten:
                self.painter.drawText(end + QPointF(0, 3), f"{x}")
        for y in range(indexing(y_b), indexing(y_t) + 1, 5):
            if y == 0:
                continue
            is_ten = y % 10 == 0
            end = QPointF(10 if is_ten else 5, y * self.zoom)
            self.painter.drawLine(QPointF(0, y) * self.zoom, end)
            if self.show_ticks == _TickMark.SHOW_NUM and is_ten:
                self.painter.drawText(end + QPointF(3, 0), f"{-y}")
        # Please to call the "end" method when ending paint event.

    def draw_circle(self, p: QPointF, r: float) -> None:
        """Draw circle."""
        self.painter.drawEllipse(p, r, r)

    def draw_point(
        self,
        i: int,
        cx: float,
        cy: float,
        fixed: bool,
        color: Optional[Tuple[int, int, int]],
        mul: int = 1
    ) -> None:
        """Draw a joint."""
        if self.monochrome or color is None:
            color = Qt.black
        else:
            color = QColor(*color)
        pen = QPen(color)
        pen.setWidth(2)
        self.painter.setPen(pen)
        x = cx * self.zoom
        y = cy * -self.zoom
        if fixed:
            # Draw a triangle below
            self.painter.drawPolygon(
                QPointF(x, y),
                QPointF(x - self.joint_size, y + 2 * self.joint_size),
                QPointF(x + self.joint_size, y + 2 * self.joint_size)
            )
        r = self.joint_size
        for _ in range(1 if mul < 1 else mul):
            self.draw_circle(QPointF(x, y), r)
            r += 5
        if not self.show_point_mark:
            return
        pen.setColor(Qt.darkGray)
        pen.setWidth(2)
        self.painter.setPen(pen)
        text = f"[Point{i}]"
        if self.show_dimension:
            text += f":({cx:.02f}, {cy:.02f})"
        self.painter.drawText(QPointF(x, y) + QPointF(6, -6), text)

    def draw_ranges(self) -> None:
        """Draw rectangle ranges."""
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
                self.draw_circle(QPointF(cx, cy), 3)
            range_color.setAlpha(255)
            pen.setColor(range_color)
            self.painter.setPen(pen)
            self.painter.drawText(QPointF(cx, cy) + QPointF(6, -6), tag)
            self.painter.setBrush(Qt.NoBrush)

    def draw_target_path(self) -> None:
        """Draw solving path."""
        pen = QPen()
        pen.setWidth(self.path_width)
        for i, n in enumerate(sorted(self.target_path)):
            path = self.target_path[n]
            if self.monochrome:
                line, dot = target_path_style(0)
            else:
                line, dot = target_path_style(i + 1)
            pen.setColor(line)
            self.painter.setPen(pen)
            if len(path) == 1:
                x, y = path[0]
                p = QPointF(x, -y) * self.zoom
                self.painter.drawText(p + QPointF(6, -6), f"P{n}")
                pen.setColor(dot)
                self.painter.setPen(pen)
                self.draw_circle(p, self.joint_size)
            else:
                painter_path = QPainterPath()
                for j, (x, y) in enumerate(path):
                    p = QPointF(x, -y) * self.zoom
                    self.draw_circle(p, self.joint_size)
                    if j == 0:
                        self.painter.drawText(p + QPointF(6, -6), f"P{n}")
                        painter_path.moveTo(p)
                    else:
                        xb, yb = path[j - 1]
                        self.draw_arrow(xb, yb, x, y, line=False)
                        painter_path.lineTo(p)
                pen.setColor(line)
                self.painter.setPen(pen)
                self.painter.drawPath(painter_path)
                for x, y in path:
                    pen.setColor(dot)
                    self.painter.setPen(pen)
                    self.draw_circle(QPointF(x, -y) * self.zoom,
                                     self.joint_size)
        self.painter.setBrush(Qt.NoBrush)

    def draw_arrow(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        zoom: bool = True,
        line: bool = True,
        text: str = ''
    ) -> None:
        """Base point -> Vector point"""
        if zoom:
            x1 *= self.zoom
            y1 *= self.zoom
            x2 *= self.zoom
            y2 *= self.zoom
        a = atan2(y1 - y2, x1 - x2)
        x2 = (x1 + x2) / 2 - 7.5 * cos(a)
        y2 = (y1 + y2) / 2 - 7.5 * sin(a)
        first_point = QPointF(x2, -y2)
        if line:
            self.painter.drawLine(QLineF(x1, -y1, x2, -y2))
        self.painter.drawLine(first_point, QPointF(
            x2 + 15 * cos(a + radians(20)),
            -y2 - 15 * sin(a + radians(20))
        ))
        self.painter.drawLine(first_point, QPointF(
            x2 + 15 * cos(a - radians(20)),
            -y2 - 15 * sin(a - radians(20))
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

    def draw_curve(self, path: Sequence[_Coord]) -> None:
        """Draw path as curve."""
        if len(set(path)) < 2:
            return
        painter_path = QPainterPath()
        error = False
        for i, (x, y) in enumerate(path):
            if isnan(x):
                error = True
                self.painter.drawPath(painter_path)
                painter_path = QPainterPath()
            else:
                p = QPointF(x, -y) * self.zoom
                if i == 0:
                    painter_path.moveTo(p)
                    self.draw_circle(p, 2)
                    continue
                if error:
                    painter_path.moveTo(p)
                    error = False
                else:
                    painter_path.lineTo(p)
        self.painter.drawPath(painter_path)

    def draw_dot(self, path: Sequence[_Coord]) -> None:
        """Draw path as dots."""
        if len(set(path)) < 2:
            return
        for i, (x, y) in enumerate(path):
            if isnan(x):
                continue
            p = QPointF(x, -y) * self.zoom
            if i == 0:
                self.draw_circle(p, 2)
            else:
                self.painter.drawPoint(p)

    def solution_polygon(
        self,
        func: str,
        args: Sequence[str],
        target: str,
        pos: Sequence[VPoint]
    ) -> Tuple[List[_Coord], QColor]:
        """Get solution polygon."""
        params = [args[0]]
        if func == 'PLLP':
            color = QColor(121, 171, 252)
            params.append(args[-1])
        elif func == 'PLAP':
            color = QColor(249, 84, 216)
        else:
            if func == 'PLPP':
                color = QColor(94, 255, 185)
            else:
                # PXY
                color = QColor(249, 175, 27)
        params.append(target)
        polygon = []
        for name in params:
            try:
                index = int(name.replace('P', ''))
            except ValueError:
                continue
            else:
                vpoint = pos[index]
                polygon.append((vpoint.cx * self.zoom, -vpoint.cy * self.zoom))
        return polygon, color

    def draw_solution(
        self,
        func: str,
        args: Sequence[str],
        target: str,
        pos: Sequence[VPoint]
    ) -> None:
        """Draw the solution triangle."""
        points, color = self.solution_polygon(func, args, target, pos)
        color.setAlpha(150)
        pen = QPen(color)
        pen.setWidth(self.joint_size)
        self.painter.setPen(pen)

        def draw_arrow(index: int, text: str) -> None:
            """Draw arrow."""
            x0, y0 = points[index]
            x1, y1 = points[-1]
            self.draw_arrow(x0, -y0, x1, -y1, zoom=False, line=False, text=text)

        draw_arrow(0, args[1])
        if func == 'PLLP':
            draw_arrow(1, args[2])
        color.setAlpha(30)
        self.painter.setBrush(QBrush(color))
        self.painter.drawPolygon(
            QPolygonF([QPointF(x, y) for x, y in points]))
        self.painter.setBrush(Qt.NoBrush)

    @Slot(int)
    def set_show_ticks(self, show: int):
        """Set the appearance of tick mark."""
        self.show_ticks = _TickMark(show + 1)
        self.update()

    @Slot(bool)
    def set_monochrome_mode(self, monochrome: bool) -> None:
        """Set monochrome mode."""
        self.monochrome = monochrome
        self.update()


class AnimationCanvas(BaseCanvas, ABC):
    """A auto zooming canvas with time sequence."""
    update_pos = Signal(float, float)

    def __init__(self, parent: QWidget):
        super(AnimationCanvas, self).__init__(parent)
        self.no_mechanism = False

    def __zoom_to_fit_size(self) -> Tuple[float, float, float, float]:
        """Limitations of four side."""
        r = RangeDetector()
        # Paths
        for i, path in enumerate(self.path.path):
            if self.no_mechanism and i not in self.target_path:
                continue
            for x, y in path:
                r(x, x, y, y)
        # Solving paths
        for path in self.target_path.values():
            for x, y in path:
                r(x, x, y, y)
        # Ranges
        for rect in self.ranges.values():
            r(rect.right(), rect.left(), rect.top(), rect.bottom())
        return r.right, r.left, r.top, r.bottom

    def paintEvent(self, event: QPaintEvent) -> None:
        """Adjust functions."""
        width = self.width()
        height = self.height()
        x_right, x_left, y_top, y_bottom = self.__zoom_to_fit_size()
        x_diff = x_left - x_right or 1.
        y_diff = y_top - y_bottom or 1.
        if width / x_diff < height / y_diff:
            self.zoom = width / x_diff * 0.95
        else:
            self.zoom = height / y_diff * 0.95
        self.ox = width / 2 - (x_left + x_right) / 2 * self.zoom
        self.oy = height / 2 + (y_top + y_bottom) / 2 * self.zoom
        super(AnimationCanvas, self).paintEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Set mouse position."""
        self.update_pos.emit((event.x() - self.ox) / self.zoom,
                             (event.y() - self.oy) / self.zoom)


class PreviewCanvas(BaseCanvas):
    """A preview canvas use to show structure diagram."""
    cus: Dict[int, int]
    same: Dict[int, int]
    pos: Dict[int, _Coord]
    status: Dict[int, bool]
    driver: Set[int]
    target: Set[int]

    view_size: ClassVar[int] = 240

    def __init__(self, parent: QWidget):
        """Input parameters and attributes."""
        super(PreviewCanvas, self).__init__(parent)
        self.graph = Graph([])
        self.cus = {}
        self.same = {}
        self.pos = {}
        self.status = {}
        # Additional attributes
        self.grounded = -1
        self.driver = set()
        self.target = set()
        self.clear()

    def clear(self) -> None:
        """Clear the attributes."""
        self.graph = Graph([])
        self.cus.clear()
        self.same.clear()
        self.pos.clear()
        self.status.clear()
        self.grounded = -1
        self.driver.clear()
        self.target.clear()
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Draw the structure."""
        width = self.width()
        height = self.height()
        if self.pos:
            x_right, x_left, y_top, y_bottom = self.__zoom_to_fit_limit()
            self.zoom = self.zoom_factor(
                width,
                height,
                x_right,
                x_left,
                y_top,
                y_bottom
            ) * 0.75
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
        color = color_qt('dark-gray') if self.monochrome else LINK_COLOR
        color.setAlpha(150)
        self.painter.setBrush(QBrush(color))
        # Links
        for link in self.graph.vertices:
            if link == self.grounded:
                continue
            points = []
            # Points that is belong with the link
            for num, edge in edges_view(self.graph):
                if link in edge:
                    if num in self.same:
                        num = self.same[num]
                    x, y = self.pos[num]
                    points.append((x * self.zoom, y * -self.zoom))
            # Customize points
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
                color = color_qt('red')
            elif node in self.target:
                color = color_qt('orange')
            elif self.get_status(node):
                color = color_qt('green')
            else:
                color = color_qt('blue')
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.setBrush(QBrush(color))
            self.draw_circle(QPointF(x, y), self.joint_size)
            pen.setColor(Qt.black)
            self.painter.setPen(pen)

        # Text of node
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

    def set_graph(self, graph: Graph, pos: Mapping[int, _Coord]) -> None:
        """Set the graph from NetworkX graph type."""
        self.graph = graph
        self.pos = dict(pos)
        self.status = {k: False for k in pos}
        self.update()

    def set_grounded(self, link: int) -> None:
        """Set the grounded link number."""
        self.grounded = link
        for n, edge in edges_view(self.graph):
            self.status[n] = self.grounded in edge
        for n, link in self.cus.items():
            self.status[n] = self.grounded == link
        self.update()

    def set_driver(self, input_list: List[Tuple[int, int]]) -> None:
        """Set driver nodes."""
        self.driver.clear()
        self.driver.update(pair[0] for pair in input_list)
        self.update()

    def set_target(self, points: Sequence[int]) -> None:
        """Set target nodes."""
        self.target.clear()
        self.target.update(points)
        self.update()

    def set_status(self, point: str, status: bool) -> None:
        """Set status node."""
        self.status[int(point.replace('P', ''))] = status
        self.update()

    def get_status(self, point: int) -> bool:
        """Get status. If multiple joints, return true."""
        return self.status[point] or (point in self.same)

    @staticmethod
    def grounded_detect(
        placement: Set[int],
        g: Graph,
        same: Mapping[int, int]
    ) -> Iterator[int]:
        """Find the grounded link."""
        links: List[Set[int]] = [set() for _ in range(len(g.vertices))]
        for joint, link in edges_view(g):
            for node in link:
                links[node].add(joint)
        for row, link in enumerate(links):
            if placement == link - set(same):
                # Return once
                yield row
                return

    def from_profile(self, params: Mapping[str, Any]) -> None:
        """Simple load by dict object."""
        # Customize points and multiple joints
        g = Graph(params['graph'])
        expression: str = params['expression']
        pos_list = parse_pos(expression)
        cus: Mapping[int, int] = params['cus']
        same: Mapping[int, int] = params['same']
        self.cus = dict(cus)
        self.same = dict(same)
        for node, ref in sorted(self.same.items()):
            pos_list.insert(node, pos_list[ref])
        self.set_graph(g, {i: (x, y) for i, (x, y) in enumerate(pos_list)})

        # Grounded setting
        for row in self.grounded_detect(set(params['placement']), g, self.same):
            self.set_grounded(row)

        # Driver setting
        input_list: List[Tuple[int, int]] = params['input']
        self.driver.clear()
        self.driver.update(b for b, _ in input_list)

        # Target setting
        target: Mapping[int, Sequence[_Coord]] = params['target']
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
