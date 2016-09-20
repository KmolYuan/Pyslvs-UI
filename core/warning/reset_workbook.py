# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_reset_workbook import Ui_Warning_reset

class reset_show(QDialog, Ui_Warning_reset):
    def __init__(self, parent=None):
        super(reset_show, self).__init__(parent)
        self.setupUi(self)
