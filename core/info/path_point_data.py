# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_path_point_data import Ui_Info_Dialog

class path_point_data_show(QDialog, Ui_Info_Dialog):
    def __init__(self, Environment_variables, data, parent=None):
        super(path_point_data_show, self).__init__(parent)
        self.setupUi(self)
        self.Environment_variables = Environment_variables
        self.data = data
        for vpaths in data:
            for vpath in vpaths.paths:
                for point in vpath.path:
                    self.path_data.insertRow(self.path_data.rowCount())
                    row = self.path_data.rowCount()-1
                    self.path_data.setItem(row, 0, QTableWidgetItem('Shaft{}'.format(vpaths.shaft)))
                    self.path_data.setItem(row, 1, QTableWidgetItem('Point{}'.format(vpath.point)))
                    self.path_data.setItem(row, 2, QTableWidgetItem(str(point[0])))
                    self.path_data.setItem(row, 3, QTableWidgetItem(str(point[1])))
