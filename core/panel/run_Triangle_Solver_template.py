# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver_template import Ui_Dialog

class Triangle_Solver_template_show(QDialog, Ui_Dialog):
    def __init__(self, Point, row, template='4-bar linkage', parent=None):
        super(Triangle_Solver_template_show, self).__init__(parent)
        self.setupUi(self)
        self.Point = Point
        self.on_templateType_currentIndexChanged(0)
        self.templateType.setCurrentIndex(self.templateType.findText(template))
        self.isOk()
    
    @pyqtSlot(int)
    def on_templateType_currentIndexChanged(self, pos):
        self.clearTables()
        if pos==0:
            pic = ":/icons/preview/4Bar.png"
            self.paramaTable(5)
        elif pos==1:
            pic = ":/icons/preview/8Bar.png"
            self.paramaTable(8)
        self.templateImage.setPixmap(QPixmap(pic).scaledToWidth(500))
    
    def clearTables(self):
        for table in [self.triangleTable, self.parameterTable]:
            for i in range(table.rowCount()): table.removeRow(0)
    
    def paramaTable(self, c):
        for i in range(c):
            self.parameterTable.insertRow(i)
            self.parameterTable.setItem(i, 0, QTableWidgetItem('P{}'.format(i)))
            pointBox = QComboBox(self.parameterTable)
            for k in range(len(self.Point)): pointBox.insertItem(k, 'Point{}'.format(k))
            pointBox.currentIndexChanged.connect(self.isOk)
            self.parameterTable.setCellWidget(i, 1, pointBox)
    
    @pyqtSlot(int)
    def isOk(self, *args):
        parameters = [self.parameterTable.cellWidget(i, 1).currentIndex() for i in range(self.parameterTable.rowCount())]
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(set(parameters))==len(parameters))
