# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Drive_rod import Ui_Form

class Drive_rod_show(QWidget, Ui_Form):
    positionChange = pyqtSignal(float, int)
    def __init__(self, table, tablePoint, parent=None):
        super(Drive_rod_show, self).__init__(parent)
        self.setupUi(self)
        self.table = table
        self.tablePoint = tablePoint
        for i in range(len(table)): self.Rod.insertItem(i, QIcon(QPixmap(":/icons/spring.png")), 'Rod{}'.format(i))
        self.on_Rod_currentIndexChanged(0)
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index):
        start = self.table[index].start
        end = self.table[index].end
        distance = int(((self.tablePoint[start].cx-self.tablePoint[end].cx)**2+(self.tablePoint[start].cy-self.tablePoint[end].cy)**2)**(1/2)*100)
        self.Position.setMaximum(distance)
        self.Position.setValue(int(self.table[index].pos*100))
        self.Distance_text.setValue(distance/100)
        self.Center.setText(str(self.table[index].cen))
        self.Start.setText(str(start))
    
    @pyqtSlot()
    def on_ResetButton_clicked(self):
        index = self.Rod.currentIndex()
        start = self.table[index].start
        end = self.table[index].end
        distance = int(((self.tablePoint[start].cx-self.tablePoint[end].cx)**2+(self.tablePoint[start].cy-self.tablePoint[end].cy)**2)**(1/2)*100)
        self.Position.setMaximum(distance)
        self.Position.setValue(int(self.table[index].pos*100))
        self.Distance_text.setValue(distance/100)
    
    @pyqtSlot(float)
    def on_Distance_text_valueChanged(self, p0): self.Position.setMaximum(int(p0*100))
    @pyqtSlot(int)
    def on_Position_valueChanged(self, value): self.Distance.setText(str(value/100))
    
    def __del__(self): self.positionChange.emit(self.Distance_text.value(), self.Rod.currentIndex())
