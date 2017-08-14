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
    def __init__(self, Title, mechanism_data=list(), parent=None):
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle('Chart')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        self.mechanism_data = mechanism_data
        #Fitness / Generation Chart
        FG_Chart = QChart()
        FG_Chart.setTitle(Title)
        self.setChart(FG_Chart, 0, 1)
        #Fitness / Time Chart
        FT_Chart = QChart()
        FT_Chart.setTitle(Title)
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
        chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = chart.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        if self.mechanism_data:
            '''
            posX / posY = [0] / [1] / [2]
            TimeAndFitness = [[(gen, fitness, time), ...], ...]
            '''
            if type(self.mechanism_data[0]['TimeAndFitness'][0])==float:
                TimeAndFitness = [
                    [(data['generateData']['maxGen']*i/len(data['TimeAndFitness']), Tnf, 0)
                    for i, Tnf in enumerate(data['TimeAndFitness'])]
                    for data in self.mechanism_data]
            else:
                #Just copy from mechanism_data
                TimeAndFitness = [[Tnf for Tnf in data['TimeAndFitness']] for data in self.mechanism_data]
        axisX = QCategoryAxis()
        axisY = QValueAxis()
        axisX.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axisX.setMin(0)
        axisY.setTickCount(11)
        if self.mechanism_data:
            maximaX = int(max([max([Tnf[posX] for Tnf in data]) for data in TimeAndFitness])*100)
            axisX.setMax(maximaX)
            if int(maximaX/10):
                for i in range(0, maximaX+1, int(maximaX/10)):
                    axisX.append(str(i/100), i)
            else:
                for i in range(0, 1000, 100):
                    axisX.append(str(i/100), i)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        for data in self.mechanism_data:
            line = QLineSeries()
            scatter = QScatterSeries()
            gen = data['generateData']['maxGen']
            Tnf = TimeAndFitness[self.mechanism_data.index(data)]
            points = Tnf[:-1] if Tnf[-1]==Tnf[-2] else Tnf
            line.setName("{} ({} gen, {} chrom)".format(data['Algorithm'], gen, data['mechanismParams']['VARS']))
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
        if self.mechanism_data:
            maximaY = max([max([Tnf[posY] for Tnf in data]) for data in TimeAndFitness])+10
        else:
            maximaY = 100
        maximaY -= maximaY%10
        axisY.setRange(0., maximaY)
