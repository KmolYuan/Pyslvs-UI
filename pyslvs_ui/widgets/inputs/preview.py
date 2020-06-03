# -*- coding: utf-8 -*-

"""The animation dialog."""

from typing import Sequence, Tuple
from qtpy.QtCore import Qt, Slot
from qtpy.QtWidgets import QWidget, QDialog, QVBoxLayout, QSlider
from qtpy.QtGui import QPaintEvent, QPen, QColor
from pyslvs import VPoint
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

    @Slot(int)
    def set_index(self, ind: int):
        """Set current index."""
        self.ind = ind

    def paintEvent(self, event: QPaintEvent) -> None:
        """Drawing function."""
        super(_DynamicCanvas, self).paintEvent(event)
        self.__draw_paths()
        self.painter.end()

    def __draw_paths(self) -> None:
        """Draw paths."""
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
        slider.setMaximum(max(len(p) for p in path))
        slider.valueChanged.connect(canvas.set_index)
        layout.addWidget(slider)
