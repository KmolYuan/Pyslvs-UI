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
"""This part is using PyQtChart module."""

class dataChart(QChart):
    def __init__(self, Title, axisX, axisY, parent=None):
        super(dataChart, self).__init__(parent)
        self.setTitle(Title)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        legend = self.legend()
        legend.setAlignment(Qt.AlignBottom)
        legend.setFont(QFont(legend.font().family(), 12, QFont.Medium))
        self.addAxis(axisX, Qt.AlignBottom)
        self.addAxis(axisY, Qt.AlignLeft)

class ChartDialog(QDialog):
    def __init__(self, Title, mechanism_data=[], parent=None):
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle('Chart')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        self.Title = Title
        self.mechanism_data = mechanism_data
        #Widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        self.tabWidget = QTabWidget(self)
        self.setChart("Fitness / Generation Chart", 0, 1)
        self.setChart("Generation / Time Chart", 2, 0)
        self.setChart("Fitness / Time Chart", 2, 1)
        main_layout.addWidget(self.tabWidget)
    
    def setChart(self, tabName, posX, posY):
        if self.mechanism_data:
            '''
            #posX / posY = [0] / [1] / [2]
            #TimeAndFitness = [[(gen, fitness, time), ...], ...]
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
        #X maxima
        if self.mechanism_data:
            maximaX = int(max([max([Tnf[posX] for Tnf in data]) for data in TimeAndFitness])*100)
            axisX.setMax(maximaX)
            i10 = int(maximaX/10)
            if i10:
                for i in range(0, maximaX+1, i10):
                    axisX.append(str(i/100), i)
            else:
                for i in range(0, 1000, 100):
                    axisX.append(str(i/100), i)
        #Y maxima
        if self.mechanism_data:
            maximaY = max([max([Tnf[posY] for Tnf in data]) for data in TimeAndFitness])+10
        else:
            maximaY = 100
        maximaY -= maximaY%10
        axisY.setRange(0., maximaY)
        chart = dataChart(self.Title, axisX, axisY)
        #Append datasets
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
        #Add chart into tab widget
        widget = QWidget()
        self.tabWidget.addTab(widget, QIcon(), tabName)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        chartView = QChartView(chart)
        chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(chartView)
