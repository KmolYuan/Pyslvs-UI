# -*- coding: utf-8 -*-
from .modules import *
from .Ui_run_Drive_rod import Ui_Form

class Drive_rod_show(QWidget, Ui_Form):
    Rod_change = pyqtSignal(int)
    def __init__(self, table, parent=None):
        super(Drive_rod_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(table.rowCount()): self.Rod.insertItem(i, QIcon(QPixmap(":/icons/spring.png")), table.item(i, 0).text())
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index): self.Rod_change.emit(index)
