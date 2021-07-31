# -*- coding: utf-8 -*-

"""The option dialog use to adjust target path."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from math import cos, sin, atan2, radians, hypot
from numpy import ndarray, array, linspace, concatenate, full_like
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QDialog
from pyslvs import efd_fitting
from pyslvs_ui.graphics import DataChartDialog
from pyslvs_ui.info import HAS_SCIPY
from .edit_path_ui import Ui_Dialog

if TYPE_CHECKING:
    from pyslvs_ui.synthesis import Optimizer
if HAS_SCIPY:
    from scipy.interpolate import splprep, splev


class EditPathDialog(QDialog, Ui_Dialog):
    """Option dialog.

    Only edit the target path after closed.
    """

    def __init__(self, parent: Optimizer):
        """Just load in path data."""
        super(EditPathDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        # Get the current path from parent widget
        self.path = array(parent.current_path(), dtype=float)
        self.set_path = parent.set_path
        # GUI settings
        self.bspline_option.setEnabled(HAS_SCIPY)
        self.efd_option.clicked.connect(self.close_path_option.setChecked)
        self.efd_option.toggled.connect(self.close_path_option.setDisabled)
        self.num_points.setValue(len(self.path))

    def __gen_fitting(self) -> ndarray:
        """Generate the fitted curve."""
        num = self.num_points.value()
        is_close = self.close_path_option.isChecked()
        if is_close:
            num += 1
        if self.bspline_option.isChecked():
            if is_close:
                path = concatenate((self.path, self.path[:1, :]))
            else:
                path = self.path
            tck = splprep((path[:, 0], path[:, 1]), per=is_close)
            path = array(splev(linspace(0, 1, num, endpoint=True), tck[0])).T
        else:
            path = efd_fitting(self.path, num)
        if is_close:
            path = path[:-1]
        return path

    @Slot(name='on_fitting_preview_btn_clicked')
    def __fitting_preview(self) -> None:
        """Curve fitting preview."""
        dlg = DataChartDialog(self, "Preview")
        ax = dlg.ax()[0]
        ax.plot(self.path[:, 0], self.path[:, 1], 'ro')
        path = self.__gen_fitting()
        ax.plot(path[:, 0], path[:, 1], 'b--')
        dlg.set_margin(0.2)
        dlg.show()
        dlg.exec()
        dlg.deleteLater()

    @Slot(name='on_fitting_btn_clicked')
    def __fitting(self) -> None:
        """Curve fitting function."""
        path = self.__gen_fitting()
        self.set_path(path)
        self.accept()

    @Slot(name='on_move_btn_clicked')
    def __move(self) -> None:
        """Translate function."""
        mx = self.move_x.value()
        my = self.move_y.value()
        offset = full_like(self.path, mx)
        offset[:, 1] = my
        self.set_path(self.path + offset)
        self.accept()

    @Slot(name='on_rotate_btn_clicked')
    def __rotate(self) -> None:
        """Rotate by origin."""
        angle = radians(self.rotate_angle.value())
        path = []
        for x, y in self.path:
            h = hypot(x, y)
            a = atan2(y, x) + angle
            path.append((h * cos(a), h * sin(a)))
        self.set_path(path)
        self.accept()

    @Slot(name='on_scale_btn_clicked')
    def __scale(self) -> None:
        """Scale function."""
        ox = self.scale_rx.value()
        oy = self.scale_ry.value()
        rx = self.scale_rx.value()
        ry = self.scale_ry.value()
        sh = self.scale_h.value()
        sv = self.scale_v.value()
        self.set_path((ox + (x - rx) * sh, oy + (y - ry) * sv)
                      for x, y in self.path)
        self.accept()
