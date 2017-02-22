# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_path_point_data import Ui_Info_Dialog

class path_point_data_show(QDialog, Ui_Info_Dialog):
    def __init__(self, Environment_variables, data, Run_list, parent=None):
        super(path_point_data_show, self).__init__(parent)
        self.setupUi(self)
        self.Environment_variables = Environment_variables
        for i in range(len(data)):
            nPath = data[i]
            for j in range(0, len(nPath), 2):
                X_path = nPath[j]
                Y_path = nPath[j+1]
                for k in range(len(X_path)-1):
                    self.path_data.insertRow(self.path_data.rowCount())
                    self.path_data.setItem(self.path_data.rowCount()-1, 0, QTableWidgetItem(Run_list[int(j/2)]))
                    self.path_data.setItem(self.path_data.rowCount()-1, 1, QTableWidgetItem(str(X_path[k])))
                    self.path_data.setItem(self.path_data.rowCount()-1, 2, QTableWidgetItem(str(Y_path[k])))
    
    @pyqtSlot()
    def on_save_clicked(self):
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', self.Environment_variables, 'Spreadsheet(*.csv)')
        if fileName:
            fileName = fileName.replace(".csv", "")+".csv"
            with open(fileName, 'w', newline="") as stream:
                writer = csv.writer(stream)
                for row in range(table.rowCount()):
                    rowdata = list()
                    for column in range(path_data.columnCount()-1):
                        item = table.item(row, column)
                        if item is not None: rowdata.append(item.text()+(str() if column==k-1 else '\t'))
                writer.writerow(rowdata)
            print("Successful Save Spreadsheet: "+fileName)
