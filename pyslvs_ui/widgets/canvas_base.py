# -*- coding: utf-8 -*-

"""This module contains the functions that main canvas needed."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, Tuple, List, Deque, Sequence, Dict
from abc import ABC, abstractmethod
from enum import IntEnum, auto, unique
from dataclasses import dataclass, field
from math import degrees, sin, cos, atan2, hypot
from qtpy.QtCore import Signal, Slot, Qt, QRectF, QPoint, QPointF, QLineF
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QPolygonF, QFont, QPen, QColor, QPaintEvent, QMouseEvent
from pyslvs import VJoint, VPoint, VLink
from pyslvs_ui.graphics import (
    convex_hull, BaseCanvas, color_qt, LINK_COLOR, RangeDetector,
)

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase

_Coord = Tuple[float, float]
_Path = Sequence[_Coord]
_Paths = Sequence[Sequence[_Coord]]


@dataclass(repr=False, eq=False)
class _Selector:
    """Use to record mouse clicked point.

    Attributes:

    + x, y, sx, sy: Four coordinates of selection rectangle.
    + selection_rect: The selection of mouse dragging.
    + selection_old: The selection before mouse dragging.
    + middle_dragged: Is dragged by middle button.
    + left_dragged: Is dragged by left button.
    + picking: Is selecting (for drawing function).
    """
    x: float = 0.
    y: float = 0.
    sx: float = 0.
    sy: float = 0.
    selection_rect: List[int] = field(default_factory=list)
    selection_old: List[int] = field(default_factory=list)
    middle_dragged: bool = False
    left_dragged: bool = False
    picking: bool = False

    def release(self) -> None:
        """Release the dragging status."""
        self.selection_rect.clear()
        self.middle_dragged = False
        self.left_dragged = False
        self.picking = False

    def is_close(self, x: float, y: float, limit: float) -> bool:
        """Return the distance of selector."""
        return hypot(x - self.x, y - self.y) <= limit

    def in_rect(self, x: float, y: float) -> bool:
        """Return true if input coordinate is in the rectangle."""
        x_right = max(self.x, self.sx)
        x_left = min(self.x, self.sx)
        y_top = max(self.y, self.sy)
        y_btn = min(self.y, self.sy)
        return x_left <= x <= x_right and y_btn <= y <= y_top

    def to_rect(self, zoom: float) -> QRectF:
        """Return limit as QRectF type."""
        return QRectF(
            QPointF(self.x, -self.y) * zoom,
            QPointF(self.sx, -self.sy) * zoom
        )

    def current_selection(self) -> Tuple[int, ...]:
        km = QApplication.keyboardModifiers()
        if km == Qt.ControlModifier or km == Qt.ShiftModifier:
            return tuple(set(self.selection_old + self.selection_rect))
        else:
            return tuple(self.selection_rect)


@unique
class FreeMode(IntEnum):
    """Free move mode"""
    NO_FREE_MOVE = auto()
    TRANSLATE = auto()
    ROTATE = auto()
    REFLECT = auto()


@unique
class SelectMode(IntEnum):
    """Selection mode"""
    JOINT = auto()
    LINK = auto()
    SOLUTION = auto()


@unique
class ZoomBy(IntEnum):
    """Zooming center option"""
    CURSOR = auto()
    CANVAS = auto()


_selection_unit = {
    SelectMode.JOINT: 'point',
    SelectMode.LINK: 'link',
    SelectMode.SOLUTION: 'solution',
}


class MainCanvasBase(BaseCanvas, ABC):
    """Abstract class for wrapping main canvas class."""
    vangles: Tuple[float, ...]
    exprs: List[Tuple[str, ...]]
    selections: List[int]
    path_preview: List[List[_Coord]]
    slider_path_preview: Dict[int, List[_Coord]]
    path_record: List[Deque[_Coord]]
    slider_record: Dict[int, Deque[_Coord]]

    tracking = Signal(float, float)
    browse_tracking = Signal(float, float)
    selected = Signal(tuple, bool)
    selected_tips = Signal(QPoint, str)
    selected_tips_hide = Signal()
    free_moved = Signal(tuple)
    no_selected = Signal()
    alt_add = Signal(float, float)
    doubleclick_edit = Signal(int)
    zoom_changed = Signal(int)
    fps_updated = Signal()
    set_target_point = Signal(float, float)

    @abstractmethod
    def __init__(self, parent: MainWindowBase):
        super(MainCanvasBase, self).__init__(parent)
        self.setStatusTip("Use mouse wheel or middle button to look around.")
        # The current mouse coordinates
        self.selector = _Selector()
        # Entities
        self.vpoints = parent.vpoint_list
        self.vlinks = parent.vlink_list
        self.vangles = ()
        # Solution
        self.exprs = []
        # Select function
        self.select_mode = SelectMode.JOINT
        self.sr = 10
        self.selections = []
        # Link transparency
        self.transparency = 1.
        # Default zoom rate
        self.default_zoom = 400
        # Show dimension
        self.show_dimension = False
        # Free move mode
        self.free_move = FreeMode.NO_FREE_MOVE
        # Path preview
        self.path_preview = []
        self.slider_path_preview = {}
        self.preview_path = parent.preview_path
        # Path record
        self.path_record = []
        self.slider_record = {}
        # Zooming center
        # 0: By cursor
        # 1: By canvas center
        self.zoomby = ZoomBy.CANVAS
        # Mouse snapping value
        self.snap = 5.
        # Default margin factor
        self.margin_factor = 0.95
        # Widget size
        self.width_old = None
        self.height_old = None

    def __draw_frame(self) -> None:
        """Draw an external frame."""
        pos_x = self.width() - self.ox
        pos_y = -self.oy
        neg_x = -self.ox
        neg_y = self.height() - self.oy
        self.painter.drawLine(QLineF(neg_x, pos_y, pos_x, pos_y))
        self.painter.drawLine(QLineF(neg_x, neg_y, pos_x, neg_y))
        self.painter.drawLine(QLineF(neg_x, pos_y, neg_x, neg_y))
        self.painter.drawLine(QLineF(pos_x, pos_y, pos_x, neg_y))

    def __draw_point(self, i: int, vpt: VPoint) -> None:
        """Draw a point."""
        connected = len(vpt.links) - 1
        if vpt.type in {VJoint.P, VJoint.RP}:
            pen = QPen(color_qt(vpt.color))
            pen.setWidth(2)
            # Draw slot point and pin point
            for j, (cx, cy) in enumerate(vpt.c):
                # Slot point
                if j == 0 or vpt.type == VJoint.P:
                    if self.monochrome:
                        color = Qt.black
                    else:
                        color = color_qt(vpt.color)
                    pen.setColor(color)
                    self.painter.setPen(pen)
                    cp = QPointF(cx, -cy) * self.zoom
                    jr = self.joint_size * (2 if j == 0 else 1)
                    rp = QPointF(jr, -jr)
                    self.painter.drawRect(QRectF(cp + rp, cp - rp))
                    if self.show_point_mark:
                        pen.setColor(Qt.darkGray)
                        self.painter.setPen(pen)
                        text = f"[Point{i}]"
                        if self.show_dimension:
                            text += f":({cx:.02f}, {cy:.02f})"
                        self.painter.drawText(cp + rp, text)
                else:
                    grounded = (len(vpt.c) == len(vpt.links)
                                and vpt.links[j] == VLink.FRAME)
                    self.draw_point(i, cx, cy, grounded, vpt.color, connected)
            # Slider line
            pen.setColor(color_qt(vpt.color).darker())
            self.painter.setPen(pen)
            line_m = QLineF(
                QPointF(vpt.c[1, 0], -vpt.c[1, 1]) * self.zoom,
                QPointF(vpt.c[0, 0], -vpt.c[0, 1]) * self.zoom
            )
            nv = line_m.normalVector()
            nv.setLength(self.joint_size)
            nv.setPoints(nv.p2(), nv.p1())
            line1 = nv.normalVector()
            line1.setLength(line_m.length())
            self.painter.drawLine(line1)
            nv.setLength(nv.length() * 2)
            nv.setPoints(nv.p2(), nv.p1())
            line2 = nv.normalVector()
            line2.setLength(line_m.length())
            line2.setAngle(line2.angle() + 180)
            self.painter.drawLine(line2)
        else:
            self.draw_point(i, vpt.cx, vpt.cy, vpt.grounded(), vpt.color,
                            connected)
        # For selects function
        if self.select_mode == SelectMode.JOINT and (i in self.selections):
            pen = QPen(QColor(161, 16, 239))
            pen.setWidth(3)
            self.painter.setPen(pen)
            self.painter.drawRect(QRectF(
                vpt.cx * self.zoom - 12,
                vpt.cy * -self.zoom - 12,
                24, 24
            ))

    def __draw_link(self, vlink: VLink) -> None:
        """Draw a link."""
        if vlink.name == VLink.FRAME or not vlink.points:
            return
        pen = QPen()
        # Rearrange: Put the nearest point to the next position.
        qpoints = convex_hull(
            [(c.x * self.zoom, c.y * -self.zoom)
             for c in vlink.points_pos(self.vpoints)], as_qpoint=True)
        if (
            self.select_mode == SelectMode.LINK
            and self.vlinks.index(vlink) in self.selections
        ):
            pen.setWidth(self.link_width + 6)
            pen.setColor(Qt.black if self.monochrome else QColor(161, 16, 239))
            self.painter.setPen(pen)
            self.painter.drawPolygon(*qpoints)
        pen.setWidth(self.link_width)
        pen.setColor(Qt.black if self.monochrome else color_qt(vlink.color))
        self.painter.setPen(pen)
        self.painter.drawPolygon(*qpoints)
        if not self.show_point_mark:
            return
        pen.setColor(Qt.darkGray)
        self.painter.setPen(pen)
        p_count = len(qpoints)
        cen_x = sum(p.x() for p in qpoints) / p_count
        cen_y = sum(p.y() for p in qpoints) / p_count
        self.painter.drawText(
            QRectF(cen_x - 50, cen_y - 50, 100, 100),
            Qt.AlignCenter,
            f'[{vlink.name}]'
        )

    def __draw_path(self) -> None:
        """Draw paths. Recording first."""
        paths: _Paths = self.path_record or self.path.path or self.path_preview
        if len(self.vpoints) != len(paths):
            return
        pen = QPen()
        fmt_paths = [(i, p) for i, p in enumerate(paths)]
        if paths is self.path_preview:
            fmt_paths.extend(self.slider_path_preview.items())
        elif paths is self.path_record:
            fmt_paths.extend(self.slider_record.items())
        else:
            # User paths
            fmt_paths.extend(self.path.slider_path.items())
        for i, path in fmt_paths:
            if self.path.show != i and self.path.show != -1:
                continue
            vpoint = self.vpoints[i]
            if self.monochrome:
                color = color_qt('gray')
            else:
                color = color_qt(vpoint.color)
            pen.setColor(color)
            pen.setWidth(self.path_width)
            self.painter.setPen(pen)
            if self.path.curve:
                self.draw_curve(path)
            else:
                self.draw_dot(path)

    def __emit_free_move(self, targets: Sequence[int]) -> None:
        """Emit free move targets to edit."""
        self.free_moved.emit(tuple((num, (
            self.vpoints[num].cx,
            self.vpoints[num].cy,
            self.vpoints[num].angle,
        )) for num in targets))

    def __select_func(self, *, rect: bool = False) -> None:
        """Select function."""
        if self.show_target_path:
            return
        self.selector.selection_rect.clear()
        if self.select_mode == SelectMode.JOINT:
            def catch_p(x: float, y: float) -> bool:
                """Detection function for points."""
                if rect:
                    return self.selector.in_rect(x, y)
                else:
                    return self.selector.is_close(x, y, self.sr / self.zoom)

            for i, vpoint in enumerate(self.vpoints):
                if (
                    catch_p(vpoint.cx, vpoint.cy)
                    and i not in self.selector.selection_rect
                ):
                    self.selector.selection_rect.append(i)

        elif self.select_mode == SelectMode.LINK:
            def catch_l(vlink: VLink) -> bool:
                """Detection function for links.

                + Is polygon: Using Qt polygon geometry.
                + If just a line: Create a range for mouse detection.
                """
                points = [(c.x * self.zoom, c.y * -self.zoom)
                          for c in vlink.points_pos(self.vpoints)]
                if len(points) > 2:
                    polygon = QPolygonF(convex_hull(points, as_qpoint=True))
                else:
                    polygon = QPolygonF(convex_hull(
                        [(x + self.sr, y + self.sr) for x, y in points]
                        + [(x - self.sr, y - self.sr) for x, y in points],
                        as_qpoint=True
                    ))
                if rect:
                    return polygon.intersects(
                        QPolygonF(self.selector.to_rect(self.zoom)))
                else:
                    return polygon.containsPoint(
                        QPointF(self.selector.x, -self.selector.y) * self.zoom,
                        Qt.WindingFill
                    )

            for i, vl in enumerate(self.vlinks):
                if (
                    i != 0 and catch_l(vl)
                    and i not in self.selector.selection_rect
                ):
                    self.selector.selection_rect.append(i)

        elif self.select_mode == SelectMode.SOLUTION:
            def catch(exprs: Sequence[str]) -> bool:
                """Detection function for solution polygons."""
                points, _ = self.solution_polygon(
                    exprs[0],
                    exprs[1:-1],
                    exprs[-1],
                    self.vpoints
                )
                if len(points) < 3:
                    points = convex_hull(
                        [(x + self.sr, y + self.sr) for x, y in points]
                        + [(x - self.sr, y - self.sr) for x, y in points],
                        as_qpoint=True
                    )
                else:
                    points = [QPointF(x, y) for x, y in points]
                polygon = QPolygonF(points)
                if rect:
                    return polygon.intersects(
                        QPolygonF(self.selector.to_rect(self.zoom)))
                else:
                    return polygon.containsPoint(
                        QPointF(self.selector.x, -self.selector.y) * self.zoom,
                        Qt.WindingFill
                    )

            for i, expr in enumerate(self.exprs):
                if catch(expr) and i not in self.selector.selection_rect:
                    self.selector.selection_rect.append(i)

    def __snap(self, num: float, *, is_zoom: bool = True) -> float:
        """Close to a multiple of coefficient."""
        snap_val = self.snap * self.zoom if is_zoom else self.snap
        if not snap_val:
            return num
        times = num // snap_val
        if num % snap_val >= snap_val / 2:
            times += 1
        return snap_val * times

    def __zoom_to_fit_size(self) -> Tuple[float, float, float, float]:
        """Limitations of four side."""
        r = RangeDetector()
        # Paths
        if self.path.show != -2:
            paths = self.path_record or self.path.path or self.path_preview
            for i, path in enumerate(self.path_preview + [v for k, v in sorted(
                self.slider_path_preview.items(),
                key=lambda e: e[1]
            )] if paths is self.path_preview else paths):
                if self.path.show != -1 and self.path.show != i:
                    continue
                for x, y in path:
                    r(x, x, y, y)
        # Points
        for vpoint in self.vpoints:
            r(vpoint.cx, vpoint.cx, vpoint.cy, vpoint.cy)
        # Synthesis page
        if self.show_target_path:
            # Solving paths
            for path in self.target_path.values():
                for x, y in path:
                    r(x, x, y, y)
            # Ranges
            for rect in self.ranges.values():
                r(rect.x(), rect.x() + rect.width(), rect.y(),
                  rect.y() - rect.height())
        # Background image
        if not self.background.isNull():
            x_r = self.background_offset.x()
            y_t = self.background_offset.y()
            r(
                x_r,
                x_r + self.background.width() * self.background_scale,
                y_t,
                y_t - self.background.height() * self.background_scale
            )
        return r.right, r.left, r.top, r.bottom

    def emit_free_move_all(self) -> None:
        """Edit all points to edit."""
        self.__emit_free_move(range(len(self.vpoints)))

    def paintEvent(self, event: QPaintEvent) -> None:
        """Drawing functions."""
        width = self.width()
        height = self.height()
        if self.width_old is None:
            self.width_old = width
        if self.height_old is None:
            self.height_old = height
        if self.width_old != width or self.height_old != height:
            self.ox += (width - self.width_old) / 2
            self.oy += (height - self.height_old) / 2
        # 'self' is the instance of 'DynamicCanvas'.
        BaseCanvas.paintEvent(self, event)
        # Draw links except ground
        brush = color_qt('dark-gray') if self.monochrome else LINK_COLOR
        brush.setAlphaF(self.transparency)
        self.painter.setBrush(brush)
        for vlink in self.vlinks[1:]:
            self.__draw_link(vlink)
        self.painter.setBrush(Qt.NoBrush)
        # Draw path
        if self.path.show != -2:
            self.__draw_path()
        # Draw solving path
        if self.show_target_path:
            self.painter.setFont(QFont("Arial", self.font_size + 5))
            self.draw_ranges()
            self.draw_target_path()
            self.painter.setFont(QFont("Arial", self.font_size))
        # Draw points
        for i, vpoint in enumerate(self.vpoints):
            self.__draw_point(i, vpoint)
        # Draw solutions
        if self.select_mode == SelectMode.SOLUTION:
            for i, expr in enumerate(self.exprs):
                func = expr[0]
                params = expr[1:-1]
                target = expr[-1]
                self.draw_solution(func, params, target, self.vpoints)
                if i in self.selections:
                    pos, _ = self.solution_polygon(func, params, target,
                                                   self.vpoints)
                    pen = QPen()
                    pen.setWidth(self.link_width + 3)
                    pen.setColor(QColor(161, 16, 239))
                    self.painter.setPen(pen)
                    self.painter.drawPolygon(QPolygonF([QPointF(x, y)
                                                        for x, y in pos]))
        # Draw a colored frame for free move mode
        if self.free_move != FreeMode.NO_FREE_MOVE:
            pen = QPen()
            if self.free_move == FreeMode.TRANSLATE:
                pen.setColor(QColor(161, 16, 229))
            elif self.free_move == FreeMode.ROTATE:
                pen.setColor(QColor(219, 162, 6))
            elif self.free_move == FreeMode.REFLECT:
                pen.setColor(QColor(79, 249, 193))
            pen.setWidth(8)
            self.painter.setPen(pen)
            self.__draw_frame()
        # Rectangular selection
        if self.selector.picking:
            pen = QPen(Qt.gray)
            pen.setWidth(1)
            self.painter.setPen(pen)
            self.painter.drawRect(self.selector.to_rect(self.zoom))
        # Show FPS
        self.fps_updated.emit()
        self.painter.end()
        # Record the widget size
        self.width_old = width
        self.height_old = height

    def __mouse_pos(self, event: QMouseEvent) -> Tuple[float, float]:
        """Return the mouse position mapping to main canvas."""
        return (event.x() - self.ox) / self.zoom, (
            event.y() - self.oy) / -self.zoom

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Press event.

        Middle button: Move canvas of view.
        Left button: Select the point (only first point will be catch).
        """
        self.selector.x, self.selector.y = self.__mouse_pos(event)
        button = event.buttons()
        if button == Qt.MiddleButton:
            self.selector.middle_dragged = True
            self.browse_tracking.emit(self.selector.x, self.selector.y)
        elif button == Qt.LeftButton:
            self.selector.left_dragged = True
            self.__select_func()
            if self.selector.selection_rect:
                self.selected.emit(tuple(self.selector.selection_rect[:1]),
                                   True)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """Mouse double click.

        + Middle button: Zoom to fit.
        + Left button: Edit point function.
        """
        button = event.buttons()
        if button == Qt.MidButton:
            self.zoom_to_fit()
        elif button == Qt.LeftButton and (not self.show_target_path):
            self.selector.x, self.selector.y = self.__mouse_pos(event)
            self.__select_func()
            if self.selector.selection_rect:
                self.selected.emit(tuple(self.selector.selection_rect[:1]),
                                   True)
                if self.free_move == FreeMode.NO_FREE_MOVE:
                    self.doubleclick_edit.emit(self.selector.selection_rect[0])

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Release mouse button.

        + Alt & Left button: Add a point.
        + Left button: Select a point.
        + Free move mode: Edit the point(s) coordinate.
        """
        if self.selector.left_dragged:
            km = QApplication.keyboardModifiers()
            self.selector.selection_old = list(self.selections)
            if (
                self.select_mode == SelectMode.JOINT
                and self.free_move != FreeMode.NO_FREE_MOVE
            ):
                x, y = self.__mouse_pos(event)
                if self.selector.x != x and self.selector.y != y:
                    # Edit point coordinates
                    self.__emit_free_move(self.selections)
                elif (
                    (not self.selector.selection_rect)
                    and km != Qt.ControlModifier
                    and km != Qt.ShiftModifier
                ):
                    self.no_selected.emit()
            else:
                if km == Qt.AltModifier:
                    # Add Point
                    self.alt_add.emit(
                        self.__snap(self.selector.x, is_zoom=False),
                        self.__snap(self.selector.y, is_zoom=False)
                    )
                elif (
                    (not self.selector.selection_rect)
                    and km != Qt.ControlModifier
                    and km != Qt.ShiftModifier
                ):
                    self.no_selected.emit()
        self.selected_tips_hide.emit()
        self.selector.release()
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Move mouse.

        + Middle button: Translate canvas view.
        + Left button: Free move mode / Rectangular selection.
        """
        x, y = self.__mouse_pos(event)
        if self.selector.middle_dragged:
            self.ox = event.x() - self.selector.x * self.zoom
            self.oy = event.y() + self.selector.y * self.zoom
            self.update()
        elif self.selector.left_dragged:
            if self.free_move == FreeMode.NO_FREE_MOVE:
                if self.show_target_path:
                    self.set_target_point.emit(x, y)
                else:
                    # Rectangular selection
                    self.selector.picking = True
                    self.selector.sx = self.__snap(x, is_zoom=False)
                    self.selector.sy = self.__snap(y, is_zoom=False)
                    self.__select_func(rect=True)
                    selection = self.selector.current_selection()
                    if selection:
                        self.selected.emit(selection, False)
                    else:
                        self.no_selected.emit()
                    self.selected_tips.emit(
                        event.globalPos(),
                        f"({self.selector.x:.02f}, {self.selector.y:.02f})\n"
                        f"({self.selector.sx:.02f}, {self.selector.sy:.02f})\n"
                        f"{len(selection)} "
                        f"{_selection_unit[self.select_mode]}(s)"
                    )
            elif self.select_mode == SelectMode.JOINT:
                if self.free_move == FreeMode.TRANSLATE:
                    # Free move translate function
                    mouse_x = self.__snap(x - self.selector.x, is_zoom=False)
                    mouse_y = self.__snap(y - self.selector.y, is_zoom=False)
                    self.selected_tips.emit(
                        event.globalPos(),
                        f"{mouse_x:+.02f}, {mouse_y:+.02f}"
                    )
                    for num in self.selections:
                        vpoint = self.vpoints[num]
                        vpoint.move((mouse_x + vpoint.x, mouse_y + vpoint.y))
                elif self.free_move == FreeMode.ROTATE:
                    # Free move rotate function
                    alpha = atan2(y, x) - atan2(self.selector.y,
                                                self.selector.x)
                    self.selected_tips.emit(
                        event.globalPos(),
                        f"{degrees(alpha):+.02f}°"
                    )
                    for num in self.selections:
                        vpoint = self.vpoints[num]
                        r = hypot(vpoint.x, vpoint.y)
                        beta = atan2(vpoint.y, vpoint.x)
                        vpoint.move(
                            (r * cos(beta + alpha), r * sin(beta + alpha)))
                        if vpoint.type in {VJoint.P, VJoint.RP}:
                            vpoint.rotate(
                                self.vangles[num] + degrees(beta + alpha))
                elif self.free_move == FreeMode.REFLECT:
                    # Free move reflect function
                    fx = 1 if x > 0 else -1
                    fy = 1 if y > 0 else -1
                    self.selected_tips.emit(
                        event.globalPos(),
                        f"{fx:+d}, {fy:+d}"
                    )
                    for num in self.selections:
                        vpoint = self.vpoints[num]
                        if vpoint.type == VJoint.R:
                            vpoint.move((vpoint.x * fx, vpoint.y * fy))
                        else:
                            vpoint.move((vpoint.x * fx, vpoint.y * fy))
                            if (x > 0) != (y > 0):
                                vpoint.rotate(180 - self.vangles[num])
                if self.free_move != FreeMode.NO_FREE_MOVE and self.selections:
                    self.update_preview_path()
            self.update()
        self.tracking.emit(x, y)

    def zoom_to_fit(self) -> None:
        """Zoom to fit function."""
        width = self.width()
        height = self.height()
        width = width if width else 1
        height = height if height else 1
        x_right, x_left, y_top, y_bottom = self.__zoom_to_fit_size()
        inf = float('inf')
        if (inf in {x_right, y_bottom}) or (-inf in {x_left, y_top}):
            # Default scale value
            self.zoom_changed.emit(self.default_zoom)
            self.ox = width / 2
            self.oy = height / 2
            self.update()
            return
        factor = BaseCanvas.zoom_factor(width, height, x_right, x_left, y_top,
                                        y_bottom)
        self.zoom_changed.emit(int(factor * self.margin_factor * 50))
        self.ox = (width - (x_left + x_right) * self.zoom) / 2
        self.oy = (height + (y_top + y_bottom) * self.zoom) / 2
        self.update()

    @Slot()
    def update_preview_path(self) -> None:
        """Update preview path."""
        self.preview_path(self.path_preview, self.slider_path_preview,
                          self.vpoints)
        self.update()
