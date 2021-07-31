# -*- coding: utf-8 -*-

"""The vector animation dialog."""

from typing import Sequence, Tuple, Mapping
from math import cos, sin, atan2, hypot, degrees
from qtpy.QtCore import Qt, Slot, QTimer
from qtpy.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QSlider, QPushButton, QLabel,
    QSpacerItem, QSizePolicy, QDoubleSpinBox, QComboBox,
)
from qtpy.QtGui import QPaintEvent, QPen, QPixmap, QIcon
from numpy import array, ndarray, isclose, isnan
from pyslvs import VPoint, VLink, VJoint
from pyslvs.optimization import derivative
from pyslvs_ui.graphics import (
    AnimationCanvas, color_qt, convex_hull, LINK_COLOR,
)

_Coord = Tuple[float, float]
_Paths = Sequence[Sequence[_Coord]]
_SliderPaths = Mapping[int, Sequence[_Coord]]
_Vecs = Mapping[int, ndarray]


class _DynamicCanvas(AnimationCanvas):
    vel: _Vecs
    vel_slider: _Vecs
    acc: _Vecs
    acc_slider: _Vecs

    def __init__(
        self,
        vpoints: Sequence[VPoint],
        vlinks: Sequence[VLink],
        path: _Paths,
        slider_path: _SliderPaths,
        parent: QWidget
    ):
        super(_DynamicCanvas, self).__init__(parent)
        self.ind = 0
        self.vpoints = vpoints
        self.vlinks = vlinks
        self.path.path = path
        self.path.slider_path = slider_path
        self.vel = {i: derivative(array(path))
                    for i, path in enumerate(self.path.path)}
        self.vel_slider = {i: derivative(array(p))
                           for i, p in self.path.slider_path.items()}
        self.acc = {i: derivative(p) for i, p in self.vel.items()}
        self.acc_slider = {i: derivative(p)
                           for i, p in self.vel_slider.items()}
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
        self.factor = scalar / self.max_ind
        self.update()

    def get_vel(self, ind: int) -> Tuple[float, float]:
        """Get the magnitude and angle from velocity."""
        vx, vy = self.vel[ind][self.ind]
        return hypot(vx, vy), degrees(atan2(vy, vx))

    def get_acc(self, ind: int) -> Tuple[float, float]:
        """Get the magnitude and angle from acceleration."""
        vx, vy = self.acc[ind][self.ind]
        return hypot(vx, vy), degrees(atan2(vy, vx))

    def paintEvent(self, event: QPaintEvent) -> None:
        """Drawing function."""
        super(_DynamicCanvas, self).paintEvent(event)
        pen = QPen()
        pen.setWidth(self.link_width)
        brush = color_qt('dark-gray') if self.monochrome else LINK_COLOR
        self.painter.setBrush(brush)
        for vlink in self.vlinks:
            if vlink.name == VLink.FRAME or not vlink.points:
                continue
            points = []
            for i in vlink.points:
                vpoint = self.vpoints[i]
                if (vpoint.type == VJoint.R
                        or not vpoint.is_slot_link(vlink.name)):
                    x, y = self.path.path[i][self.ind]
                else:
                    x, y = self.path.slider_path[i][self.ind]
                points.append((x * self.zoom, y * -self.zoom))
            qpoints = convex_hull(points, as_qpoint=True)
            pen.setColor(Qt.black if self.monochrome else color_qt(vlink.color))
            self.painter.setPen(pen)
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        pen.setWidth(self.path_width)
        for paths, vel, acc in [
            (enumerate(self.path.path), self.vel, self.acc),
            (self.path.slider_path.items(), self.vel_slider, self.acc_slider),
        ]:
            for i, path in paths:
                vpoint = self.vpoints[i]
                if self.monochrome:
                    color = color_qt('gray')
                else:
                    color = color_qt(vpoint.color)
                pen.setColor(color)
                self.painter.setPen(pen)
                self.draw_curve(path)
                x, y = path[self.ind]
                zoom = 1.
                for vec, color in [(vel[i], Qt.blue), (acc[i], Qt.red)]:
                    if self.ind >= len(vec):
                        break
                    vx, vy = vec[self.ind]
                    if isnan(vx) or isnan(vy):
                        break
                    zoom /= self.factor
                    r = hypot(vx, vy) * zoom
                    if isclose(r, 0):
                        break
                    th = atan2(vy, vx)
                    pen.setColor(color)
                    self.painter.setPen(pen)
                    self.draw_arrow(x, y, x + r * cos(th), y + r * sin(th))
                self.draw_point(i, x, y, vpoint.grounded(), vpoint.color)
        self.painter.end()


class AnimateDialog(QDialog):

    def __init__(
        self,
        vpoints: Sequence[VPoint],
        vlinks: Sequence[VLink],
        path: _Paths,
        slider_path: _SliderPaths,
        monochrome: bool,
        parent: QWidget
    ):
        super(AnimateDialog, self).__init__(parent)
        self.setWindowTitle("Vector Animation")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint
                            & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(800, 600)
        self.setModal(True)
        main_layout = QVBoxLayout(self)
        self.canvas = _DynamicCanvas(vpoints, vlinks, path, slider_path, self)
        self.canvas.set_monochrome_mode(monochrome)
        self.canvas.update_pos.connect(self.__set_pos)
        layout = QHBoxLayout(self)
        pt_option = QComboBox(self)
        pt_option.addItems([f"P{p}" for p in range(len(vpoints))])
        layout.addWidget(pt_option)
        value_label = QLabel(self)

        @Slot(int)
        def show_values(ind: int):
            vel, vel_deg = self.canvas.get_vel(ind)
            acc, acc_deg = self.canvas.get_acc(ind)
            value_label.setText(f"Velocity: {vel:.04f} ({vel_deg:.04f}deg) | "
                                f"Acceleration: {acc:.04f} ({acc_deg:.04f}deg)")

        pt_option.currentIndexChanged.connect(show_values)
        layout.addWidget(value_label)
        self.pos_label = QLabel(self)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding,
                                   QSizePolicy.Minimum))
        layout.addWidget(self.pos_label)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.canvas)
        layout = QHBoxLayout(self)
        self.play = QPushButton(QIcon(QPixmap("icons:play.png")), "", self)
        self.play.setCheckable(True)
        self.play.clicked.connect(self.__play)
        layout.addWidget(self.play)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMaximum(max(len(p) for p in path) - 1)
        self.slider.valueChanged.connect(self.canvas.set_index)
        layout.addWidget(self.slider)
        layout.addWidget(QLabel("Total times:", self))
        factor = QDoubleSpinBox(self)
        factor.valueChanged.connect(self.canvas.set_factor)
        factor.setSuffix('s')
        factor.setRange(0.01, 999999)
        factor.setValue(10)
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
        self.pos_label.setText(f"({x:.04f}, {y:.04f})")

    @Slot()
    def __play(self):
        """Start playing."""
        if self.play.isChecked():
            self.timer.start()
        else:
            self.timer.stop()
