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
from typing import Tuple, List
from core.QtModules import (
    Qt,
    QApplication,
    QPolygonF,
    QRectF,
    QPointF,
    QFont,
    QPen,
    QColor,
    QToolTip,
)
from core.graphics import (
    convex_hull,
    BaseCanvas,
    colorQt,
    colorNum,
)
from core.libs import VPoint, VLink


class Selector:
    
    """Use to record mouse clicked point."""
    
    __slots__ = (
        'x', 'y', 'sx', 'sy',
        'selection',
        'selection_rect',
        'selection_old',
        'middle_dragged',
        'left_dragged',
        'picking',
    )
    
    def __init__(self):
        """Attributes:
        
        + x, y, sx, sy: Four coordinates of selection rectangle.
        + selection_rect: The selection of mouse dragging.
        + selection_old: The selection before mouse dragging.
        + middle_dragged: Is dragged by middle button.
        + left_dragged: Is dragged by left button.
        + picking: Is selecting (for drawing function).
        """
        self.x = 0.
        self.y = 0.
        self.sx = 0.
        self.sy = 0.
        self.selection_rect = []
        self.selection_old = []
        self.middle_dragged = False
        self.left_dragged = False
        self.picking = False
    
    def km(self) -> int:
        """Qt keyboard modifiers."""
        return QApplication.keyboardModifiers()
    
    def release(self):
        """Release the dragging status."""
        self.selection_rect.clear()
        self.middle_dragged = False
        self.left_dragged = False
        self.picking = False
    
    def isClose(self, x: float, y: float, limit: float) -> bool:
        """Return the distance of selector."""
        return hypot(x - self.x, y - self.y) <= limit
    
    def inRect(self, x: float, y: float) -> bool:
        """Return True if input coordinate is in the rectangle."""
        return (
            min(self.x, self.sx) <= x <= max(self.x, self.sx) and
            min(self.y, self.sy) <= y <= max(self.y, self.sy)
        )
    
    def toQRect(self) -> QRectF:
        """Return limit as QRectF type."""
        return QRectF(QPointF(self.x, self.y), QPointF(self.sx, self.sy))
    
    def currentSelection(self) -> Tuple[int]:
        if self.km() in (Qt.ControlModifier, Qt.ShiftModifier):
            return tuple(set(self.selection_old + self.selection_rect))
        else:
            return tuple(self.selection_rect)


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
    if vpoint.type in (1, 2):
        #Draw slider
        silder_points = vpoint.c
        for j, (cx, cy) in enumerate(silder_points):
            if not vpoint.links:
                grounded = False
            else:
                grounded = vpoint.links[j] == 'ground'
            if vpoint.type == 1:
                if j == 0:
                    self.drawPoint(i, cx, cy, grounded, vpoint.color)
                else:
                    pen = QPen(vpoint.color)
                    pen.setWidth(2)
                    self.painter.setPen(pen)
                    r = 5
                    self.painter.drawRect(QRectF(
                        QPointF(cx * self.zoom + r, cy * -self.zoom + r),
                        QPointF(cx * self.zoom - r, cy * -self.zoom - r)
                    ))
            elif vpoint.type == 2:
                if j == 0:
                    self.drawPoint(i, cx, cy, grounded, vpoint.color)
                else:
                    #Turn off point mark.
                    show_point_mark = self.show_point_mark
                    self.show_point_mark = False
                    self.drawPoint(i, cx, cy, grounded, vpoint.color)
                    self.show_point_mark = show_point_mark
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
        self.drawPoint(i, vpoint.cx, vpoint.cy, vpoint.grounded(), vpoint.color)
    #For selects function.
    if (self.select_mode == 0) and (i in self.selections):
        pen = QPen(QColor(161, 16, 239))
        pen.setWidth(3)
        self.painter.setPen(pen)
        self.painter.drawRect(
            vpoint.cx * self.zoom - 12,
            vpoint.cy * -self.zoom - 12,
            24, 24
        )


def _pointsPos(self, vlink: VLink) -> List[Tuple[float, float]]:
    """Get geometry of the vlink."""
    points = []
    for i in vlink.points:
        vpoint = self.vpoints[i]
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
    return points


