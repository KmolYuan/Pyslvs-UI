# -*- coding: utf-8 -*-

"""The canvas of main window."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    pyqtSignal,
    pyqtSlot,
    QRectF,
    QPointF,
    QSizeF,
    QFont,
    QPen,
    QColor,
    Qt,
    QApplication,
)
from core.graphics import (
    BaseCanvas,
    convex_hull,
    colorQt,
    colorNum
)
from core.io import VPoint, VLink
from math import (
    sin,
    cos,
    atan2,
    sqrt
)
from collections import deque
from typing import (
    List,
    Tuple,
    Dict,
    Callable
)
inf = float('inf')

class Selector:
    
    """Use to record mouse clicked point."""
    
    __slots__ = (
        'x', 'y',
        'selection',
        'selection_rect',
        'selection_old',
        'MiddleButtonDrag',
        'LeftButtonDrag',
        'sx', 'sy',
        'RectangularSelection'
    )
    
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.selection = []
        self.selection_rect = []
        self.selection_old = []
        self.MiddleButtonDrag = False
        self.LeftButtonDrag = False
        self.RectangularSelection = False
        self.sx = 0.
        self.sy = 0.
    
    def distance(self, x: float, y: float):
        """Return the distance of selector."""
        x = self.x - x
        y = self.y - y
        return round(sqrt(x*x + y*y), 2)
    
    def inRect(self, x: float, y: float) -> bool:
        """Return if input coordinate is in the rectangle."""
        return (
            min(self.x, self.sx) <= x <= max(self.x, self.sx) and
            min(self.y, self.sy) <= y <= max(self.y, self.sy)
        )

class DynamicCanvas(BaseCanvas):
    
    """The canvas in main window.
    
    + Parse and show PMKS expression.
    + Show paths.
    + Show settings of dimensional synthesis widget.
    + Mouse interactions.
    + Zoom to fit function.
    """
    
    mouse_track = pyqtSignal(float, float)
    mouse_browse_track = pyqtSignal(float, float)
    mouse_getSelection = pyqtSignal(tuple, bool)
    mouse_freemoveSelection = pyqtSignal(tuple)
    mouse_noSelection = pyqtSignal()
    mouse_getAltAdd = pyqtSignal()
    mouse_getDoubleClickEdit = pyqtSignal(int)
    zoom_change = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip("Use mouse wheel or middle button to look around.")
        self.Selector = Selector()
        #Entities.
        self.Point = tuple()
        self.Link = tuple()
        #Point selection.
        self.selectionRadius = 10
        self.pointsSelection = ()
        #Linkage transparency.
        self.transparency = 1.
        #Path solving range.
        self.ranges = {}
        #Set showDimension to False.
        self.showDimension = False
        """Free move mode.
        
        0: no free move.
        1: translate.
        2: rotate.
        3: reflect.
        """
        self.freemove = 0
        def setZoomValue(a):
            """Set zoom bar function."""
            parent.ZoomBar.setValue(
                parent.ZoomBar.value() +
                parent.ScaleFactor.value() * a / abs(a)
            )
        self.setZoomValue = setZoomValue
        #Default margin factor
        self.marginFactor = 0.95
    
    def update_figure(self,
        Point: Tuple[VPoint],
        Link: Tuple[VLink],
        path: List[Tuple[float, float]]
    ):
        """Update with Point and Link data."""
        self.Point = Point
        self.Link = Link
        self.Path.path = path
        self.update()
    
    @pyqtSlot(int)
    def setLinkWidth(self, linkWidth):
        """Update width of linkages."""
        self.linkWidth = linkWidth
        self.update()
    
    @pyqtSlot(int)
    def setPathWidth(self, pathWidth):
        """Update width of linkages."""
        self.pathWidth = pathWidth
        self.update()
    
    @pyqtSlot(bool)
    def setPointMark(self, showPointMark):
        """Update show point mark or not."""
        self.showPointMark = showPointMark
        self.update()
    
    @pyqtSlot(bool)
    def setShowDimension(self, showDimension):
        """Update show dimension or not."""
        self.showDimension = showDimension
        self.update()
    
    @pyqtSlot(bool)
    def setCurveMode(self, curve):
        """Update show as curve mode or not."""
        self.Path.curve = curve
        self.update()
    
    @pyqtSlot(int)
    def setFontSize(self, fontSize):
        """Update font size."""
        self.fontSize = fontSize
        self.update()
    
    @pyqtSlot(int)
    def setZoom(self, zoom):
        """Update zoom factor."""
        self.zoom = zoom / 100 * self.rate
        self.update()
    
    def setShowTargetPath(self, showTargetPath: bool):
        """Update show target path or not."""
        self.showTargetPath = showTargetPath
        self.update()
    
    def setFreeMove(self, freemove: int):
        """Update freemove mode number."""
        self.freemove = freemove
        self.update()
    
    @pyqtSlot(int)
    def setSelectionRadius(self, selectionRadius):
        """Update radius of point selector."""
        self.selectionRadius = selectionRadius
    
    @pyqtSlot(int)
    def setTransparency(self, transparency):
        """Update transparency.
        
        0%: opaque.
        """
        self.transparency = (100 - transparency) / 100
        self.update()
    
    @pyqtSlot(int)
    def setMarginFactor(self, marginFactor):
        """Update margin factor when zoom to fit."""
        self.marginFactor = 1 - marginFactor / 100
        self.update()
    
    @pyqtSlot(tuple)
    def changePointsSelection(self,
        pointsSelection: Tuple[int]
    ):
        """Update the selected points."""
        self.pointsSelection = pointsSelection
        self.update()
    
    @pyqtSlot(dict)
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
        1: Show path 1.
        2: Show path 2.
        ...
        """
        self.Path.show = p
        self.update()
    
    @pyqtSlot(dict)
    def update_ranges(self,
        ranges: Dict[str, Tuple[float, float, float]]
    ):
        """Update the ranges of dimensional synthesis."""
        self.ranges.clear()
        self.ranges.update({tag: QRectF(
            QPointF(values[0] - values[2]/2, values[1] + values[2]/2),
            QSizeF(values[2], values[2])
        ) for tag, values in ranges.items()})
        self.update()
    
    def paintEvent(self, event):
        """Drawing functions."""
        width = self.width()
        height = self.height()
        if self.width_old != width or self.height_old != height:
            self.ox += (width - self.width_old) / 2
            self.oy += (height - self.height_old) / 2
        super(DynamicCanvas, self).paintEvent(event)
        self.painter.setFont(QFont('Arial', self.fontSize))
        if self.freemove:
            #Draw a colored frame for free move mode.
            pen = QPen()
            if self.freemove==1:
                pen.setColor(QColor(161, 105, 229))
            elif self.freemove==2:
                pen.setColor(QColor(219, 162, 6))
            elif self.freemove==3:
                pen.setColor(QColor(79, 249, 193))
            pen.setWidth(8)
            self.painter.setPen(pen)
            self.drawFrame()
        if self.Selector.RectangularSelection:
            pen = QPen(Qt.gray)
            pen.setWidth(1)
            self.painter.setPen(pen)
            self.painter.drawRect(QRectF(
                QPointF(self.Selector.x, self.Selector.y),
                QPointF(self.Selector.sx, self.Selector.sy)
            ))
        #Draw links.
        for vlink in self.Link[1:]:
            self.drawLink(vlink)
        #Draw path.
        if self.Path.show>-2:
            self.drawPath()
        #Draw solving path.
        if self.showTargetPath:
            self.drawSlvsRanges()
            self.drawTargetPath()
        #Draw points.
        for i, vpoint in enumerate(self.Point):
            self.drawPoint(i, vpoint)
        self.painter.end()
        self.width_old = width
        self.height_old = height
    
    def drawPoint(self, i: int, vpoint: VPoint):
        """Draw a point."""
        if vpoint.type==1 or vpoint.type==2:
            #Draw slider
            silder_points = vpoint.c
            for j, (cx, cy) in enumerate(silder_points):
                if vpoint.type==1:
                    if j==0:
                        super(DynamicCanvas, self).drawPoint(
                            i, cx, cy,
                            vpoint.links[j] == 'ground',
                            vpoint.color
                        )
                    else:
                        pen = QPen(vpoint.color)
                        pen.setWidth(2)
                        self.painter.setPen(pen)
                        r = 5
                        self.painter.drawRect(QRectF(
                            QPointF(cx*self.zoom + r, cy*-self.zoom + r),
                            QPointF(cx*self.zoom - r, cy*-self.zoom - r)
                        ))
                elif vpoint.type==2:
                    if j==0:
                        super(DynamicCanvas, self).drawPoint(
                            i, cx, cy,
                            vpoint.links[j] == 'ground',
                            vpoint.color
                        )
                    else:
                        #Turn off point mark.
                        showPointMark = self.showPointMark
                        self.showPointMark = False
                        super(DynamicCanvas, self).drawPoint(
                            i, cx, cy,
                            vpoint.links[j] == 'ground',
                            vpoint.color
                        )
                        self.showPointMark = showPointMark
            pen = QPen(vpoint.color.darker())
            pen.setWidth(2)
            self.painter.setPen(pen)
            x_all = tuple(cx for cx, cy in silder_points)
            if x_all:
                p_left = silder_points[x_all.index(min(x_all))]
                p_right = silder_points[x_all.index(max(x_all))]
                if p_left==p_right:
                    y_all = tuple(cy for cx, cy in silder_points)
                    p_left = silder_points[y_all.index(min(y_all))]
                    p_right = silder_points[y_all.index(max(y_all))]
                self.painter.drawLine(
                    QPointF(p_left[0] * self.zoom, p_left[1] * -self.zoom),
                    QPointF(p_right[0] * self.zoom, p_right[1] * -self.zoom)
                )
        else:
            super(DynamicCanvas, self).drawPoint(
                i, vpoint.cx, vpoint.cy,
                'ground' in vpoint.links,
                vpoint.color
            )
        #For selects function.
        if i in self.pointsSelection:
            pen = QPen(QColor(161, 16, 239))
            pen.setWidth(3)
            self.painter.setPen(pen)
            self.painter.drawRect(
                vpoint.cx * self.zoom - 12,
                vpoint.cy * -self.zoom - 12,
                24, 24
            )
    
    def drawLink(self, vlink: VLink):
        """Draw a link."""
        points = []
        for i in vlink.points:
            vpoint = self.Point[i]
            if vpoint.type==1 or vpoint.type==2:
                coordinate = vpoint.c[vpoint.links.index(vlink.name)]
                x = coordinate[0] * self.zoom
                y = coordinate[1] * -self.zoom
            else:
                x = vpoint.cx * self.zoom
                y = vpoint.cy * -self.zoom
            points.append((x, y))
        pen = QPen(vlink.color)
        pen.setWidth(self.linkWidth)
        self.painter.setPen(pen)
        brush = QColor(226, 219, 190)
        brush.setAlphaF(self.transparency)
        self.painter.setBrush(brush)
        #Rearrange: Put the nearest point to the next position.
        qpoints = convex_hull(points)
        if qpoints:
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.showPointMark and vlink.name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            text = '[{}]'.format(vlink.name)
            cenX = sum([p[0] for p in points])/len(points)
            cenY = sum([p[1] for p in points])/len(points)
            self.painter.drawText(QPointF(cenX, cenY), text)
    
    def drawPath(self):
        """Draw paths. Recording first."""
        pen = QPen()
        if hasattr(self, 'PathRecord'):
            Path = self.PathRecord
        else:
            Path = self.Path.path
        for i, path in enumerate(Path):
            if self.Path.show!=i and self.Path.show!=-1:
                continue
            if len(set(path))>1:
                try:
                    color = self.Point[i].color
                except:
                    color = colorQt('Green')
                pen.setColor(color)
                pen.setWidth(self.pathWidth)
                self.painter.setPen(pen)
                if self.Path.curve:
                    self.drawCurve(path)
                else:
                    self.drawDot(path)
    
    def drawSlvsRanges(self):
        """Draw solving range."""
        pen = QPen()
        self.painter.setFont(QFont("Arial", self.fontSize+5))
        pen.setWidth(5)
        for i, (tag, rect) in enumerate(self.ranges.items()):
            range_color = QColor(colorNum(i+1))
            range_color.setAlpha(30)
            self.painter.setBrush(range_color)
            range_color.setAlpha(255)
            pen.setColor(range_color)
            self.painter.setPen(pen)
            cx = rect.x()*self.zoom
            cy = rect.y()*-self.zoom
            if rect.width():
                self.painter.drawRect(QRectF(
                    cx,
                    cy,
                    rect.width() * self.zoom,
                    rect.height() * self.zoom
                ))
            else:
                self.painter.drawEllipse(QPointF(cx, cy), 3, 3)
            range_color.setAlpha(255)
            pen.setColor(range_color)
            self.painter.setPen(pen)
            self.painter.drawText(QPointF(cx + 6, cy - 6), tag)
            self.painter.setBrush(Qt.NoBrush)
    
    def recordStart(self, limit: int):
        """Start a limit from main window."""
        self.PathRecord = [deque([], limit) for i in range(len(self.Point))]
    
    def recordPath(self):
        """Recording path."""
        for i, vpoint in enumerate(self.Point):
            self.PathRecord[i].append((vpoint.cx, vpoint.cy))
    
    def getRecordPath(self):
        """Return paths."""
        path = tuple(
            tuple(path) if len(set(path))>1 else ()
            for path in self.PathRecord
        )
        del self.PathRecord
        return path
    
    def wheelEvent(self, event):
        """Set zoom bar value by mouse wheel."""
        self.setZoomValue(event.angleDelta().y())
    
    def mousePressEvent(self, event):
        """Press event.
        
        Middle button: Move canvas of view.
        Left button: Select the point(s).
        """
        self.Selector.x = event.x() - self.ox
        self.Selector.y = event.y() - self.oy
        if event.buttons() == Qt.MiddleButton:
            self.Selector.MiddleButtonDrag = True
            x = self.Selector.x / self.zoom
            y = self.Selector.y / -self.zoom
            self.mouse_browse_track.emit(x, y)
        if event.buttons() == Qt.LeftButton:
            self.Selector.LeftButtonDrag = True
            self.mouseSelectedPoint()
            if self.Selector.selection:
                self.mouse_getSelection.emit(tuple(self.Selector.selection), True)
    
    def mouseDoubleClickEvent(self, event):
        """Mouse double click.
        
        + Middle button: Zoom to fit.
        + Left button: Edit point function.
        """
        if event.button() == Qt.MidButton:
            self.zoom_to_fit()
        if event.buttons() == Qt.LeftButton:
            self.Selector.x = event.x() - self.ox
            self.Selector.y = event.y() - self.oy
            self.mouseSelectedPoint()
            if self.Selector.selection:
                self.mouse_getSelection.emit((self.Selector.selection[0],), True)
                self.mouse_getDoubleClickEdit.emit(self.Selector.selection[0])
    
    def mouseSelectedPoint(self):
        """Select one point."""
        self.selectedPointFunc(
            self.Selector.selection,
            lambda *args: self.Selector.distance(*args) < self.selectionRadius
        )
    
    def RectangularSelectedPoint(self):
        """Select points by rectangle."""
        self.selectedPointFunc(
            self.Selector.selection_rect,
            self.Selector.inRect
        )
    
    def selectedPointFunc(self,
        selection: List[int],
        inSelection: Callable[[float, float], bool]
    ):
        """Select point(s) function."""
        selection.clear()
        for i, vpoint in enumerate(self.Point):
            if inSelection(vpoint.cx * self.zoom, vpoint.cy * -self.zoom):
                if i not in selection:
                    selection.append(i)
    
    def mouseReleaseEvent(self, event):
        """Release mouse button.
        
        + Alt & Left button: Add a point.
        + Left button: Select a point.
        + Free move mode: Edit the point(s) coordinate.
        """
        if self.Selector.LeftButtonDrag:
            self.Selector.selection_old = list(self.pointsSelection)
            km = QApplication.keyboardModifiers()
            #Add Point
            if km == Qt.AltModifier:
                self.mouse_getAltAdd.emit()
            #Only one clicked.
            elif (
                (abs(event.x() - self.ox - self.Selector.x) < self.selectionRadius/2) and
                (abs(event.y() - self.oy - self.Selector.y) < self.selectionRadius/2)
            ):
                if (
                    (not self.Selector.selection) and
                    km != Qt.ControlModifier and
                    km != Qt.ShiftModifier
                ):
                    self.mouse_noSelection.emit()
            #Edit point coordinates.
            elif self.freemove:
                self.mouse_freemoveSelection.emit(tuple(
                    (row, (self.Point[row].cx, self.Point[row].cy))
                    for row in self.pointsSelection
                ))
        self.Selector.selection_rect.clear()
        self.Selector.MiddleButtonDrag = False
        self.Selector.LeftButtonDrag = False
        self.Selector.RectangularSelection = False
        self.update()
    
    def mouseMoveEvent(self, event):
        """Move mouse.
        
        + Middle button: Translate canvas view.
        + Left button: Free move mode / Rectangular selection.
        """
        x = (event.x() - self.ox) / self.zoom
        y = (event.y() - self.oy) / -self.zoom
        if self.Selector.MiddleButtonDrag:
            self.ox = event.x() - self.Selector.x
            self.oy = event.y() - self.Selector.y
            self.update()
        elif self.Selector.LeftButtonDrag:
            if self.freemove:
                if self.pointsSelection:
                    if self.freemove==1:
                        #Free move translate function.
                        mouse_x = x - self.Selector.x/self.zoom
                        mouse_y = y - self.Selector.y/-self.zoom
                        for row in self.pointsSelection:
                            vpoint = self.Point[row]
                            vpoint.move((
                                mouse_x + vpoint.x,
                                mouse_y + vpoint.y
                            ))
                    elif self.freemove == 2:
                        #Free move rotate function.
                        alpha = atan2(y, x) - atan2(
                            self.Selector.y / -self.zoom,
                            self.Selector.x / self.zoom
                        )
                        for row in self.pointsSelection:
                            vpoint = self.Point[row]
                            r = sqrt(vpoint.x*vpoint.x + vpoint.y*vpoint.y)
                            beta = atan2(vpoint.y, vpoint.x)
                            vpoint.move((
                                r*cos(alpha + beta),
                                r*sin(alpha + beta)
                            ))
                    elif self.freemove == 3:
                        #Free move reflect function.
                        factor_x = 1 if x > 0 else -1
                        factor_y = 1 if y > 0 else -1
                        for row in self.pointsSelection:
                            vpoint = self.Point[row]
                            vpoint.move((vpoint.x * factor_x, vpoint.y * factor_y))
            else:
                #Rectangular selection
                self.Selector.RectangularSelection = True
                self.Selector.sx = event.x() - self.ox
                self.Selector.sy = event.y() - self.oy
                self.RectangularSelectedPoint()
                km = QApplication.keyboardModifiers()
                if self.Selector.selection_rect:
                    if km == Qt.ControlModifier or km == Qt.ShiftModifier:
                        self.mouse_getSelection.emit(tuple(set(
                            self.Selector.selection_old +
                            self.Selector.selection_rect
                        )), False)
                    else:
                        self.mouse_getSelection.emit(
                            tuple(self.Selector.selection_rect),
                            False
                        )
                else:
                    self.mouse_noSelection.emit()
            self.update()
        self.mouse_track.emit(x, y)
    
    def zoom_to_fit_limit(self):
        """Limitations of four side."""
        x_right = inf
        x_left = -inf
        y_top = -inf
        y_bottom = inf
        #Points
        for vpoint in self.Point:
            if vpoint.cx < x_right:
                x_right = vpoint.cx
            if vpoint.cx > x_left:
                x_left = vpoint.cx
            if vpoint.cy < y_bottom:
                y_bottom = vpoint.cy
            if vpoint.cy > y_top:
                y_top = vpoint.cy
        #Paths
        if self.Path.show>-2:
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
        if self.showTargetPath:
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
        #Ranges
        for rect in self.ranges.values():
            x_r = rect.x()
            x_l = rect.x() + rect.width()
            y_t = rect.y()
            y_b = rect.y() - rect.height()
            if x_r < x_right:
                x_right = x_r
            if x_l > x_left:
                x_left = x_l
            if y_b < y_bottom:
                y_bottom = y_b
            if y_t > y_top:
                y_top = y_t
        return x_right, x_left, y_top, y_bottom
    
    def zoom_to_fit(self):
        """Zoom to fit function."""
        width = self.width()
        height = self.height()
        width = width if not width==0 else 1
        height = height if not height==0 else 1
        x_right, x_left, y_top, y_bottom = self.zoom_to_fit_limit()
        if (inf in (x_right, y_bottom)) or (-inf in (x_left, y_top)):
            self.zoom_change.emit(200)
            self.ox = width/2
            self.oy = height/2
            self.update()
            return
        x_diff = x_left - x_right
        y_diff = y_top - y_bottom
        x_diff = x_diff if x_diff!=0 else 1
        y_diff = y_diff if y_diff!=0 else 1
        if width / x_diff < height / y_diff:
            factor = width / x_diff
        else:
            factor = height / y_diff
        self.zoom_change.emit(int(factor * self.marginFactor * 50))
        self.ox = width / 2 - (x_left + x_right) / 2 *self.zoom
        self.oy = height / 2 + (y_top + y_bottom) / 2 *self.zoom
        self.update()
