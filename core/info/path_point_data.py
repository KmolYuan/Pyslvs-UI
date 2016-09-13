# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_path_point_data import Ui_Info_Dialog

Environment_variables = '../'

class path_point_data_show(QDialog, Ui_Info_Dialog):
    def __init__(self, parent=None):
        super(path_point_data_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_save_clicked(self):
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Spreadsheet(*.csv)')
        if fileName:
            fileName = fileName.replace(".csv", "")+".csv"
            with open(fileName, 'w', newline="") as stream:
                writer = csv.writer(stream)
                for row in range(table.rowCount()):
                    rowdata = []
                    for column in range(path_data.columnCount()-1):
                        item = table.item(row, column)
                        if item is not None:
                            if column==k-1: rowdata += [item.text()]
                            else: rowdata += [item.text()+'\t']
                writer.writerow(rowdata)
            print("Successful Save Spreadsheet: "+fileName)
