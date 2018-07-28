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
    Union,
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
    QWidget,
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
    
    def __init__(self, parent: QWidget):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip("Use mouse wheel or middle button to look around.")
        #The current mouse coordinates.
        self.selector = Selector()
        #Entities.
        self.vpoints = ()
        self.vlinks = ()
        self.vangles = ()
        #Solution.
        self.exprs = []
        #Select function.
        self.select_mode = 0
        self.sr = 10
        self.selections = []
        #Link transparency.
        self.transparency = 1.
        #Path solving range.
        self.ranges = {}
        #Set show_dimension to False.
        self.show_dimension = False
        #Free move mode.
        self.freemove = FreeMode.NoFreeMove
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
        self.margin_factor = 0.95
        #Widget size.
        self.width_old = None
        self.height_old = None
    
    def updateFigure(self,
        vpoints: Tuple[VPoint],
        vlinks: Tuple[VLink],
        exprs: List[Tuple[str]],
        path: List[Tuple[float, float]]
    ):
        """Update with Point and Links data."""
        self.vpoints = vpoints
        self.vlinks = vlinks
        self.vangles = tuple(vpoint.angle for vpoint in self.vpoints)
        self.exprs = exprs
        self.Path.path = path
        self.update()
    
    @pyqtSlot(int)
    def setLinkWidth(self, link_width: int):
        """Update width of links."""
        self.link_width = link_width
        self.update()
    
    @pyqtSlot(int)
    def setPathWidth(self, path_width: int):
        """Update width of links."""
        self.path_width = path_width
        self.update()
    
    @pyqtSlot(bool)
    def setPointMark(self, show_point_mark: bool):
        """Update show point mark or not."""
        self.show_point_mark = show_point_mark
        self.update()
    
    @pyqtSlot(bool)
    def setShowDimension(self, show_dimension: bool):
        """Update show dimension or not."""
        self.show_dimension = show_dimension
        self.update()
    
    @pyqtSlot(bool)
    def setCurveMode(self, curve: bool):
        """Update show as curve mode or not."""
        self.Path.curve = curve
        self.update()
    
    @pyqtSlot(int)
    def setFontSize(self, font_size: int):
        """Update font size."""
        self.font_size = font_size
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
    
    def setShowTargetPath(self, show_target_path: bool):
        """Update show target path or not."""
        self.show_target_path = show_target_path
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
    def setMarginFactor(self, margin_factor: int):
        """Update margin factor when zoom to fit."""
        self.margin_factor = 1 - margin_factor / 100
        self.update()
    
    @pyqtSlot(int)
    def setJointSize(self, joint_size: int):
        """Update size for each joint."""
        self.joint_size = joint_size
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
    def setSelectionMode(self, select_mode: int):
        """Update the selection."""
        self.select_mode = select_mode
        self.update()
    
    @pyqtSlot(list)
    def setSelection(self, selections: List[int]):
        """Update the selection."""
        self.selections = selections
        self.update()
    
    def setSolvingPath(self,
        target_path: Dict[str, Tuple[Tuple[float, float]]]
    ):
        """Update target path."""
        self.target_path = target_path
        self.update()
    
    def setPathShow(self, p: int):
        """Update path present mode.
        
        -2: Hide all paths.
        -1: Show all paths.
        i: Show path i.
        """
        self.Path.show = p
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
        self.path_record = [deque([], limit) for i in range(len(self.vpoints))]
    
    def recordPath(self):
        """Recording path."""
        for i, vpoint in enumerate(self.vpoints):
            self.path_record[i].append((vpoint.cx, vpoint.cy))
    
    def getRecordPath(self) -> Tuple[Tuple[Tuple[float, float]]]:
        """Return paths."""
        path = tuple(
            tuple(path) if (len(set(path)) > 1) else ()
            for path in self.path_record
        )
        del self.path_record
        return path
    
    def adjustLink(self,
        coords: Tuple[Union[Tuple[Tuple[float, float], Tuple[float, float]]]]
    ):
        """Change points coordinates."""
        for i, c in enumerate(coords):
            vpoint = self.vpoints[i]
            if type(c[0]) == float:
                vpoint.move(c)
            else:
                vpoint.move(*c)
        self.update()
    
    def emit_freemove_all(self):
        _method.emit_freemove_all(self)
    
    def paintEvent(self, event):
        _method.paintEvent(self, event)
    
    def wheelEvent(self, event):
        """Switch function by mouse wheel.
        
        + Set zoom bar value.
        + Set select mode.
        """
        value = event.angleDelta().y()
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.__setSelectionMode(self.__selectionMode() + (-1 if (value > 0) else 1))
            i = self.__selectionMode()
            QToolTip.showText(
                event.globalPos(),
                "<p style=\"background-color: #77abff\">" + ''.join(
                    "<img width=\"{}\" src=\":icons/{}.png\"/>".format(70 if (i == j) else 40, icon)
                    for j, icon in enumerate(('bearing', 'link', 'triangular-iteration'))
                ) + "</p>",
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
