# -*- coding: utf-8 -*-

"""Chart dialog of Pyslvs.

This part is using PyQtChart module.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    Qt,
    QChart,
    QValueAxis,
    QSizePolicy,
    QFont,
)


class DataChart(QChart):

    """Two axises Qt chart widget."""

    def __init__(
        self,
        title: str,
        axis_x: QValueAxis,
        axis_y: QValueAxis
    ):
        """Input title and two axis, QChart class has no parent."""
        super(DataChart, self).__init__()
        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        self.addAxis(axis_x, Qt.AlignBottom)
        self.addAxis(axis_y, Qt.AlignLeft)
