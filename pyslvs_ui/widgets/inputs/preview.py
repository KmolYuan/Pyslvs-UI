# -*- coding: utf-8 -*-

"""The animation dialog."""

from typing import Sequence, Tuple
from math import cos, sin, atan2, hypot
from qtpy.QtCore import Qt, Slot, QTimer
from qtpy.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QSlider, QPushButton, QLabel,
    QSpacerItem, QSizePolicy, QDoubleSpinBox,
)
from qtpy.QtGui import QPaintEvent, QPen, QColor, QPixmap, QIcon
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
        self.max_ind = max(len(p) for p in self.path.path)
        self.factor = 1.

    @Slot(int)
    def set_index(self, ind: int):
        """Set current index."""
        self.ind = ind
        self.update()

    @Slot(float)
    def set_factor(self, scalar: float):
        """Set the size of the derived value."""
        self.factor = scalar
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
            zoom = 1.
            for vec, color in [(self.vel[i], Qt.blue), (self.acc[i], Qt.red)]:
                if self.ind >= len(vec):
                    break
                zoom *= self.factor
                vx, vy = vec[self.ind]
                r = hypot(vx, vy) * zoom
                if r == 0:
                    break
                theta = atan2(vy, vx)
                pen.setColor(color)
                self.painter.setPen(pen)
                self.draw_arrow(x, y, x + r * cos(theta), y + r * sin(theta))
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
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint
                            & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(800, 600)
        self.setModal(True)
        main_layout = QVBoxLayout(self)
        layout = QHBoxLayout(self)
        self.label = QLabel(self)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding,
                                   QSizePolicy.Minimum))
        layout.addWidget(self.label)
        main_layout.addLayout(layout)
        self.canvas = _DynamicCanvas(vpoints, path, self)
        self.canvas.set_monochrome_mode(monochrome)
        self.canvas.update_pos.connect(self.__set_pos)
        main_layout.addWidget(self.canvas)
        layout = QHBoxLayout(self)
        self.play = QPushButton(QIcon(QPixmap(":/icons/play.png")), "", self)
        self.play.setCheckable(True)
        self.play.clicked.connect(self.__play)
        layout.addWidget(self.play)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMaximum(max(len(p) for p in path) - 1)
        self.slider.valueChanged.connect(self.canvas.set_index)
        layout.addWidget(self.slider)
        factor = QDoubleSpinBox(self)
        factor.valueChanged.connect(self.canvas.set_factor)
        factor.setRange(0.01, 9999)
        factor.setValue(50)
        layout.addWidget(factor)
        main_layout.addLayout(layout)
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.__move_ind)

    @Slot()
    def __move_ind(self):
        """Move indicator."""
        value = self.slider.value() + 1
        self.slider.setValue(value)
        if value > self.slider.maximum():
            self.slider.setValue(0)

    @Slot(float, float)
    def __set_pos(self, x: float, y: float) -> None:
        """Set mouse position."""
        self.label.setText(f"({x:.04f}, {y:.04f})")

    @Slot()
    def __play(self):
        """Start playing."""
        if self.play.isChecked():
            self.timer.start()
        else:
            self.timer.stop()
