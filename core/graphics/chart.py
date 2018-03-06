# -*- coding: utf-8 -*-

"""Chart dialog of Pyslvs.

This part is using PyQtChart module.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QChart,
    QSizePolicy,
    Qt,
    QFont,
)

class DataChart(QChart):
    
    """A axis setted Qt chart widget."""
    
    def __init__(self, Title, axisX, axisY, parent=None):
        super(DataChart, self).__init__(parent)
        self.setTitle(Title)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        self.addAxis(axisX, Qt.AlignBottom)
        self.addAxis(axisY, Qt.AlignLeft)
