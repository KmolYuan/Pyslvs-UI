# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Measurement import Ui_Form as Measurement_Form

class Measurement_show(QWidget, Measurement_Form):
    point_change = pyqtSignal(int, int)
    def __init__(self, table, parent=None):
        super(Measurement_show, self).__init__(parent)
        self.setupUi(self)
        self.Distance.setPlainText("0.0")
        self.First_Detection = True
        for i in range(table.rowCount()):
            self.Start.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
            self.End.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
    
    @pyqtSlot(float, float)
    def show_mouse_track(self, x, y): self.Mouse.setPlainText("("+str(x)+", "+str(y)+")")
    
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index):
        self.First_Detection = True
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index):
        self.First_Detection = True
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    @pyqtSlot(float)
    def change_distance(self, val): self.Distance.setPlainText(str(val))
    
    @pyqtSlot()
    def Detection_do(self):
        if self.First_Detection:
            self.First_Detection = False
            self.Max_val.setPlainText(self.Distance.toPlainText())
            self.Min_val.setPlainText(self.Distance.toPlainText())
        else:
            if float(self.Max_val.toPlainText())<float(self.Distance.toPlainText()): self.Max_val.setPlainText(self.Distance.toPlainText())
            if float(self.Min_val.toPlainText())>float(self.Distance.toPlainText()): self.Min_val.setPlainText(self.Distance.toPlainText())
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
