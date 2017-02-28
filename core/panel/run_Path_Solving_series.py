# -*- coding: utf-8 -*-
from ..draw.modules import *
from .Ui_run_Path_Solving_series import Ui_Dialog as PathSolvingSeries_Dialog

class Path_Solving_series_show(QDialog, PathSolvingSeries_Dialog):
    def __init__(self, parent=None):
        super(Path_Solving_series_show, self).__init__(parent)
        self.setupUi(self)