def _drawLink(self, vlink: VLink):
    """Draw a link."""
    if (vlink.name == 'ground') or (not vlink.points):
        return
    points = _pointsPos(self, vlink)
    pen = QPen()
    #Rearrange: Put the nearest point to the next position.
    qpoints = convex_hull(points, as_qpoint = True)
    if (
        (self.select_mode == 1) and
        (self.vlinks.index(vlink) in self.selections)
    ):
        pen.setWidth(self.link_width + 6)
        pen.setColor(QColor(161, 16, 239))
        self.painter.setPen(pen)
        self.painter.drawPolygon(*qpoints)
    pen.setWidth(self.link_width)
    pen.setColor(vlink.color)
    self.painter.setPen(pen)
    brush = QColor(226, 219, 190)
    brush.setAlphaF(self.transparency)
    self.painter.setBrush(brush)
    self.painter.drawPolygon(*qpoints)
    self.painter.setBrush(Qt.NoBrush)
    if not self.show_point_mark:
        return
    pen.setColor(Qt.darkGray)
    self.painter.setPen(pen)
    p_count = len(points)
    cen_x = sum(p[0] for p in points) / p_count
    cen_y = sum(p[1] for p in points) / p_count
    self.painter.drawText(
        QRectF(cen_x - 50, cen_y - 50, 100, 100),
        Qt.AlignCenter,
        '[{}]'.format(vlink.name)
    )


def _drawPath(self):
    """Draw paths. Recording first."""
    pen = QPen()
    #Path record
    if hasattr(self, 'path_record'):
        paths = self.path_record
    else:
        paths = self.Path.path
    for i, path in enumerate(paths):
        if (self.Path.show != i) and (self.Path.show != -1):
            continue
        if self.vpoints[i].color:
            color = self.vpoints[i].color
        else:
            color = colorQt('Green')
        pen.setColor(color)
        pen.setWidth(self.path_width)
        self.painter.setPen(pen)
        if self.Path.curve:
            self.drawCurve(path)
        else:
            self.drawDot(path)


def _drawSlvsRanges(self):
    """Draw solving range."""
    pen = QPen()
    pen.setWidth(5)
    for i, (tag, rect) in enumerate(self.ranges.items()):
        range_color = QColor(colorNum(i + 1))
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


def _emit_freemove(self, targets: List[int]):
    """Emit free move targets to edit."""
    self.freemoved.emit(tuple((num, (
        self.vpoints[num].cx,
        self.vpoints[num].cy,
        self.vpoints[num].angle,
    )) for num in targets))


def _select_func(self, *, rect: bool = False):
    """Select function."""
    self.selector.selection_rect.clear()
    if self.select_mode == 0:
        
        def catch(x: float, y: float) -> bool:
            """Detection function for points."""
            if rect:
                return self.selector.inRect(x, y)
            else:
                return self.selector.isClose(x, y, self.sr)
        
        for i, vpoint in enumerate(self.vpoints):
            if catch(vpoint.cx * self.zoom, vpoint.cy * -self.zoom):
                if i not in self.selector.selection_rect:
                    self.selector.selection_rect.append(i)
        
    elif self.select_mode == 1:
        
        def catch(vlink: VLink) -> bool:
            """Detection function for links.
            
            + Is polygon: Using Qt polygon geometry.
            + If just a line: Create a range for mouse detection.
            """
            points = _pointsPos(self, vlink)
            if len(points) > 2:
                polygon = QPolygonF(convex_hull(points, as_qpoint=True))
            else:
                polygon = QPolygonF(convex_hull(
                    [(x + self.sr, y + self.sr) for x, y in points] +
                    [(x - self.sr, y - self.sr) for x, y in points],
                    as_qpoint=True
                ))
            if rect:
                return polygon.intersects(QPolygonF(self.selector.toQRect()))
            else:
                return polygon.containsPoint(
                    QPointF(self.selector.x, self.selector.y),
                    Qt.WindingFill
                )
        
        for i, vlink in enumerate(self.vlinks):
            if i == 0:
                continue
            if catch(vlink):
                if i not in self.selector.selection_rect:
                    self.selector.selection_rect.append(i)
        
    elif self.select_mode == 2:
        
        def catch(expr: str) -> bool:
            """Detection function for solution polygons."""
            points, _ = self.solutionPolygon(
                expr[0],
                expr[1:-1],
                expr[-1],
                self.vpoints
            )
            polygon = QPolygonF([QPointF(x, -y) * self.zoom for x, y in points])
            if rect:
                return polygon.intersects(QPolygonF(self.selector.toQRect()))
            else:
                return polygon.containsPoint(
                    QPointF(self.selector.x, self.selector.y),
                    Qt.WindingFill
                )
        
        for i, expr in enumerate(self.exprs):
            if catch(expr):
                if i not in self.selector.selection_rect:
                    self.selector.selection_rect.append(i)


