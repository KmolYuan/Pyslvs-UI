# -*- coding: utf-8 -*-

"""The canvas of main window."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from collections import deque
from typing import (
    TYPE_CHECKING,
    List,
    Tuple,
    Sequence,
    Dict,
    Union,
)
from core.QtModules import (
    Slot,
    Qt,
    QApplication,
    QRectF,
    QPoint,
    QPointF,
    QSizeF,
    QCursor,
    QToolTip,
    QWheelEvent,
)
from .main_canvas_method import (
    DynamicCanvasInterface,
    FreeMode,
    SelectMode,
)
if TYPE_CHECKING:
    from core.widgets import MainWindowBase

_Coord = Tuple[float, float]


class DynamicCanvas(DynamicCanvasInterface):

    """The canvas in main window.

    + Parse and show PMKS expression.
    + Show paths.
    + Show settings of dimensional synthesis widget.
    + Mouse interactions.
    + Zoom to fit function.
    """

    def __init__(self, parent: MainWindowBase):
        super(DynamicCanvas, self).__init__(parent)
        # Dependent functions to set zoom bar.
        self.set_zoom_bar = parent.zoom_bar.setValue
        self.zoom_value = parent.zoom_bar.value
        self.zoom_factor = parent.scalefactor_option.value
        # Dependent functions to set selection mode.
        self.selection_mode_wheel = parent.entities_tab.setCurrentIndex
        self.selection_mode = parent.entities_tab.currentIndex

    def update_figure(self, exprs: List[Tuple[str, ...]], path: List[_Coord]):
        """Update with Point and Links data."""
        self.vangles = tuple(vpoint.angle for vpoint in self.vpoints)
        self.exprs = exprs
        self.path.path = path
        self.update()

    @Slot()
    def update_preview_path(self):
        """Update preview path."""
        self.preview_path(self.path_preview, self.slider_path_preview, self.vpoints)
        self.update()

    @Slot(int)
    def set_link_width(self, link_width: int):
        """Update width of links."""
        self.link_width = link_width
        self.update()

    @Slot(int)
    def set_path_width(self, path_width: int):
        """Update width of links."""
        self.path_width = path_width
        self.update()

    @Slot(bool)
    def set_point_mark(self, show_point_mark: bool):
        """Update show point mark or not."""
        self.show_point_mark = show_point_mark
        self.update()

    @Slot(bool)
    def set_show_dimension(self, show_dimension: bool):
        """Update show dimension or not."""
        self.show_dimension = show_dimension
        self.update()

    @Slot(bool)
    def set_curve_mode(self, curve: bool):
        """Update show as curve mode or not."""
        self.path.curve = curve
        self.update()

    @Slot(int)
    def set_font_size(self, font_size: int):
        """Update font size."""
        self.font_size = font_size
        self.update()

    @Slot(int)
    def set_zoom(self, zoom: int):
        """Update zoom factor."""
        zoom_old = self.zoom
        self.zoom = zoom / 100 * self.rate
        zoom_old -= self.zoom
        if self.zoomby == 0:
            pos = self.mapFromGlobal(QCursor.pos())
        else:
            pos = QPointF(self.width() / 2, self.height() / 2)
        self.ox += (pos.x() - self.ox) / self.zoom * zoom_old
        self.oy += (pos.y() - self.oy) / self.zoom * zoom_old
        self.update()

    def set_show_target_path(self, show_target_path: bool):
        """Update show target path or not."""
        self.show_target_path = show_target_path
        self.update()

    def set_free_move(self, free_move: int):
        """Update free move mode number."""
        self.free_move = FreeMode(free_move + 1)
        self.update()

    @Slot(int)
    def set_selection_radius(self, sr: int):
        """Update radius of point selector."""
        self.sr = sr

    @Slot(int)
    def set_transparency(self, transparency: int):
        """Update transparency. (0%: opaque)"""
        self.transparency = (100 - transparency) / 100
        self.update()

    @Slot(int)
    def set_margin_factor(self, margin_factor: int):
        """Update margin factor when zoom to fit."""
        self.margin_factor = 1 - margin_factor / 100
        self.update()

    @Slot(int)
    def set_joint_size(self, joint_size: int):
        """Update size for each joint."""
        self.joint_size = joint_size
        self.update()

    @Slot(int)
    def set_zoom_by(self, zoomby: int):
        """Update zooming center option."""
        self.zoomby = zoomby

    @Slot(float)
    def set_snap(self, snap: float):
        """Update mouse capture value."""
        self.snap = snap

    @Slot(str)
    def set_background(self, path: str):
        """Set background from file path."""
        if self.background.load(path):
            self.update()

    @Slot(float)
    def set_background_opacity(self, opacity: float):
        """Set opacity of background."""
        self.background_opacity = opacity
        self.update()

    @Slot(float)
    def set_background_scale(self, scale: float):
        """Set scale value of background."""
        self.background_scale = scale
        self.update()

    @Slot(float)
    def set_background_offset_x(self, x: float):
        """Set offset x value of background."""
        self.background_offset.setX(x)
        self.update()

    @Slot(float)
    def set_background_offset_y(self, y: float):
        """Set offset y value of background."""
        self.background_offset.setY(-y)
        self.update()

    @Slot(int)
    def set_selection_mode(self, select_mode: int):
        """Update the selection."""
        self.select_mode = SelectMode(select_mode + 1)
        self.update()

    @Slot(list)
    def set_selection(self, selections: List[int]):
        """Update the selection."""
        self.selections = selections
        self.update()

    def set_solving_path(
        self,
        target_path: Dict[str, Tuple[_Coord]]
    ):
        """Update target path."""
        self.target_path = target_path
        self.update()

    def set_path_show(self, p: int):
        """Update path present mode.

        -2: Hide all paths.
        -1: Show all paths.
        i: Show path i.
        """
        self.path.show = p
        self.update()

    def update_ranges(self, ranges: Dict[str, Tuple[float, float, float]]):
        """Update the ranges of dimensional synthesis."""
        self.ranges.clear()
        self.ranges.update({tag: QRectF(
            QPointF(values[0] - values[2], values[1] + values[2]),
            QSizeF(values[2] * 2, values[2] * 2)
        ) for tag, values in ranges.items()})
        self.update()

    def record_start(self, limit: int):
        """Start a limit from main window."""
        self.path_record = []
        for _ in range(len(self.vpoints)):
            self.path_record.append(deque([], limit))

    def record_path(self):
        """Recording path."""
        for i, vpoint in enumerate(self.vpoints):
            self.path_record[i].append((vpoint.cx, vpoint.cy))

    def get_record_path(self) -> Tuple[Tuple[_Coord, ...], ...]:
        """Return paths."""
        paths = tuple(
            tuple(path) if len(set(path)) > 1 else ()
            for path in self.path_record
        )
        self.path_record.clear()
        return paths

    def adjust_link(
        self,
        coords: Sequence[Union[Tuple[_Coord, ...], _Coord]]
    ):
        """Change points coordinates."""
        for i, c in enumerate(coords):
            if type(c[0]) is float:
                self.vpoints[i].move(c)
            else:
                self.vpoints[i].move(*c)
        self.update_preview_path()

    def wheelEvent(self, event: QWheelEvent):
        """Switch function by mouse wheel.

        + Set zoom bar value.
        + Set select mode.
        """
        p: QPoint = event.angleDelta()
        value_x = p.x()
        value_y = p.y()
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            value = value_y
        elif value_x != 0:
            value = value_x
        elif value_y != 0:
            self.set_zoom_bar(self.zoom_value() + self.zoom_factor() * (1 if value_y > 0 else -1))
            return
        else:
            return

        mode = self.selection_mode() + (-1 if value > 0 else 1)
        self.selection_mode_wheel(1 if mode > 1 else mode)
        mode = ["Points", "Links"][self.selection_mode()]
        QToolTip.showText(event.globalPos(), f"Selection mode: {mode}", self)
        event.accept()
