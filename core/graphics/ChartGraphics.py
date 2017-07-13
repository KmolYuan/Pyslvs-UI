# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from ..QtModules import *
from PyQt5.QtChart import *

class ChartDialog(QDialog):
    def __init__(self, Title, DataSet=list(), parent=None):
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle('Chart')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        chart = QChart()
        chart.setTitle(Title)
        chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = chart.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        axisX = QCategoryAxis()
        axisY = QValueAxis()
        axisX.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axisX.setMin(0)
        axisY.setTickCount(11)
        if len(DataSet)>0:
            maxGen = max([data[1] for data in DataSet])
            axisX.setMax(maxGen)
            chart.setTitle("{} (max {} generations)".format(Title, maxGen))
            for i in range(0, maxGen+1, int(maxGen/10)): axisX.append(str(i), i)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        for data in DataSet:
            line = QLineSeries()
            scatter = QScatterSeries()
            gen = data[1]
            points = data[2][:-1]
            pnum = len(points)
            line.setName("{} ({} Generations, {} Chromosome)".format(data[0], gen, data[3]))
            scatter.setMarkerSize(7)
            scatter.setColor(QColor(110, 190, 30))
            for i, e in enumerate(points):
                x = round(i*gen/(pnum-1), 0)
                line.append(QPointF(x, e))
                scatter.append(QPointF(x, e))
            for series in [line, scatter]:
                chart.addSeries(series)
                series.attachAxis(axisX)
                series.attachAxis(axisY)
            legend.markers(scatter)[0].setVisible(False)
        maxima = max([max(e[2]) for e in DataSet])+10 if DataSet else 100
        maxima -= maxima%10
        axisY.setRange(0., maxima if DataSet else 100.)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*([2]*4))
        chartView = QChartView(chart)
        chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(chartView)