def _snap(self, num: float, *, is_zoom: bool = True) -> float:
    """Close to a multiple of coefficient."""
    snap_val = self.snap * self.zoom if is_zoom else self.snap
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
    for vpoint in self.vpoints:
        if vpoint.cx < x_right:
            x_right = vpoint.cx
        if vpoint.cx > x_left:
            x_left = vpoint.cx
        if vpoint.cy < y_bottom:
            y_bottom = vpoint.cy
        if vpoint.cy > y_top:
            y_top = vpoint.cy
    #Solving paths
    if self.show_target_path:
        for path in self.target_path.values():
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


def emit_freemove_all(self):
    """Edit all points to edit."""
    _emit_freemove(self, list(range(len(self.vpoints))))


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
    #'self' is the instance of 'DynamicCanvas'.
    BaseCanvas.paintEvent(self, event)
    #Draw links except ground.
    for vlink in self.vlinks[1:]:
        _drawLink(self, vlink)
    #Draw path.
    if self.Path.show != -2:
        _drawPath(self)
    #Draw solving path.
    if self.show_target_path:
        self.painter.setFont(QFont("Arial", self.font_size + 5))
        _drawSlvsRanges(self)
        self.drawTargetPath()
        self.painter.setFont(QFont("Arial", self.font_size))
    #Draw points.
    for i, vpoint in enumerate(self.vpoints):
        _drawPoint(self, i, vpoint)
    #Draw solutions.
    if self.select_mode == 2:
        for i, expr in enumerate(self.exprs):
            args = [
                expr[0],
                expr[1:-1],
                expr[-1],
                self.vpoints
            ]
            self.drawSolution(*args)
            if i in self.selections:
                pos, _ = self.solutionPolygon(*args)
                pen = QPen()
                pen.setWidth(self.link_width + 3)
                pen.setColor(QColor(161, 16, 239))
                self.painter.setPen(pen)
                self.painter.drawPolygon(*[
                    QPointF(x, -y) * self.zoom for x, y in pos
                ])
    #Draw a colored frame for free move mode.
    if self.freemove != FreeMode.NoFreeMove:
        pen = QPen()
        if self.freemove == FreeMode.Translate:
            pen.setColor(QColor(161, 16, 229))
        elif self.freemove == FreeMode.Rotate:
            pen.setColor(QColor(219, 162, 6))
        elif self.freemove == FreeMode.Reflect:
            pen.setColor(QColor(79, 249, 193))
        pen.setWidth(8)
        self.painter.setPen(pen)
        _drawFrame(self)
    #Rectangular selection
    if self.selector.picking:
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.painter.setPen(pen)
        self.painter.drawRect(self.selector.toQRect())
    self.painter.end()
    #Record the widget size.
    self.width_old = width
    self.height_old = height


def mousePressEvent(self, event):
    """Press event.
    
    Middle button: Move canvas of view.
    Left button: Select the point (only first point will be catch).
    """
    self.selector.x = _snap(self, event.x() - self.ox)
    self.selector.y = _snap(self, event.y() - self.oy)
    if event.buttons() == Qt.MiddleButton:
        self.selector.middle_dragged = True
        x = self.selector.x / self.zoom
        y = self.selector.y / -self.zoom
        self.browse_tracking.emit(x, y)
    if event.buttons() == Qt.LeftButton:
        self.selector.left_dragged = True
        _select_func(self)
        if self.selector.selection_rect:
            self.selected.emit(tuple(self.selector.selection_rect[:1]), True)


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
        _select_func(self)
        if self.selector.selection_rect:
            self.selected.emit(tuple(self.selector.selection_rect[:1]), True)
            self.doubleclick_edit.emit(self.selector.selection_rect[0])
    event.accept()


def mouseReleaseEvent(self, event):
    """Release mouse button.
    
    + Alt & Left button: Add a point.
    + Left button: Select a point.
    + Free move mode: Edit the point(s) coordinate.
    """
    if self.selector.left_dragged:
        self.selector.selection_old = list(self.selections)
        km = self.selector.km()
        #Add Point
        if km == Qt.AltModifier:
            self.alt_add.emit()
        #Only one clicked.
        elif (
            (abs(event.x() - self.ox - self.selector.x) < self.sr/2) and
            (abs(event.y() - self.oy - self.selector.y) < self.sr/2)
        ):
            if (
                (not self.selector.selection_rect) and
                km != Qt.ControlModifier and
                km != Qt.ShiftModifier
            ):
                self.noselected.emit()
        #Edit point coordinates.
        elif (self.select_mode == 0) and (self.freemove != FreeMode.NoFreeMove):
            _emit_freemove(self, self.selections)
    self.selector.release()
    self.update()
    event.accept()


