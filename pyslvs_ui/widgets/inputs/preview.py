# -*- coding: utf-8 -*-

"""The animation dialog."""

from typing import Sequence, Tuple
from math import cos, sin, atan2, hypot
from qtpy.QtCore import Qt, Slot
from qtpy.QtWidgets import QWidget, QDialog, QVBoxLayout, QSlider
from qtpy.QtGui import QPaintEvent, QPen, QColor
from numpy import array
from pyslvs import VPoint, derivative
from pyslvs_ui.graphics import AnimationCanvas, color_qt


class _DynamicCanvas(AnimationCanvas):
    def __init__(
        self,
        vpoints: Sequence[VPoint],
        path: Sequence[Sequence[Tuple[float, float]]],
        parent: QWidget
    ):
        super(_DynamicCanvas, self).__init__(parent)
        self.ind = 0
        self.vpoints = vpoints
        self.path.path = path
        self.vel = [derivative(array(path)) for path in self.path.path]
        self.acc = [derivative(vel) for vel in self.vel]

    @Slot(int)
    def set_index(self, ind: int):
        """Set current index."""
        self.ind = ind
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Drawing function."""
        super(_DynamicCanvas, self).paintEvent(event)
        pen = QPen()
        pen.setWidth(self.path_width)
        for i, path in enumerate(self.path.path):
            if self.monochrome:
                pen.setColor(color_qt('gray'))
            elif self.vpoints[i].color is None:
                pen.setColor(color_qt('green'))
            else:
                pen.setColor(QColor(*self.vpoints[i].color))
            self.painter.setPen(pen)
            self.draw_curve(path)
            vpoint = self.vpoints[i]
            x, y = path[self.ind]
            zoom = 50
            for vec, color in [(self.vel[i], Qt.blue), (self.acc[i], Qt.red)]:
                if self.ind >= len(vec):
                    break
                vx, vy = vec[self.ind]
                r = hypot(vx, vy) * zoom
                theta = atan2(vy, vx)
                pen.setColor(color)
                self.painter.setPen(pen)
                self.draw_arrow(x, y, x + r * cos(theta), y + r * sin(theta))
                zoom *= 50
            self.draw_point(i, x, y, vpoint.grounded(), vpoint.color)
        self.painter.end()


class AnimateDialog(QDialog):
    def __init__(
        self,
        vpoints: Sequence[VPoint],
        path: Sequence[Sequence[Tuple[float, float]]],
        monochrome: bool,
        parent: QWidget
    ):
        super(AnimateDialog, self).__init__(parent)
        self.setWindowTitle("Animation")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setMinimumSize(800, 600)
        self.setModal(True)
        layout = QVBoxLayout(self)
        canvas = _DynamicCanvas(vpoints, path, self)
        canvas.set_monochrome_mode(monochrome)
        layout.addWidget(canvas)
        slider = QSlider(Qt.Horizontal, self)
        slider.setMaximum(max(len(p) for p in path) - 1)
        slider.valueChanged.connect(canvas.set_index)
        layout.addWidget(slider)
