# -*- coding: utf-8 -*-

"""A QGraphics widget to rotate the QDial widget."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from qtpy.QtCore import Qt, Signal, Slot, QSize
from qtpy.QtWidgets import QWidget, QDial, QGraphicsView, QGraphicsScene


class QRotatableView(QGraphicsView):
    """Rotate QDial widget."""
    value_changed = Signal(float)

    def __init__(self, parent: QWidget):
        super(QRotatableView, self).__init__(parent)
        scene = QGraphicsScene(self)
        self.setScene(scene)
        self.dial = QDial()
        self.dial.setMinimumSize(QSize(150, 150))
        self.dial.setSingleStep(100)
        self.dial.setPageStep(100)
        self.dial.setInvertedAppearance(True)
        self.dial.setWrapping(True)
        self.dial.setNotchTarget(0.1)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.__value_changed)
        self.set_maximum(360)
        graphics_item = scene.addWidget(self.dial)
        graphics_item.setRotation(-90)
        # Make the QGraphicsView invisible
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(self.dial.height())
        self.setFixedWidth(self.dial.width())
        self.setStyleSheet("border: 0px;")

    @Slot(int)
    def __value_changed(self, value: int) -> None:
        """Value changed signal."""
        self.value_changed.emit(value / 100)

    def value(self) -> float:
        """Get value method."""
        return self.dial.value() / 100

    @Slot(float)
    def set_value(self, value: float) -> None:
        """Set value method."""
        self.dial.setValue(int(value % 360 * 100))

    def minimum(self) -> float:
        """Set maximum method."""
        return self.dial.minimum() / 100

    @Slot(float)
    def set_minimum(self, value: float) -> None:
        """Set minimum."""
        self.dial.setMinimum(int(value * 100))

    def maximum(self) -> float:
        """Set maximum method."""
        return self.dial.maximum() / 100

    @Slot(float)
    def set_maximum(self, value: float) -> None:
        """Set minimum."""
        self.dial.setMaximum(int(value * 100))

    def setEnabled(self, enabled: bool) -> None:
        """Set enabled."""
        super(QRotatableView, self).setEnabled(enabled)
        self.dial.setEnabled(enabled)
