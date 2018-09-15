# -*- coding: utf-8 -*-

"""The preview dialog of dimensional synthesis result."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from math import isnan
from itertools import chain
from typing import (
    Tuple,
    List,
    Dict,
    Sequence,
    Any,
)
from core.QtModules import (
    pyqtSlot,
    Qt,
    QTimer,
    QPen,
    QColor,
    QPointF,
    QFont,
    QDialog,
    QWidget,
)
from core.graphics import BaseCanvas, colorQt
from core.io import strbetween
from .Ui_preview import Ui_Dialog


class _DynamicCanvas(BaseCanvas):
    
    """Custom canvas for preview algorithm result."""
    
    def __init__(
        self,
        mechanism: Dict[str, Any],
        path: Sequence[Sequence[Tuple[float, float]]],
        parent: QWidget
    ):
        """Input link and path data."""
        super(_DynamicCanvas, self).__init__(parent)
        self.mechanism = mechanism
        self.Path.path = path
        self.target_path = self.mechanism['Target']
        self.__index = 0
        self.__interval = 1
        self.__path_count = max(len(path) for path in self.Path.path) - 1
        self.pos: List[Tuple[float, float]] = []
        
        # exp_symbol = {'P1', 'P2', 'P3', ...}
        exp_symbol = set()
        self.links = []
        for exp in self.mechanism['Link_expr'].split(';'):
            names = strbetween(exp, '[', ']').split(',')
            self.links.append(tuple(names))
            for name in names:
                exp_symbol.add(name)
        self.exp_symbol = sorted(exp_symbol, key=lambda e: int(e.replace('P', '')))
        # Error
        self.error = False
        self.__no_error = 0
        # Timer start.
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__change_index)
        self.__timer.start(18)
    
    def __zoomToFitLimit(self) -> Tuple[float, float, float, float]:
        """Limitations of four side."""
        inf = float('inf')
        x_right = inf
        x_left = -inf
        y_top = -inf
        y_bottom = inf
        # Points
        for name in self.exp_symbol:
            x, y = self.mechanism[name]
            if x < x_right:
                x_right = x
            if x > x_left:
                x_left = x
            if y < y_bottom:
                y_bottom = y
            if y > y_top:
                y_top = y
        # Paths
        for i, path in enumerate(self.Path.path):
            if self.Path.show != -1 and self.Path.show != i:
                continue
            for x, y in path:
                if x < x_right:
                    x_right = x
                if x > x_left:
                    x_left = x
                if y < y_bottom:
                    y_bottom = y
                if y > y_top:
                    y_top = y
        # Solving paths
        for path in self.target_path.values():
            for x, y in path:
                if x < x_right:
                    x_right = x
                if x > x_left:
                    x_left = x
                if y < y_bottom:
                    y_bottom = y
                if y > y_top:
                    y_top = y
        return x_right, x_left, y_top, y_bottom
    
    def paintEvent(self, event):
        """Drawing functions."""
        width = self.width()
        height = self.height()
        x_right, x_left, y_top, y_bottom = self.__zoomToFitLimit()
        x_diff = x_left - x_right
        y_diff = y_top - y_bottom
        x_diff = x_diff if x_diff else 1
        y_diff = y_diff if y_diff else 1
        if width / x_diff < height / y_diff:
            factor = width / x_diff
        else:
            factor = height / y_diff
        self.zoom = factor * 0.95
        self.ox = width / 2 - (x_left + x_right) / 2 * self.zoom
        self.oy = height / 2 + (y_top + y_bottom) / 2 * self.zoom
        super(_DynamicCanvas, self).paintEvent(event)
        
        # First check.
        for path in self.Path.path:
            if not path:
                continue
            x, y = path[self.__index]
            if isnan(x):
                self.__index, self.__no_error = self.__no_error, self.__index
                self.error = True
                self.__interval = -self.__interval
        
        # Points that in the current angle section.
        self.pos.clear()
        for i, name in enumerate(self.exp_symbol):
            if (name in self.mechanism['Driver']) or (name in self.mechanism['Follower']):
                self.pos.append(self.mechanism[name])
            else:
                x, y = self.Path.path[i][self.__index]
                self.pos.append((x, y))
        
        # Draw links.
        for i, exp in enumerate(self.links):
            if i == 0:
                continue
            self.__drawLink(f"link_{i}", [self.exp_symbol.index(tag) for tag in exp])
        
        # Draw path.
        self.__drawPath()
        
        # Draw solving path.
        self.drawTargetPath()
        
        # Draw points.
        for i, name in enumerate(self.exp_symbol):
            if not self.pos[i]:
                continue
            self.__drawPoint(i, name)
        
        self.painter.end()
        
        if self.error:
            self.error = False
            self.__index, self.__no_error = self.__no_error, self.__index
        else:
            self.__no_error = self.__index
    
    def __drawPoint(self, i: int, name: str):
        """Draw point function."""
        x, y = self.pos[i]
        color = colorQt('Green')
        fixed = False
        if name in self.mechanism['Target']:
            color = colorQt('Dark-Orange')
        elif name in self.mechanism['Driver']:
            color = colorQt('Red')
            fixed = True
        elif name in self.mechanism['Follower']:
            color = colorQt('Blue')
            fixed = True
        self.drawPoint(i, x, y, fixed, color)
    
    def __drawLink(self, name: str, points: List[int]):
        """Draw link function.
        
        The link color will be the default color.
        """
        color = colorQt('Blue')
        pen = QPen(color)
        pen.setWidth(self.link_width)
        self.painter.setPen(pen)
        brush = QColor(226, 219, 190)
        brush.setAlphaF(0.70)
        self.painter.setBrush(brush)
        qpoints = tuple(
            QPointF(self.pos[i][0], -self.pos[i][1]) * self.zoom
            for i in points if self.pos[i] and (not isnan(self.pos[i][0]))
        )
        if len(qpoints) == len(points):
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.show_point_mark and (name != 'ground') and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.font_size))
            text = f"[{name}]"
            cen_x = sum(self.pos[i][0] for i in points if self.pos[i])
            cen_y = sum(self.pos[i][1] for i in points if self.pos[i])
            self.painter.drawText(QPointF(cen_x, -cen_y) * self.zoom / len(points), text)
    
    def __drawPath(self):
        """Draw a path.
        
        A simple function than main canvas.
        """
        pen = QPen()
        for i, path in enumerate(self.Path.path):
            color = colorQt('Green')
            if self.exp_symbol[i] in self.mechanism['Target']:
                color = colorQt('Dark-Orange')
            pen.setColor(color)
            pen.setWidth(self.path_width)
            self.painter.setPen(pen)
            self.drawCurve(path)
    
    @pyqtSlot()
    def __change_index(self):
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
        path: Sequence[Sequence[Tuple[float, float]]],
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
        self.main_splitter.setSizes([800, 100])
        self.splitter.setSizes([100, 100, 100])
        preview_widget = _DynamicCanvas(mechanism, path, self)
        self.left_layout.insertWidget(0, preview_widget)
        # Basic information
        link_tags = []
        for expr in mechanism['Expression'].split(';'):
            for p in strbetween(expr, '[', ']').split(','):
                if ('L' in p) and (p not in link_tags):
                    link_tags.append(p)
        self.basic_label.setText("\n".join([f"{tag}: {mechanism[tag]}" for tag in chain(
            ('Algorithm', 'time'),
            mechanism['Driver'],
            mechanism['Follower'],
            sorted(link_tags)
        )]))
        # Algorithm information
        fitness = mechanism['time_fitness'][-1]
        if mechanism['interrupted'] == 'False':
            interrupt_icon = "task-completed.png"
        elif mechanism['interrupted'] == 'N/A':
            interrupt_icon = "question-mark.png"
        else:
            interrupt_icon = "interrupted.png"
        text_list = [
            f"Max generation: {mechanism['last_gen']}",
            f"Fitness: {fitness if type(fitness) == float else fitness[1]}",
            f"<img src=\":/icons/{interrupt_icon}\" width=\"15\"/>"
            f"Interrupted at: {mechanism['interrupted']}"
        ]
        for k, v in mechanism['settings'].items():
            text_list.append(f"{k}: {v}")
        text = "<br/>".join(text_list)
        self.algorithm_label.setText(f"<html><head/><body><p>{text}</p></body></html>")
        # Hardware information
        self.hardware_label.setText("\n".join([
            f"{tag}: {mechanism['hardware_info'][tag]}" for tag in ('os', 'memory', 'cpu')
        ]))
