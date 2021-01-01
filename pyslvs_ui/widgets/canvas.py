# -*- coding: utf-8 -*-

"""The canvas of main window."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from collections import deque
from typing import (
    cast, TYPE_CHECKING, List, Tuple, Sequence, Union, Mapping,
)
from qtpy.QtCore import Slot, Qt, QRectF, QPoint, QPointF, QSizeF
from qtpy.QtWidgets import QApplication, QToolTip, QWidget
from qtpy.QtGui import QRegion, QCursor, QWheelEvent, QPixmap, QImage
from pyslvs import VJoint
from .canvas_base import MainCanvasBase, FreeMode, SelectMode, ZoomBy

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase

_Coord = Tuple[float, float]
_Paths = Sequence[Sequence[_Coord]]
_SliderPaths = Mapping[int, Sequence[_Coord]]


class MainCanvas(MainCanvasBase):
    """The canvas in main window.

    + Parse and show PMKS expression.
    + Show paths.
    + Show settings of dimensional synthesis widget.
    + Mouse interactions.
    + Zoom to fit function.
    """

    def __init__(self, parent: MainWindowBase):
        super(MainCanvas, self).__init__(parent)
        # Dependent functions to set zoom bar
        self.set_zoom_bar = parent.zoom_bar.setValue
        self.zoom_value = parent.zoom_bar.value
        self.prefer = parent.prefer
        # Dependent functions to set selection mode
        self.selection_mode_wheel = parent.entities_tab.setCurrentIndex
        self.selection_mode = parent.entities_tab.currentIndex

    def update_canvas(
        self,
        exprs: List[Tuple[str, ...]],
        paths: _Paths,
        slider_paths: _SliderPaths
    ) -> None:
        """Update with Point and Links data."""
        self.vangles = tuple(vpoint.angle for vpoint in self.vpoints)
        self.exprs = exprs
        self.path.path = paths
        self.path.slider_path = slider_paths
        self.update()

    @Slot(int)
    def set_link_width(self, width: int) -> None:
        """Update width of links."""
        self.link_width = width
        self.update()

    @Slot(int)
    def set_path_width(self, width: int) -> None:
        """Update width of links."""
        self.path_width = width
        self.update()

    @Slot(bool)
    def set_point_mark(self, show: bool) -> None:
        """Update show point mark or not."""
        self.show_point_mark = show
        self.update()

    @Slot(bool)
    def set_show_dimension(self, show: bool) -> None:
        """Update show dimension or not."""
        self.show_dimension = show
        self.update()

    @Slot(bool)
    def set_curve_mode(self, curve: bool) -> None:
        """Update show as curve mode or not."""
        self.path.curve = curve
        self.update()

    @Slot(int)
    def set_font_size(self, font_size: int) -> None:
        """Update font size."""
        self.font_size = font_size
        self.update()

    @Slot(int)
    def set_zoom(self, zoom: int) -> None:
        """Update zoom factor."""
        zoom_old = self.zoom
        self.zoom = zoom / 50.
        zoom_old -= self.zoom
        if self.zoomby == ZoomBy.CANVAS:
            pos = self.mapFromGlobal(QCursor.pos())
        else:
            pos = QPointF(self.width() / 2, self.height() / 2)
        self.ox += (pos.x() - self.ox) / self.zoom * zoom_old
        self.oy += (pos.y() - self.oy) / self.zoom * zoom_old
        self.update()

    def get_zoom(self) -> float:
        """Return zoom factor."""
        return self.zoom

    def set_default_zoom(self, zoom: int) -> None:
        """Set default zoom value."""
        self.default_zoom = zoom

    def set_show_target_path(self, show: bool) -> None:
        """Update show target path or not."""
        self.show_target_path = show
        self.update()

    def set_free_move(self, free_move: int) -> None:
        """Update free move mode number."""
        self.free_move = FreeMode(free_move + 1)
        self.update()

    @Slot(int)
    def set_selection_radius(self, sr: int) -> None:
        """Update radius of point selector."""
        self.sr = sr

    @Slot(int)
    def set_transparency(self, transparency: int) -> None:
        """Update transparency. (0%: opaque)"""
        self.transparency = (100 - transparency) / 100
        self.update()

    @Slot(int)
    def set_margin_factor(self, factor: int) -> None:
        """Update margin factor when zoom to fit."""
        self.margin_factor = 1 - factor / 100
        self.update()

    @Slot(int)
    def set_joint_size(self, size: int) -> None:
        """Update size for each joint."""
        self.joint_size = size
        self.update()

    @Slot(int)
    def set_zoom_by(self, zoomby: int) -> None:
        """Update zooming center option.

        + 0: Cursor
        + 1: Canvas center
        """
        self.zoomby = ZoomBy(zoomby + 1)

    @Slot(float)
    def set_snap(self, snap: float) -> None:
        """Update mouse capture value."""
        self.snap = snap

    @Slot(str)
    def set_background(self, path: str) -> None:
        """Set background from file path."""
        self.background.load(path)
        self.update()

    @Slot(float)
    def set_background_opacity(self, opacity: float) -> None:
        """Set opacity of background."""
        self.background_opacity = opacity
        self.update()

    @Slot(float)
    def set_background_scale(self, scale: float) -> None:
        """Set scale value of background."""
        self.background_scale = scale
        self.update()

    @Slot(float)
    def set_background_offset_x(self, x: float) -> None:
        """Set offset x value of background."""
        self.background_offset.setX(x)
        self.update()

    @Slot(float)
    def set_background_offset_y(self, y: float) -> None:
        """Set offset y value of background."""
        self.background_offset.setY(-y)
        self.update()

    @Slot(int)
    def set_selection_mode(self, mode: int) -> None:
        """Update the selection."""
        self.select_mode = SelectMode(mode + 1)
        self.update()

    @Slot(list)
    def set_selection(self, selections: List[int]) -> None:
        """Update the selection."""
        self.selections = selections
        self.update()

    def set_solving_path(self, path: Mapping[int, Sequence[_Coord]]):
        """Update target path."""
        self.target_path = dict(path)
        self.update()

    def set_path_show(self, p: int) -> None:
        """Update path present mode.

        -2: Hide all paths.
        -1: Show all paths.
        i: Show path i.
        """
        self.path.show = p
        self.update()

    def update_ranges(self,
                      ranges: Mapping[str, Tuple[float, float, float]]) -> None:
        """Update the ranges of dimensional synthesis."""
        self.ranges.clear()
        self.ranges.update({tag: QRectF(
            QPointF(values[0] - values[2], values[1] + values[2]),
            QSizeF(values[2], values[2]) * 2
        ) for tag, values in ranges.items()})
        self.update()

    def record_start(self, limit: int) -> None:
        """Start a limit from main window."""
        self.path_record.clear()
        self.slider_record.clear()
        self.path_record.extend(deque([], limit) for _ in self.vpoints)
        self.slider_record.update((i, deque([], limit))
                                  for i, vp in enumerate(self.vpoints)
                                  if vp.type in {VJoint.P, VJoint.RP})

    def record_path(self) -> None:
        """Recording path."""
        for i, vpoint in enumerate(self.vpoints):
            self.path_record[i].append((vpoint.cx, vpoint.cy))
            if vpoint.type in {VJoint.P, VJoint.RP}:
                self.slider_record[i].append((vpoint.c[0, 0], vpoint.c[0, 1]))

    def get_record_path(self) -> Tuple[Sequence[Sequence[_Coord]],
                                       Mapping[int, Sequence[_Coord]]]:
        """Return paths."""
        paths = tuple(tuple(path) for path in self.path_record)
        paths_slider = {i: tuple(p) for i, p in self.slider_record.items()}
        self.path_record.clear()
        self.slider_record.clear()
        return paths, paths_slider

    def adjust_link(
        self,
        coords: Sequence[Union[Tuple[_Coord, ...], _Coord]]
    ):
        """Change points coordinates."""
        for i, c in enumerate(coords):
            if isinstance(c[0], float):
                self.vpoints[i].move(cast(_Coord, c))
            else:
                self.vpoints[i].move(*cast(Tuple[_Coord, _Coord], c))
        self.update_preview_path()

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Switch function by mouse wheel.

        + Set zoom bar value.
        + Set select mode.
        """
        p = event.angleDelta()
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            value = p.y()
        elif p.x() != 0:
            value = p.x()
        elif p.y() != 0:
            value = self.prefer.scale_factor_option * (1 if p.y() > 0 else -1)
            value += self.zoom_value()
            self.set_zoom_bar(value)
            return
        else:
            return
        tags = ("Points", "Links")
        mode = (self.selection_mode() + (-1 if value > 0 else 1)) % len(tags)
        self.selection_mode_wheel(mode)
        QToolTip.showText(event.globalPos(), f"Selection mode: {tags[mode]}",
                          self)
        event.accept()

    def grab_no_background(self) -> QPixmap:
        """Grab function without background."""
        image = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
        image.fill(Qt.transparent)
        self.switch_grab()
        self.painter.begin(image)
        self.render(self.painter, QPoint(), QRegion(), QWidget.DrawChildren)
        self.switch_grab()
        return QPixmap.fromImage(image)
