# -*- coding: utf-8 -*-

"""The option dialog use to adjust target path."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QDialog,
    Qt,
    pyqtSlot,
    QMessageBox,
)
import numpy as np
from typing import Sequence
from .Ui_path_adjust import Ui_Dialog

class Path_adjust_show(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the target path after closed.
    """
    
    def __init__(self, parent):
        super(Path_adjust_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.path = parent.currentPath()
        self.r_path = []
        for x, y in self.path:
            self.path_list.addItem("({}, {})".format(x, y))
        self.points_num.setText(str(len(self.path)))
        self.match_num.setValue(len(self.path))
    
    @pyqtSlot()
    def on_scaling_button_clicked(self):
        ox = self.scaling_rx.value()
        oy = self.scaling_ry.value()
        rx = self.scaling_rx.value()
        ry = self.scaling_ry.value()
        sh = self.scaling_h.value()
        sv = self.scaling_v.value()
        self.r_path = [
            (ox + (x - rx)*sh, oy + (y - ry)*sv)
            for x, y in self.path
        ]
        self.accept()
    
    @pyqtSlot()
    def on_moving_button_clicked(self):
        """Translate functions."""
        mx = self.moving_x_coordinate.value()
        my = self.moving_y_coordinate.value()
        self.r_path = [(x + mx, y + my) for x, y in self.path]
        self.accept()
    
    @pyqtSlot()
    def on_match_button_clicked(self):
        """Fitting function."""
        l = len(self.path)
        if l==0:
            return
        index = list(range(l))
        
        def polyfit(x: Sequence[float], y: Sequence[float], d: int):
            """Return a 2D fitting equation."""
            coeffs = np.polyfit(x, y, d)
            #Fit values and mean.
            yhat = np.poly1d(coeffs)(x)
            ybar = np.sum(y)/len(y)
            return (
                lambda t: sum(c * t**pow for pow, c in enumerate(reversed(coeffs))),
                np.sum((yhat - ybar)**2) / np.sum((y - ybar)**2)
            )
        
        x_func, x_accuracy = polyfit(index, [x for x, y in self.path], 4)
        y_func, y_accuracy = polyfit(index, [y for x, y in self.path], 4)
        QMessageBox.information(self,
            "Curve fitting",
            "Accuracy:\nx: {:.02f}%\ny: {:.02f}%".format(x_accuracy, y_accuracy),
            QMessageBox.Ok,
            QMessageBox.Ok
        )
        m = self.match_num.value()
        self.r_path = [(x_func(i/m*l), y_func(i/m*l)) for i in range(m)]
        self.accept()
