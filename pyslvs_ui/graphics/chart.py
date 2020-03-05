# -*- coding: utf-8 -*-

"""Chart dialog of Pyslvs.

This part is using PyQtChart module.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtGui import QFont
from qtpy.QtCharts import QtCharts


class DataChart(QtCharts.QChart):
    """Two axises Qt chart widget."""

    def __init__(
        self,
        title: str,
        axis_x: QtCharts.QValueAxis,
        axis_y: QtCharts.QValueAxis,
        monochrome: bool
    ):
        """Input title and two axis, QChart class has no parent."""
        super(DataChart, self).__init__()
        if monochrome:
            self.setTheme(DataChart.ChartThemeLight)
        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        self.addAxis(axis_x, Qt.AlignBottom)
        self.addAxis(axis_y, Qt.AlignLeft)
