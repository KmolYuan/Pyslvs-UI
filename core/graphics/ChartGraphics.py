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
"""This part using PyQtChart module."""
from PyQt5.QtChart import *

class ChartDialog(QDialog):
    def __init__(self, Title, DataSet=list(), parent=None):
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle('Chart')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        self.DataSet = DataSet
        #Fitness / Generation Chart
        FG_Chart = QChart()
        FG_Chart.setTitle(Title)
        FG_Chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        FG_legend = FG_Chart.legend()
        FG_legend.setAlignment(Qt.AlignBottom)
        FG_legend.setFont(QFont(FG_legend.font().family(), 12, QFont.Medium))
        self.setChart(FG_Chart, 0, 1)
        #Fitness / Time Chart
        FT_Chart = QChart()
        FT_Chart.setTitle(Title)
        FT_legend = FT_Chart.legend()
        FT_legend.setAlignment(Qt.AlignBottom)
        FT_legend.setFont(QFont(FT_legend.font().family(), 12, QFont.Medium))
        self.setChart(FT_Chart, 2, 1)
        #Widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        tabwidget = QTabWidget(self)
        #Widgets -> Fitness / Generation Chart
        FG_widget = QWidget()
        tabwidget.addTab(FG_widget, QIcon(), "Fitness / Generation Chart")
        FG_layout = QVBoxLayout(FG_widget)
        FG_layout.setContentsMargins(2, 2, 2, 2)
        FG_chartView = QChartView(FG_Chart)
        FG_chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        FG_layout.addWidget(FG_chartView)
        #Widgets -> Fitness / Time Chart
        FT_widget = QWidget()
        tabwidget.addTab(FT_widget, QIcon(), "Fitness / Time Chart")
        FT_layout = QVBoxLayout(FT_widget)
        FT_layout.setContentsMargins(2, 2, 2, 2)
        FT_chartView = QChartView(FT_Chart)
        FT_chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        FT_layout.addWidget(FT_chartView)
        main_layout.addWidget(tabwidget)
    
    def setChart(self, chart, posX, posY):
        axisX = QCategoryAxis()
        axisY = QValueAxis()
        axisX.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axisX.setMin(0)
        axisY.setTickCount(11)
        if len(self.DataSet)>0:
            Max = int(max([max([e[posX] for e in data[2]]) for data in self.DataSet])*100)
            axisX.setMax(Max)
            for i in range(0, Max+1, int(Max/10)):
                axisX.append(str(i/100), i)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        for data in self.DataSet:
            line = QLineSeries()
            scatter = QScatterSeries()
            gen = data[1]
            points = data[2][:-1]
            line.setName("{} ({} gen, {} chrom)".format(data[0], gen, data[3]))
            scatter.setMarkerSize(7)
            scatter.setColor(QColor(110, 190, 30))
            for i, e in enumerate(points):
                y = e[posY]
                x = e[posX]*100
                line.append(QPointF(x, y))
                scatter.append(QPointF(x, y))
            for series in [line, scatter]:
                chart.addSeries(series)
                series.attachAxis(axisX)
                series.attachAxis(axisY)
            chart.legend().markers(scatter)[0].setVisible(False)
        maxima = max([max(data[2] if type(data[2])==float else data[2][1]) for data in self.DataSet])+10 if self.DataSet else 100
        maxima -= maxima%10
        axisY.setRange(0., maxima if self.DataSet else 100.)
