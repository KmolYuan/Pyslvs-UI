# -*- coding: utf-8 -*-

"""The canvas of main window."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from collections import deque
from typing import (
    List,
    Tuple,
    Dict,
)
from core.QtModules import (
    pyqtSignal,
    pyqtSlot,
    Qt,
    QApplication,
    QRectF,
    QPointF,
    QSizeF,
    QCursor,
    QToolTip,
)
from core.graphics import BaseCanvas
from core.libs import VPoint, VLink
from . import main_canvas_method as _method
from .main_canvas_method import Selector, FreeMode


class DynamicCanvas(BaseCanvas):
    
    """The canvas in main window.
    
    + Parse and show PMKS expression.
    + Show paths.
    + Show settings of dimensional synthesis widget.
    + Mouse interactions.
    + Zoom to fit function.
    """
    
    tracking = pyqtSignal(float, float)
    browse_tracking = pyqtSignal(float, float)
    selected = pyqtSignal(tuple, bool)
    freemoved = pyqtSignal(tuple)
    noselected = pyqtSignal()
    alt_add = pyqtSignal()
    doubleclick_edit = pyqtSignal(int)
    zoom_changed = pyqtSignal(int)
    
    def __init__(self, parent):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip("Use mouse wheel or middle button to look around.")
        #Functions from the main window.
        self.getTriangle = parent.getTriangle
        self.rightInput = parent.rightInput
        self.pathInterval = parent.pathInterval
        #The current mouse coordinates.
        self.selector = Selector()
        #Entities.
        self.Points = tuple()
        self.Links = tuple()
        #Select function.
        self.selectionMode = 0
        self.sr = 10
        self.selections = []
        #Linkage transparency.
        self.transparency = 1.
        #Path solving range.
        self.ranges = {}
        #Set showDimension to False.
        self.showDimension = False
        #Free move mode.
        self.freemove = FreeMode.NoFreeMove
        #Auto preview function.
        self.autoPathShow = True
        #Zooming center.
        """
        0: By cursor.
        1: By canvas center.
        """
        self.zoomby = 0
        #Mouse snapping value.
        self.snap = 5
        #Dependent functions to set zoom bar.
        self.__setZoom = parent.ZoomBar.setValue
        self.__zoom = parent.ZoomBar.value
        self.__zoom_factor = parent.scalefactor_option.value
        #Dependent functions to set selection mode.
        self.__setSelectionMode = parent.EntitiesTab.setCurrentIndex
        self.__selectionMode = parent.EntitiesTab.currentIndex
        #Default margin factor.
        self.marginFactor = 0.95
        #Widget size.
        self.width_old = None
        self.height_old = None
    
    def updateFigure(self,
        Points: Tuple[VPoint],
        Links: Tuple[VLink],
        path: List[Tuple[float, float]]
    ):
        """Update with Point and Links data."""
        self.Points = Points
        self.Links = Links
        self.Path.path = path
        self.update()
    
    @pyqtSlot(int)
    def setLinkWidth(self, linkWidth: int):
        """Update width of linkages."""
        self.linkWidth = linkWidth
        self.update()
    
    @pyqtSlot(int)
    def setPathWidth(self, pathWidth: int):
        """Update width of linkages."""
        self.pathWidth = pathWidth
        self.update()
    
    @pyqtSlot(bool)
    def setPointMark(self, showPointMark: bool):
        """Update show point mark or not."""
        self.showPointMark = showPointMark
        self.update()
    
    @pyqtSlot(bool)
    def setShowDimension(self, showDimension: bool):
        """Update show dimension or not."""
        self.showDimension = showDimension
        self.update()
    
    @pyqtSlot(bool)
    def setCurveMode(self, curve: bool):
        """Update show as curve mode or not."""
        self.Path.curve = curve
        self.update()
    
    @pyqtSlot(int)
    def setFontSize(self, fontSize: int):
        """Update font size."""
        self.fontSize = fontSize
        self.update()
    
    @pyqtSlot(int)
    def setZoom(self, zoom: int):
        """Update zoom factor."""
        zoom_old = self.zoom
        self.zoom = zoom / 100 * self.rate
        dz = zoom_old - self.zoom
        if self.zoomby == 0:
            pos = self.mapFromGlobal(QCursor.pos())
        elif self.zoomby == 1:
            pos = QPointF(self.width() / 2, self.height() / 2)
        self.ox += (pos.x() - self.ox) / self.zoom * dz
        self.oy += (pos.y() - self.oy) / self.zoom * dz
        self.update()
    
    def setShowTargetPath(self, showTargetPath: bool):
        """Update show target path or not."""
        self.showTargetPath = showTargetPath
        self.update()
    
    def setFreeMove(self, freemove: int):
        """Update freemove mode number."""
        self.freemove = FreeMode(freemove)
        self.update()
    
    @pyqtSlot(int)
    def setSelectionRadius(self, sr: int):
        """Update radius of point selector."""
        self.sr = sr
    
    @pyqtSlot(int)
    def setTransparency(self, transparency: int):
        """Update transparency.
        
        0%: opaque.
        """
        self.transparency = (100 - transparency) / 100
        self.update()
    
    @pyqtSlot(int)
    def setMarginFactor(self, marginFactor: int):
        """Update margin factor when zoom to fit."""
        self.marginFactor = 1 - marginFactor / 100
        self.update()
    
    @pyqtSlot(int)
    def setJointSize(self, jointsize: int):
        """Update size for each joint."""
        self.jointsize = jointsize
        self.update()
    
    @pyqtSlot(int)
    def setZoomBy(self, zoomby: int):
        """Update zooming center option."""
        self.zoomby = zoomby
    
    @pyqtSlot(float)
    def setSnap(self, snap: float):
        """Update mouse capture value."""
        self.snap = snap
    
    @pyqtSlot(int)
    def setSelectionMode(self, selectionMode: int):
        """Update the selection."""
        self.selectionMode = selectionMode
        self.update()
    
    @pyqtSlot(list)
    def setSelection(self, selections: List[int]):
        """Update the selection."""
        self.selections = selections
        self.update()
    
    def setSolvingPath(self,
        targetPath: Dict[str, Tuple[Tuple[float, float]]]
    ):
        """Update target path."""
        self.targetPath = targetPath
        self.update()
    
    def setPathShow(self, p: int):
        """Update path present mode.
        
        -2: Hide all paths.
        -1: Show all paths.
        i: Show path i.
        """
        self.Path.show = p
        self.update()
    
    def setAutoPath(self, autoPathShow: bool):
        """Enable auto preview function."""
        self.autoPathShow = autoPathShow
        self.update()
    
    def updateRanges(self, ranges: Dict[str, Tuple[float, float, float]]):
        """Update the ranges of dimensional synthesis."""
        self.ranges.clear()
        self.ranges.update({tag: QRectF(
            QPointF(values[0] - values[2]/2, values[1] + values[2]/2),
            QSizeF(values[2], values[2])
        ) for tag, values in ranges.items()})
        self.update()
    
    def recordStart(self, limit: int):
        """Start a limit from main window."""
        self.path_record = [deque([], limit) for i in range(len(self.Points))]
    
    def recordPath(self):
        """Recording path."""
        for i, vpoint in enumerate(self.Points):
            self.path_record[i].append((vpoint.cx, vpoint.cy))
    
    def getRecordPath(self) -> Tuple[Tuple[Tuple[float, float]]]:
        return _method.getRecordPath(self)
    
    def paintEvent(self, event):
        _method.paintEvent(self, event)
    
    def wheelEvent(self, event):
        """Set zoom bar value by mouse wheel."""
        value = event.angleDelta().y()
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.__setSelectionMode(self.__selectionMode() + (-1 if (value > 0) else 1))
            i = self.__selectionMode()
            QToolTip.showText(
                event.globalPos(),
                "<p style=\"background-color: #77abff\">{}</p>".format(''.join(
                    "<img width=\"{}\" src=\":icons/{}.png\"/>".format(70 if (i == j) else 40, icon)
                    for j, icon in enumerate(('bearing', 'link', 'triangular-iteration'))
                )),
                self
            )
        else:
            self.__setZoom(self.__zoom() + self.__zoom_factor() * (1 if (value > 0) else -1))
        event.accept()
    
    def mousePressEvent(self, event):
        _method.mousePressEvent(self, event)
    
    def mouseDoubleClickEvent(self, event):
        _method.mouseDoubleClickEvent(self, event)
    
    def mouseReleaseEvent(self, event):
        _method.mouseReleaseEvent(self, event)
    
    def mouseMoveEvent(self, event):
        _method.mouseMoveEvent(self, event)
    
    def zoomToFit(self):
        _method.zoomToFit(self)
