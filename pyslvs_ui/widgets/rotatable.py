# -*- coding: utf-8 -*-

"""A QGraphics widget to rotate the QDial widget."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QGraphicsView, QGraphicsScene


class RotatableView(QGraphicsView):

    """Rotate QDial widget."""

    def __init__(self, item) -> None:
        QGraphicsView.__init__(self)
        scene = QGraphicsScene(self)
        self.setScene(scene)
        item.setMinimumSize(QSize(150, 150))
        item.setMaximum(36000)
        item.setSingleStep(100)
        item.setPageStep(100)
        item.setInvertedAppearance(True)
        item.setWrapping(True)
        item.setNotchTarget(.1)
        item.setNotchesVisible(True)
        graphics_item = scene.addWidget(item)
        graphics_item.setRotation(-90)
        # make the QGraphicsView invisible.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(item.height())
        self.setFixedWidth(item.width())
        self.setStyleSheet("border: 0px;")
