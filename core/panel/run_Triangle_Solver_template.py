# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver_template import Ui_Dialog

class Triangle_Solver_template_show(QDialog, Ui_Dialog):
    def __init__(self, Point, row, Type='Bar4', parent=None):
        super(Triangle_Solver_template_show, self).__init__(parent)
        self.setupUi(self)
        self.Point = Point
