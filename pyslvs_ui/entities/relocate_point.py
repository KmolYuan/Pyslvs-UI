# -*- coding: utf-8 -*-

"""The option dialog used to relocate the points."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from math import isnan, radians
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QDialog, QDialogButtonBox
from pyslvs import plap, pllp, Coord
from pyslvs_ui.widgets import QRotatableView
from .relocate_point_ui import Ui_Dialog as SubUiDialog

if TYPE_CHECKING:
    from .edit_point import EditPointDialog


class RelocateDialog(QDialog, SubUiDialog):
    """Relocation option dialog."""

    def __init__(self, parent: EditPointDialog):
        super(RelocateDialog, self).__init__(parent)
        self.setupUi(self)
        self.__x = self.__y = float('nan')
        self.vpoints = parent.vpoints
        self.plap_dial = QRotatableView(self)
        self.panel_layout.insertWidget(0, self.plap_dial)
        self.plap_dial.value_changed.connect(self.plap_angle_box.setValue)
        icon = self.windowIcon()
        for combo in (self.plap_p1_box, self.pllp_p1_box, self.pllp_p2_box):
            for p in range(len(self.vpoints)):
                combo.addItem(icon, f"Point{p}")
        for spinbox in (
            self.plap_p1x_box,
            self.plap_p1y_box,
            self.plap_distance_box,
            self.plap_angle_box,
            self.pllp_p1x_box,
            self.pllp_p1y_box,
            self.pllp_distance1_box,
            self.pllp_distance2_box,
            self.pllp_p2x_box,
            self.pllp_p2y_box,
        ):
            spinbox.valueChanged.connect(self.__is_ok)
        self.pllp_inversed_box.toggled.connect(self.__is_ok)
        self.tab_widget.currentChanged.connect(self.__is_ok)
        self.__is_ok()

    @Slot(int, name='on_plap_p1_box_currentIndexChanged')
    @Slot(int, name='on_pllp_p1_box_currentIndexChanged')
    @Slot(int, name='on_pllp_p2_box_currentIndexChanged')
    def __set_pos(self, index: int) -> None:
        """Set position when switch the combobox."""
        p = self.vpoints[index]
        combo = self.sender()
        if combo is self.plap_p1_box:
            self.plap_p1x_box.setValue(p.cx)
            self.plap_p1y_box.setValue(p.cy)
        elif combo is self.pllp_p1_box:
            self.pllp_p1x_box.setValue(p.cx)
            self.pllp_p1y_box.setValue(p.cy)
        elif combo is self.pllp_p2_box:
            self.pllp_p2x_box.setValue(p.cx)
            self.pllp_p2y_box.setValue(p.cy)

    @Slot()
    def __is_ok(self) -> None:
        """Check and show the final position."""
        mode = self.tab_widget.currentIndex()
        if mode == 0:
            x = self.plap_p1x_box.value()
            y = self.plap_p1y_box.value()
            c = plap(
                Coord(x, y),
                self.plap_distance_box.value(),
                radians(self.plap_angle_box.value())
            )
        elif mode == 1:
            x1 = self.pllp_p1x_box.value()
            y1 = self.pllp_p1y_box.value()
            x2 = self.pllp_p2x_box.value()
            y2 = self.pllp_p2y_box.value()
            c = pllp(
                Coord(x1, y1),
                self.pllp_distance1_box.value(),
                self.pllp_distance2_box.value(),
                Coord(x2, y2),
                self.pllp_inversed_box.isChecked()
            )
        else:
            raise ValueError("invalid option")
        self.preview_label.setText(f"({c.x}, {c.y})")
        self.__x = c.x
        self.__y = c.y
        ok_btn = self.btn_box.button(QDialogButtonBox.Ok)
        ok_btn.setEnabled(not (isnan(c.x) or isnan(c.y)))

    def get_x(self) -> float:
        """Get final x position."""
        return self.__x

    def get_y(self) -> float:
        """Get final y position."""
        return self.__y
