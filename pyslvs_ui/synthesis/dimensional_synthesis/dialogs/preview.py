# -*- coding: utf-8 -*-

"""The preview dialog of dimensional synthesis result."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from math import isnan
from itertools import chain
from typing import Tuple, List, Dict, Sequence, Any
from qtpy.QtCore import Slot, Qt, QTimer, QPointF, QRectF, QSizeF
from qtpy.QtWidgets import QDialog, QWidget, QVBoxLayout
from qtpy.QtGui import QPen, QFont, QPaintEvent
from pyslvs import color_rgb, get_vlinks, VPoint, VLink, parse_vpoints
from pyslvs_ui.graphics import BaseCanvas, color_qt, LINK_COLOR
from .preview_ui import Ui_Dialog

_Coord = Tuple[float, float]
_Range = Tuple[float, float, float]


class _DynamicCanvas(BaseCanvas):

    """Custom canvas for preview algorithm result."""

    def __init__(
        self,
        mechanism: Dict[str, Any],
        path: Sequence[Sequence[_Coord]],
        vpoints: List[VPoint] = None,
        vlinks: List[VLink] = None,
        parent: QWidget = None
    ):
        """Input link and path data."""
        super(_DynamicCanvas, self).__init__(parent)
        self.mechanism = mechanism
        self.path.path = path
        self.vpoints = vpoints or []
        self.vlinks = vlinks or []
        self.__index = 0
        self.__interval = 1
        self.__path_count = max(len(path) for path in self.path.path) - 1
        self.pos: List[_Coord] = []
        # Target path
        same: Dict[int, int] = self.mechanism['same']
        target_path: Dict[int, List[_Coord]] = self.mechanism['target']
        for i, path in target_path.items():
            for j in range(i):
                if j in same:
                    i -= 1
            self.target_path[i] = path
        # Error
        self.error = False
        self.__no_error = 0
        # No mechanism mode
        self.__no_mechanism = not self.vpoints or not self.vlinks
        if self.__no_mechanism:
            return
        # Ranges
        ranges: Dict[int, _Range] = self.mechanism['placement']
        self.ranges.update({f"P{i}": QRectF(
            QPointF(values[0] - values[2], values[1] + values[2]),
            QSizeF(values[2] * 2, values[2] * 2)
        ) for i, values in ranges.items()})
        # Timer
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__change_index)
        self.__timer.start(18)

    def __zoom_to_fit_size(self) -> Tuple[float, float, float, float]:
        """Limitations of four side."""
        inf = float('inf')
        x_right = inf
        x_left = -inf
        y_top = -inf
        y_bottom = inf

        def set_range(r: float, l: float, t: float, b: float) -> None:
            nonlocal x_right, x_left, y_top, y_bottom
            if r < x_right:
                x_right = r
            if l > x_left:
                x_left = l
            if t > y_top:
                y_top = t
            if b < y_bottom:
                y_bottom = b

        # Paths
        for i, path in enumerate(self.path.path):
            if self.__no_mechanism and i not in self.target_path:
                continue
            for x, y in path:
                set_range(x, x, y, y)
        # Solving paths
        for path in self.target_path.values():
            for x, y in path:
                set_range(x, x, y, y)
        # Ranges
        for rect in self.ranges.values():
            set_range(rect.right(), rect.left(), rect.top(), rect.bottom())
        return x_right, x_left, y_top, y_bottom

    def paintEvent(self, event: QPaintEvent) -> None:
        """Drawing functions."""
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
        super(_DynamicCanvas, self).paintEvent(event)
        # First check
        for path in self.path.path:
            if not path:
                continue
            x, y = path[self.__index]
            if not isnan(x):
                continue
            self.__index, self.__no_error = self.__no_error, self.__index
            self.error = True
            self.__interval = -self.__interval
        # Points that in the current angle section
        self.pos.clear()
        for i in range(len(self.vpoints)):
            if i in self.mechanism['placement']:
                self.pos.append(self.vpoints[i].c[0])
            else:
                x, y = self.path.path[i][self.__index]
                self.pos.append((x, y))
        # Draw links
        for vlink in self.vlinks:
            if vlink.name == VLink.FRAME:
                continue
            self.__draw_link(vlink.name, vlink.points)
        # Draw path
        self.__draw_path()
        # Draw solving path
        self.draw_target_path()
        self.draw_slvs_ranges()
        # Draw points
        for i in range(len(self.vpoints)):
            if not self.pos[i]:
                continue
            self.__draw_point(i)

        self.painter.end()

        if self.error:
            self.error = False
            self.__index, self.__no_error = self.__no_error, self.__index
        else:
            self.__no_error = self.__index

    def __draw_point(self, i: int) -> None:
        """Draw point function."""
        k = i
        for j in range(i):
            if j in self.mechanism['same']:
                k += 1
        x, y = self.pos[i]
        color = color_rgb('Green')
        fixed = False
        if i in self.target_path:
            color = color_rgb('Dark-Orange')
        elif k in self.mechanism['placement']:
            color = color_rgb('Blue')
            fixed = True
        self.draw_point(i, x, y, fixed, color)

    def __draw_link(self, name: str, points: Sequence[int]) -> None:
        """Draw link function.

        The link color will be the default color.
        """
        color = color_qt('Blue')
        pen = QPen(color)
        pen.setWidth(self.link_width)
        self.painter.setPen(pen)
        brush = LINK_COLOR
        brush.setAlphaF(0.70)
        self.painter.setBrush(brush)
        qpoints = tuple(
            QPointF(self.pos[i][0], -self.pos[i][1]) * self.zoom
            for i in points if self.pos[i] and (not isnan(self.pos[i][0]))
        )
        if len(qpoints) == len(points):
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.show_point_mark and name != VLink.FRAME and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.font_size))
            text = f"[{name}]"
            cen_x = sum(self.pos[i][0] for i in points if self.pos[i])
            cen_y = sum(self.pos[i][1] for i in points if self.pos[i])
            self.painter.drawText(QPointF(cen_x, -cen_y) * self.zoom / len(points), text)

    def __draw_path(self) -> None:
        """Draw a path.

        A simple function than main canvas.
        """
        pen = QPen()
        for i, path in enumerate(self.path.path):
            color = color_qt('Green')
            if i in self.target_path:
                color = color_qt('Dark-Orange')
            elif self.__no_mechanism:
                continue
            pen.setColor(color)
            pen.setWidth(self.path_width)
            self.painter.setPen(pen)
            self.draw_curve(path)

    @Slot()
    def __change_index(self) -> None:
        """A slot to change the path index."""
        self.__index += self.__interval
        if self.__index > self.__path_count:
            self.__index = 0
        self.update()


class PreviewDialog(QDialog, Ui_Dialog):

    """Preview dialog has some information.

    We will not be able to change result settings here.
    """

    def __init__(
        self,
        mechanism: Dict[str, Any],
        path: Sequence[Sequence[_Coord]],
        parent: QWidget
    ):
        """Show the information of results, and setup the preview canvas."""
        super(PreviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(
            f"Preview: {mechanism['Algorithm']} "
            f"(max {mechanism['last_gen']} generations)"
        )
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.main_splitter.setSizes([400, 150])
        self.splitter.setSizes([100, 100, 100])
        vpoints = parse_vpoints(mechanism['expression'])
        vlinks = get_vlinks(vpoints)
        self.left_layout.insertWidget(
            0,
            _DynamicCanvas(mechanism, path, vpoints, vlinks, self)
        )
        layout = QVBoxLayout(self.path_cmp_tab)
        layout.addWidget(_DynamicCanvas(mechanism, path, parent=self))
        labels = []
        for tag, data in chain(
            [(tag, mechanism[tag]) for tag in ('Algorithm', 'time')],
            [(f"P{i}", vpoints[i].c[0]) for i in mechanism['placement']]
        ):
            if type(data) is tuple:
                label = f"({data[0]:.02f}, {data[1]:.02f})"
            elif type(data) is float:
                label = f"{data:.02f}"
            else:
                label = f"{data}"
            labels.append(f"{tag}: {label}")
        self.basic_label.setText("\n".join(labels))

        # Algorithm information
        inter = mechanism.get('interrupted', 'N/A')
        if inter == 'False':
            inter_icon = "task_completed.png"
        elif inter == 'N/A':
            inter_icon = "question.png"
        else:
            inter_icon = "interrupted.png"
        if 'last_fitness' in mechanism:
            fitness = f"{mechanism['last_fitness']:.06f}"
        else:
            fitness = 'N/A'
        text_list = [
            f"Max generation: {mechanism.get('last_gen', 'N/A')}",
            f"Fitness: {fitness}",
            f"<img src=\":/icons/{inter_icon}\" width=\"15\"/>"
            f"Interrupted at: {inter}"
        ]
        for k, v in mechanism['settings'].items():
            text_list.append(f"{k}: {v}")
        text = "<br/>".join(text_list)
        self.algorithm_label.setText(f"<html><head/><body><p>{text}</p></body></html>")

        # Hardware information
        self.hardware_label.setText("\n".join([
            f"{tag}: {mechanism['hardware_info'][tag]}" for tag in ('os', 'memory', 'cpu')
        ]))
