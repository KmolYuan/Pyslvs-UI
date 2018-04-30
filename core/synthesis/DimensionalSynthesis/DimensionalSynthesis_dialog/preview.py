# -*- coding: utf-8 -*-

"""The preview dialog of dimensional synthesis result."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from math import isnan
from typing import Tuple
from core.QtModules import (
    QTimer,
    QPen,
    QColor,
    Qt,
    QPointF,
    QFont,
    pyqtSlot,
    QDialog,
)
from core.graphics import (
    BaseCanvas,
    colorQt
)
from core.io import strbetween
from .Ui_preview import Ui_Dialog


class DynamicCanvas(BaseCanvas):
    
    """Custom canvas for preview algorithm result."""
    
    def __init__(self, mechanism, Path, parent):
        super(DynamicCanvas, self).__init__(parent)
        self.mechanism = mechanism
        self.Path.path = Path
        self.length = 0
        for path in self.Path.path:
            l = len(path)
            if l > self.length:
                self.length = l
        self.targetPath = self.mechanism['Target']
        self.index = 0
        #exp_symbol = ('A', 'B', 'C', 'D', 'E')
        self.exp_symbol = set()
        self.links = []
        for exp in self.mechanism['Link_Expression'].split(';'):
            names = strbetween(exp, '[', ']').split(',')
            self.links.append(tuple(names))
            for name in names:
                self.exp_symbol.add(name)
        self.exp_symbol = sorted(
            self.exp_symbol,
            key = lambda e: int(e.replace('P', ''))
        )
        #Error
        self.ERROR = False
        self.no_error = 0
        #Timer start.
        timer = QTimer(self)
        timer.timeout.connect(self.change_index)
        timer.start(17)
    
    def __zoomToFitLimit(self):
        """Limitations of four side."""
        inf = float('inf')
        x_right = inf
        x_left = -inf
        y_top = -inf
        y_bottom = inf
        #Points
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
        #Paths
        for i, path in enumerate(self.Path.path):
            if self.Path.show!=-1 and self.Path.show!=i:
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
        #Solving paths
        for path in self.targetPath.values():
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
        x_diff = x_diff if x_diff!=0 else 1
        y_diff = y_diff if y_diff!=0 else 1
        if width / x_diff < height / y_diff:
            factor = width / x_diff
        else:
            factor = height / y_diff
        self.zoom = factor * 0.95
        self.ox = width / 2 - (x_left + x_right) / 2 *self.zoom
        self.oy = height / 2 + (y_top + y_bottom) / 2 *self.zoom
        super(DynamicCanvas, self).paintEvent(event)
        #Points that in the current angle section.
        """First check."""
        for path in self.Path.path:
            if not path:
                continue
            x, y = path[self.index]
            if isnan(x):
                self.index, self.no_error = self.no_error, self.index
                self.ERROR = True
        self.Point = []
        for i, name in enumerate(self.exp_symbol):
            if (name in self.mechanism['Driver']) or (name in self.mechanism['Follower']):
                self.Point.append(self.mechanism[name])
            else:
                x, y = self.Path.path[i][self.index]
                self.Point.append((x, y))
        #Draw links.
        for i, exp in enumerate(self.links):
            if i == 0:
                continue
            name = "link_{}".format(i)
            self.drawLink(name, tuple(self.exp_symbol.index(tag) for tag in exp))
        #Draw path.
        self.drawPath()
        #Draw solving path.
        self._BaseCanvas__drawTargetPath()
        #Draw points.
        for i, name in enumerate(self.exp_symbol):
            if not self.Point[i]:
                continue
            x, y = self.Point[i]
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
            self._BaseCanvas__drawPoint(i, x, y, fixed, color)
        self.painter.end()
        if self.ERROR:
            self.ERROR = False
            self.index, self.no_error = self.no_error, self.index
        else:
            self.no_error = self.index
    
    def drawLink(self,
        name: str,
        points: Tuple[int]
    ):
        """Draw linkage function.
        
        The link color will be the default color.
        """
        color = colorQt('Blue')
        pen = QPen(color)
        pen.setWidth(self.linkWidth)
        self.painter.setPen(pen)
        brush = QColor(226, 219, 190)
        brush.setAlphaF(0.70)
        self.painter.setBrush(brush)
        qpoints = tuple(
            QPointF(self.Point[i][0]*self.zoom, self.Point[i][1]*-self.zoom)
            for i in points if self.Point[i] and not isnan(self.Point[i][0])
        )
        if len(qpoints)==len(points):
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.showPointMark and name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.fontSize))
            text = "[{}]".format(name)
            cenX = sum(
                self.Point[i][0]
                for i in points if self.Point[i]
            )
            cenY = sum(
                self.Point[i][1]
                for i in points if self.Point[i]
            )
            cenX *= self.zoom / len(points)
            cenY *= -self.zoom / len(points)
            self.painter.drawText(QPointF(cenX, cenY), text)
    
    def drawPath(self):
        """Draw a path.
        
        A simple function than main canvas.
        """
        pen = QPen()
        Path = self.Path.path
        for i, path in enumerate(Path):
            color = colorQt('Green')
            if self.exp_symbol[i] in self.mechanism['Target']:
                color = colorQt('Dark-Orange')
            pen.setColor(color)
            pen.setWidth(self.pathWidth)
            self.painter.setPen(pen)
            self._BaseCanvas__drawCurve(path)
    
    @pyqtSlot()
    def change_index(self):
        """A slot to change the path index."""
        self.index += 1
        self.index %= self.length
        self.update()


class PreviewDialog(QDialog, Ui_Dialog):
    
    """Preview dialog has some informations.
    
    We will not be able to change result settings here.
    """
    
    def __init__(self, mechanism, Path, parent):
        super(PreviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.mechanism = mechanism
        self.setWindowTitle("Preview: {} (max {} generations)".format(
            self.mechanism['Algorithm'], self.mechanism['lastGen']
        ))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.main_splitter.setSizes([800, 100])
        self.splitter.setSizes([100, 100, 100])
        previewWidget = DynamicCanvas(self.mechanism, Path, self)
        self.left_layout.insertWidget(0, previewWidget)
        #Basic information
        link_tags = []
        for expr in self.mechanism['Expression'].split(';'):
            for p in strbetween(expr, '[', ']').split(','):
                if ('L' in p) and (p not in link_tags):
                    link_tags.append(p)
        self.basic_label.setText("\n".join(
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in ['Algorithm', 'time']] +
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in self.mechanism['Driver']] +
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in self.mechanism['Follower']] +
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in sorted(link_tags)]
        ))
        #Algorithm information
        interrupt = self.mechanism['interrupted']
        fitness = self.mechanism['TimeAndFitness'][-1]
        self.algorithm_label.setText("<html><head/><body><p>"+
            "<br/>".join(["Max generation: {}".format(self.mechanism['lastGen'])]+
            ["Fitness: {}".format(fitness if type(fitness)==float else fitness[1])]+
            ["<img src=\"{}\" width=\"15\"/>".format(":/icons/task-completed.png" if interrupt=='False' else
            ":/icons/question-mark.png" if interrupt=='N/A' else ":/icons/interrupted.png")+
            "Interrupted at: {}".format(interrupt)]+
            ["{}: {}".format(k, v) for k, v in self.mechanism['settings'].items()])+
            "</p></body></html>")
        #Hardware information
        self.hardware_label.setText("\n".join([
            "{}: {}".format(tag, self.mechanism['hardwareInfo'][tag])
            for tag in ['os', 'memory', 'cpu']
        ]))