def mouseMoveEvent(self, event):
    """Move mouse.
    
    + Middle button: Translate canvas view.
    + Left button: Free move mode / Rectangular selection.
    """
    x = (event.x() - self.ox) / self.zoom
    y = (event.y() - self.oy) / -self.zoom
    if self.selector.middle_dragged:
        self.ox = event.x() - self.selector.x
        self.oy = event.y() - self.selector.y
        self.update()
    elif self.selector.left_dragged:
        if self.freemove == FreeMode.NoFreeMove:
            #Rectangular selection.
            self.selector.picking = True
            self.selector.sx = _snap(self, event.x() - self.ox)
            self.selector.sy = _snap(self, event.y() - self.oy)
            _select_func(self, rect=True)
            selection = self.selector.currentSelection()
            if selection:
                self.selected.emit(selection, False)
            else:
                self.noselected.emit()
            QToolTip.showText(
                event.globalPos(),
                "({:.02f}, {:.02f})\n({:.02f}, {:.02f})\n{} {}(s)".format(
                    self.selector.x / self.zoom,
                    self.selector.y / self.zoom,
                    self.selector.sx / self.zoom,
                    self.selector.sy / -self.zoom,
                    len(selection),
                    'point' if self.select_mode == 0 else
                    'link' if self.select_mode == 1 else
                    'solution'
                ),
                self
            )
        elif self.select_mode == 0:
            if self.freemove == FreeMode.Translate:
                #Free move translate function.
                mouse_x = _snap(self,
                    x - self.selector.x / self.zoom,
                    is_zoom=False
                )
                mouse_y = _snap(self,
                    y - self.selector.y / -self.zoom,
                    is_zoom=False
                )
                QToolTip.showText(
                    event.globalPos(),
                    "{:+.02f}, {:+.02f}".format(mouse_x, mouse_y),
                    self
                )
                for num in self.selections:
                    vpoint = self.vpoints[num]
                    vpoint.move((mouse_x + vpoint.x, mouse_y + vpoint.y))
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
                for num in self.selections:
                    vpoint = self.vpoints[num]
                    r = hypot(vpoint.x, vpoint.y)
                    beta = atan2(vpoint.y, vpoint.x)
                    vpoint.move((r * cos(beta + alpha), r * sin(beta + alpha)))
                    if vpoint.type != 0:
                        vpoint.rotate(self.vangles[num] + degrees(beta + alpha))
            elif self.freemove == FreeMode.Reflect:
                #Free move reflect function.
                fx = 1 if (x > 0) else -1
                fy = 1 if (y > 0) else -1
                QToolTip.showText(
                    event.globalPos(),
                    "{:+d}, {:+d}".format(fx, fy),
                    self
                )
                for num in self.selections:
                    vpoint = self.vpoints[num]
                    if vpoint.type == 0:
                        vpoint.move((vpoint.x * fx, vpoint.y * fy))
                    else:
                        vpoint.move((vpoint.x * fx, vpoint.y * fy))
                        if (x > 0) != (y > 0):
                            vpoint.rotate(180 - self.vangles[num])
        self.update()
    self.tracking.emit(x, y)
    event.accept()


def zoomToFit(self):
    """Zoom to fit function."""
    width = self.width()
    height = self.height()
    width = width if width else 1
    height = height if height else 1
    x_right, x_left, y_top, y_bottom = _zoomToFitLimit(self)
    inf = float('inf')
    if (inf in (x_right, y_bottom)) or (-inf in (x_left, y_top)):
        self.zoom_changed.emit(200)
        self.ox = width / 2
        self.oy = height / 2
        self.update()
        return
    x_diff = x_left - x_right
    y_diff = y_top - y_bottom
    x_diff = x_diff if x_diff else 1
    y_diff = y_diff if y_diff else 1
    if (width / x_diff) < (height / y_diff):
        factor = width / x_diff
    else:
        factor = height / y_diff
    self.zoom_changed.emit(int(factor * self.margin_factor * 50))
    self.ox = (width - (x_left + x_right) * self.zoom) / 2
    self.oy = (height + (y_top + y_bottom) * self.zoom) / 2
    self.update()
