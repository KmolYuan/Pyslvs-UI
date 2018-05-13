# -*- coding: utf-8 -*-

"""This module contain the functions that main canvas needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from enum import Enum
from math import (
    degrees,
    sin,
    cos,
    atan2,
    hypot,
)
from typing import (
    Tuple,
    List,
    Callable,
)
from core.QtModules import (
    Qt,
    QApplication,
    QRectF,
    QPointF,
    QFont,
    QPen,
    QColor,
    QToolTip,
)
from core.graphics import (
    convex_hull,
    colorQt,
    colorNum,
)
from core.libs import (
    expr_path,
    VPoint,
    VLink,
)


class Selector:
    
    """Use to record mouse clicked point."""
    
    __slots__ = (
        'x', 'y', 'sx', 'sy',
        'selection',
        'selection_rect',
        'selection_old',
        'middleDragged',
        'leftDragged',
        'hasSelection',
    )
    
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.selection = []
        self.selection_rect = []
        self.selection_old = []
        self.middleDragged = False
        self.leftDragged = False
        self.hasSelection = False
        self.sx = 0.
        self.sy = 0.
    
    def distanceLimit(self, x: float, y: float, limit: float) -> bool:
        """Return the distance of selector."""
        return hypot(x - self.x, y - self.y) <= limit
    
    def inRect(self, x: float, y: float) -> bool:
        """Return if input coordinate is in the rectangle."""
        return (
            min(self.x, self.sx) <= x <= max(self.x, self.sx) and
            min(self.y, self.sy) <= y <= max(self.y, self.sy)
        )


class FreeMode(Enum):
    
    """Free move mode."""
    
    NoFreeMove = 0
    Translate = 1
    Rotate = 2
    Reflect = 3


def _drawFrame(self):
    """Draw a outer frame."""
    positive_x = self.width() - self.ox
    positive_y = -self.oy
    negative_x = -self.ox
    negative_y = self.height() - self.oy
    self.painter.drawLine(
        QPointF(negative_x, positive_y), QPointF(positive_x, positive_y)
    )
    self.painter.drawLine(
        QPointF(negative_x, negative_y), QPointF(positive_x, negative_y)
    )
    self.painter.drawLine(
        QPointF(negative_x, positive_y), QPointF(negative_x, negative_y)
    )
    self.painter.drawLine(
        QPointF(positive_x, positive_y), QPointF(positive_x, negative_y)
    )


def _drawPoint(self, i: int, vpoint: VPoint):
    """Draw a point."""
    if vpoint.type==1 or vpoint.type==2:
        #Draw slider
        silder_points = vpoint.c
        for j, (cx, cy) in enumerate(silder_points):
            if vpoint.type == 1:
                if j == 0:
                    self._BaseCanvas__drawPoint(
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
            elif vpoint.type == 2:
                if j == 0:
                    self._BaseCanvas__drawPoint(
                        i, cx, cy,
                        vpoint.links[j] == 'ground',
                        vpoint.color
                    )
                else:
                    #Turn off point mark.
                    showPointMark = self.showPointMark
                    self.showPointMark = False
                    self._BaseCanvas__drawPoint(
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
            if p_left == p_right:
                y_all = tuple(cy for cx, cy in silder_points)
                p_left = silder_points[y_all.index(min(y_all))]
                p_right = silder_points[y_all.index(max(y_all))]
            self.painter.drawLine(
                QPointF(p_left[0] * self.zoom, p_left[1] * -self.zoom),
                QPointF(p_right[0] * self.zoom, p_right[1] * -self.zoom)
            )
    else:
        self._BaseCanvas__drawPoint(
            i, vpoint.cx, vpoint.cy,
            vpoint.grounded(),
            vpoint.color
        )
    #For selects function.
    if i in self.selections:
        pen = QPen(QColor(161, 16, 239))
        pen.setWidth(3)
        self.painter.setPen(pen)
        self.painter.drawRect(
            vpoint.cx * self.zoom - 12,
            vpoint.cy * -self.zoom - 12,
            24, 24
        )


def _drawLink(self, vlink: VLink):
    """Draw a link."""
    points = []
    for i in vlink.points:
        vpoint = self.Points[i]
        if vpoint.type == 0:
            x = vpoint.cx * self.zoom
            y = vpoint.cy * -self.zoom
        else:
            coordinate = vpoint.c[
                0 if (vlink.name == vpoint.links[0]) else 1
            ]
            x = coordinate[0] * self.zoom
            y = coordinate[1] * -self.zoom
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
    if (
        (not self.showPointMark) or
        (vlink.name == 'ground') or
        (not qpoints)
    ):
        return
    pen.setColor(Qt.darkGray)
    self.painter.setPen(pen)
    cenX = sum(p[0] for p in points) / len(points)
    cenY = sum(p[1] for p in points) / len(points)
    self.painter.drawText(QPointF(cenX, cenY), '[{}]'.format(vlink.name))


def _drawPath(self):
    """Draw paths. Recording first."""
    pen = QPen()
    if self.autoPathShow and self.rightInput():
        """Replace to auto preview path."""
        exprs = self.getTriangle(self.Points)
        self.Path.path = expr_path(
            exprs,
            {n: 'P{}'.format(n) for n in range(len(self.Points))},
            self.Points,
            self.pathInterval()
        )
        if self.solutionShow:
            for expr in exprs:
                self._BaseCanvas__drawSolution(
                    expr[0],
                    expr[1:-1],
                    expr[-1],
                    self.Points
                )
    if hasattr(self, 'path_record'):
        paths = self.path_record
    else:
        paths = self.Path.path
    for i, path in enumerate(paths):
        if (
            (self.Path.show != i) and
            (self.Path.show != -1) or
            (len(path) <= 1)
        ):
            continue
        try:
            color = self.Points[i].color
        except:
            color = colorQt('Green')
        pen.setColor(color)
        pen.setWidth(self.pathWidth)
        self.painter.setPen(pen)
        if self.Path.curve:
            self._BaseCanvas__drawCurve(path)
        else:
            self._BaseCanvas__drawDot(path)


def _drawSlvsRanges(self):
    """Draw solving range."""
    pen = QPen()
    self.painter.setFont(QFont("Arial", self.fontSize + 5))
    pen.setWidth(5)
    for i, (tag, rect) in enumerate(self.ranges.items()):
        range_color = QColor(colorNum(i+1))
        range_color.setAlpha(30)
        self.painter.setBrush(range_color)
        range_color.setAlpha(255)
        pen.setColor(range_color)
        self.painter.setPen(pen)
        cx = rect.x() * self.zoom
        cy = rect.y() * -self.zoom
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


def _selectedPointFunc(self,
    selection: List[int],
    inSelection: Callable[[float, float], bool]
):
    """Select point(s) function."""
    selection.clear()
    for i, vpoint in enumerate(self.Points):
        if inSelection(vpoint.cx * self.zoom, vpoint.cy * -self.zoom):
            if i not in selection:
                selection.append(i)


def _mouseSelectedPoint(self):
    """Select one point."""
    _selectedPointFunc(self,
        self.selector.selection,
        lambda x, y: self.selector.distanceLimit(x, y, self.selectionRadius)
    )


def _rectangularSelectedPoint(self):
    """Select points by rectangle."""
    _selectedPointFunc(self,
        self.selector.selection_rect,
        self.selector.inRect
    )


def _snap(self, num: float, isZoom: bool = True) -> float:
    """Close to a multiple of coefficient."""
    snap_val = self.snap * self.zoom if isZoom else self.snap
    if not snap_val:
        return num
    times = num // snap_val
    remainder = num % snap_val
    if remainder < (snap_val / 2):
        return snap_val * times
    else:
        return snap_val * (times + 1)


def _zoomToFitLimit(self) -> Tuple[float, float, float, float]:
    """Limitations of four side."""
    inf = float('inf')
    x_right = inf
    x_left = -inf
    y_top = -inf
    y_bottom = inf
    #Paths
    has_path = bool(self.Path.path and (self.Path.show != -2))
    if has_path:
        for i, path in enumerate(self.Path.path):
            if self.Path.show != -1 and self.Path.show != i:
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
    #Points
    for vpoint in self.Points:
        if has_path and (not vpoint.grounded()):
            continue
        if vpoint.cx < x_right:
            x_right = vpoint.cx
        if vpoint.cx > x_left:
            x_left = vpoint.cx
        if vpoint.cy < y_bottom:
            y_bottom = vpoint.cy
        if vpoint.cy > y_top:
            y_top = vpoint.cy
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


def paintEvent(self, event):
    """Drawing functions."""
    width = self.width()
    height = self.height()
    if ((self.width_old is not None) and (
        (self.width_old != width) or
        (self.height_old != height)
    )):
        self.ox += (width - self.width_old) / 2
        self.oy += (height - self.height_old) / 2
    #It only can be called when 'self' is the instance of 'DynamicCanvas'.
    super(self.__class__, self).paintEvent(event)
    self.painter.setFont(QFont('Arial', self.fontSize))
    #Draw links except ground.
    for vlink in self.Links[1:]:
        _drawLink(self, vlink)
    #Draw path.
    if self.Path.show != -2:
        _drawPath(self)
    #Draw solving path.
    if self.showTargetPath:
        _drawSlvsRanges(self)
        self._BaseCanvas__drawTargetPath()
    #Draw points.
    for i, vpoint in enumerate(self.Points):
        _drawPoint(self, i, vpoint)
    #Draw a colored frame for free move mode.
    if self.freemove != FreeMode.NoFreeMove:
        pen = QPen()
        if self.freemove == FreeMode.Translate:
            pen.setColor(QColor(161, 105, 229))
        elif self.freemove == FreeMode.Rotate:
            pen.setColor(QColor(219, 162, 6))
        elif self.freemove == FreeMode.Reflect:
            pen.setColor(QColor(79, 249, 193))
        pen.setWidth(8)
        self.painter.setPen(pen)
        _drawFrame(self)
    #Rectangular selection
    if self.selector.hasSelection:
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.painter.setPen(pen)
        self.painter.drawRect(QRectF(
            QPointF(self.selector.x, self.selector.y),
            QPointF(self.selector.sx, self.selector.sy)
        ))
    self.painter.end()
    #Record the widget size.
    self.width_old = width
    self.height_old = height


def getRecordPath(self) -> Tuple[Tuple[Tuple[float, float]]]:
    """Return paths."""
    path = tuple(
        tuple(path) if (len(set(path)) > 1) else ()
        for path in self.path_record
    )
    del self.path_record
    return path


def mousePressEvent(self, event):
    """Press event.
    
    Middle button: Move canvas of view.
    Left button: Select the point(s).
    """
    self.selector.x = _snap(self, event.x() - self.ox)
    self.selector.y = _snap(self, event.y() - self.oy)
    if event.buttons() == Qt.MiddleButton:
        self.selector.middleDragged = True
        x = self.selector.x / self.zoom
        y = self.selector.y / -self.zoom
        self.browse_tracking.emit(x, y)
    if event.buttons() == Qt.LeftButton:
        self.selector.leftDragged = True
        _mouseSelectedPoint(self)
        if self.selector.selection:
            self.selected.emit(tuple(self.selector.selection), True)


def mouseDoubleClickEvent(self, event):
    """Mouse double click.
    
    + Middle button: Zoom to fit.
    + Left button: Edit point function.
    """
    button = event.button()
    if button == Qt.MidButton:
        self.zoomToFit()
    if button == Qt.LeftButton:
        self.selector.x = _snap(self, event.x() - self.ox)
        self.selector.y = _snap(self, event.y() - self.oy)
        _mouseSelectedPoint(self)
        if self.selector.selection:
            self.selected.emit((self.selector.selection[0],), True)
            self.doubleclick_edit.emit(self.selector.selection[0])


def mouseReleaseEvent(self, event):
    """Release mouse button.
    
    + Alt & Left button: Add a point.
    + Left button: Select a point.
    + Free move mode: Edit the point(s) coordinate.
    """
    if self.selector.leftDragged:
        self.selector.selection_old = list(self.selections)
        km = QApplication.keyboardModifiers()
        #Add Point
        if km == Qt.AltModifier:
            self.alt_add.emit()
        #Only one clicked.
        elif (
            (abs(event.x() - self.ox - self.selector.x) < self.selectionRadius/2) and
            (abs(event.y() - self.oy - self.selector.y) < self.selectionRadius/2)
        ):
            if (
                (not self.selector.selection) and
                km != Qt.ControlModifier and
                km != Qt.ShiftModifier
            ):
                self.noselected.emit()
        #Edit point coordinates.
        elif (self.freemove != FreeMode.NoFreeMove):
            self.freemoved.emit(tuple((row, (
                self.Points[row].cx,
                self.Points[row].cy,
            )) for row in self.selections))
    self.selector.selection_rect.clear()
    self.selector.middleDragged = False
    self.selector.leftDragged = False
    self.selector.hasSelection = False
    self.update()


def mouseMoveEvent(self, event):
    """Move mouse.
    
    + Middle button: Translate canvas view.
    + Left button: Free move mode / Rectangular selection.
    """
    x = (event.x() - self.ox) / self.zoom
    y = (event.y() - self.oy) / -self.zoom
    if self.selector.middleDragged:
        self.ox = event.x() - self.selector.x
        self.oy = event.y() - self.selector.y
        self.update()
    elif self.selector.leftDragged:
        if self.freemove != FreeMode.NoFreeMove:
            if self.freemove == FreeMode.Translate:
                #Free move translate function.
                mouse_x = _snap(self, x - self.selector.x/self.zoom, False)
                mouse_y = _snap(self, y - self.selector.y/-self.zoom, False)
                QToolTip.showText(
                    event.globalPos(),
                    "{:+.02f}, {:+.02f}".format(mouse_x, mouse_y),
                    self
                )
                for row in self.selections:
                    vpoint = self.Points[row]
                    vpoint.move((
                        mouse_x + vpoint.x,
                        mouse_y + vpoint.y
                    ))
            elif self.freemove == FreeMode.Rotate:
                #Free move rotate function.
                alpha = atan2(y, x) - atan2(
                    -self.selector.y, self.selector.x
                )
                QToolTip.showText(
                    event.globalPos(),
                    "{:+.02f}°".format(degrees(alpha)),
                    self
                )
                for row in self.selections:
                    vpoint = self.Points[row]
                    r = hypot(vpoint.x, vpoint.y)
                    beta = atan2(vpoint.y, vpoint.x)
                    vpoint.move((
                        r*cos(alpha + beta),
                        r*sin(alpha + beta)
                    ))
            elif self.freemove == FreeMode.Reflect:
                #Free move reflect function.
                fx = 1 if (x > 0) else -1
                fy = 1 if (y > 0) else -1
                QToolTip.showText(
                    event.globalPos(),
                    "{:+d}, {:+d}".format(fx, fy),
                    self
                )
                for row in self.selections:
                    vpoint = self.Points[row]
                    if vpoint.type == 0:
                        vpoint.move((vpoint.x * fx, vpoint.y * fy))
                    else:
                        vpoint.move(
                            (vpoint.x * fx, vpoint.y * fy),
                            (vpoint.x * fx, vpoint.y * fy)
                        )
        else:
            #Rectangular selection.
            self.selector.hasSelection = True
            self.selector.sx = _snap(self, event.x() - self.ox)
            self.selector.sy = _snap(self, event.y() - self.oy)
            QToolTip.showText(event.globalPos(), "{:.02f}, {:.02f}".format(
                self.selector.sx / self.zoom,
                self.selector.sy / -self.zoom
            ), self)
            _rectangularSelectedPoint(self)
            km = QApplication.keyboardModifiers()
            if self.selector.selection_rect:
                if km in (Qt.ControlModifier, Qt.ShiftModifier):
                    self.selected.emit(tuple(set(
                        self.selector.selection_old +
                        self.selector.selection_rect
                    )), False)
                else:
                    self.selected.emit(
                        tuple(self.selector.selection_rect),
                        False
                    )
            else:
                self.noselected.emit()
        self.update()
    self.tracking.emit(x, y)


def zoomToFit(self):
    """Zoom to fit function."""
    width = self.width()
    height = self.height()
    width = width if not (width == 0) else 1
    height = height if not (height == 0) else 1
    x_right, x_left, y_top, y_bottom = _zoomToFitLimit(self)
    inf = float('inf')
    if (inf in (x_right, y_bottom)) or (-inf in (x_left, y_top)):
        self.zoom_changed.emit(200)
        self.ox = width/2
        self.oy = height/2
        self.update()
        return
    x_diff = x_left - x_right
    y_diff = y_top - y_bottom
    x_diff = x_diff if (x_diff != 0) else 1
    y_diff = y_diff if (y_diff != 0) else 1
    if (width / x_diff) < (height / y_diff):
        factor = width / x_diff
    else:
        factor = height / y_diff
    self.zoom_changed.emit(int(factor * self.marginFactor * 50))
    self.ox = width / 2 - (x_left + x_right) / 2 *self.zoom
    self.oy = height / 2 + (y_top + y_bottom) / 2 *self.zoom
    self.update()
