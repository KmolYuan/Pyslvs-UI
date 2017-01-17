# -*- coding: utf-8 -*-
from .modules import *

class Path_Solving_series_show(QDialog, PathSolvingSeries_Dialog):
    def __init__(self, parent=None):
        super(Path_Solving_series_show, self).__init__(parent)
        self.setupUi(self)
